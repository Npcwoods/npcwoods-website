#!/usr/bin/env python3
"""Deploy /uti-care/ noindex paid-traffic clone of /uti-treatment/.

Steps (in order, with rollback hooks):
 1. Backup existing remote files (if any) to remote-backups/
 2. SFTP upload html/uti-care/index.html
 3. SFTP upload mu-plugin npcwoods-paid-pages.php
 4. SFTP upload modified shared/tracking.js to BOTH /tracking.js and /shared/tracking.js
 5. WP REST: create page stub at slug 'uti-care' (or find existing) → record page ID
 6. Patch php/npcwoods-faq-schema.php with the page ID in the exclusion array
 7. SFTP upload the patched faq-schema.php to mu-plugins/
 8. WP REST: touch the stub (empty patch) to flush GoDaddy Varnish
 9. Print page ID + verification URLs

Reference incidents: GL-005 (April ghost-conv burn), GL-008 (Varnish cache trap), WL-002 (cache lies).
"""
import base64
import json
import os
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
BACKUP_DIR = ROOT.parent / "content-output" / "reports" / "uti-care-launch" / "remote-backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

LOCAL_HTML = ROOT / "landing-pages" / "uti-care" / "index.html"
LOCAL_MUPLUGIN = ROOT / "php" / "npcwoods-paid-pages.php"
LOCAL_TRACKING = ROOT / "html" / "shared" / "tracking.js"
LOCAL_FAQ_SCHEMA = ROOT / "php" / "npcwoods-faq-schema.php"

REMOTE_HTML = "html/uti-care/index.html"
REMOTE_MUPLUGIN = "html/wp-content/mu-plugins/npcwoods-paid-pages.php"
REMOTE_TRACKING_PATHS = ["html/tracking.js", "html/shared/tracking.js"]
REMOTE_FAQ_SCHEMA = "html/wp-content/mu-plugins/npcwoods-faq-schema.php"

TS = datetime.now().strftime("%Y%m%d-%H%M%S")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


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


def sftp_backup_then_upload(sftp, local, remote, label):
    """Read remote (if it exists), save to BACKUP_DIR, then upload local."""
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


def get_or_create_stub(env, slug, title):
    # Try to find existing
    existing = wp_request(env, "GET", f"/pages?slug={slug}&status=publish,draft")
    if isinstance(existing, list) and existing:
        page = existing[0]
        print(f"  [stub] found existing page id={page['id']} ({page['link']})")
        return page["id"]
    # Create
    created = wp_request(env, "POST", "/pages", {
        "title": title,
        "slug": slug,
        "status": "publish",
        "content": "<!-- This page is routed by npcwoods-paid-pages.php mu-plugin. The content here is irrelevant. -->",
        "comment_status": "closed",
        "ping_status": "closed",
    })
    if "id" not in created:
        print(f"  [stub] FAILED to create stub: {created}")
        sys.exit(1)
    print(f"  [stub] created page id={created['id']} ({created['link']})")
    return created["id"]


def patch_faq_schema(page_id):
    """Insert the UTI Care page ID into the sitemap exclusion array.

    Idempotent — won't insert twice. Marks insertion with a unique comment string.
    """
    text = LOCAL_FAQ_SCHEMA.read_text()
    marker = f"// /uti-care/ paid Google + Facebook clone (noindexed)"
    if marker in text:
        print(f"  [patch] already patched — marker present, skipping")
        return False
    if str(page_id) + "," in text and marker not in text:
        print(f"  [patch] page id {page_id} already in file (different comment) — skipping insert")
        return False
    # Insert after the existing "noindexed pages" block (after page 674).
    insertion = f"""        674,  // /pay/ (noindexed payment handoff)

        // ============================================================
        // PAID-ONLY NOINDEX CLONES (not in sitemap; only paid traffic lands here)
        // ============================================================
        {page_id},  // /uti-care/ paid Google + Facebook clone (noindexed)
"""
    new_text = text.replace(
        "        674,  // /pay/ (noindexed payment handoff)\n",
        insertion,
        1,
    )
    if new_text == text:
        print(f"  [patch] FAILED — anchor line not found; manual edit needed")
        sys.exit(1)
    LOCAL_FAQ_SCHEMA.write_text(new_text)
    print(f"  [patch] inserted page id {page_id} into exclusion array (local)")
    return True


def touch_stub_to_flush_varnish(env, page_id):
    """Touch the WP page (empty content patch) to invalidate GoDaddy Varnish cache."""
    result = wp_request(env, "POST", f"/pages/{page_id}", {
        "content": f"<!-- Stub touched at {TS} to flush Varnish; routed by mu-plugin. -->",
    })
    if "id" in result:
        print(f"  [flush] WP stub {page_id} touched ({result.get('modified', 'modified')})")
    else:
        print(f"  [flush] WARNING: touch returned {result}")


def verify(env, page_id):
    print("\n[verify] cache-busted live checks:")
    bust = int(time.time())
    for label, url in [
        ("clone w/ gclid", f"https://npcwoods.com/uti-care/?gclid=DEPLOY_VERIFY_{TS}&v={bust}"),
        ("clone plain", f"https://npcwoods.com/uti-care/?v={bust}"),
        ("organic regression", f"https://npcwoods.com/uti-treatment/?v={bust}"),
        ("robots.txt", "https://npcwoods.com/robots.txt"),
    ]:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read(8000).decode(errors="ignore")
                title_match = re.search(r"<title>([^<]+)</title>", body)
                title = title_match.group(1) if title_match else "(no title)"
                has_noindex = "noindex" in body.lower()
                has_uti_care_disallow = "disallow: /uti-care" in body.lower()
                print(f"  [{label}] {resp.status} | title={title[:60]!r} | noindex={has_noindex} | robots_blocks_uti_care={has_uti_care_disallow}")
        except urllib.error.HTTPError as e:
            print(f"  [{label}] HTTP {e.code} {url}")
        except Exception as e:
            print(f"  [{label}] ERROR {e}")


def main():
    print(f"=== Deploy /uti-care/ at {TS} ===\n")

    # Preflight
    for f in [LOCAL_HTML, LOCAL_MUPLUGIN, LOCAL_TRACKING, LOCAL_FAQ_SCHEMA]:
        if not f.exists():
            print(f"[err] missing: {f}")
            return 1

    env = load_env()
    print(f"[sftp] connecting to {env['SFTP_HOST']}:{env['SFTP_PORT']}\n")

    sftp, transport = sftp_connect(env)
    try:
        print("[1/4] SFTP uploads (HTML + mu-plugin + tracking.js)")
        sftp_backup_then_upload(sftp, LOCAL_HTML, REMOTE_HTML, "uti-care HTML")
        sftp_backup_then_upload(sftp, LOCAL_MUPLUGIN, REMOTE_MUPLUGIN, "paid-pages mu-plugin")
        for remote in REMOTE_TRACKING_PATHS:
            sftp_backup_then_upload(sftp, LOCAL_TRACKING, remote, "tracking.js")

        print("\n[2/4] WP REST: stub creation")
        page_id = get_or_create_stub(env, "uti-care", "UTI Care")

        print("\n[3/4] Patch faq-schema with sitemap exclusion")
        patched = patch_faq_schema(page_id)
        if patched:
            sftp_backup_then_upload(sftp, LOCAL_FAQ_SCHEMA, REMOTE_FAQ_SCHEMA, "faq-schema patched")

        print("\n[4/4] Touch WP stub to flush Varnish")
        touch_stub_to_flush_varnish(env, page_id)
    finally:
        sftp.close()
        transport.close()

    # Wait briefly for cache to settle before verification
    print("\n[wait] 5s for Varnish to settle...")
    time.sleep(5)

    verify(env, page_id)

    print(f"\n=== Done. UTI_CARE_PAGE_ID={page_id} ===")
    print(f"Backups at: {BACKUP_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
