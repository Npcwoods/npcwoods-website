#!/usr/bin/env python3
"""Purge Cloudflare cache for npcwoods.com.

Reads CLOUDFLARE_API_TOKEN and CLOUDFLARE_ZONE_ID from .env.

Usage:
    python3 scripts/cf-purge.py              # purge everything
    python3 scripts/cf-purge.py URL1 URL2    # purge specific URLs

Token needs Zone.Cache Purge permission (scoped to npcwoods.com).
"""

from pathlib import Path
import json
import sys
import urllib.request
import urllib.error

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def load_env():
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def cf_post(token: str, zone: str, path: str, body: dict):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone}/{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


def resolve_zone(token: str, zone_name: str):
    url = f"https://api.cloudflare.com/client/v4/zones?name={zone_name}"
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    if data.get("success") and data.get("result"):
        return data["result"][0]["id"]
    return None


def main():
    env = load_env()
    token = env.get("CLOUDFLARE_API_TOKEN")
    zone = env.get("CLOUDFLARE_ZONE_ID")
    if not token:
        print("[fatal] CLOUDFLARE_API_TOKEN not set in .env", file=sys.stderr)
        return 2
    if not zone:
        print("[info] CLOUDFLARE_ZONE_ID not set — looking it up")
        zone = resolve_zone(token, "npcwoods.com")
        if not zone:
            print("[fatal] could not resolve zone id for npcwoods.com", file=sys.stderr)
            return 2
        print(f"[info] zone id: {zone} (add to .env as CLOUDFLARE_ZONE_ID to skip lookup)")

    args = sys.argv[1:]
    if args:
        body = {"files": args}
        label = f"{len(args)} URL(s)"
    else:
        body = {"purge_everything": True}
        label = "EVERYTHING"

    print(f"[purge] {label}")
    result = cf_post(token, zone, "purge_cache", body)
    if result.get("success"):
        print("[ok] purged")
        return 0
    else:
        print("[fail]", json.dumps(result.get("errors"), indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
