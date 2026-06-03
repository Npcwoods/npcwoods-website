#!/usr/bin/env python3
"""Unified page deployment script for NPCWoods.com.

Automates:
 1. SFTP upload of local HTML landing page to remote server.
 2. Dynamic patching of the target mu-plugin routing file on the server.
 3. WP REST API stub creation/discovery.
 4. Sitemap exclusion patching in npcwoods-faq-schema.php (if --noindex).
 5. Invalidation of GoDaddy Varnish cache (empty page patch touch).
 6. Cache-busted HTTP verification of the live page.
"""
import argparse
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
BACKUP_DIR = ROOT.parent / "content-output" / "backups" / "deploys"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
TS = datetime.now().strftime("%Y%m%d-%H%M%S")


def load_env():
    if not ENV_PATH.exists():
        print(f"[fatal] .env file not found at {ENV_PATH}", file=sys.stderr)
        sys.exit(1)
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


def sftp_backup_and_upload(sftp, local_path, remote_path):
    backup_name = f"{remote_path.replace('/', '__')}.remote-backup-{TS}"
    backup_path = BACKUP_DIR / backup_name
    try:
        with sftp.file(remote_path, "r") as rf:
            backup_path.write_bytes(rf.read())
        print(f"  [backup] {remote_path} -> {backup_path.name}")
    except IOError:
        print(f"  [backup] {remote_path} did not exist yet (first deploy)")
    
    sftp_mkdir_safe(sftp, remote_path)
    sftp.put(str(local_path), remote_path)
    print(f"  [upload] {local_path.name} -> {remote_path}")


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
    existing = wp_request(env, "GET", f"/pages?slug={slug}&status=publish,draft")
    if isinstance(existing, list) and existing:
        page = existing[0]
        print(f"  [stub] found existing page id={page['id']} ({page['link']})")
        return page["id"]
    
    created = wp_request(env, "POST", "/pages", {
        "title": title,
        "slug": slug,
        "status": "publish",
        "content": f"<!-- This page is routed dynamically. The content here is irrelevant. -->",
        "comment_status": "closed",
        "ping_status": "closed",
    })
    if "id" not in created:
        print(f"  [stub] FAILED to create stub: {created}")
        sys.exit(1)
    print(f"  [stub] created page id={created['id']} ({created['link']})")
    return created["id"]


def patch_local_faq_schema(page_id, slug):
    faq_file = ROOT / "php" / "npcwoods-faq-schema.php"
    if not faq_file.exists():
        print(f"  [patch] faq-schema not found locally, skipping sitemap exclusion")
        return False
        
    text = faq_file.read_text(encoding="utf-8")
    marker = f"// /{slug}/ paid/noindex exclusion"
    if marker in text or f"{page_id}," in text:
        print(f"  [patch] sitemap exclusion already exists for page id={page_id}")
        return False
        
    # Find insertion point (we can insert after /pay/ exclusion, page 674)
    anchor = "        674,  // /pay/ (noindexed payment handoff)\n"
    insertion = f"{anchor}        {page_id},  {marker}\n"
    if anchor not in text:
        print("  [patch] WARNING: sitemap exclusion anchor not found in faq-schema.php")
        return False
        
    new_text = text.replace(anchor, insertion, 1)
    faq_file.write_text(new_text, encoding="utf-8")
    print(f"  [patch] added page id={page_id} to sitemap exclusion list locally")
    return True


def patch_mu_plugin(plugin_text, slug, remote_relative_path):
    if f"'{slug}'" in plugin_text or f'"{slug}"' in plugin_text:
        print(f"  [mu-plugin] route for '{slug}' already exists in map.")
        return plugin_text, False
        
    array_match = re.search(r'\$page_map\s*=\s*array\s*\(', plugin_text)
    if not array_match:
        print("  [mu-plugin] ERROR: Could not find $page_map array definition.")
        sys.exit(1)
        
    start_pos = array_match.end()
    new_entry = f'\n        "{slug}" => "{remote_relative_path}",'
    new_text = plugin_text[:start_pos] + new_entry + plugin_text[start_pos:]
    print(f"  [mu-plugin] added route: '{slug}' => '{remote_relative_path}'")
    return new_text, True


def main():
    parser = argparse.ArgumentParser(description="Unified deployment script for NPCWoods.com")
    parser.add_argument("--local", required=True, help="Local HTML file path")
    parser.add_argument("--slug", required=True, help="WordPress page slug (e.g. uti-care)")
    parser.add_argument("--title", required=True, help="WordPress page title")
    parser.add_argument("--remote", help="Remote HTML path (default: html/{slug}/index.html)")
    parser.add_argument("--mu-plugin", default="npcwoods-static-pages.php", help="Routing mu-plugin filename")
    parser.add_argument("--noindex", action="store_true", help="Add page to sitemap exclusion schema")
    args = parser.parse_args()

    local_html = Path(args.local)
    if not local_html.exists():
        print(f"[err] Local file not found: {local_html}", file=sys.stderr)
        return 1

    slug = args.slug.strip().lower()
    title = args.title.strip()
    remote_path = args.remote or f"html/{slug}/index.html"
    mu_plugin_name = args.mu_plugin

    print(f"=== Unified Deploy: /{slug}/ ===")
    print(f"  Time: {TS}")
    print(f"  Local HTML: {local_html}")
    print(f"  Remote HTML: {remote_path}")
    print(f"  Routing Plugin: {mu_plugin_name}\n")

    env = load_env()
    sftp, transport = sftp_connect(env)

    try:
        # Step 1: Upload HTML
        print("[1/5] Uploading HTML page...")
        sftp_backup_and_upload(sftp, local_html, remote_path)

        # Step 2: Route configuration in mu-plugin
        print("\n[2/5] Configuring mu-plugin routing...")
        remote_mu_path = f"html/wp-content/mu-plugins/{mu_plugin_name}"
        remote_relative_path = remote_path
        if remote_relative_path.startswith("html/"):
            remote_relative_path = remote_relative_path[len("html/"):]

        plugin_text = ""
        try:
            with sftp.file(remote_mu_path, "r") as rf:
                plugin_text = rf.read().decode("utf-8")
        except IOError:
            print(f"  [mu-plugin] remote mu-plugin '{mu_plugin_name}' not found. Cannot configure route.")
            return 1

        new_plugin_text, patched = patch_mu_plugin(plugin_text, slug, remote_relative_path)
        if patched:
            local_temp = ROOT / "backups" / f"{mu_plugin_name}.patched-{TS}"
            local_temp.parent.mkdir(parents=True, exist_ok=True)
            local_temp.write_text(new_plugin_text, encoding="utf-8")
            sftp_backup_and_upload(sftp, local_temp, remote_mu_path)
            local_temp.unlink()

        # Step 3: WordPress page stub creation
        print("\n[3/5] Setting up WordPress page stub...")
        page_id = get_or_create_stub(env, slug, title)

        # Step 4: Sitemap exclusion (if --noindex)
        if args.noindex:
            print("\n[4/5] Configuring sitemap exclusion (noindex)...")
            patched_faq = patch_local_faq_schema(page_id, slug)
            if patched_faq:
                local_faq = ROOT / "php" / "npcwoods-faq-schema.php"
                remote_faq = "html/wp-content/mu-plugins/npcwoods-faq-schema.php"
                sftp_backup_and_upload(sftp, local_faq, remote_faq)
        else:
            print("\n[4/5] Skipping sitemap exclusion (page is indexable)")

        # Step 5: Flush GoDaddy Varnish Cache
        print("\n[5/5] Flushing Varnish cache...")
        wp_request(env, "POST", f"/pages/{page_id}", {
            "content": f"<!-- Stub flushed at {TS}; routed dynamically by {mu_plugin_name}. -->"
        })
        print(f"  [flush] WP stub page {page_id} touched.")

    finally:
        sftp.close()
        transport.close()

    print("\n[wait] 5 seconds for Varnish cache to settle...")
    time.sleep(5)

    # Verification check
    print("\n[verify] Live URL cache-busted check:")
    bust = int(time.time())
    verify_url = f"https://npcwoods.com/{slug}/?v={bust}"
    req = urllib.request.Request(verify_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read(8000).decode("utf-8", errors="ignore")
            title_match = re.search(r"<title>([^<]+)</title>", body)
            live_title = title_match.group(1) if title_match else "(no title)"
            has_noindex = "noindex" in body.lower()
            print(f"  URL: https://npcwoods.com/{slug}/")
            print(f"  Status: {resp.status}")
            print(f"  Live Title: {live_title!r}")
            print(f"  Noindex Present: {has_noindex}")
    except urllib.error.HTTPError as e:
        print(f"  [verify] HTTP Error {e.code} for URL: {verify_url}")
    except Exception as e:
        print(f"  [verify] Error during verification: {e}")

    print(f"\n=== Deploy Complete for /{slug}/ (ID: {page_id}) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
