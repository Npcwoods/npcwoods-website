#!/usr/bin/env python3
"""Upload a list of local files (relative to repo root) to the GoDaddy SFTP
server, preserving the directory layout under the remote web root `html/`.

Usage:
    python3 scripts/sftp-upload.py path/to/file1 path/to/file2 ...

Paths can be:
  - landing-pages/foo/index.html → uploaded to html/landing-pages/foo/index.html
  - html/experience/index.html   → uploaded to html/experience/index.html
    (the leading html/ is stripped — site web root IS html/)
  - homepage/page-npcwoods-home.php → SKIPPED (WordPress theme, deployed via
    REST API separately — see npcwoods-deploy/SKILL.md)

Creds come from /Users/chriswoods/Desktop/Chris-HQ/.env.
"""

from pathlib import Path
import os
import sys

try:
    import paramiko
except ImportError:
    print("paramiko not installed. Run: pip3 install paramiko", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = Path("/Users/chriswoods/Desktop/Chris-HQ/.env")
REMOTE_ROOT = "html"


def load_env():
    env = {}
    if not ENV_PATH.exists():
        print(f"[fatal] env not found: {ENV_PATH}", file=sys.stderr)
        sys.exit(2)
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def remote_path_for(local: Path) -> str | None:
    """Map local path → remote path on GoDaddy.

    Remote web root is `html/`. Local `landing-pages/foo/` is served at
    `https://npcwoods.com/foo/` so it lives at `html/foo/` on the server
    (the `landing-pages/` prefix is a local-only folder convention).
    Local `html/foo/` pages (experience, pharmacy, pharmacy-partners) already
    match the remote layout.
    """
    rel = local.relative_to(ROOT).as_posix()
    if rel == "homepage/page-npcwoods-home.php":
        return "html/wp-content/themes/twentytwentyfour/page-npcwoods-home.php"
    if rel.startswith("homepage/"):
        return None
    if rel.startswith("landing-pages/"):
        return f"{REMOTE_ROOT}/{rel[len('landing-pages/'):]}"
    if rel.startswith("html/"):
        return rel
    if rel.startswith("php/") and rel.endswith(".php"):
        # mu-plugin sources live in repo php/, deploy to wp-content/mu-plugins/
        return f"{REMOTE_ROOT}/wp-content/mu-plugins/{rel[len('php/'):]}"
    return None


def mkdir_p(sftp, path):
    parts = path.split("/")
    cur = ""
    for p in parts:
        cur = f"{cur}/{p}" if cur else p
        try:
            sftp.stat(cur)
        except IOError:
            try:
                sftp.mkdir(cur)
            except IOError:
                pass


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1

    files = []
    for arg in argv[1:]:
        p = (ROOT / arg).resolve()
        if not p.exists():
            print(f"[skip] missing: {arg}")
            continue
        files.append(p)

    if not files:
        print("[fatal] no files to upload")
        return 1

    env = load_env()
    host = env.get("SFTP_HOST")
    port = int(env.get("SFTP_PORT") or 22)
    user = env.get("SFTP_USERNAME")
    pw = env.get("SFTP_PASSWORD")
    if not all([host, user, pw]):
        print("[fatal] missing SFTP_HOST/USERNAME/PASSWORD in .env")
        return 2

    transport = paramiko.Transport((host, port))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    try:
        transport.connect(username=user, password=pw)
        sftp = paramiko.SFTPClient.from_transport(transport)

        uploaded = 0
        skipped = 0
        for local in files:
            remote = remote_path_for(local)
            if remote is None:
                print(f"[skip] WP theme (deploy separately): {local.relative_to(ROOT)}")
                skipped += 1
                continue
            remote_dir = "/".join(remote.split("/")[:-1])
            if remote_dir:
                mkdir_p(sftp, remote_dir)
            sftp.put(str(local), remote)
            uploaded += 1
            print(f"[up] {local.relative_to(ROOT)} -> {remote}")
        sftp.close()
        print()
        print(f"  uploaded: {uploaded}")
        print(f"  skipped:  {skipped}")
    finally:
        transport.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
