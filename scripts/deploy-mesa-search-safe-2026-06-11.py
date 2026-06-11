#!/usr/bin/env python3
"""Deploy the 2026-06-11 Mesa search-safe canonical-claim fix (single page).

The /uti-treatment/mesa-az/search-safe/ paid landing page gets one FAQ answer
aligned to Chris's canonical response-time wording before the Mesa UTI
campaign relaunch. Uploads the page and touches WP stub 13 (the mesa-az
parent) to flush the GoDaddy cache. Chris approved the Mesa relaunch on
2026-06-11.

Dry-run is the default; add --execute to deploy.
"""
import argparse
import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT.parent / ".env"

LOCAL = "landing-pages/uti-treatment/mesa-az/search-safe/index.html"
REMOTE = "html/uti-treatment/mesa-az/search-safe/index.html"
STUB_ID = 13  # /uti-treatment/mesa-az/ per flush-discovery-audit-2026-06-10.py
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

REQUIRED = [
    "GTM-59QSWZRC",
    "gtag/js?id=G-EFFRQMG8TC",
    "AW-610222919",
    "tracking.js",
    'content="noindex,follow"',
    "Most patients hear back the same day, usually within a few hours.",
]
FORBIDDEN = [
    "connect.facebook.net",
    "facebook.com/tr",
    'fbq("init"',
    "fbq('init'",
    "nitrofurantoin",
    "trimethoprim",
    "antibiotic",
    "insurance",
]


def load_env():
    env = {}
    for raw in ENV_PATH.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def wp_req(url, auth, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": f"Basic {auth}", "User-Agent": UA}
    if body is not None:
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, json.loads(resp.read() or "null")
    except urllib.error.HTTPError as e:
        return e.code, None


def touch_stub(auth):
    base = f"https://npcwoods.com/wp-json/wp/v2/pages/{STUB_ID}"
    st, cur = wp_req(f"{base}?_fields=id,content,title,status", auth)
    if st != 200 or not cur:
        return False
    payload = {
        "title": cur.get("title", {}).get("raw") or cur.get("title", {}).get("rendered", ""),
        "content": cur.get("content", {}).get("raw") or cur.get("content", {}).get("rendered", ""),
        "status": cur.get("status", "publish"),
    }
    st2, _ = wp_req(base, auth, method="POST", body=payload)
    return st2 == 200


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Deploy Mesa search-safe fix. Dry-run by default.")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args((argv or sys.argv)[1:])

    html = (ROOT / LOCAL).read_text()
    lower = html.lower()
    for marker in REQUIRED:
        if marker not in html:
            raise RuntimeError(f"{LOCAL} missing required marker: {marker}")
    for bad in FORBIDDEN:
        if bad.lower() in lower:
            raise RuntimeError(f"{LOCAL} contains forbidden marker: {bad}")
    print(f"[plan] {LOCAL} -> {REMOTE} (then touch WP stub {STUB_ID})")

    if not args.execute:
        print("[dry-run] nothing uploaded. Add --execute to deploy.")
        return 0

    env = load_env()
    import paramiko

    print(f"[sftp] connecting to {env['SFTP_HOST']}:{env['SFTP_PORT']}")
    transport = paramiko.Transport((env["SFTP_HOST"], int(env["SFTP_PORT"])))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(str(ROOT / LOCAL), REMOTE)
    sftp.close()
    transport.close()
    print(f"[up] {REMOTE}")

    auth = base64.b64encode(f"{env['WP_USERNAME']}:{env['WP_APP_PASSWORD']}".encode()).decode()
    ok = touch_stub(auth)
    print(f"[cache] WP stub {STUB_ID} touch: {'ok' if ok else 'FAILED — flush manually'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
