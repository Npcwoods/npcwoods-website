#!/usr/bin/env python3
"""Create or update the WordPress page stub for /trust-video/."""

from __future__ import annotations

import base64
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HQ_ROOT = ROOT.parent
ENV_PATH = HQ_ROOT / ".env"
SITE_URL = "https://npcwoods.com"
WP_BASE = f"{SITE_URL}/wp-json/wp/v2"
PAGE_SLUG = "trust-video"
PAGE_TITLE = "Is NPCWoods Real?"
PAGE_CONTENT = "<!-- Served by npcwoods-static-pages.php -->"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def load_env() -> dict[str, str]:
    if not ENV_PATH.exists():
        raise FileNotFoundError(f"missing env: {ENV_PATH}")
    env: dict[str, str] = {}
    for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def auth_header(env: dict[str, str]) -> str:
    user = env.get("WP_USERNAME")
    password = env.get("WP_APP_PASSWORD")
    if not user or not password:
        raise RuntimeError("missing WP_USERNAME or WP_APP_PASSWORD")
    token = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def wp_request(path: str, auth: str, method: str = "GET", payload: dict | None = None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        f"{WP_BASE}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": auth,
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            body = resp.read()
            return json.loads(body.decode("utf-8")) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"WordPress REST failed: HTTP {exc.code} {detail}") from exc


def find_page(auth: str) -> dict | None:
    query = urllib.parse.urlencode(
        {
            "slug": PAGE_SLUG,
            "context": "edit",
            "_fields": "id,slug,status,title,link,modified",
            "per_page": 20,
        }
    )
    pages = wp_request(f"/pages?{query}", auth)
    for page in pages:
        if page.get("slug") == PAGE_SLUG:
            return page
    return None


def upsert_page(auth: str) -> dict:
    current = find_page(auth)
    payload = {
        "title": PAGE_TITLE,
        "slug": PAGE_SLUG,
        "status": "publish",
        "content": PAGE_CONTENT,
        "comment_status": "closed",
        "ping_status": "closed",
    }
    if current:
        page_id = current["id"]
        updated = wp_request(
            f"/pages/{page_id}?_fields=id,slug,status,link,modified",
            auth,
            method="POST",
            payload=payload,
        )
        print(
            f"[wp-stub] updated id={updated.get('id')} "
            f"slug={updated.get('slug')} status={updated.get('status')}"
        )
        return updated

    created = wp_request(
        "/pages?_fields=id,slug,status,link,modified",
        auth,
        method="POST",
        payload=payload,
    )
    print(
        f"[wp-stub] created id={created.get('id')} "
        f"slug={created.get('slug')} status={created.get('status')}"
    )
    return created


def main() -> int:
    env = load_env()
    auth = auth_header(env)
    page = upsert_page(auth)
    print(f"[wp-stub] link={page.get('link')}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[fatal] {exc}", file=sys.stderr)
        raise SystemExit(1)
