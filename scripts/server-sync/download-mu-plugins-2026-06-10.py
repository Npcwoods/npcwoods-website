#!/usr/bin/env python3
"""READ-ONLY snapshot of production mu-plugins (2026-06-10).

Downloads every file in html/wp-content/mu-plugins/ to
scripts/server-sync/mu-plugins-2026-06-10/, plus
html/llmseo/blog-burning-when-you-pee-albuquerque.html if present.
No uploads, no writes to the server.
"""

import os
import stat
import sys
from pathlib import Path

import paramiko

ROOT = Path(__file__).resolve().parent.parent.parent  # npcwoods-website/
ENV_PATH = ROOT.parent / ".env"
OUT_DIR = Path(__file__).resolve().parent / "mu-plugins-2026-06-10"
EXTRA_REMOTE = "html/llmseo/blog-burning-when-you-pee-albuquerque.html"
EXTRA_LOCAL = Path(__file__).resolve().parent / "blog-burning-when-you-pee-albuquerque.html"
MU_REMOTE = "html/wp-content/mu-plugins"


def load_env():
    env = {}
    for raw in ENV_PATH.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("SFTP_HOST", "SFTP_USERNAME", "SFTP_PASSWORD"):
        if not env.get(k):
            sys.exit(f"[err] .env missing {k}")
    env.setdefault("SFTP_PORT", "22")
    return env


def main():
    env = load_env()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[sftp] connecting to {env['SFTP_HOST']}:{env['SFTP_PORT']}")
    transport = paramiko.Transport((env["SFTP_HOST"], int(env["SFTP_PORT"])))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(transport)

    entries = sftp.listdir_attr(MU_REMOTE)
    print(f"[sftp] {len(entries)} entries in {MU_REMOTE}")
    for e in sorted(entries, key=lambda x: x.filename):
        kind = "dir " if stat.S_ISDIR(e.st_mode) else "file"
        print(f"  {kind}  {e.st_size:>9}  {e.filename}")

    downloaded = 0
    for e in entries:
        if stat.S_ISDIR(e.st_mode):
            continue
        remote = f"{MU_REMOTE}/{e.filename}"
        local = OUT_DIR / e.filename
        sftp.get(remote, str(local))
        downloaded += 1
    print(f"[sftp] downloaded {downloaded} files -> {OUT_DIR}")

    try:
        sftp.stat(EXTRA_REMOTE)
        sftp.get(EXTRA_REMOTE, str(EXTRA_LOCAL))
        print(f"[sftp] downloaded {EXTRA_REMOTE} -> {EXTRA_LOCAL}")
    except FileNotFoundError:
        print(f"[sftp] NOT FOUND on server: {EXTRA_REMOTE}")
    except IOError as exc:
        print(f"[sftp] error fetching {EXTRA_REMOTE}: {exc}")

    sftp.close()
    transport.close()
    print("[done]")


if __name__ == "__main__":
    main()
