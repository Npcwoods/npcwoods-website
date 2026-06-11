#!/usr/bin/env python3
"""Flush GoDaddy/CDN cache for the June 10 discovery-audit pages by touching
their WordPress stubs (no-op REST update -> GoDaddy auto-purge).

Mirrors the proven approach in bulk-flush-pages-2026-04-22.py but is driven by
the exact files in commit f9a2d94. Dry-run prints the plan; --execute touches.
"""
import argparse
import base64
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT.parent / ".env"
COMMIT = "f9a2d94"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

KNOWN_IDS = {
    "/": 63, "/experience/": 310, "/blog/": 413,
    "/georgia-telemedicine/": 252, "/north-carolina-telemedicine/": 253,
    "/dental-pain/": 336, "/pharmacy/": 334, "/pharmacy-partners/": 335,
    "/uti-treatment/mesa-az/": 13, "/uti-treatment/surprise-az/": 20,
    "/uti-treatment/scottsdale-az/": 17, "/uti-treatment/albuquerque-nm/": 411,
    "/do-i-need-antibiotics-sinus-infection/": 454,
}


def load_env():
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def deployed_urls():
    out = subprocess.run(["git", "show", "--name-status", "--format=", COMMIT],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    urls = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if parts[0].startswith("D"):
            continue
        rel = parts[-1]
        if not rel.endswith("index.html"):
            continue
        if "_archive/" in rel or ".bak" in rel:
            continue
        if rel.startswith("landing-pages/"):
            d = rel[len("landing-pages/"):-len("index.html")]
        elif rel.startswith("html/"):
            d = rel[len("html/"):-len("index.html")]
        else:
            continue
        url = "/" + d.strip("/")
        url = (url + "/") if not url.endswith("/") else url
        if url == "//":
            url = "/"
        urls.append(url)
    return sorted(set(urls))


def req(url, auth, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": f"Basic {auth}", "User-Agent": UA}
    if body is not None:
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, json.loads(resp.read() or "null")
    except urllib.error.HTTPError as e:
        return e.code, None


def lookup_id(slug, auth):
    u = f"https://npcwoods.com/wp-json/wp/v2/pages?slug={urllib.parse.quote(slug)}&_fields=id&per_page=3"
    st, data = req(u, auth)
    if st == 200 and isinstance(data, list) and data:
        return int(data[0]["id"])
    return None


def touch(page_id, auth):
    for pt in ("pages", "posts"):
        base = f"https://npcwoods.com/wp-json/wp/v2/{pt}/{page_id}"
        st, cur = req(f"{base}?_fields=id,content,title,status", auth)
        if st == 404 or not cur:
            continue
        payload = {
            "title": cur.get("title", {}).get("raw") or cur.get("title", {}).get("rendered", ""),
            "content": cur.get("content", {}).get("raw") or cur.get("content", {}).get("rendered", ""),
            "status": cur.get("status", "publish"),
        }
        st2, _ = req(base, auth, method="POST", body=payload)
        return st2 == 200
    return False


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="touch only first N (for testing)")
    args = ap.parse_args((argv or sys.argv)[1:])

    env = load_env()
    auth = base64.b64encode(f"{env['WP_USERNAME']}:{env['WP_APP_PASSWORD']}".encode()).decode()
    urls = deployed_urls()
    if args.limit:
        urls = urls[: args.limit]
    print(f"[plan] {len(urls)} pages to flush")

    if not args.execute:
        for u in urls[:10]:
            print("  ", u)
        if len(urls) > 10:
            print(f"   ...+{len(urls)-10} more")
        print("\n[dry-run] add --execute to touch WP stubs.")
        return 0

    flushed, no_stub, failed = [], [], []
    for u in urls:
        pid = KNOWN_IDS.get(u) or lookup_id(u.strip("/").split("/")[-1] or "home", auth)
        if not pid:
            no_stub.append(u)
            print(f"  [no-stub] {u} (relies on GoDaddy auto-purge of static file)")
            continue
        ok = touch(pid, auth)
        (flushed if ok else failed).append(u)
        print(f"  [{'ok' if ok else 'FAIL'}] {u} (id {pid})")
        time.sleep(0.4)
    print(f"\n[done] flushed {len(flushed)}, no-stub {len(no_stub)}, failed {len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
