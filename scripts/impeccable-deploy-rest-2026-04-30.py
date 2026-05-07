#!/usr/bin/env python3
"""
Impeccable deploy — WP REST API leg

1. Update blog post 326 (title + content) — clears em-dashes from title and
   pushes the full new HTML body produced by the clarify pass.
2. Trigger cache flush on pages 63 (homepage), 13 (mesa-az UTI),
   355 (arizona-telemedicine) by re-publishing each (per memory
   reference_godaddy_cache_purge.md).

Reads creds from /Users/chriswoods/Desktop/Chris-HQ/.env. WordPress REST
auth is application-password basic auth.
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = Path("/Users/chriswoods/Desktop/Chris-HQ/.env")
WP_BASE = "https://npcwoods.com/wp-json/wp/v2"
BLOG_FILE = ROOT / "blog" / "no-insurance-no-problem.html"


def load_env():
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def wp_request(method: str, url: str, auth_b64: str, body: dict | None = None):
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Basic {auth_b64}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8") or "{}")


def main():
    import base64

    env = load_env()
    user = env.get("WP_USERNAME")
    pw = env.get("WP_APP_PASSWORD")
    if not (user and pw):
        sys.exit("missing WP_USERNAME / WP_APP_PASSWORD in .env")
    auth = base64.b64encode(f"{user}:{pw}".encode()).decode()

    print("=== 1. Update blog post 326 ===")
    if not BLOG_FILE.exists():
        sys.exit(f"missing blog file: {BLOG_FILE}")
    body_html = BLOG_FILE.read_text(encoding="utf-8")
    new_title = "Paying Out of Pocket? Text a Nurse Practitioner for $59 Flat Fee, No Catches"
    blog_payload = {
        "title": new_title,
        "content": body_html,
        "comment_status": "closed",
        "ping_status": "closed",
    }
    code, resp = wp_request("POST", f"{WP_BASE}/posts/326", auth, blog_payload)
    print(f"  HTTP {code}")
    if 200 <= code < 300:
        print(f"  title:  {resp.get('title', {}).get('rendered', '?')}")
        print(f"  status: {resp.get('status')}")
        print(f"  modified: {resp.get('modified')}")
    else:
        print(f"  error: {resp}")
        return 1

    print()
    print("=== 2. Flush cache on static page stubs ===")
    for label, page_id in [("homepage", 63), ("mesa-uti-treatment", 13), ("arizona-telemedicine", 355)]:
        # Re-publish via no-op status update — triggers post_updated hook,
        # GoDaddy's cache layer purges, Cloudflare follows.
        code, resp = wp_request("POST", f"{WP_BASE}/pages/{page_id}", auth, {"status": "publish"})
        modified = resp.get("modified", "?")
        slug = resp.get("slug", "?")
        print(f"  page {page_id} ({label} slug={slug}) → HTTP {code}, modified={modified}")
        if not (200 <= code < 300):
            print(f"    error: {resp}")

    print()
    print("=== Done ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
