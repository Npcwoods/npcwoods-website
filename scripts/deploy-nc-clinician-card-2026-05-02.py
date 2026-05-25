#!/usr/bin/env python3
"""One-shot deploy: NC telemedicine page (Variant C receipt hero + new clinician card).

Why a one-shot script: deploy-changed-pages.py only picks up files with .synced.bak
or .footer-synced.bak (sync triggers). NC was edited directly, so it needs a
targeted upload. Idempotent: rerunning re-uploads the same file.
"""
import sys
from pathlib import Path

import paramiko

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT.parent / ".env"
LOCAL = ROOT / "landing-pages" / "north-carolina-telemedicine" / "index.html"
REMOTE = "html/north-carolina-telemedicine/index.html"


def load_env():
    env = {}
    for raw in ENV_PATH.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def main() -> int:
    if not LOCAL.exists():
        print(f"[err] local file missing: {LOCAL}")
        return 1

    env = load_env()
    print(f"[deploy] {LOCAL.relative_to(ROOT)}")
    print(f"[sftp] connecting to {env['SFTP_HOST']}:{env['SFTP_PORT']}")

    transport = paramiko.Transport((env["SFTP_HOST"], int(env["SFTP_PORT"])))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Ensure parent dirs exist
    parts = REMOTE.split("/")
    for i in range(1, len(parts)):
        try:
            sftp.mkdir("/".join(parts[:i]))
        except IOError:
            pass

    sftp.put(str(LOCAL), REMOTE)
    print(f"[sftp] uploaded -> {REMOTE}")

    sftp.close()
    transport.close()
    print("[done]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
