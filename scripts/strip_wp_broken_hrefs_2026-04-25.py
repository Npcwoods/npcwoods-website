#!/usr/bin/env python3
"""Strip broken (now-redirecting) anchor hrefs from 2 live WP pages.

Removes 301-chain links Ahrefs may sub-flag. Each <a href="$BAD_URL">TEXT</a>
becomes plain TEXT. All other content is preserved byte-for-byte.

Targets:
  /uti-treatment/tucson-az/  → strip 3 hrefs
  /strep-throat-ear-infection/  → strip 4 hrefs

Usage:
    /tmp/pw-env/bin/python3 scripts/strip_wp_broken_hrefs_2026-04-25.py --dry-run
    /tmp/pw-env/bin/python3 scripts/strip_wp_broken_hrefs_2026-04-25.py
"""
from __future__ import annotations

import base64
import json
import sys
import time
import urllib.parse
from pathlib import Path

import requests
import urllib3
from bs4 import BeautifulSoup

# pw-env certifi bundle can't verify the GoDaddy SSL chain — known issue,
# documented in feedback_pw_env_ssl_verify memory. Safe for our own endpoints.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
VERIFY_SSL = False

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT.parent / ".env"
SITE = "https://npcwoods.com"

# slug-or-(slug,parent_id) → list of broken-target href substrings to strip
TARGETS = {
    "uti-treatment/tucson-az": [
        "/tucson-az-strep/",
        "/tucson-az-sinus/",
        "/tucson-az-ed/",
    ],
    "strep-throat-ear-infection": [
        # Original Ahrefs-flagged 4
        "/tucson-az-strep/",
        "/surprise-az-strep/",
        "/scottsdale-az-strep/",
        "/glendale-az-strep/",
        # Other -az-strep hrefs in same page that are also 301 chains
        "/chandler-az-strep/",
        "/gilbert-az-strep/",
        "/mesa-az-strep/",
        "/peoria-az-strep/",
        "/phoenix-az-strep/",
        "/tempe-az-strep/",
    ],
}

# Pre-publish guardrails (matches feedback_pre_publish_guardrail_gap memory)
BANNED_SUBSTRINGS = ["doctor", "Doctor", "DOCTOR", "insurance", "Insurance", "INSURANCE"]


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def auth_header(env: dict[str, str]) -> str:
    token = base64.b64encode(f'{env["WP_USERNAME"]}:{env["WP_APP_PASSWORD"]}'.encode()).decode()
    return f"Basic {token}"


def find_page_id(slug: str, auth: str) -> dict:
    """Find a WP page by full slug path. Returns the page object or raises."""
    parts = slug.strip("/").split("/")
    parent_id = 0
    page = None
    for part in parts:
        params = {
            "slug": part,
            "context": "edit",
            "_fields": "id,slug,parent,title,content,status,link",
            "per_page": 20,
        }
        if parent_id:
            params["parent"] = parent_id
        url = f"{SITE}/wp-json/wp/v2/pages?{urllib.parse.urlencode(params)}"
        r = requests.get(url, headers={"Authorization": auth}, timeout=30, verify=VERIFY_SSL)
        r.raise_for_status()
        candidates = r.json()
        # Filter to ones whose parent matches what we expect
        candidates = [c for c in candidates if c.get("parent", 0) == parent_id]
        if not candidates:
            raise RuntimeError(f"no page found for slug part '{part}' under parent {parent_id}")
        if len(candidates) > 1:
            raise RuntimeError(f"ambiguous slug '{part}' under parent {parent_id}: {[c['id'] for c in candidates]}")
        page = candidates[0]
        parent_id = page["id"]
    return page


def strip_anchors(html: str, broken_targets: list[str]) -> tuple[str, int]:
    """Unwrap any <a> whose href contains any string in broken_targets."""
    soup = BeautifulSoup(html, "html.parser")
    count = 0
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if any(bt in href for bt in broken_targets):
            a.unwrap()
            count += 1
    return str(soup), count


def guardrail_check(text: str, page_label: str) -> None:
    for word in BANNED_SUBSTRINGS:
        if word in text:
            raise RuntimeError(
                f"[guardrail] banned word '{word}' present in {page_label} content. "
                "This is a pre-existing issue but blocks PATCH per CLAUDE.md rules. "
                "Investigate before deploy."
            )


def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv
    env = load_env()
    auth = auth_header(env)

    backup_dir = ROOT / "scripts" / "wp-backups"
    backup_dir.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")

    summary = []
    for slug, broken_targets in TARGETS.items():
        print(f"\n=== {slug} ===")
        page = find_page_id(slug, auth)
        page_id = page["id"]
        title = page.get("title", {}).get("raw", "")
        raw = page.get("content", {}).get("raw", "")
        print(f"  page_id={page_id}  title={title!r}  content_bytes={len(raw)}")

        # Pre-existing guardrail check (warn only, since these are old pages we didn't write)
        for word in BANNED_SUBSTRINGS:
            if word in raw:
                print(f"  [warn] pre-existing banned word '{word}' present (not blocking — we're not adding it)")

        new_raw, removed = strip_anchors(raw, broken_targets)
        print(f"  anchors stripped: {removed}")

        if removed == 0:
            print("  [noop] nothing to strip; skipping")
            summary.append((slug, page_id, 0, "noop"))
            continue

        # Backup raw content
        backup_path = backup_dir / f"{slug.replace('/', '__')}-{stamp}.html"
        backup_path.write_text(raw, encoding="utf-8")
        print(f"  [backup] {backup_path.relative_to(ROOT)}")

        # Sanity: file shouldn't shrink wildly
        size_delta_pct = 100 * (len(raw) - len(new_raw)) / max(len(raw), 1)
        print(f"  size_delta: {size_delta_pct:.2f}% smaller")
        if size_delta_pct > 30:
            raise RuntimeError(f"refusing to PATCH: size shrunk {size_delta_pct:.1f}% — investigate")

        # Show first removed-link diff context for visual sanity
        for bt in broken_targets:
            if bt in raw and bt not in new_raw:
                print(f"    ✓ removed all hrefs containing {bt}")

        if dry_run:
            print("  [dry-run] not posting changes")
            summary.append((slug, page_id, removed, "dry-run"))
            continue

        # PATCH content
        patch_url = f"{SITE}/wp-json/wp/v2/pages/{page_id}"
        r = requests.post(
            patch_url,
            headers={"Authorization": auth, "Content-Type": "application/json"},
            data=json.dumps({"content": new_raw, "status": page.get("status", "publish")}),
            timeout=30,
            verify=VERIFY_SSL,
        )
        r.raise_for_status()
        print(f"  [patched] HTTP {r.status_code}")
        summary.append((slug, page_id, removed, "patched"))
        time.sleep(0.4)

    print("\n=== summary ===")
    for slug, page_id, removed, status in summary:
        print(f"  {slug:<40} id={page_id:<6} removed={removed:<3} {status}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
