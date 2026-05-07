#!/usr/bin/env python3
"""
NPCWoods SFTP Upload Helper
============================
Uploads files and directories to GoDaddy via SFTP using paramiko.

Usage (via osascript):
    Write this script to /tmp/ with credentials filled in, then execute:

    do shell script "cat > /tmp/npc_upload.py << 'PYEOF'
    ... (paste this with credentials filled in) ...
    PYEOF
    python3 /tmp/npc_upload.py"

Configuration:
    Fill in the variables in the CONFIG section below before running.
    Read credentials from: /Users/chriswoods/Desktop/Chris-HQ/ChrisOS/.env
"""

import paramiko
import os
import sys

# ============================================================
# CONFIG — Fill these in from the .env file
# ============================================================
SFTP_HOST = ''        # e.g., vki.0b3.myftpupload.com
SFTP_PORT = 22
SFTP_USERNAME = ''    # e.g., client_373e6043b2_1085255
SFTP_PASSWORD = ''

# Local base path (where files are on Chris's Mac)
LOCAL_BASE = '/Users/chriswoods/Desktop/Chris-HQ/npcwoods-website'

# Remote web root on GoDaddy
REMOTE_ROOT = 'html'

# ============================================================
# UPLOAD MAP — Define what to upload
# Format: (local_relative_path, remote_relative_path)
# Paths are relative to LOCAL_BASE and REMOTE_ROOT respectively
# ============================================================
UPLOADS = [
    # Example:
    # ('landing-pages/learn/strep-throat/index.html', 'learn/strep-throat/index.html'),
    # ('php/npcwoods-education-pages.php', 'wp-content/mu-plugins/npcwoods-education-pages.php'),
]

# ============================================================
# DIRECTORIES — Create these on the server before uploading
# (relative to REMOTE_ROOT)
# ============================================================
DIRECTORIES = [
    # Example:
    # 'learn',
    # 'learn/strep-throat',
]


def mkdir_safe(sftp, path):
    """Create a directory, ignoring if it already exists."""
    try:
        sftp.mkdir(path)
        print(f'  Created dir: {path}')
    except IOError:
        pass  # already exists


def main():
    if not SFTP_HOST or not SFTP_USERNAME:
        print('ERROR: Fill in SFTP credentials before running!')
        sys.exit(1)

    if not UPLOADS:
        print('ERROR: No files defined in UPLOADS list!')
        sys.exit(1)

    print(f'Connecting to {SFTP_HOST}:{SFTP_PORT}...')
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.banner_timeout = 30
    transport.auth_timeout = 30
    transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    print('Connected.')

    # Create directories
    if DIRECTORIES:
        print(f'\nCreating {len(DIRECTORIES)} directories...')
        for d in DIRECTORIES:
            mkdir_safe(sftp, f'{REMOTE_ROOT}/{d}')

    # Upload files
    print(f'\nUploading {len(UPLOADS)} files...')
    uploaded = 0
    for local_rel, remote_rel in UPLOADS:
        local_path = os.path.join(LOCAL_BASE, local_rel)
        remote_path = f'{REMOTE_ROOT}/{remote_rel}'

        if not os.path.exists(local_path):
            print(f'  SKIP (not found): {local_path}')
            continue

        sftp.put(local_path, remote_path)
        uploaded += 1
        stat = sftp.stat(remote_path)
        print(f'  [{uploaded}/{len(UPLOADS)}] {remote_rel} ({stat.st_size} bytes)')

    sftp.close()
    transport.close()
    print(f'\nDone! {uploaded}/{len(UPLOADS)} files uploaded.')


if __name__ == '__main__':
    main()
