#!/usr/bin/env python3
"""Deploy conversion-tracking-modified files to npcwoods.com via SFTP."""

import os
import paramiko

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(os.path.dirname(REPO_ROOT), ".env")

def load_env():
    env = {}
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, val = line.split("=", 1)
                env[key.strip()] = val.strip()
    return env

def local_to_remote(rel_path):
    """Map local repo path to remote server path."""
    if rel_path.startswith("homepage/page-npcwoods-home.php"):
        return "html/wp-content/themes/twentytwentyfour/page-npcwoods-home.php"
    elif rel_path == "html/shared/tracking.js":
        return "html/tracking.js"
    elif rel_path.startswith("landing-pages/"):
        return "html/" + rel_path[len("landing-pages/"):]
    elif rel_path.startswith("html/"):
        return "html/" + rel_path[len("html/"):]
    else:
        raise ValueError(f"Unknown path mapping for: {rel_path}")

def mkdir_recursive(sftp, remote_dir):
    """Create remote directory tree, ignoring already-exists errors."""
    parts = remote_dir.split("/")
    current = ""
    for part in parts:
        current = current + "/" + part if current else part
        try:
            sftp.mkdir(current)
        except IOError:
            pass

def main():
    env = load_env()
    host = env["SFTP_HOST"]
    port = int(env.get("SFTP_PORT", "22"))
    username = env["SFTP_USERNAME"]
    password = env["SFTP_PASSWORD"]

    # Read modified files list
    list_path = os.path.join(REPO_ROOT, "scripts", "modified-files.txt")
    with open(list_path) as f:
        files = [line.strip() for line in f if line.strip()]

    print(f"Connecting to {host}...")
    transport = paramiko.Transport((host, port))
    transport.banner_timeout = 30
    transport.auth_timeout = 30
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    print(f"Uploading {len(files)} files...\n")

    success = 0
    errors = []

    for rel_path in files:
        local_path = os.path.join(REPO_ROOT, rel_path)
        remote_path = local_to_remote(rel_path)

        # Ensure remote directory exists
        remote_dir = os.path.dirname(remote_path)
        mkdir_recursive(sftp, remote_dir)

        try:
            sftp.put(local_path, remote_path)
            print(f"  ✅  {remote_path}")
            success += 1
        except Exception as e:
            print(f"  ❌  {remote_path} — {e}")
            errors.append(rel_path)

    sftp.close()
    transport.close()

    print(f"\nDone: {success}/{len(files)} files uploaded successfully.")
    if errors:
        print(f"Errors: {len(errors)}")
        for e in errors:
            print(f"  - {e}")

if __name__ == "__main__":
    main()
