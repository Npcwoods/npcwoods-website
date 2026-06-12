#!/usr/bin/env python3
"""Deploy the 7 search-safe UTI city pages (Chris approval required).

Pages built overnight 2026-06-11 by scripts/build-uti-search-safe-cities-2026-06-11.py
from the proven Mesa search-safe template, Playwright-verified on the Vercel
review lane. This script uploads them to GoDaddy and flushes cache stubs
where they exist. New-city URLs (chandler/gilbert/tempe/glendale) have never
been served, so they have no stale cache and need no stub.

Dry-run is the default; add --execute to deploy. After deploy, run:
    python3 tests/verify-uti-search-safe-cities-tracking.py
"""
import argparse
import base64
import json
import posixpath
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT.parent / ".env"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# slug -> WP stub ID for cache flush (None = brand-new URL, nothing cached)
PAGES = {
    "mesa-az": 13,
    "scottsdale-az": 17,
    "surprise-az": 20,
    "albuquerque-nm": 411,
    "chandler-az": None,
    "gilbert-az": None,
    "tempe-az": None,
    "glendale-az": None,
}

REQUIRED = [
    "GTM-59QSWZRC",
    "gtag/js?id=G-EFFRQMG8TC",
    "AW-610222919",
    "tracking.js",
    'content="noindex,follow"',
    "Most patients hear back the same day, usually within a few hours.",
]
FORBIDDEN = [
    "connect.facebook.net",
    "facebook.com/tr",
    'fbq("init"',
    "fbq('init'",
    "nitrofurantoin",
    "trimethoprim",
    "macrobid",
    "bactrim",
    "cephalexin",
    "phenazopyridine",
    "nystatin",
    "antibiotic",
    "prescription",
    "insurance",
]


def load_env():
    env = {}
    for raw in ENV_PATH.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def wp_req(url, auth, method="GET", body=None):
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


def touch_stub(auth, stub_id):
    base = f"https://npcwoods.com/wp-json/wp/v2/pages/{stub_id}"
    st, cur = wp_req(f"{base}?_fields=id,content,title,status", auth)
    if st != 200 or not cur:
        return False
    payload = {
        "title": cur.get("title", {}).get("raw") or cur.get("title", {}).get("rendered", ""),
        "content": cur.get("content", {}).get("raw") or cur.get("content", {}).get("rendered", ""),
        "status": cur.get("status", "publish"),
    }
    st2, _ = wp_req(base, auth, method="POST", body=payload)
    return st2 == 200


def sftp_mkdirs(sftp, remote_dir):
    parts = remote_dir.split("/")
    path = ""
    for part in parts:
        path = f"{path}/{part}" if path else part
        try:
            sftp.stat(path)
        except FileNotFoundError:
            sftp.mkdir(path)


def verify_live(slug):
    url = f"https://npcwoods.com/uti-treatment/{slug}/search-safe/?v={int(time.time())}"
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(r, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="replace")
    if resp.status != 200 or not html.lstrip().startswith("<!DOCTYPE html>"):
        return f"bad response ({resp.status})"
    missing = [m for m in REQUIRED if m not in html]
    if missing:
        return f"missing markers: {missing}"
    return None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Deploy 7 search-safe UTI city pages. Dry-run by default.")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args((argv or sys.argv)[1:])

    # pre-flight: marker checks on every local file before anything uploads
    for slug in PAGES:
        local = ROOT / f"landing-pages/uti-treatment/{slug}/search-safe/index.html"
        html = local.read_text()
        lower = html.lower()
        for marker in REQUIRED:
            if marker not in html:
                raise RuntimeError(f"{slug}: missing required marker: {marker}")
        for bad in FORBIDDEN:
            if bad.lower() in lower:
                raise RuntimeError(f"{slug}: contains forbidden marker: {bad}")
        print(f"[plan] {slug} -> html/uti-treatment/{slug}/search-safe/index.html"
              + (f" (touch stub {PAGES[slug]})" if PAGES[slug] else " (new URL, no stub)"))

    if not args.execute:
        print("[dry-run] nothing uploaded. Add --execute to deploy.")
        return 0

    env = load_env()
    import paramiko

    print(f"[sftp] connecting to {env['SFTP_HOST']}:{env['SFTP_PORT']}")
    transport = paramiko.Transport((env["SFTP_HOST"], int(env["SFTP_PORT"])))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(transport)
    for slug in PAGES:
        remote = f"html/uti-treatment/{slug}/search-safe/index.html"
        sftp_mkdirs(sftp, posixpath.dirname(remote))
        sftp.put(str(ROOT / f"landing-pages/uti-treatment/{slug}/search-safe/index.html"), remote)
        print(f"[up] {remote}")
    sftp.close()
    transport.close()

    auth = base64.b64encode(f"{env['WP_USERNAME']}:{env['WP_APP_PASSWORD']}".encode()).decode()
    failures = 0
    for slug, stub_id in PAGES.items():
        if stub_id:
            ok = touch_stub(auth, stub_id)
            print(f"[cache] stub {stub_id} ({slug}): {'ok' if ok else 'FAILED — flush manually'}")
            failures += 0 if ok else 1

    print("[verify] checking live URLs with cache buster")
    time.sleep(10)
    for slug in PAGES:
        problem = verify_live(slug)
        print(f"[live] {slug}: {'OK' if not problem else problem}")
        failures += 0 if not problem else 1

    if not failures:
        print("[next] python3 tests/verify-uti-search-safe-cities-tracking.py")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
