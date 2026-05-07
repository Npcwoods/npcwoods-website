#!/usr/bin/env python3
"""Bulk-flush NPCWoods WP page cache after schema fix deploy (2026-04-22).

For each route in scripts/modified-files.txt, we:
  1. Derive the expected URL slug from the local path
  2. Look up the WP page ID via REST (cached in scripts/page-ids-2026-04-22.json)
  3. POST a no-op update to trigger GoDaddy's Varnish auto-purge
  4. For routes without WP stubs, fall back to Cloudflare URL purge

Known IDs are seeded from npcwoods-website/CLAUDE.md + task brief. Unknown slugs
resolve via GET /wp-json/wp/v2/pages?slug=<slug>.
"""

import argparse
import base64
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests not installed. Run: pip3 install requests", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = Path("/Users/chriswoods/Desktop/Chris-HQ/.env")
MANIFEST = REPO_ROOT / "scripts" / "modified-files.txt"
CACHE = REPO_ROOT / "scripts" / "page-ids-2026-04-22.json"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# From npcwoods-website/CLAUDE.md + task brief
KNOWN_IDS: dict[str, int] = {
    "/": 63,
    "/experience/": 310,
    "/blog/": 413,
    "/georgia-telemedicine/": 252,
    "/north-carolina-telemedicine/": 253,
    "/affordable-telemedicine-arizona-no-insurance/": 198,
    "/dental-pain/": 336,
    "/pharmacy/": 334,
    "/pharmacy-partners/": 335,
    # UTI city pages served by npcwoods-llmseo-pages.php
    "/uti-treatment/mesa-az/": 13,
    "/uti-treatment/surprise-az/": 20,
    "/uti-treatment/scottsdale-az/": 17,
    "/uti-treatment/albuquerque-nm/": 411,
}


def load_env() -> dict:
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def local_path_to_url(rel: str) -> str:
    """Map local repo path → production URL path.

    landing-pages/uti-treatment/index.html -> /uti-treatment/
    landing-pages/uti-treatment/mesa-az/index.html -> /uti-treatment/mesa-az/
    landing-pages/medications/amoxicillin/index.html -> /medications/amoxicillin/
    landing-pages/learn/uti/index.html -> /learn/uti/
    html/experience/index.html -> /experience/
    html/about/index.html -> /about/
    """
    if rel.endswith("/index.html"):
        dir_path = rel[: -len("index.html")]
    else:
        dir_path = rel
    for prefix in ("landing-pages/", "html/"):
        if dir_path.startswith(prefix):
            dir_path = dir_path[len(prefix):]
            break
    if not dir_path.startswith("/"):
        dir_path = "/" + dir_path
    if not dir_path.endswith("/"):
        dir_path = dir_path + "/"
    return dir_path


def url_to_slug(url_path: str) -> str:
    """Last non-empty path segment is typically the WP slug.

    /uti-treatment/ -> uti-treatment
    /uti-treatment/mesa-az/ -> mesa-az
    /medications/amoxicillin/ -> amoxicillin
    """
    parts = [p for p in url_path.strip("/").split("/") if p]
    return parts[-1] if parts else ""


def lookup_page_id(slug: str, auth: str) -> int | None:
    """GET /wp-json/wp/v2/pages?slug=<slug> — returns first match's ID."""
    url = f"https://npcwoods.com/wp-json/wp/v2/pages?slug={urllib.parse.quote(slug)}&_fields=id,slug,link&per_page=5"
    try:
        r = requests.get(url, headers={"Authorization": auth, "User-Agent": UA}, timeout=20)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and data:
            return int(data[0]["id"])
    except Exception as e:
        print(f"  [lookup fail] slug={slug!r}: {e}")
    return None


def touch_page(page_id: int, auth: str) -> bool:
    """POST a no-op update to /wp-json/wp/v2/pages/{id} to trigger cache purge."""
    url = f"https://npcwoods.com/wp-json/wp/v2/pages/{page_id}"
    # Re-send current content to trigger save hook -> GoDaddy cache purge
    try:
        # Fetch current content first
        r = requests.get(
            f"{url}?_fields=id,content,title,status",
            headers={"Authorization": auth, "User-Agent": UA},
            timeout=20,
        )
        r.raise_for_status()
        current = r.json()
        payload = {
            "title": current.get("title", {}).get("raw") or current.get("title", {}).get("rendered", ""),
            "content": current.get("content", {}).get("raw") or current.get("content", {}).get("rendered", ""),
            "status": current.get("status", "publish"),
        }
        r2 = requests.post(
            url,
            headers={"Authorization": auth, "User-Agent": UA, "Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=30,
        )
        r2.raise_for_status()
        return True
    except Exception as e:
        print(f"  [touch fail] id={page_id}: {e}")
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--sleep", type=float, default=0.6, help="seconds between POSTs")
    args = ap.parse_args()

    env = load_env()
    wp_user = env.get("WP_USERNAME")
    wp_pw = env.get("WP_APP_PASSWORD")
    if not wp_user or not wp_pw:
        print("[fatal] missing WP_USERNAME / WP_APP_PASSWORD in .env", file=sys.stderr)
        return 2
    auth = "Basic " + base64.b64encode(f"{wp_user}:{wp_pw}".encode()).decode()

    if not MANIFEST.exists():
        print(f"[fatal] {MANIFEST} missing")
        return 2

    paths = [p for p in MANIFEST.read_text(encoding="utf-8").splitlines() if p.strip()]
    # Always include the homepage since we deployed page-npcwoods-home.php
    urls = ["/"]
    for rel in paths:
        urls.append(local_path_to_url(rel))
    # Deduplicate preserving order
    seen = set()
    urls = [u for u in urls if not (u in seen or seen.add(u))]

    # Cache of resolved IDs
    id_cache: dict[str, int] = {}
    if CACHE.exists():
        id_cache = json.loads(CACHE.read_text(encoding="utf-8"))

    print(f"Flushing cache for {len(urls)} URL(s)")
    touched: list[str] = []
    not_found: list[str] = []
    errors: list[str] = []

    for i, url_path in enumerate(urls):
        cache_key = url_path
        page_id = KNOWN_IDS.get(url_path) or id_cache.get(cache_key)

        if page_id is None:
            slug = url_to_slug(url_path)
            if slug:
                page_id = lookup_page_id(slug, auth)
                if page_id:
                    id_cache[cache_key] = page_id

        if page_id is None:
            print(f"  [{i+1}/{len(urls)}] {url_path}  -- no stub found")
            not_found.append(url_path)
            continue

        if args.dry_run:
            print(f"  [{i+1}/{len(urls)}] {url_path}  -> id={page_id}  [DRY]")
        else:
            ok = touch_page(page_id, auth)
            status = "OK" if ok else "FAIL"
            print(f"  [{i+1}/{len(urls)}] {url_path}  -> id={page_id}  [{status}]")
            if ok:
                touched.append(url_path)
            else:
                errors.append(url_path)

        if i < len(urls) - 1:
            time.sleep(args.sleep)

    # Persist the id cache
    CACHE.write_text(json.dumps(id_cache, indent=2), encoding="utf-8")

    print()
    print(f"Touched:   {len(touched)}")
    print(f"Not found: {len(not_found)}")
    print(f"Errors:    {len(errors)}")
    print(f"ID cache:  {CACHE.relative_to(REPO_ROOT)}  ({len(id_cache)} entries)")

    if not_found:
        print()
        print("Routes without WP stubs (need Cloudflare purge):")
        for u in not_found:
            print(f"  - https://npcwoods.com{u}")
        # Emit a list for cf-purge
        cf_list = REPO_ROOT / "scripts" / "cf-purge-list-2026-04-22.txt"
        cf_list.write_text("\n".join(f"https://npcwoods.com{u}" for u in not_found) + "\n", encoding="utf-8")
        print(f"\nWrote: {cf_list.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
