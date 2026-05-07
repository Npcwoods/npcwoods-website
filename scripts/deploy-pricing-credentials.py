#!/usr/bin/env python3
"""
Deploy /pricing/ and /credentials/ to NPCWoods.com.

Steps (all idempotent — safe to rerun):
  1. Load .env
  2. Add 'pricing' + 'credentials' to npcwoods-static-pages.php page_map (skip if present)
  3. SFTP upload:
       - html/pricing/index.html
       - html/credentials/index.html
       - html/wp-content/mu-plugins/npcwoods-static-pages.php
       - html/llms.txt
       - html/llms-full.txt
  4. Create/update WP page stubs for /pricing/ and /credentials/ via REST API (sitemap inclusion)
  5. Cache-bust curl verify both URLs return 200
  6. Print a schema-validator URL for each page

Uses:
  - paramiko with banner_timeout/auth_timeout = 30 (per feedback_paramiko_godaddy_timeout)
  - cache-bust `?v=<epoch>` on verification (per feedback_cf_cache_verification)
"""

import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path

import paramiko
import requests

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = Path("/Users/chriswoods/Desktop/Chris-HQ/.env")

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

PAGES = [
    {
        "slug": "pricing",
        "title": "Pricing — $59 Flat Fee, Same-Day Care",
        "local": ROOT / "landing-pages/pricing/index.html",
        "remote": "html/pricing/index.html",
    },
    {
        "slug": "credentials",
        "title": "Credentials — Chris Woods, MSN, APRN, FNP-C",
        "local": ROOT / "landing-pages/credentials/index.html",
        "remote": "html/credentials/index.html",
    },
]

MU_PLUGIN_LOCAL = ROOT / "php/npcwoods-static-pages.php"
MU_PLUGIN_REMOTE = "html/wp-content/mu-plugins/npcwoods-static-pages.php"

LLMS_FILES = [
    (ROOT / "llms.txt", "html/llms.txt"),
    (ROOT / "llms-full.txt", "html/llms-full.txt"),
]

# --------------------------------------------------------------------------
# .env loader
# --------------------------------------------------------------------------

def load_env():
    env = {}
    if not ENV_PATH.exists():
        sys.exit(f"[err] .env not found at {ENV_PATH}")
    for raw in ENV_PATH.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    required = ["SFTP_HOST", "SFTP_USERNAME", "SFTP_PASSWORD", "WP_USERNAME", "WP_APP_PASSWORD"]
    missing = [k for k in required if not env.get(k)]
    if missing:
        sys.exit(f"[err] .env missing required keys: {', '.join(missing)}")
    env.setdefault("SFTP_PORT", "22")
    return env


# --------------------------------------------------------------------------
# Step 1: Update mu-plugin locally (idempotent)
# --------------------------------------------------------------------------

def update_mu_plugin():
    src = MU_PLUGIN_LOCAL.read_text()
    new_entries = [
        ('"pricing"', '"pricing/index.html"'),
        ('"credentials"', '"credentials/index.html"'),
    ]
    changed = False
    for key, val in new_entries:
        if key in src:
            print(f"[mu-plugin] {key} already present, skipping")
            continue
        # Insert before the closing `);` of the $page_map array
        line = f'        {key:<28} => {val},\n'
        src_new = re.sub(r"(\n\s*\);\s*\n\s*\$slug = get_post_field)", line + r"\1", src, count=1)
        if src_new == src:
            sys.exit(f"[err] could not locate $page_map closing in {MU_PLUGIN_LOCAL}")
        src = src_new
        changed = True
        print(f"[mu-plugin] added {key} => {val}")
    if changed:
        MU_PLUGIN_LOCAL.write_text(src)
    return changed


# --------------------------------------------------------------------------
# Step 2: SFTP uploads (paramiko with banner_timeout workaround)
# --------------------------------------------------------------------------

def sftp_upload_all(env):
    print(f"[sftp] connecting to {env['SFTP_HOST']}:{env['SFTP_PORT']}")
    transport = paramiko.Transport((env["SFTP_HOST"], int(env["SFTP_PORT"])))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(transport)

    def mkdir_safe(path):
        try:
            sftp.mkdir(path)
        except IOError:
            pass  # exists

    # Ensure dirs exist for the HTML pages
    for page in PAGES:
        mkdir_safe(f"html/{page['slug']}")

    # Upload HTML pages
    for page in PAGES:
        print(f"[sftp] uploading {page['local']} -> {page['remote']}")
        sftp.put(str(page["local"]), page["remote"])

    # Upload updated mu-plugin
    print(f"[sftp] uploading {MU_PLUGIN_LOCAL} -> {MU_PLUGIN_REMOTE}")
    sftp.put(str(MU_PLUGIN_LOCAL), MU_PLUGIN_REMOTE)

    # Upload llms files
    for local, remote in LLMS_FILES:
        print(f"[sftp] uploading {local} -> {remote}")
        sftp.put(str(local), remote)

    sftp.close()
    transport.close()
    print("[sftp] done")


# --------------------------------------------------------------------------
# Step 3: WP REST — create/update page stubs for sitemap inclusion
# --------------------------------------------------------------------------

WP_BASE = "https://npcwoods.com/wp-json/wp/v2"


def wp_auth(env):
    return (env["WP_USERNAME"], env["WP_APP_PASSWORD"])


def wp_ensure_page_stub(env, slug: str, title: str):
    auth = wp_auth(env)
    # Check if a page with this slug already exists
    r = requests.get(f"{WP_BASE}/pages", params={"slug": slug}, auth=auth, timeout=30)
    r.raise_for_status()
    existing = r.json()
    stub_payload = {
        "title": title,
        "slug": slug,
        "status": "publish",
        "content": f'<!-- Served via mu-plugin: html/{slug}/index.html -->',
        "excerpt": f"Canonical {slug} page at https://npcwoods.com/{slug}/",
    }
    if existing:
        page_id = existing[0]["id"]
        print(f"[wp] updating existing stub id={page_id} for /{slug}/")
        r2 = requests.post(f"{WP_BASE}/pages/{page_id}", json=stub_payload, auth=auth, timeout=30)
    else:
        print(f"[wp] creating new stub for /{slug}/")
        r2 = requests.post(f"{WP_BASE}/pages", json=stub_payload, auth=auth, timeout=30)
    r2.raise_for_status()
    data = r2.json()
    print(f"[wp] {slug} -> id={data['id']} status={data['status']} link={data['link']}")
    return data


# --------------------------------------------------------------------------
# Step 4: Verify (cache-bust curl)
# --------------------------------------------------------------------------

def verify(slug: str):
    url = f"https://npcwoods.com/{slug}/?v={int(time.time())}"
    r = requests.get(url, timeout=30, headers={"User-Agent": "NPCWoods-Deploy-Verify/1.0"})
    ok = r.status_code == 200 and "<title>" in r.text
    status = "OK" if ok else "FAIL"
    # Look for signature content we placed on the page
    signature = "1285125468" if slug == "credentials" else "$59. One price. One promise."
    sig_found = signature in r.text
    print(f"[verify] {status} {url} ({r.status_code}, {len(r.text):,} bytes) signature={'yes' if sig_found else 'NO'}")
    return ok and sig_found


def verify_llms():
    for suffix in ["llms.txt", "llms-full.txt"]:
        url = f"https://npcwoods.com/{suffix}?v={int(time.time())}"
        r = requests.get(url, timeout=30)
        has_pricing = "/pricing/" in r.text
        has_creds = "/credentials/" in r.text
        status = "OK" if r.status_code == 200 and has_pricing and has_creds else "FAIL"
        print(f"[verify] {status} {url} ({r.status_code}) pricing={'yes' if has_pricing else 'NO'} credentials={'yes' if has_creds else 'NO'}")


def print_schema_links():
    for page in PAGES:
        url = f"https://npcwoods.com/{page['slug']}/"
        encoded = urllib.parse.quote(url, safe="")
        validator = f"https://validator.schema.org/#url={encoded}"
        rich_results = f"https://search.google.com/test/rich-results?url={encoded}"
        print(f"  {page['slug']}: schema   -> {validator}")
        print(f"  {page['slug']}: rich    -> {rich_results}")


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    env = load_env()

    print("=== 1. Update mu-plugin locally ===")
    update_mu_plugin()

    print("\n=== 2. SFTP upload ===")
    sftp_upload_all(env)

    print("\n=== 3. Create/update WP page stubs (sitemap inclusion) ===")
    for page in PAGES:
        wp_ensure_page_stub(env, page["slug"], page["title"])

    print("\n=== 4. Verify live URLs ===")
    all_ok = True
    for page in PAGES:
        all_ok = verify(page["slug"]) and all_ok
    verify_llms()

    print("\n=== 5. Schema validator links ===")
    print_schema_links()

    if not all_ok:
        print("\n[WARN] Some pages did not verify cleanly. Investigate before trusting.")
        sys.exit(2)

    print("\n[done] /pricing/ and /credentials/ are LIVE. Yoast sitemap will update on next crawl/regen.")


if __name__ == "__main__":
    main()
