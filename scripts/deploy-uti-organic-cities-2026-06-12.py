#!/usr/bin/env python3
"""Deploy the 4 INDEXABLE organic UTI city pages (Chris approval required).

Chandler, Gilbert, Tempe, Glendale already have published WP page stubs under
/uti-treatment/ (ids 14/15/16/19) that currently return 403 because no static
file backs them — a live SEO problem (published-but-broken URLs in the XML
sitemap). This uploads the real Apple-design organic pages, then touches each
stub to flush the GoDaddy edge cache. Apache serves the physical index.html
directly, and the page is already in sitemap_index.xml via its published stub.

Dry-run is the default; add --execute to deploy.
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

# slug -> published WP stub id under /uti-treatment/ (for cache flush)
PAGES = {
    "chandler-az": 14,
    "gilbert-az": 15,
    "glendale-az": 16,
    "tempe-az": 19,
}

REQUIRED = [
    "GTM-59QSWZRC",
    "gtag/js?id=G-EFFRQMG8TC",
    "AW-610222919",
    "tracking.js",
    "window.fbq = function",
]
FORBIDDEN = [
    "connect.facebook.net",
    "facebook.com/tr",
    "insurance",
    "surprise-az",
    "Adelante",
    "Banner Del E. Webb",
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
    path = ""
    for part in remote_dir.split("/"):
        path = f"{path}/{part}" if path else part
        try:
            sftp.stat(path)
        except FileNotFoundError:
            sftp.mkdir(path)


def verify_live(slug):
    url = f"https://npcwoods.com/uti-treatment/{slug}/?v={int(time.time())}"
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            status = resp.status
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    if status != 200 or not html.lstrip().startswith("<!DOCTYPE html>"):
        return f"bad response ({status})"
    if "noindex" in html.lower():
        return "page is noindex (must stay indexable)"
    missing = [m for m in REQUIRED if m not in html]
    if missing:
        return f"missing markers: {missing}"
    if f"/uti-treatment/{slug}/" not in html:
        return "canonical not localized"
    return None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Deploy 4 organic UTI city pages. Dry-run by default.")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args((argv or sys.argv)[1:])

    for slug in PAGES:
        local = ROOT / f"landing-pages/uti-treatment/{slug}/index.html"
        html = local.read_text()
        low = html.lower()
        for m in REQUIRED:
            if m not in html:
                raise RuntimeError(f"{slug}: missing required marker: {m}")
        for b in FORBIDDEN:
            if b.lower() in low:
                raise RuntimeError(f"{slug}: contains forbidden marker: {b}")
        if "noindex" in low:
            raise RuntimeError(f"{slug}: has noindex — organic pages must stay indexable")
        print(f"[plan] {slug} -> html/uti-treatment/{slug}/index.html (touch stub {PAGES[slug]})")

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
        remote = f"html/uti-treatment/{slug}/index.html"
        sftp_mkdirs(sftp, posixpath.dirname(remote))
        sftp.put(str(ROOT / f"landing-pages/uti-treatment/{slug}/index.html"), remote)
        print(f"[up] {remote}")
    sftp.close()
    transport.close()

    auth = base64.b64encode(f"{env['WP_USERNAME']}:{env['WP_APP_PASSWORD']}".encode()).decode()
    failures = 0
    for slug, stub_id in PAGES.items():
        ok = touch_stub(auth, stub_id)
        print(f"[cache] stub {stub_id} ({slug}): {'ok' if ok else 'FAILED — flush manually'}")
        failures += 0 if ok else 1

    print("[verify] checking live URLs with cache buster")
    time.sleep(10)
    for slug in PAGES:
        problem = verify_live(slug)
        print(f"[live] {slug}: {'OK (200, indexable)' if not problem else problem}")
        failures += 0 if not problem else 1

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
