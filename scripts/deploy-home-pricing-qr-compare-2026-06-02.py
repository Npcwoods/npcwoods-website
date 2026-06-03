#!/usr/bin/env python3
"""Deploy homepage + pricing QR/comparison update (2026-06-02).

Two files, both via SFTP, then a Varnish flush so the new HTML is served fresh.

 1. Backup + SFTP upload homepage PHP template -> theme dir
 2. Backup + SFTP upload pricing static HTML -> html/pricing/index.html
 3. WP REST: touch homepage (page 63) + pricing stub to flush GoDaddy Varnish
 4. Cache-busted live verification

Refs: WL-002 (cache lies), GL-008 (Varnish trap), GL-010 (verify live).
"""
import base64
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

import paramiko

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT.parent / ".env"
BACKUP_DIR = ROOT.parent / "content-output" / "reports" / "home-pricing-qr-compare" / "remote-backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

LOCAL_HOMEPAGE = ROOT / "homepage" / "page-npcwoods-home.php"
LOCAL_PRICING = ROOT / "landing-pages" / "pricing" / "index.html"

REMOTE_HOMEPAGE = "html/wp-content/themes/twentytwentyfour/page-npcwoods-home.php"
REMOTE_PRICING = "html/pricing/index.html"

HOMEPAGE_PAGE_ID = 63  # per npcwoods-website/CLAUDE.md

TS = datetime.now().strftime("%Y%m%d-%H%M%S")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
CONFIRM = "CHRIS APPROVED LIVE DEPLOY"


def load_env():
    env = {}
    for raw in ENV_PATH.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def sftp_connect(env):
    transport = paramiko.Transport((env["SFTP_HOST"], int(env["SFTP_PORT"])))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    return paramiko.SFTPClient.from_transport(transport), transport


def sftp_mkdir_safe(sftp, remote_path):
    parts = remote_path.split("/")
    for i in range(1, len(parts)):
        try:
            sftp.mkdir("/".join(parts[:i]))
        except IOError:
            pass


def sftp_backup_then_upload(sftp, local, remote):
    backup_name = f"{remote.replace('/', '__')}.remote-backup-{TS}"
    backup_path = BACKUP_DIR / backup_name
    try:
        with sftp.file(remote, "r") as rf:
            backup_path.write_bytes(rf.read())
        print(f"  [backup] {remote} -> {backup_path.name}")
    except IOError:
        print(f"  [backup] {remote} did not exist (first deploy)")
    sftp_mkdir_safe(sftp, remote)
    sftp.put(str(local), remote)
    print(f"  [upload] {local.name} -> {remote}")


def wp_request(env, method, path, body=None):
    url = f"https://npcwoods.com/wp-json/wp/v2{path}"
    auth = base64.b64encode(f"{env['WP_USERNAME']}:{env['WP_APP_PASSWORD']}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    }
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode()[:500]}


def touch_page(env, page_id, label):
    result = wp_request(env, "POST", f"/pages/{page_id}", {
        "content": f"<!-- {label} stub touched at {TS} to flush Varnish. -->",
    }) if False else None
    # Homepage (63) renders via theme template, not REST content — do NOT overwrite
    # its content. Instead touch its meta via a no-op modified bump using a draft-safe
    # approach: re-save without changing content by sending the same title.
    page = wp_request(env, "GET", f"/pages/{page_id}?context=edit")
    if "id" not in page:
        print(f"  [flush] WARNING: could not load page {page_id}: {page}")
        return
    raw_title = page.get("title", {}).get("raw") or page.get("title", {}).get("rendered", "")
    bumped = wp_request(env, "POST", f"/pages/{page_id}", {"title": raw_title})
    if "id" in bumped:
        print(f"  [flush] {label} (id {page_id}) touched -> {bumped.get('modified')}")
    else:
        print(f"  [flush] WARNING: touch returned {bumped}")


def find_stub_id(env, slug):
    res = wp_request(env, "GET", f"/pages?slug={slug}&status=publish,draft")
    if isinstance(res, list) and res:
        return res[0]["id"]
    return None


def verify(env):
    print("\n[verify] cache-busted live checks:")
    bust = int(time.time())
    checks = [
        ("homepage", f"https://npcwoods.com/?v={bust}", ["NPCWoods vs. Big Telehealth", "Scan to Text Us", "npc-qr-code"]),
        ("pricing", f"https://npcwoods.com/pricing/?v={bust}", ["NPCWoods vs. Big Telehealth", "vscmp"]),
    ]
    for label, url, needles in checks:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                body = resp.read().decode(errors="ignore")
                title_match = re.search(r"<title>([^<]+)</title>", body)
                title = title_match.group(1) if title_match else "(no title)"
                found = {n: (n in body) for n in needles}
                charset_ok = bool(re.match(r"\s*<meta charset", body[body.lower().find("<head>") + 6:], re.I)) or "<meta charset=\"UTF-8\">" in body[:body.lower().find("<head>") + 120]
                print(f"  [{label}] {resp.status} | title={title[:55]!r}")
                for n, ok in found.items():
                    print(f"      {'OK ' if ok else 'MISS'} contains {n!r}")
        except urllib.error.HTTPError as e:
            print(f"  [{label}] HTTP {e.code} {url}")
        except Exception as e:
            print(f"  [{label}] ERROR {e}")


def main():
    if "--execute" not in sys.argv:
        print("DRY RUN. Would upload:")
        print(f"  {LOCAL_HOMEPAGE.relative_to(ROOT)} -> {REMOTE_HOMEPAGE}")
        print(f"  {LOCAL_PRICING.relative_to(ROOT)} -> {REMOTE_PRICING}")
        print(f"\nRe-run with: --execute --confirm \"{CONFIRM}\"")
        return 0
    if CONFIRM not in sys.argv:
        print(f"[gate] missing confirmation phrase: \"{CONFIRM}\"")
        return 2

    for f in [LOCAL_HOMEPAGE, LOCAL_PRICING]:
        if not f.exists():
            print(f"[err] missing: {f}")
            return 1

    print(f"=== Deploy homepage + pricing (QR/comparison) at {TS} ===\n")
    env = load_env()
    print(f"[sftp] connecting to {env['SFTP_HOST']}:{env['SFTP_PORT']}\n")
    sftp, transport = sftp_connect(env)
    try:
        print("[1/3] SFTP uploads")
        sftp_backup_then_upload(sftp, LOCAL_HOMEPAGE, REMOTE_HOMEPAGE)
        sftp_backup_then_upload(sftp, LOCAL_PRICING, REMOTE_PRICING)
    finally:
        sftp.close()
        transport.close()

    print("\n[2/3] Flush Varnish (touch homepage + pricing stub)")
    touch_page(env, HOMEPAGE_PAGE_ID, "homepage")
    pricing_id = find_stub_id(env, "pricing")
    if pricing_id:
        touch_page(env, pricing_id, "pricing")
    else:
        print("  [flush] pricing stub not found by slug 'pricing' (skipping touch)")

    print("\n[3/3] Wait 6s for Varnish to settle...")
    time.sleep(6)
    verify(env)
    print(f"\n=== Done. Backups at: {BACKUP_DIR} ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
