#!/usr/bin/env python3
"""Nightly Site Guardian — read-only compliance + tracking sweep of npcwoods.com.

Strictly read-only against the live site: GET/HEAD requests and headless
Playwright page loads only. Never POSTs, never logs in, never modifies anything.
Needs no credentials.

Checks per page (from tests/guardian/manifest.json):
  1. HTTP 200 and the page actually renders (not the WP 404 theme page)
  2. tracking.js script tag present (+ the file itself returns 200, checked once)
  3. GTM container present in <head>
  4. Health pages: ZERO Meta/Facebook pixel — no connect.facebook.net, no live
     fbq(...) calls (the no-op fbq stub that BLOCKS the pixel is allowed)
  5. Canonical claim wording drift (response time / hours / med cost / reviews)
  6. Forbidden words in visible text: insurance, doctor, subscription language
  7. Paid LPs (*/search-safe/, /uti-care/): noindex meta present, absent from
     the live sitemap
  8. Internal links: every unique internal href HEAD-checked once
  9. Playwright spot-check on a small rotating sample: GTM/GA4 requests fire,
     zero facebook requests on health pages

Output: content-output/guardian-reports/latest.md (temp-file + os.replace, safe
for launchd) plus a dated copy. Exit 0 = all green, 1 = red flags.

Usage:
    python3 tests/guardian/guardian.py [--manifest PATH] [--out-dir PATH]
                                       [--skip-playwright] [--sample N] [--limit N]
"""
from __future__ import annotations

import argparse
import datetime as dt
import html as htmllib
import json
import os
import re
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_MANIFEST = SCRIPT_DIR / "manifest.json"
DEFAULT_OUT_DIR = REPO_ROOT / "content-output" / "guardian-reports"
FALLBACK_OUT_DIR = Path.home() / ".local/npcwoods/reports/guardian-reports"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 NPCWoodsSiteGuardian/1.0"
)
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)
TIMEOUT = 25
CONCURRENCY = 4
RETRY_PAUSE = 3

# ---------------------------------------------------------------- compliance
FORBIDDEN_WORDS = [
    ("insurance", re.compile(r"\binsuran\w*", re.I)),
    ("doctor", re.compile(r"\bdoctors?\b", re.I)),
    ("subscription", re.compile(r"\bsubscriptions?\b", re.I)),
    ("per month", re.compile(r"\bper\s+month\b", re.I)),
    ("/mo", re.compile(r"\$\s?\d+\s?/\s?mo\b", re.I)),
]

# Canonical claims (memory/canonical-site-claims.md, approved 2026-06-10):
#   response time: "Most patients hear back the same day, usually within a few hours."
#   hours:         "Messages are reviewed 7 days a week." (no clock hours anywhere)
#   med cost:      "typically $4-$20 with GoodRx" (never "under $10")
#   reviews:       "50+ five-star reviews"
CLAIM_CHECKS = [
    (
        "response-time drift (canonical: 'usually within a few hours')",
        re.compile(
            r"\b(?:under|within|in)\s+\d+\s*min(?:ute)?s?\b"
            r"|\b\d+\s*[-–]?\s*min(?:ute)?s?\s+(?:response|reply|answer)"
            r"|\bunder\s+(?:an?|1|one|half\s+an?)\s+hour\b"
            r"|\bwithin\s+(?:the|an?|1|one)\s+hour\b"
            r"|\b(?:5|five|10|ten|15|30|thirty)[-\s]min(?:ute)?\b",
            re.I,
        ),
    ),
    (
        "med-cost drift (canonical: 'typically $4-$20 with GoodRx')",
        re.compile(r"\bunder\s+\$10\b", re.I),
    ),
    (
        # Only flag hour RANGES ("8am-5pm", "9 AM to 5 PM") — lone timestamps
        # inside patient testimonials ("messaged at 10:08am") are fine.
        "published clock hours (canonical: no exact hours anywhere)",
        re.compile(
            r"\b\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)?\s*(?:-|–|—|to|until)\s*"
            r"\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)\b",
            re.I,
        ),
    ),
]
REVIEW_COUNT_RE = re.compile(r"\b(\d+)\s*\+?\s*(?:five|5)[-\s]star", re.I)
CANONICAL_REVIEW_COUNT = 50

TRACKING_JS_RE = re.compile(r"<script[^>]+src=[\"'][^\"']*tracking\.js[^\"']*[\"']", re.I)
GTM_RE = re.compile(r"googletagmanager\.com|GTM-[A-Z0-9]{4,}", re.I)
META_REFRESH_RE = re.compile(
    r"""<meta[^>]+http-equiv=["']refresh["'][^>]*url=([^"'>\s]+)""", re.I
)
NOINDEX_RE = re.compile(
    r"<meta[^>]+name=[\"']robots[\"'][^>]*content=[\"'][^\"']*noindex", re.I
)
NOINDEX_RE2 = re.compile(
    r"<meta[^>]+content=[\"'][^\"']*noindex[^\"']*[\"'][^>]*name=[\"']robots[\"']", re.I
)
FBQ_CALL_RE = re.compile(r"\bfbq\s*\(\s*[\"']", re.I)
WP404_RE = re.compile(r"error404|<title>\s*Page not found", re.I)
HREF_RE = re.compile(r"<a\s[^>]*?href=[\"']([^\"'#]+)[\"']", re.I)

GOOD_TRACKING_DOMAINS = (
    "googletagmanager.com",
    "google-analytics.com",
    "googleadservices.com",
    "doubleclick.net",
)
META_PIXEL_DOMAINS = ("connect.facebook.net", "facebook.com/tr")


@dataclass
class Finding:
    severity: str  # RED | YELLOW
    url: str
    check: str
    detail: str


@dataclass
class PageResult:
    page: dict
    status: int | None = None
    error: str | None = None
    html: str = ""
    findings: list[Finding] = field(default_factory=list)


# ----------------------------------------------------------------- helpers
def strip_to_visible_text(html: str) -> str:
    """Crude but dependency-free visible-text extraction: drop script/style/
    noscript/template blocks and comments, keep title + meta description
    (ad-platform-visible), then strip tags."""
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    meta_desc = re.search(
        r"<meta[^>]+name=[\"']description[\"'][^>]*content=[\"']([^\"']*)[\"']",
        html,
        re.I,
    )
    body = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    body = re.sub(
        r"<(script|style|noscript|template|svg)\b.*?</\1\s*>", " ", body,
        flags=re.I | re.S,
    )
    body = re.sub(r"<[^>]+>", " ", body)
    parts = [title.group(1) if title else "", meta_desc.group(1) if meta_desc else "", body]
    text = htmllib.unescape(" ".join(parts))
    return re.sub(r"\s+", " ", text)


def context_snippets(text: str, pattern: re.Pattern, cap: int = 3) -> list[str]:
    out = []
    for m in pattern.finditer(text):
        start, end = max(0, m.start() - 45), min(len(text), m.end() + 45)
        out.append("..." + text[start:end].strip() + "...")
        if len(out) >= cap:
            break
    return out


def fetch(session: requests.Session, url: str, method: str = "GET") -> requests.Response:
    last_exc = None
    for attempt in range(2):
        try:
            return session.request(
                method, url, timeout=TIMEOUT, allow_redirects=True,
                headers={"User-Agent": UA},
            )
        except requests.RequestException as exc:
            last_exc = exc
            if attempt == 0:
                time.sleep(RETRY_PAUSE)
    raise last_exc


# ------------------------------------------------------------- page checks
def check_page(session: requests.Session, page: dict, sitemap_urls: set[str]) -> PageResult:
    res = PageResult(page=page)
    url = page["url"]
    try:
        resp = fetch(session, url)
    except requests.RequestException as exc:
        res.error = str(exc)
        res.findings.append(Finding("RED", url, "fetch", f"request failed: {exc}"))
        return res

    res.status = resp.status_code
    # GoDaddy omits charset on some pages -> requests falls back to latin-1
    # and snippets turn to mojibake. These pages are all UTF-8.
    if "charset" not in (resp.headers.get("Content-Type") or "").lower():
        resp.encoding = "utf-8"
    html = resp.text or ""
    res.html = html

    # 1. up + actually rendering
    if resp.status_code != 200:
        res.findings.append(
            Finding("RED", url, "http-status", f"HTTP {resp.status_code} (expected 200)")
        )
        return res
    if WP404_RE.search(html[:6000]):
        res.findings.append(
            Finding("RED", url, "wp-404", "returns 200 but renders the WP 404 theme page")
        )
        return res

    # Client-side redirect stub (retired page pointing at its replacement):
    # not a marketing surface, so skip tracking/compliance checks — but say so.
    refresh = META_REFRESH_RE.search(html[:4000])
    if refresh or "window.location.replace(" in html[:4000]:
        target = refresh.group(1) if refresh else "(JS redirect)"
        res.findings.append(
            Finding("YELLOW", url, "redirect-stub",
                    f"page is a client-side redirect stub -> {target}; "
                    "tracking/compliance checks skipped (consider a server 301 "
                    "and dropping it from the manifest)")
        )
        return res
    if len(html) < 2000:
        res.findings.append(
            Finding("RED", url, "thin-page", f"page body suspiciously small ({len(html)} bytes)")
        )

    head = html.split("</head>", 1)[0]

    # 2. tracking.js script tag
    if not TRACKING_JS_RE.search(html):
        res.findings.append(
            Finding("RED", url, "tracking.js", "no <script src=...tracking.js> tag found")
        )

    # 3. GTM in <head>
    if not GTM_RE.search(head):
        if GTM_RE.search(html):
            res.findings.append(
                Finding("YELLOW", url, "gtm-placement",
                        "GTM container found but not in <head>")
            )
        else:
            res.findings.append(
                Finding("RED", url, "gtm-missing", "no GTM container on page")
            )

    # 4. Meta pixel on health pages
    if page["is_health_page"]:
        if "connect.facebook.net" in html:
            res.findings.append(
                Finding("RED", url, "meta-pixel",
                        "connect.facebook.net present on a health page")
            )
        else:
            # fbq(...) CALLS are the pixel; a bare no-op stub definition
            # (window.fbq = function () {}; — blocks GTM-injected pixel) is allowed.
            # A leftover call WITH the stub present is neutralized at runtime
            # (stub swallows it) -> YELLOW residual code; without the stub -> RED.
            calls = FBQ_CALL_RE.findall(html)
            if calls:
                has_stub = "window.fbq = function" in html or "window.fbq=function" in html
                if has_stub:
                    res.findings.append(
                        Finding("YELLOW", url, "meta-pixel-residual",
                                f"{len(calls)} leftover fbq('...') call(s) on a health "
                                "page — currently neutralized by the no-op stub, but "
                                "dead pixel code should be removed")
                    )
                else:
                    res.findings.append(
                        Finding("RED", url, "meta-pixel",
                                f"{len(calls)} fbq('...') call(s) on a health page "
                                "with NO blocking stub")
                    )

    # 5 + 6. claims + forbidden words on visible text
    text = strip_to_visible_text(html)
    for label, pattern in FORBIDDEN_WORDS:
        snips = context_snippets(text, pattern)
        if snips:
            res.findings.append(
                Finding("RED", url, f"forbidden-word: {label}",
                        f"{len(pattern.findall(text))} hit(s); e.g. " + " | ".join(snips))
            )
    for label, pattern in CLAIM_CHECKS:
        snips = context_snippets(text, pattern)
        if snips:
            res.findings.append(
                Finding("YELLOW", url, f"claim-drift: {label}", " | ".join(snips))
            )
    for m in REVIEW_COUNT_RE.finditer(text):
        if int(m.group(1)) != CANONICAL_REVIEW_COUNT:
            start, end = max(0, m.start() - 45), min(len(text), m.end() + 45)
            res.findings.append(
                Finding("YELLOW", url,
                        "claim-drift: review count (canonical: '50+ five-star reviews')",
                        "..." + text[start:end].strip() + "...")
            )

    # 7. paid LP: noindex + sitemap exclusion
    if page["is_paid_lp"]:
        has_meta = bool(NOINDEX_RE.search(html) or NOINDEX_RE2.search(html))
        has_header = "noindex" in (resp.headers.get("X-Robots-Tag") or "").lower()
        if not (has_meta or has_header):
            res.findings.append(
                Finding("RED", url, "paid-lp-noindex",
                        "paid landing page has NO noindex (meta or X-Robots-Tag)")
            )
        if sitemap_urls and url.rstrip("/") + "/" in sitemap_urls:
            res.findings.append(
                Finding("RED", url, "paid-lp-in-sitemap",
                        "paid landing page is listed in the live sitemap")
            )
    return res


# -------------------------------------------------------------- site-level
def fetch_sitemap_urls(session: requests.Session, base: str) -> tuple[set[str], list[Finding]]:
    findings: list[Finding] = []
    urls: set[str] = set()
    loc_re = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")
    try:
        idx = fetch(session, base + "/sitemap_index.xml")
        if idx.status_code != 200:
            findings.append(Finding("YELLOW", base + "/sitemap_index.xml", "sitemap",
                                    f"HTTP {idx.status_code} fetching sitemap index"))
            return urls, findings
        children = loc_re.findall(idx.text)
        child_maps = [u for u in children if u.endswith(".xml")]
        urls.update(u for u in children if not u.endswith(".xml"))
        for child in child_maps:
            try:
                c = fetch(session, child)
                if c.status_code == 200:
                    urls.update(u for u in loc_re.findall(c.text) if not u.endswith(".xml"))
            except requests.RequestException as exc:
                findings.append(Finding("YELLOW", child, "sitemap", f"child sitemap fetch failed: {exc}"))
    except requests.RequestException as exc:
        findings.append(Finding("YELLOW", base, "sitemap", f"sitemap index fetch failed: {exc}"))
    return urls, findings


def check_tracking_js(session: requests.Session, base: str) -> list[Finding]:
    url = base + "/tracking.js"
    try:
        r = fetch(session, url)
    except requests.RequestException as exc:
        return [Finding("RED", url, "tracking.js-file", f"fetch failed: {exc}")]
    if r.status_code != 200:
        return [Finding("RED", url, "tracking.js-file", f"HTTP {r.status_code}")]
    if len(r.text) < 200:
        return [Finding("YELLOW", url, "tracking.js-file",
                        f"file unusually small ({len(r.text)} bytes)")]
    return []


def collect_internal_links(results: list[PageResult], base: str) -> dict[str, set[str]]:
    """unique internal URL -> set of pages that link to it"""
    host = urlparse(base).netloc
    links: dict[str, set[str]] = {}
    for res in results:
        if not res.html:
            continue
        for href in HREF_RE.findall(res.html):
            href = htmllib.unescape(href.strip())
            if href.startswith(("mailto:", "tel:", "sms:", "javascript:", "data:")):
                continue
            absu = urljoin(res.page["url"], href)
            p = urlparse(absu)
            if p.scheme not in ("http", "https") or p.netloc.replace("www.", "") != host:
                continue
            clean = p.scheme + "://" + p.netloc.replace("www.", "") + (p.path or "/")
            links.setdefault(clean, set()).add(res.page["url"])
    return links


def check_links(session: requests.Session, links: dict[str, set[str]]) -> list[Finding]:
    findings: list[Finding] = []

    def head_check(u: str):
        try:
            r = fetch(session, u, method="HEAD")
            if r.status_code in (403, 405, 501):  # some servers reject HEAD
                r = fetch(session, u)
            return u, r.status_code
        except requests.RequestException as exc:
            return u, f"error: {exc}"

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = [pool.submit(head_check, u) for u in sorted(links)]
        for fut in as_completed(futures):
            u, status = fut.result()
            bad = isinstance(status, str) or status >= 400
            if bad:
                sources = sorted(links[u])
                findings.append(
                    Finding("YELLOW", u, "broken-internal-link",
                            f"status {status}; linked from {len(sources)} page(s), "
                            f"e.g. {', '.join(sources[:3])}")
                )
    return findings


# --------------------------------------------------------------- playwright
def pick_playwright_sample(pages: list[dict], n: int) -> list[dict]:
    """Deterministic daily rotation: ~half paid LPs / health pages, rest others."""
    day = dt.date.today().toordinal()
    paid = [p for p in pages if p["is_paid_lp"]]
    health = [p for p in pages if p["is_health_page"] and not p["is_paid_lp"]]
    other = [p for p in pages if not p["is_health_page"] and not p["is_paid_lp"]]
    sample: list[dict] = []

    def take(bucket: list[dict], k: int):
        if not bucket:
            return
        for i in range(min(k, len(bucket))):
            sample.append(bucket[(day * k + i) % len(bucket)])

    take(paid, max(1, n // 3))
    take(health, max(1, n // 3))
    take(other, n - len(sample))
    # dedupe, preserve order
    seen, out = set(), []
    for p in sample:
        if p["url"] not in seen:
            seen.add(p["url"])
            out.append(p)
    return out[:n]


def playwright_spot_checks(sample: list[dict]) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    notes: list[str] = []
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        findings.append(Finding("YELLOW", "-", "playwright",
                                "playwright not importable in this python; spot-checks skipped"))
        return findings, notes

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for page_meta in sample:
            url = page_meta["url"]
            ctx = browser.new_context(
                viewport={"width": 390, "height": 844}, user_agent=MOBILE_UA
            )
            pw_page = ctx.new_page()
            good_hits: list[str] = []
            fb_hits: list[str] = []
            pw_page.on("request", lambda r: (
                good_hits.append(r.url)
                if any(d in r.url for d in GOOD_TRACKING_DOMAINS)
                else fb_hits.append(r.url)
                if any(d in r.url for d in META_PIXEL_DOMAINS)
                else None
            ))
            try:
                pw_page.goto(url, wait_until="networkidle", timeout=60000)
                pw_page.wait_for_timeout(2500)
            except Exception as exc:
                findings.append(Finding("RED", url, "playwright-load", f"page load failed: {exc}"))
                ctx.close()
                continue
            gtm = any("googletagmanager.com" in u for u in good_hits)
            ga4 = any("google-analytics.com" in u or "/g/collect" in u for u in good_hits)
            if not gtm:
                findings.append(Finding("RED", url, "playwright-gtm",
                                        "no googletagmanager.com request fired on load"))
            if not ga4:
                findings.append(Finding("YELLOW", url, "playwright-ga4",
                                        "no GA4 collect request observed on load"))
            if page_meta["is_health_page"] and fb_hits:
                findings.append(Finding("RED", url, "playwright-meta-pixel",
                                        f"{len(fb_hits)} facebook request(s) fired on a "
                                        "health page: "
                                        + "; ".join(u[:110] for u in fb_hits[:3])))
            notes.append(
                f"{url} — GTM={'Y' if gtm else 'N'} GA4={'Y' if ga4 else 'N'} "
                f"fb-requests={len(fb_hits)}"
            )
            ctx.close()
        browser.close()
    return findings, notes


# ------------------------------------------------------------------ report
def write_report(out_dir: Path, body: str) -> Path:
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        probe = out_dir / ".write-probe"
        probe.write_text("ok")
        probe.unlink()
    except (PermissionError, OSError):
        out_dir = FALLBACK_OUT_DIR
        out_dir.mkdir(parents=True, exist_ok=True)
    dated = out_dir / f"guardian-{dt.date.today().isoformat()}.md"
    for target in (out_dir / "latest.md", dated):
        # temp file + atomic rename: launchd-safe, readers never see a partial file
        fd, tmp = tempfile.mkstemp(dir=str(out_dir), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(body)
        os.replace(tmp, target)
    return out_dir / "latest.md"


def build_report(manifest: dict, results: list[PageResult], site_findings: list[Finding],
                 pw_notes: list[str], elapsed: float, pw_sample: list[dict]) -> tuple[str, int, int]:
    all_findings = site_findings + [f for r in results for f in r.findings]
    reds = [f for f in all_findings if f.severity == "RED"]
    yellows = [f for f in all_findings if f.severity == "YELLOW"]
    n = len(results)
    if not reds and not yellows:
        verdict = f"ALL GREEN — {n} pages checked"
    elif not reds:
        verdict = f"GREEN with {len(yellows)} YELLOW warnings — {n} pages checked"
    else:
        verdict = f"{len(reds)} RED FLAGS ({len(yellows)} yellow) — {n} pages checked"

    s = manifest["summary"]
    lines = [
        f"# Site Guardian — {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"**{verdict}**",
        "",
        f"- Pages: {n} total ({s['health_pages']} health, {s['paid_lps']} paid LP)",
        f"- Sweep runtime: {elapsed:.0f}s | concurrency {CONCURRENCY} | read-only "
        "(GET/HEAD + headless page loads only)",
        f"- Playwright spot-check sample today: "
        + (", ".join(p['url'] for p in pw_sample) if pw_sample else "(skipped)"),
        "",
    ]

    def section(title: str, items: list[Finding]):
        lines.append(f"## {title}")
        lines.append("")
        if not items:
            lines.append("- none")
        else:
            by_check: dict[str, list[Finding]] = {}
            for f in items:
                by_check.setdefault(f.check, []).append(f)
            for check, fs in sorted(by_check.items()):
                lines.append(f"### {check} ({len(fs)})")
                for f in fs:
                    lines.append(f"- {f.url}")
                    lines.append(f"  - {f.detail}")
                lines.append("")
        lines.append("")

    section("RED — fix before traffic hits these pages", reds)
    section("YELLOW — review when convenient", yellows)

    lines.append("## Playwright spot-check detail")
    lines.append("")
    lines.extend(f"- {note}" for note in (pw_notes or ["(skipped)"]))
    lines.append("")
    lines.append("## Pages checked")
    lines.append("")
    for r in results:
        flag = "RED" if any(f.severity == "RED" for f in r.findings) else (
            "yellow" if r.findings else "ok")
        lines.append(f"- [{flag}] {r.page['url']} (HTTP {r.status})")
    lines.append("")
    return "\n".join(lines), len(reds), len(yellows)


# -------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--skip-playwright", action="store_true")
    ap.add_argument("--sample", type=int, default=6, help="playwright sample size")
    ap.add_argument("--limit", type=int, default=0, help="check only first N pages (debug)")
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    pages = manifest["pages"]
    if args.limit:
        pages = pages[: args.limit]
    base = manifest["base_url"]
    started = time.time()

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=CONCURRENCY,
                                            pool_maxsize=CONCURRENCY)
    session.mount("https://", adapter)

    site_findings: list[Finding] = []
    sitemap_urls, sm_findings = fetch_sitemap_urls(session, base)
    site_findings += sm_findings
    site_findings += check_tracking_js(session, base)

    results: list[PageResult] = []
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = {pool.submit(check_page, session, p, sitemap_urls): p for p in pages}
        for fut in as_completed(futures):
            results.append(fut.result())
    results.sort(key=lambda r: r.page["url"])

    links = collect_internal_links(results, base)
    site_findings += check_links(session, links)
    print(f"[guardian] {len(results)} pages fetched, {len(links)} unique internal links checked",
          file=sys.stderr)

    pw_sample: list[dict] = []
    pw_notes: list[str] = []
    if not args.skip_playwright:
        pw_sample = pick_playwright_sample(pages, args.sample)
        pw_findings, pw_notes = playwright_spot_checks(pw_sample)
        site_findings += pw_findings

    elapsed = time.time() - started
    body, reds, yellows = build_report(manifest, results, site_findings,
                                       pw_notes, elapsed, pw_sample)
    report_path = write_report(args.out_dir, body)
    print(body.splitlines()[2].strip("* "))
    print(f"[guardian] report: {report_path} ({elapsed:.0f}s)", file=sys.stderr)
    return 1 if reds else 0


if __name__ == "__main__":
    sys.exit(main())
