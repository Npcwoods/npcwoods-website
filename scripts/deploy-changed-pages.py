#!/usr/bin/env python3
"""Plan or deploy pages that have a .synced.bak or .footer-synced.bak.

Dry-run is the default. Live upload requires Chris's explicit approval and the
standard confirmation phrase. Run after sync-header-snippet.py /
sync-footer-snippet.py to review or push the batch update.
"""
import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deploy_guard import (  # noqa: E402
    DeployPlanItem,
    LIVE_DEPLOY_CONFIRMATION,
    require_live_deploy_confirmation,
    summarize_plan,
)

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT.parent / ".env"
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


def build_deploy_plan(targets: list[Path]) -> list[DeployPlanItem]:
    return [
        DeployPlanItem(local=target.relative_to(ROOT), remote=remote_path_for(target))
        for target in targets
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Plan or upload pages touched by header/footer snippet sync. Dry-run is the default."
    )
    parser.add_argument("--execute", action="store_true", help="Actually upload files after approval")
    parser.add_argument(
        "--confirm-live-deploy",
        help=f'Exact phrase required with --execute: "{LIVE_DEPLOY_CONFIRMATION}"',
    )
    args = parser.parse_args((argv or sys.argv)[1:])

    targets = find_changed()
    if not targets:
        print("[noop] no changed pages found")
        return 0

    print(f"[deploy] {len(targets)} changed pages to upload")
    for t in targets[:5]:
        print(f"  - {t.relative_to(ROOT)}")
    if len(targets) > 5:
        print(f"  ... +{len(targets) - 5} more")

    print()
    print(summarize_plan(build_deploy_plan(targets)))

    try:
        require_live_deploy_confirmation(args.execute, args.confirm_live_deploy)
    except RuntimeError as exc:
        print(f"[blocked] {exc}", file=sys.stderr)
        return 2

    if not args.execute:
        print()
        print(
            '[dry-run] No credentials loaded and no files uploaded. '
            f'After Chris approves, add --execute --confirm-live-deploy "{LIVE_DEPLOY_CONFIRMATION}".'
        )
        return 0

    env = load_env()
    import paramiko

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

    # Trigger IndexNow pinger for uploaded files
    if uploaded > 0:
        import subprocess
        uploaded_paths = [str(local) for local in targets]
        if uploaded_paths:
            print("\n[indexnow] Triggering instant indexing for uploaded files...")
            indexnow_script = ROOT / "scripts" / "indexnow-submit.py"
            try:
                result = subprocess.run(
                    [sys.executable, str(indexnow_script)] + uploaded_paths,
                    capture_output=True,
                    text=True,
                    check=False
                )
                print(result.stdout)
                if result.stderr:
                    print(result.stderr, file=sys.stderr)
            except Exception as e:
                print(f"[indexnow] failed to trigger IndexNow submit: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
