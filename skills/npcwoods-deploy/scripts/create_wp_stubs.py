#!/usr/bin/env python3
"""
NPCWoods WordPress Page Stub Creator
======================================
Creates WordPress pages via REST API so that mu-plugin routing works.
Without these stubs, GoDaddy returns 404 before PHP even runs.

Usage (via osascript):
    Write this script to /tmp/ with credentials and pages filled in, then execute.

Configuration:
    Fill in WP credentials from: /Users/chriswoods/Desktop/Chris-HQ/ChrisOS/.env
    Define your pages in the PAGES list below.
"""

import urllib.request
import urllib.error
import json
import base64
import sys

# ============================================================
# CONFIG — Fill these in from the .env file
# ============================================================
WP_URL = 'https://npcwoods.com/wp-json/wp/v2/pages'
WP_USERNAME = ''       # e.g., 951673pwpadmin
WP_APP_PASSWORD = ''   # e.g., 2KxP t2hI VIAJ bV2y NADh O9Tg

# ============================================================
# PAGES TO CREATE
# Format: list of dicts with 'title', 'slug', and optional 'parent_slug'
#
# Parent pages are created first. If a page has 'parent_slug',
# it will be created as a child of the page with that slug.
#
# Example:
# PARENT_PAGES = [
#     {'title': 'After Your Visit', 'slug': 'learn'},
#     {'title': 'Medications Guide', 'slug': 'medications'},
# ]
# CHILD_PAGES = [
#     {'title': 'Strep Throat', 'slug': 'strep-throat', 'parent_slug': 'learn'},
#     {'title': 'Amoxicillin', 'slug': 'amoxicillin', 'parent_slug': 'medications'},
# ]
# ============================================================
PARENT_PAGES = []
CHILD_PAGES = []


def get_headers():
    auth_string = base64.b64encode(
        (WP_USERNAME + ':' + WP_APP_PASSWORD).encode()
    ).decode()
    return {
        'Authorization': 'Basic ' + auth_string,
        'Content-Type': 'application/json',
        # CRITICAL: GoDaddy/Cloudflare blocks Python's default user agent (error 1010)
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }


def create_page(title, slug, parent_id=0):
    """Create a WordPress page and return its ID."""
    headers = get_headers()
    data = json.dumps({
        'title': title,
        'slug': slug,
        'status': 'publish',
        'content': '<!-- Served by mu-plugin -->',
        'parent': parent_id
    }).encode()

    req = urllib.request.Request(WP_URL, data=data, headers=headers, method='POST')
    try:
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read().decode())
        page_id = result['id']
        print(f'  Created: /{slug}/ (ID: {page_id})')
        return page_id
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if 'term_exists' in body or 'already exists' in body:
            print(f'  Exists: /{slug}/ (skipped)')
            # Try to find existing page ID
            try:
                search_url = f'{WP_URL}?slug={slug}&per_page=5'
                search_req = urllib.request.Request(search_url, headers=headers)
                search_resp = urllib.request.urlopen(search_req)
                pages = json.loads(search_resp.read().decode())
                if pages:
                    return pages[0]['id']
            except:
                pass
            return 0
        else:
            print(f'  ERROR /{slug}/: HTTP {e.code} — {body[:200]}')
            return 0


def main():
    if not WP_USERNAME or not WP_APP_PASSWORD:
        print('ERROR: Fill in WordPress credentials before running!')
        sys.exit(1)

    if not PARENT_PAGES and not CHILD_PAGES:
        print('ERROR: No pages defined!')
        sys.exit(1)

    # Track parent page IDs by slug
    parent_ids = {}

    # Create parent pages
    if PARENT_PAGES:
        print('Creating parent pages...')
        for page in PARENT_PAGES:
            page_id = create_page(page['title'], page['slug'])
            parent_ids[page['slug']] = page_id
        print()

    # Create child pages
    if CHILD_PAGES:
        print('Creating child pages...')
        for page in CHILD_PAGES:
            parent_slug = page.get('parent_slug', '')
            parent_id = parent_ids.get(parent_slug, 0)
            create_page(page['title'], page['slug'], parent_id)
        print()

    total = len(PARENT_PAGES) + len(CHILD_PAGES)
    print(f'Done! {total} page stubs processed.')


if __name__ == '__main__':
    main()
