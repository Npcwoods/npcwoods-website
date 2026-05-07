#!/usr/bin/env python3
"""Deploy the 2026-04-24 Ahrefs crawl-waste cleanup.

Uploads the changed static files/mu-plugins, touches affected WP page stubs to
flush GoDaddy cache, and updates exact /experience/ references in WP content.
"""
from __future__ import annotations

import base64
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import paramiko
except ImportError:
    print("paramiko is required for SFTP deploy", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
HQ_ROOT = ROOT.parent
ENV_PATH = HQ_ROOT / ".env"
SITE = "https://npcwoods.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

UPLOADS = {
    "landing-pages/arizona-telemedicine/index.html": "html/arizona-telemedicine/index.html",
    "landing-pages/sinus-infection-treatment/index.html": "html/sinus-infection-treatment/index.html",
    "landing-pages/medications/augmentin/index.html": "html/medications/augmentin/index.html",
    "landing-pages/medications/clindamycin/index.html": "html/medications/clindamycin/index.html",
    "landing-pages/medications/prednisone/index.html": "html/medications/prednisone/index.html",
    "landing-pages/learn/sinus-infection/index.html": "html/learn/sinus-infection/index.html",
    "llms.txt": "html/llms.txt",
    "llms-full.txt": "html/llms-full.txt",
    "php/npcwoods-redirects.php": "html/wp-content/mu-plugins/npcwoods-redirects.php",
    "php/npcwoods-redirects-404-cleanup.php": (
        "html/wp-content/mu-plugins/npcwoods-redirects-404-cleanup.php"
    ),
}

TOUCH_PAGE_IDS = {
    "/": 63,
    "/arizona-telemedicine/": 355,
    "/sinus-infection-treatment/": 7,
    "/medications/augmentin/": 384,
    "/medications/clindamycin/": 389,
    "/medications/prednisone/": 397,
    "/learn/sinus-infection/": 371,
}

EXPERIENCE_REPLACEMENTS = {
    "https://npcwoods.com/experience/": "https://npcwoods.com/patient-experience/",
    "/experience/": "/patient-experience/",
}


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def mkdir_p(sftp, remote_dir: str) -> None:
    cur = ""
    for part in remote_dir.split("/"):
        cur = f"{cur}/{part}" if cur else part
        try:
            sftp.stat(cur)
        except IOError:
            try:
                sftp.mkdir(cur)
            except IOError:
                pass


def upload_files(env: dict[str, str]) -> None:
    transport = paramiko.Transport((env["SFTP_HOST"], int(env.get("SFTP_PORT", "22"))))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        for rel, remote in UPLOADS.items():
            local = ROOT / rel
            if not local.exists():
                raise FileNotFoundError(local)
            mkdir_p(sftp, "/".join(remote.split("/")[:-1]))
            sftp.put(str(local), remote)
            print(f"[sftp] {rel} -> {remote}")
    finally:
        sftp.close()
        transport.close()


def auth_header(env: dict[str, str]) -> str:
    token = base64.b64encode(f'{env["WP_USERNAME"]}:{env["WP_APP_PASSWORD"]}'.encode()).decode()
    return f"Basic {token}"


def wp_request(path: str, auth: str, method: str = "GET", payload: dict | None = None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        f"{SITE}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": auth,
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read()
        return json.loads(body.decode()) if body else {}


def touch_pages(auth: str) -> None:
    for url_path, page_id in TOUCH_PAGE_IDS.items():
        current = wp_request(
            f"/wp-json/wp/v2/pages/{page_id}?context=edit&_fields=id,title,content,status",
            auth,
        )
        payload = {
            "title": current.get("title", {}).get("raw")
            or current.get("title", {}).get("rendered", ""),
            "content": current.get("content", {}).get("raw")
            or current.get("content", {}).get("rendered", ""),
            "status": current.get("status", "publish"),
        }
        wp_request(f"/wp-json/wp/v2/pages/{page_id}", auth, method="POST", payload=payload)
        print(f"[wp-touch] {url_path} id={page_id}")
        time.sleep(0.4)


def replace_experience_links(text: str) -> tuple[str, int]:
    count = 0
    for old, new in EXPERIENCE_REPLACEMENTS.items():
        hits = text.count(old)
        if hits:
            text = text.replace(old, new)
            count += hits
    return text, count


def endpoint_items(endpoint: str, auth: str) -> list[dict]:
    items: list[dict] = []
    for page in range(1, 6):
        query = urllib.parse.urlencode(
            {
                "context": "edit",
                "search": "experience",
                "per_page": 100,
                "page": page,
                "_fields": "id,slug,status,title,content",
            }
        )
        try:
            batch = wp_request(f"/wp-json/wp/v2/{endpoint}?{query}", auth)
        except Exception as exc:
            if page == 1:
                print(f"[wp-scan-skip] {endpoint}: {exc}")
            break
        if not isinstance(batch, list) or not batch:
            break
        items.extend(batch)
        if len(batch) < 100:
            break
    return items


def update_wp_experience_links(auth: str) -> None:
    backup: list[dict] = []
    updated = 0
    endpoints = ["posts", "pages", "navigation", "wp_navigation"]
    seen: set[tuple[str, int]] = set()
    for endpoint in endpoints:
        for item in endpoint_items(endpoint, auth):
            item_id = int(item["id"])
            key = (endpoint, item_id)
            if key in seen:
                continue
            seen.add(key)
            raw = item.get("content", {}).get("raw")
            if not raw:
                continue
            new_raw, hits = replace_experience_links(raw)
            if not hits:
                continue
            backup.append({"endpoint": endpoint, "item": item})
            wp_request(
                f"/wp-json/wp/v2/{endpoint}/{item_id}",
                auth,
                method="POST",
                payload={"content": new_raw, "status": item.get("status", "publish")},
            )
            title = item.get("title", {}).get("raw") or item.get("slug", "")
            print(f"[wp-link-fix] {endpoint}/{item_id} hits={hits} title={title}")
            updated += 1
            time.sleep(0.4)

    if backup:
        backup_dir = ROOT / "backups"
        backup_dir.mkdir(exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        backup_path = backup_dir / f"wp-experience-link-cleanup-{stamp}.json"
        backup_path.write_text(json.dumps(backup, indent=2), encoding="utf-8")
        print(f"[backup] {backup_path.relative_to(ROOT)}")
    print(f"[wp-link-fix] updated_items={updated}")


def main() -> int:
    env = load_env()
    auth = auth_header(env)
    upload_files(env)
    touch_pages(auth)
    update_wp_experience_links(auth)
    print("[done] deployment upload/cache-touch phase complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
