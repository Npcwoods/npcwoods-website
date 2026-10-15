#!/usr/bin/env python3
"""Deploy the slim Vercel look plate via REST API. Kitchen preview only."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

AUTH = Path.home() / "Library/Application Support/com.vercel.cli/auth.json"
PREVIEW = Path(__file__).resolve().parent.parent / "content-output" / "previews" / "vercel-review-site"
TEAM = "team_HLMaWtnpkaMW8LfDp9GEOEa9"
PROJECT = "vercel-review-site"
WANTED = [
    "index.html",
    "vercel.json",
    "robots.txt",
    "tracking.js",
    "assets/css/site.css",
    "assets/js/site.js",
    "dental-pain/ames-ia/index.html",
    "dental-pain/iowa-city-ia/index.html",
    "dental-pain/dubuque-ia/index.html",
    "dental-pain/waterloo-ia/index.html",
]


def token() -> str:
    data = json.loads(AUTH.read_text())
    for key in ("token", "accessToken", "authToken"):
        if data.get(key):
            return str(data[key])
    raise SystemExit(f"no token key in auth.json; keys={list(data)}")


def files() -> list[dict]:
    out = []
    for rel in WANTED:
        path = PREVIEW / rel
        if not path.exists():
            raise SystemExit(f"missing {rel}")
        out.append({"file": rel, "data": path.read_text(encoding="utf-8")})
    return out


def main() -> None:
    payload = {
        "name": PROJECT,
        "project": PROJECT,
        "target": "staging",
        "files": files(),
        "projectSettings": {"framework": None},
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.vercel.com/v13/deployments?teamId={TEAM}",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token()}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        err = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code}: {err[:2000]}") from None
    url = result.get("url") or result.get("alias")
    ready = result.get("readyState") or result.get("status")
    print(f"readyState={ready}")
    print(f"url=https://{url}" if url and not str(url).startswith("http") else f"url={url}")
    print(f"id={result.get('id') or result.get('uid')}")


if __name__ == "__main__":
    main()
