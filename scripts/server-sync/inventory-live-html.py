#!/usr/bin/env python3
"""Read-only inventory of live npcwoods.com plates vs this repo.

Fetches the public Yoast sitemaps + WordPress pages API, GETs each
candidate URL (no query string), and classifies:

  already_in_repo  — freezer already has HTML/PHP for this path
  real_plate       — live HTML has a title + H1 and is not an empty WP shell
  empty_shell      — ~15KB WordPress stub, no real plate
  wp_blog          — WordPress post (leave in WP; not a static HTML plate)
  skip             — homepage / admin / utility

Optionally copies dining-room-only real plates into landing-pages/.
Never uploads. Never deploys. Never writes to GoDaddy.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from pathlib import Path
from xml.etree import ElementTree as ET

REPO = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
BASE = "https://npcwoods.com"
UA = {"User-Agent": "NPCWoods-freezer-inventory/1.0 (+https://npcwoods.com)"}
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# Paths that are PHP / WP-native / not static marketing HTML.
SKIP_PATHS = {
    "/",
    "/blog/",
    "/pay/",
    "/path-visit/",
    "/wp-admin/",
    "/wp-login.php/",
}

# Unique dining-room plates that belong in landing-pages/ when missing.
# Leftover city × condition leftovers stay out of this list.
UNIQUE_PLATE_PATHS = {
    "/terms-of-service/",
    "/privacy-policy/",
    "/medical-disclaimer/",
    "/services/",
    "/urgent-care-price-guide/",
    "/when-to-see-provider-for-uti/",
    "/conditions/poison-ivy-treatment/",
    "/conditions/nausea-vomiting-treatment/",
    "/conditions/albuterol-inhaler-refill-preview/",
}

CITY_LEFTOVER_RE = re.compile(
    r"^/(ed-treatment|sinus-infection-treatment|strep-throat-ear-infection|uti-treatment)/"
    r"[a-z0-9-]+-(?:az|ga|nc|nm|co|nv|ia|or|ut|id|mt)/$"
)

# Experience HTML lives under html/experience/ but the live URL is /patient-experience/.
LOCAL_URL_ALIASES = {
    "html/experience/index.html": "/patient-experience/",
    "html/thank-you/index.html": "/thank-you/",
}


def norm_path(url: str) -> str:
    path = urllib.parse.urlparse(url).path or "/"
    if not path.startswith("/"):
        path = "/" + path
    if not path.endswith("/"):
        path += "/"
    return path


def get(url: str, timeout: int = 45) -> tuple[int, bytes, str]:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), r.geturl()
    except urllib.error.HTTPError as e:
        body = e.read() if e.fp else b""
        return e.code, body, url


def first(pattern: str, html: str, flags: int = re.I) -> str:
    m = re.search(pattern, html, flags)
    return unescape(re.sub(r"\s+", " ", m.group(1))).strip() if m else ""


def classify_html(path: str, status: int, body: bytes, final_url: str) -> dict:
    size = len(body)
    text = body.decode("utf-8", errors="replace")
    title = first(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    h1 = first(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S)
    h1_text = re.sub(r"<[^>]+>", "", h1).strip()
    has_wp_blocks = "wp-site-blocks" in text
    has_npc_nav = 'class="npc-nav"' in text or "class='npc-nav'" in text
    has_npc_plate = "npc-plate" in text
    has_doctype = "<!doctype html" in text.lower()
    final_path = norm_path(final_url) if final_url else path
    can = first(r'rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', text)
    if not can:
        can = first(r'href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', text)
    can_path = norm_path(can) if can and "npcwoods.com" in can else ""
    looks_empty = (
        size < 22000
        and has_wp_blocks
        and not has_npc_nav
        and not has_npc_plate
        and (not h1_text or "skip to" in h1_text.lower())
    )
    if path in SKIP_PATHS:
        kind = "skip"
    elif status != 200 or not has_doctype:
        kind = "not_html"
    elif final_path != path:
        kind = "redirect"
    elif can_path and can_path != path:
        kind = "wrong_plate"
    elif looks_empty or (size < 18000 and has_wp_blocks and not h1_text):
        kind = "empty_shell"
    elif path in UNIQUE_PLATE_PATHS:
        kind = "unique_plate"
    elif CITY_LEFTOVER_RE.match(path) or (has_npc_plate and size < 20000):
        kind = "leftover_city"
    elif has_npc_nav or has_npc_plate or (h1_text and size >= 20000 and not has_wp_blocks):
        kind = "unique_plate"
    elif h1_text and size >= 25000:
        kind = "unique_plate"
    else:
        kind = "empty_shell" if has_wp_blocks or size < 18000 else "leftover_city"
    return {
        "path": path,
        "status": status,
        "bytes": size,
        "final_url": final_url,
        "title": title[:160],
        "h1": h1_text[:160],
        "has_h1": bool(h1_text),
        "has_npc_nav": has_npc_nav,
        "has_npc_plate": has_npc_plate,
        "has_wp_blocks": has_wp_blocks,
        "kind": kind,
        "body": body if kind == "unique_plate" else b"",
    }


def local_url_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    mapping["/"] = "homepage/page-npcwoods-home.php"
    for base, prefix in (
        (REPO / "landing-pages", ""),
        (REPO / "html", ""),
        (REPO / "blog", "blog/"),
    ):
        if not base.exists():
            continue
        for f in base.rglob("index.html"):
            rel = f.relative_to(base).as_posix()
            folder = rel[: -len("index.html")].strip("/")
            if prefix:
                path = f"/{prefix}{folder}/" if folder else f"/{prefix}"
            else:
                path = f"/{folder}/" if folder else "/"
            mapping[path] = str(f.relative_to(REPO))
        for f in base.rglob("*.html"):
            if f.name == "index.html" or "shared" in f.parts:
                continue
            rel = f.relative_to(base).as_posix()
            slug = rel[: -len(".html")]
            path = f"/{prefix}{slug}/"
            mapping.setdefault(path, str(f.relative_to(REPO)))
    for local, url in LOCAL_URL_ALIASES.items():
        if (REPO / local).exists():
            mapping[url] = local
    # Guardian already maps a few extras.
    man = REPO / "tests/guardian/manifest.json"
    if man.exists():
        data = json.loads(man.read_text())
        for p in data.get("pages", []):
            path = norm_path(p["url"])
            src = p.get("local_source")
            if src and p.get("exists_locally") and path not in mapping:
                mapping[path] = src
    return mapping


def wp_pages() -> list[dict]:
    pages = []
    for i in (1, 2, 3):
        cached = Path(f"/tmp/npc-inventory/pages-{i}.json")
        if cached.exists():
            pages.extend(json.loads(cached.read_text()))
            continue
        status, body, _ = get(
            f"{BASE}/wp-json/wp/v2/pages?per_page=100&page={i}&_fields=id,slug,link,status,parent,title"
        )
        if status == 200:
            pages.extend(json.loads(body))
    return pages


def sitemap_urls(name: str) -> list[str]:
    path = Path(f"/tmp/npc-inventory/{name}")
    if not path.exists():
        status, body, _ = get(f"{BASE}/{name}")
        if status != 200:
            return []
        path.write_bytes(body)
    tree = ET.parse(path)
    return [el.text for el in tree.findall(".//sm:loc", NS) if el.text]


def write_report(rows: list[dict], local: dict[str, str], pulled: list[dict], dest: Path) -> None:
    by_kind: dict[str, list[dict]] = {}
    for r in rows:
        by_kind.setdefault(r["kind"], []).append(r)
    lines = [
        "# Live HTML inventory — 2026-08-29",
        "",
        "Read-only crawl of the dining room (npcwoods.com). Nothing was uploaded.",
        "SFTP was not available in this kitchen, so this used public URLs only",
        "(Yoast sitemaps + WordPress pages API + a clean-URL GET of each candidate).",
        "",
        "## Counts",
        "",
        f"- WordPress pages published: {len(wp_pages())}",
        f"- Yoast page sitemap URLs: {len(sitemap_urls('page-sitemap.xml'))}",
        f"- Yoast post sitemap URLs: {len(sitemap_urls('post-sitemap.xml'))} (left in WordPress; not static HTML)",
        f"- Freezer HTML/PHP paths already mapped: {len(local)}",
        f"- Dining-room-only unique plates pulled into git: {len(pulled)}",
        f"- Leftover city plates (not first-class): {len(by_kind.get('leftover_city', []))}",
        f"- Redirects (already have destination): {len(by_kind.get('redirect', []))}",
        f"- Wrong-plate leftovers: {len(by_kind.get('wrong_plate', []))}",
        f"- Empty shells left out: {len(by_kind.get('empty_shell', []))}",
        "",
        "## Pulled into the freezer (unique plates, were dining-room-only)",
        "",
    ]
    if pulled:
        lines.append("| Live URL | Bytes | Title | Saved as |")
        lines.append("|---|---:|---|---|")
        for r in pulled:
            lines.append(
                f"| https://npcwoods.com{r['path']} | {r['bytes']} | {r['title'] or r['h1']} | `{r['saved_as']}` |"
            )
    else:
        lines.append("None. Every real plate we could see already had a freezer copy.")
    lines += [
        "",
        "## Empty shells (not copied)",
        "",
        "These are WordPress stubs. They load, but they are not plates.",
        "Do not link them from `/sitemap/`, `/conditions/`, or state hubs.",
        "",
    ]
    shells = sorted(by_kind.get("empty_shell", []), key=lambda r: r["path"])
    if shells:
        lines.append("| Live URL | Bytes | Title | H1 |")
        lines.append("|---|---:|---|---|")
        for r in shells:
            lines.append(
                f"| https://npcwoods.com{r['path']} | {r['bytes']} | {r['title'] or '—'} | {r['h1'] or '—'} |"
            )
    else:
        lines.append("None found in this crawl.")
    lines += [
        "",
        "## Already in the freezer",
        "",
        f"{len(local)} paths already have a local HTML or PHP source.",
        "This crawl did not overwrite them.",
        "",
        "## What this could not see",
        "",
        "- Files that exist only on GoDaddy disk and are not a public WordPress page or sitemap URL.",
        "- That needs SFTP from `/Users/macmini/Desktop/Chris-HQ/.env` on the Mini.",
        "",
    ]
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_plate(path: str, body: bytes) -> str:
    rel = path.strip("/")
    dest = REPO / "landing-pages" / rel / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(body)
    return str(dest.relative_to(REPO))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--pull",
        action="store_true",
        help="Copy unique dining-room-only plates into landing-pages/ (not leftover city stubs)",
    )
    ap.add_argument(
        "--write-report",
        action="store_true",
        help="Overwrite the dated markdown report. Off by default so a hand-written inventory is kept.",
    )
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    local = local_url_map()
    print(f"[local] {len(local)} freezer paths")

    candidates: dict[str, str] = {}
    for p in wp_pages():
        candidates[norm_path(p["link"])] = "wp-page"
    for u in sitemap_urls("page-sitemap.xml"):
        candidates.setdefault(norm_path(u), "sitemap-page")
    for extra in (
        "/terms-of-service/",
        "/medical-disclaimer/",
        "/privacy-policy/",
        "/services/",
        "/thank-you/",
        "/conditions/poison-ivy-treatment/",
        "/conditions/nausea-vomiting-treatment/",
        "/urgent-care-price-guide/",
        "/when-to-see-provider-for-uti/",
    ):
        candidates.setdefault(extra, "known-legal")

    missing = {p: src for p, src in candidates.items() if p not in local and p not in SKIP_PATHS}
    print(f"[live] {len(candidates)} unique page URLs, {len(missing)} not in freezer")

    rows: list[dict] = []
    def fetch_one(path: str) -> dict:
        time.sleep(0.05)
        status, body, final = get(BASE + path)
        return classify_html(path, status, body, final)

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(fetch_one, p): p for p in sorted(missing)}
        for i, fut in enumerate(as_completed(futs), 1):
            row = fut.result()
            rows.append(row)
            print(
                f"[{i:3}/{len(missing)}] {row['kind']:12} {row['bytes']:7}  {row['path']}  {row['h1'][:50]}"
            )

    pulled = []
    if args.pull:
        for row in sorted(rows, key=lambda r: r["path"]):
            if row["kind"] != "unique_plate" or not row["body"]:
                continue
            saved = save_plate(row["path"], row["body"])
            row["saved_as"] = saved
            pulled.append(row)
            print(f"[pull] {row['path']} -> {saved} ({row['bytes']} bytes)")

    json_out = OUT_DIR / "LIVE-HTML-INVENTORY-2026-08-29.json"
    slim = [{k: v for k, v in r.items() if k != "body"} for r in rows]
    json_out.write_text(
        json.dumps({"local": local, "rows": slim, "pulled": [p["path"] for p in pulled]}, indent=2)
        + "\n"
    )
    if args.write_report:
        report = OUT_DIR / "LIVE-HTML-INVENTORY-2026-08-29.md"
        write_report(rows, local, pulled, report)
        print(f"[done] report -> {report}")
    print(
        f"[done] pulled {len(pulled)} unique plates; "
        f"leftover city {sum(1 for r in rows if r['kind']=='leftover_city')}; "
        f"redirects {sum(1 for r in rows if r['kind']=='redirect')}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
