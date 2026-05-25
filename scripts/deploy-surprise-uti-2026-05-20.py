#!/usr/bin/env python3
"""Deploy the Surprise, AZ UTI landing page refresh.

Scoped to:
  - landing-pages/uti-treatment/surprise-az/index.html
  - remote html/uti-treatment/surprise-az/index.html
  - existing WP page stub with slug surprise-az

The deploy backs up the current remote file, uploads the local HTML, touches
the WP page stub to refresh GoDaddy cache, optionally purges Cloudflare, and
verifies live marker content with a cache-busted fetch.
"""

from __future__ import annotations

import base64
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import paramiko
except ImportError:
    print("[fatal] paramiko is required for SFTP deploy", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parent.parent
HQ_ROOT = ROOT.parent
ENV_PATH = HQ_ROOT / ".env"
LOCAL_HTML = ROOT / "landing-pages" / "uti-treatment" / "surprise-az" / "index.html"
REMOTE_HTML = "html/uti-treatment/surprise-az/index.html"
BACKUP_DIR = (
    HQ_ROOT
    / "content-output"
    / "reports"
    / "surprise-uti-review"
    / "live-backups"
)
SITE_URL = "https://npcwoods.com"
PAGE_PATH = "/uti-treatment/surprise-az/"
PAGE_SLUG = "surprise-az"
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


def require_keys(env: dict[str, str], keys: list[str]) -> None:
    missing = [key for key in keys if not env.get(key)]
    if missing:
        raise RuntimeError(f"missing required env keys: {', '.join(missing)}")


def mkdir_p(sftp: paramiko.SFTPClient, remote_dir: str) -> None:
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


def sftp_backup_and_upload(env: dict[str, str]) -> Path:
    require_keys(env, ["SFTP_HOST", "SFTP_USERNAME", "SFTP_PASSWORD"])
    port = int(env.get("SFTP_PORT") or 22)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = BACKUP_DIR / f"surprise-az-uti-live-before-{timestamp}.html"
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    transport = paramiko.Transport((env["SFTP_HOST"], port))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    try:
        transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            mkdir_p(sftp, "/".join(REMOTE_HTML.split("/")[:-1]))
            sftp.get(REMOTE_HTML, str(backup_path))
            print(f"[backup] {REMOTE_HTML} -> {backup_path.relative_to(HQ_ROOT)}")
            sftp.put(str(LOCAL_HTML), REMOTE_HTML)
            print(f"[sftp] {LOCAL_HTML.relative_to(ROOT)} -> {REMOTE_HTML}")
        finally:
            sftp.close()
    finally:
        transport.close()
    return backup_path


def wp_auth_header(env: dict[str, str]) -> str:
    require_keys(env, ["WP_USERNAME", "WP_APP_PASSWORD"])
    token = base64.b64encode(f'{env["WP_USERNAME"]}:{env["WP_APP_PASSWORD"]}'.encode()).decode()
    return f"Basic {token}"


def wp_request(path: str, auth: str, method: str = "GET", payload: dict | None = None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        f"{SITE_URL}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": auth,
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        body = resp.read()
        return json.loads(body.decode("utf-8")) if body else {}


def find_page_stub(auth: str) -> dict:
    query = urllib.parse.urlencode(
        {
            "slug": PAGE_SLUG,
            "context": "edit",
            "_fields": "id,slug,status,title,content,parent,modified,link",
            "per_page": 20,
        }
    )
    results = wp_request(f"/wp-json/wp/v2/pages?{query}", auth)
    candidates = [page for page in results if page.get("slug") == PAGE_SLUG]
    if not candidates:
        raise RuntimeError(f"no WP page stub found for slug {PAGE_SLUG}")

    page = candidates[0]
    if len(candidates) > 1:
        nested = [item for item in candidates if PAGE_PATH.strip("/") in item.get("link", "")]
        if nested:
            page = nested[0]

    print(
        "[wp-stub] "
        f"id={page.get('id')} slug={page.get('slug')} "
        f"parent={page.get('parent')} link={page.get('link')}"
    )
    return page


def touch_wp_stub(auth: str) -> dict:
    current = find_page_stub(auth)
    page_id = current["id"]
    payload = {
        "title": current.get("title", {}).get("raw") or current.get("title", {}).get("rendered", ""),
        "content": current.get("content", {}).get("raw") or current.get("content", {}).get("rendered", ""),
        "status": current.get("status", "publish"),
    }
    updated = wp_request(
        f"/wp-json/wp/v2/pages/{page_id}?_fields=id,slug,status,modified",
        auth,
        method="POST",
        payload=payload,
    )
    print(f"[wp-touch] {PAGE_PATH} id={updated.get('id')} modified={updated.get('modified')}")
    return updated


def purge_cloudflare(env: dict[str, str]) -> bool:
    token = env.get("CLOUDFLARE_API_TOKEN")
    zone = env.get("CLOUDFLARE_ZONE_ID")
    if not token or not zone:
        print("[warn] Cloudflare token/zone missing; WP stub touch still ran")
        return False

    body = {"files": [f"{SITE_URL}{PAGE_PATH}", f"{SITE_URL}{PAGE_PATH.rstrip('/')}"]}
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/zones/{zone}/purge_cache",
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Cloudflare purge failed: HTTP {exc.code} {detail}") from exc

    if not result.get("success"):
        raise RuntimeError(f"Cloudflare purge failed: {result.get('errors')}")
    print("[cloudflare] purged Surprise UTI page URL")
    return True


def fetch_live(cache_bust: bool) -> str:
    suffix = f"?npcwoods_cache_bust={int(time.time())}" if cache_bust else ""
    req = urllib.request.Request(
        f"{SITE_URL}{PAGE_PATH}{suffix}",
        headers={"User-Agent": UA, "Cache-Control": "no-cache"},
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        html = resp.read().decode("utf-8", errors="replace")
        print(f"[fetch] {PAGE_PATH}{suffix} status={resp.status} bytes={len(html)}")
        return html


def verify_live() -> None:
    expected = LOCAL_HTML.read_text(encoding="utf-8")
    expected_hash = hashlib.sha256(expected.encode("utf-8")).hexdigest()
    live = fetch_live(cache_bust=True)
    plain_live = fetch_live(cache_bust=False)
    required = [
        "<title>UTI Treatment in Surprise, AZ | $59</title>",
        "UTI symptoms in Surprise? Start a $59 text visit.",
        "If appropriate, treatment can be sent to a Surprise-area pharmacy.",
        "NPCWoods &middot; UTI Visit &middot; Surprise AZ",
        "No app download, no video call, no hidden fees.",
        '<script src="/tracking.js"></script>',
        "GTM-59QSWZRC",
        "G-EFFRQMG8TC",
        "AW-610222919",
        'fbq("init", "1558261907814968")',
    ]
    forbidden = [
        "Got a UTI in Surprise? Here's the whole deal.",
        "UTI antibiotics sent same day",
        "nitrofurantoin",
        "trimethoprim",
        "affordable-telemedicine-arizona-no-insurance",
    ]
    for html, label in [(live, "cache-busted"), (plain_live, "plain")]:
        for needle in required:
            if needle not in html:
                raise RuntimeError(f"{label} live HTML missing required marker: {needle}")
        for needle in forbidden:
            if needle.lower() in html.lower():
                raise RuntimeError(f"{label} live HTML still contains old/restricted marker: {needle}")

    live_hash = hashlib.sha256(live.encode("utf-8")).hexdigest()
    plain_hash = hashlib.sha256(plain_live.encode("utf-8")).hexdigest()
    print(f"[verify] local_sha256={expected_hash}")
    print(f"[verify] cache_busted_sha256={live_hash}")
    print(f"[verify] plain_sha256={plain_hash}")
    if live_hash != expected_hash:
        print("[warn] cache-busted live HTML is not byte-identical to local; marker checks passed")
    if plain_hash != expected_hash:
        print("[warn] plain live HTML is not byte-identical to local; marker checks passed")


def main() -> int:
    if not LOCAL_HTML.exists():
        raise FileNotFoundError(LOCAL_HTML)
    env = load_env()
    sftp_backup_and_upload(env)
    auth = wp_auth_header(env)
    touch_wp_stub(auth)
    purge_cloudflare(env)
    verify_live()
    print("[done] Surprise UTI page deployed and verified")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[fatal] {exc}", file=sys.stderr)
        raise
