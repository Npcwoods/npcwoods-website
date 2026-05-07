#!/usr/bin/env python3
"""Deploy any index.html that has a .synced.bak or .footer-synced.bak (= touched today).

Idempotent. Run after sync-header-snippet.py / sync-footer-snippet.py to push the
batch update. Uses paramiko with banner_timeout=auth_timeout=60 (per
feedback_paramiko_godaddy_timeout, 30s is not always enough).
"""
import sys
from pathlib import Path

import paramiko

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = Path("/Users/chriswoods/Desktop/Chris-HQ/.env")
SCAN_DIRS = [ROOT / "html", ROOT / "landing-pages"]


def load_env():
    env = {}
    for raw in ENV_PATH.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def find_changed():
    """Pages that have a sync backup created today or recently — i.e., the sync touched them."""
    targets = []
    for root in SCAN_DIRS:
        for html in root.rglob("index.html"):
            sync_bak = html.with_suffix(html.suffix + ".synced.bak")
            footer_bak = html.with_suffix(html.suffix + ".footer-synced.bak")
            if sync_bak.exists() or footer_bak.exists():
                targets.append(html)
    return sorted(set(targets))


def remote_path_for(local: Path) -> str:
    """Map local path to server path under html/."""
    rel = local.relative_to(ROOT)
    parts = rel.parts
    # html/<section>/index.html  -> html/<section>/index.html
    # landing-pages/<section>/index.html -> html/<section>/index.html
    # landing-pages/<a>/<b>/index.html -> html/<a>/<b>/index.html
    if parts[0] == "html":
        return str(rel)
    if parts[0] == "landing-pages":
        return "html/" + "/".join(parts[1:])
    raise ValueError(f"Unexpected local path: {local}")


def main() -> int:
    env = load_env()
    targets = find_changed()
    if not targets:
        print("[noop] no changed pages found")
        return 0
    print(f"[deploy] {len(targets)} changed pages to upload")
    for t in targets[:5]:
        print(f"  - {t.relative_to(ROOT)}")
    if len(targets) > 5:
        print(f"  ... +{len(targets) - 5} more")

    print(f"\n[sftp] connecting to {env['SFTP_HOST']}:{env['SFTP_PORT']}")
    transport = paramiko.Transport((env["SFTP_HOST"], int(env["SFTP_PORT"])))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(transport)

    def mkdir_safe(path: str):
        try:
            sftp.mkdir(path)
        except IOError:
            pass

    uploaded = 0
    for local in targets:
        remote = remote_path_for(local)
        # Ensure parent dir exists
        parts = remote.split("/")
        for i in range(1, len(parts)):
            mkdir_safe("/".join(parts[:i]))
        try:
            sftp.put(str(local), remote)
            uploaded += 1
            print(f"[sftp] {local.relative_to(ROOT)} -> {remote}")
        except Exception as e:
            print(f"[err] {local.relative_to(ROOT)}: {e}")

    sftp.close()
    transport.close()
    print(f"\n[done] uploaded {uploaded}/{len(targets)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
