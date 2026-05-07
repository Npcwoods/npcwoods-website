#!/usr/bin/env python3
"""
Yoast schema content fixes — 2026-04-30 (post-deploy followup)

Three fixes:
  1. WP site tagline currently contains "No Insurance" — direct violation of
     the zero-exceptions ban. Surfaces in Yoast WebSite.description JSON-LD
     on every blog post + archive.
  2. Blog index page (ID 413) title has em-dash. Surfaces in BreadcrumbList
     schema on every blog post.
  3. Yoast SEO title for post 326 is the old short variant "Paying Out of
     Pocket? Text an NP for $59 Flat" while the Article headline is the new
     full title. Update via meta keys.

Each fix is independent. Failures are reported but don't abort the rest.
"""
import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ENV_PATH = Path("/Users/chriswoods/Desktop/Chris-HQ/.env")
WP_BASE = "https://npcwoods.com/wp-json/wp/v2"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4 Safari/605.1.15"
)


def load_env():
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def wp(method, url, auth_b64, body=None):
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Basic {auth_b64}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode("utf-8") or "{}")
        except Exception:
            payload = {"raw_error": str(e)}
        return e.code, payload


def main():
    env = load_env()
    user = env.get("WP_USERNAME")
    pw = env.get("WP_APP_PASSWORD")
    if not (user and pw):
        sys.exit("missing WP_USERNAME / WP_APP_PASSWORD in .env")
    auth = base64.b64encode(f"{user}:{pw}".encode()).decode()

    failures = 0

    # ─────────────────────────────────────────────────────────────────────
    # Fix 1: Site tagline
    # ─────────────────────────────────────────────────────────────────────
    print("=== Fix 1: Site tagline (Settings → General → Tagline) ===")
    new_tagline = "$59 Flat-Fee Urgent Care by Text. No Paperwork, No Waiting Room."
    code, resp = wp("GET", f"{WP_BASE}/settings", auth)
    if code == 200:
        old = resp.get("description", "(unknown)")
        print(f"  current: {old!r}")
    else:
        print(f"  pre-fetch failed (HTTP {code}): {resp}")
    code, resp = wp("POST", f"{WP_BASE}/settings", auth, {"description": new_tagline})
    if 200 <= code < 300:
        print(f"  new:     {resp.get('description')!r}")
        print(f"  ✓ tagline updated (HTTP {code})")
    else:
        print(f"  ✗ FAILED (HTTP {code}): {resp}")
        failures += 1
    print()

    # ─────────────────────────────────────────────────────────────────────
    # Fix 2: Blog page (ID 413) title
    # ─────────────────────────────────────────────────────────────────────
    print("=== Fix 2: Blog index page title (ID 413) ===")
    new_blog_title = "Blog: Health Tips from a Nurse Practitioner"
    code, resp = wp("POST", f"{WP_BASE}/pages/413", auth, {"title": new_blog_title})
    if 200 <= code < 300:
        print(f"  ✓ title: {resp.get('title', {}).get('rendered')!r} (HTTP {code})")
    else:
        print(f"  ✗ FAILED (HTTP {code}): {resp}")
        failures += 1
    print()

    # ─────────────────────────────────────────────────────────────────────
    # Fix 3: Yoast SEO title + OG title for post 326
    # ─────────────────────────────────────────────────────────────────────
    print("=== Fix 3: Yoast SEO + OG title on post 326 ===")
    yoast_title = "Paying Out of Pocket? Text an NP for $59 Flat Fee"
    og_title = yoast_title
    payload = {
        "meta": {
            "_yoast_wpseo_title": yoast_title,
            "_yoast_wpseo_opengraph-title": og_title,
            "_yoast_wpseo_twitter-title": og_title,
        }
    }
    code, resp = wp("POST", f"{WP_BASE}/posts/326", auth, payload)
    if 200 <= code < 300:
        meta = resp.get("meta", {}) or {}
        sample = {k: v for k, v in meta.items() if k.startswith("_yoast")}
        if sample:
            print(f"  yoast meta after update (sample): {json.dumps(sample, indent=2)[:400]}")
        else:
            print("  (no _yoast_* keys exposed in response — Yoast may not have")
            print("   registered them for REST. Need WP admin UI fallback.)")
        # Verify by re-fetching yoast_head_json
        code2, resp2 = wp("GET", f"{WP_BASE}/posts/326?_fields=yoast_head_json", auth)
        if code2 == 200:
            yhj = resp2.get("yoast_head_json", {}) or {}
            print(f"  verified yoast title:    {yhj.get('title')!r}")
            print(f"  verified og:title:       {yhj.get('og_title')!r}")
            print(f"  verified twitter:title:  {yhj.get('twitter_title')!r}")
            if yhj.get("title") != yoast_title:
                print(f"  ⚠ Yoast title did NOT update via REST meta. Falls back to title field.")
                failures += 1
        else:
            print(f"  verify-fetch failed: HTTP {code2}")
    else:
        print(f"  ✗ FAILED (HTTP {code}): {resp}")
        failures += 1
    print()

    # ─────────────────────────────────────────────────────────────────────
    # Cache flush — re-publish post 326 + page 413 + homepage so Yoast
    # schema regenerates with new tagline + title
    # ─────────────────────────────────────────────────────────────────────
    print("=== Cache flush (re-publish to regenerate Yoast schema) ===")
    for label, kind, _id in [
        ("post 326 (blog post)", "posts", 326),
        ("page 413 (blog index)", "pages", 413),
        ("page 63 (homepage)", "pages", 63),
    ]:
        code, _ = wp("POST", f"{WP_BASE}/{kind}/{_id}", auth, {"status": "publish"})
        print(f"  {label}: HTTP {code}")

    print()
    print(f"=== Done. failures: {failures} ===")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
