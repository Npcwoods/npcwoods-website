#!/usr/bin/env python3
"""Remove live GTM / GA4 / Google Ads tags from health-condition HTML pages.

HIPAA: no BAA with Meta or Google advertising pixels. Health-condition pages
(city x condition, treatment, medications, learn, condition hubs) must not
load GTM-59QSWZRC, G-EFFRQMG8TC, AW-610222919, or a live Meta pixel.

Keeps the 2026-06-10 fbq no-op stub and comment (blocks a GTM-injected Meta
pixel if one is added later). Adds a short note that GTM/GA/Ads stay off.

Does not touch homepage / marketing-only files. Does not deploy.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Same family as tests/guardian/build_manifest.py HEALTH_MARKERS, plus
# cold-sore (condition treatment) which that list previously missed.
HEALTH_MARKERS = (
    "uti",
    "sinus",
    "strep",
    "ear-infection",
    "tooth",
    "dental",
    "learn/",
    "medications/",
    "ed-treatment",
    "glp1",
    "yeast",
    "antibiotics",
    "conditions/",
    "poison-ivy",
    "cold-sore",
)

SKIP_SUBSTRINGS = (
    "/_search-safe-template/cities.json",
    "tracking-snippet.html",
    "homepage-redesign-preview",
    "/llmseo/",
    "/executive/",
    "landing-pages/executive/",
)

GA_ADS_NOTE = (
    "GTM, GA4, and Google Ads stay off this health-condition page (no BAA)."
)

STUB = """<!-- Meta Pixel disabled 2026-06-10: no BAA with Meta — health-condition pages must not send PageView there.
     The stub below also blocks a later-injected Meta pixel: Meta's base code starts with `if(f.fbq)return;`,
     so predefining a no-op fbq means fbevents.js never loads on this page.
     GTM, GA4, and Google Ads stay off this health-condition page (no BAA). -->
<script>
window.fbq = function () {};
window.fbq.queue = [];
window.fbq.loaded = true;
window.fbq.version = '2.0';
window._fbq = window.fbq;
</script>
"""

LIVE_IDS = (
    "GTM-59QSWZRC",
    "G-EFFRQMG8TC",
    "AW-610222919",
)
LIVE_FBQ_INIT = re.compile(r"""fbq\s*\(\s*['\"]init['\"]""")
LIVE_FB_TR = "facebook.com/tr"

COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

GTM_LOADER_RE = re.compile(
    r"[ \t]*<script>\s*\(function\(w,d,s,l,i\)\{w\[l\]=w\[l\]\|\|\[\];"
    r"w\[l\]\.push\(\{'gtm\.start':\s*new Date\(\)\.getTime\(\),"
    r"event:'gtm\.js'\}\);.*?"
    r"GTM-59QSWZRC'\);</script>[ \t]*\n?",
    re.DOTALL,
)

GA4_ADS_RE = re.compile(
    r"[ \t]*<script async src=\"https://www\.googletagmanager\.com/gtag/js\?id=G-EFFRQMG8TC\"></script>\s*"
    r"<script>\s*window\.dataLayer = window\.dataLayer \|\| \[\];\s*"
    r"function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*"
    r"gtag\('js', new Date\(\)\);\s*"
    r"gtag\('config', 'G-EFFRQMG8TC'\);\s*"
    r"gtag\('config', 'AW-610222919'\);\s*"
    r"</script>[ \t]*\n?",
    re.DOTALL,
)

GTM_NOSCRIPT_RE = re.compile(
    r"[ \t]*<noscript><iframe src=\"https://www\.googletagmanager\.com/ns\.html\?id=GTM-59QSWZRC\""
    r"\s*height=\"0\" width=\"0\" style=\"display:none;visibility:hidden\">"
    r"</iframe></noscript>[ \t]*\n?",
    re.DOTALL,
)

GTM_PRECONNECT_RE = re.compile(
    r"[ \t]*<link rel=\"preconnect\" href=\"https://www\.googletagmanager\.com\">[ \t]*\n?"
)

ORPHAN_COMMENTS = (
    re.compile(r"[ \t]*<!-- NPCWoods Tracking: GTM -->[ \t]*\n?"),
    re.compile(r"[ \t]*<!-- Google Tag Manager -->[ \t]*\n?"),
    re.compile(r"[ \t]*<!-- End Google Tag Manager -->[ \t]*\n?"),
    re.compile(r"[ \t]*<!-- Google Analytics -->[ \t]*\n?"),
    re.compile(r"[ \t]*<!-- Google Analytics & GTM -->[ \t]*\n?"),
    re.compile(r"[ \t]*<!-- GA4 Direct Fallback -->[ \t]*\n?"),
    re.compile(r"[ \t]*<!-- NPCWoods Tracking: GTM noscript -->[ \t]*\n?"),
    re.compile(r"[ \t]*<!-- GTM noscript -->[ \t]*\n?"),
    re.compile(r"[ \t]*<!-- Google Tag Manager \(noscript\) -->[ \t]*\n?"),
    re.compile(r"[ \t]*<!-- End Google Tag Manager \(noscript\) -->[ \t]*\n?"),
)

HEAD_RE = re.compile(r"(<head>\s*\n)", re.IGNORECASE)
META_DISABLED_RE = re.compile(r"<!-- Meta Pixel disabled.*?-->", re.DOTALL)


def is_health_html(rel: str) -> bool:
    posix = rel.replace("\\", "/").lower()
    if any(skip in posix for skip in SKIP_SUBSTRINGS):
        return False
    if posix.startswith("homepage/"):
        return False
    if posix.startswith("html/shared/"):
        return False
    return any(marker in posix for marker in HEALTH_MARKERS)


def health_html_files() -> list[Path]:
    files: list[Path] = []
    for base in (ROOT / "landing-pages", ROOT / "html"):
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.html")):
            rel = path.relative_to(ROOT).as_posix()
            if is_health_html(rel):
                files.append(path)
    return files


def strip_comments(html: str) -> str:
    return COMMENT_RE.sub("", html)


def live_hits(html: str) -> list[str]:
    live = strip_comments(html)
    hits = [token for token in LIVE_IDS if token in live]
    if LIVE_FBQ_INIT.search(live):
        hits.append("fbq('init'")
    if LIVE_FB_TR in live:
        hits.append(LIVE_FB_TR)
    return hits


def ensure_hipaa_comment(html: str) -> str:
    def inject_note(match: re.Match[str]) -> str:
        block = match.group(0)
        if GA_ADS_NOTE in block:
            if re.search(rf"\n[ \t]*{re.escape(GA_ADS_NOTE)}\s*-->", block):
                return block
            return re.sub(
                rf"[ \t]*{re.escape(GA_ADS_NOTE)}\s*-->",
                f"\n     {GA_ADS_NOTE} -->",
                block,
                count=1,
            )
        return re.sub(
            r"\s*-->\s*$",
            f"\n     {GA_ADS_NOTE} -->",
            block,
            count=1,
        )

    if META_DISABLED_RE.search(html):
        html = META_DISABLED_RE.sub(inject_note, html, count=1)
        if "window.fbq = function" in html:
            return html

    if GA_ADS_NOTE in html and "window.fbq = function" in html:
        return html

    new, n = HEAD_RE.subn(lambda m: m.group(1) + STUB, html, count=1)
    if n != 1:
        raise RuntimeError("could not locate a single <head> to insert the HIPAA stub")
    return new


def transform(html: str) -> str:
    out = GTM_LOADER_RE.sub("", html)
    out = GA4_ADS_RE.sub("", out)
    out = GTM_NOSCRIPT_RE.sub("", out)
    out = GTM_PRECONNECT_RE.sub("", out)
    for pattern in ORPHAN_COMMENTS:
        out = pattern.sub("", out)
    out = ensure_hipaa_comment(out)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="verify only, do not write")
    args = parser.parse_args(argv)

    files = health_html_files()
    if not files:
        print("[FAIL] no health HTML files found")
        return 1

    changed = clean = errors = 0
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        html = path.read_text(encoding="utf-8")
        try:
            new = transform(html)
            leftover = live_hits(new)
            if leftover:
                raise RuntimeError(f"live markers remain: {leftover}")
            if GA_ADS_NOTE not in new:
                raise RuntimeError("missing HIPAA GA/Ads-off comment")
        except RuntimeError as exc:
            print(f"[FAIL] {rel}: {exc}")
            errors += 1
            continue
        if new == html:
            print(f"[ok-already] {rel}")
            clean += 1
            continue
        if args.check:
            print(f"[would-change] {rel}")
            changed += 1
            continue
        path.write_text(new, encoding="utf-8")
        print(f"[stripped] {rel}")
        changed += 1

    print(
        f"\n{'CHECK' if args.check else 'DONE'}: "
        f"{changed} changed, {clean} already-clean, {errors} errors, "
        f"{len(files)} health HTML files"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
