#!/usr/bin/env python3
"""Deploy the June 10 2026 Meta-pixel strip: 6 UTI condition pages.

Inline Meta pixel removed and replaced with an fbq no-op stub that also blocks
the GTM-injected pixel (no BAA with Meta; health-condition pages must not send
PageView there). Chris approved this go-live bundle on 2026-06-10.

Dry-run is the default. Live upload requires the standard confirmation phrase.
"""
import argparse
import subprocess
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

PAGES = [
    "landing-pages/arizona-uti-treatment/index.html",
    "landing-pages/uti-treatment/burning-when-i-pee/index.html",
    "landing-pages/uti-treatment/uti-antibiotics-online/index.html",
    "landing-pages/uti-treatment/is-my-uti-getting-worse/index.html",
    "landing-pages/uti-treatment/no-video-uti-treatment/index.html",
    "landing-pages/uti-treatment/how-fast-do-uti-antibiotics-work/index.html",
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


def build_plan() -> list[DeployPlanItem]:
    items = []
    for rel in PAGES:
        local = ROOT / rel
        html = local.read_text()
        if "fbq('init'" in html or "facebook.com/tr" in html:
            raise RuntimeError(f"{rel} still contains an active Meta pixel — refusing to deploy")
        if "Meta Pixel disabled 2026-06-10" not in html:
            raise RuntimeError(f"{rel} is missing the fbq stub — wrong working tree state?")
        items.append(DeployPlanItem(local=Path(rel), remote="html/" + rel[len("landing-pages/"):]))
    return items


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Deploy Meta-pixel strip. Dry-run by default.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-live-deploy")
    args = parser.parse_args((argv or sys.argv)[1:])

    plan = build_plan()
    print(summarize_plan(plan))

    try:
        require_live_deploy_confirmation(args.execute, args.confirm_live_deploy)
    except RuntimeError as exc:
        print(f"[blocked] {exc}", file=sys.stderr)
        return 2

    if not args.execute:
        print(f'\n[dry-run] nothing uploaded. Add --execute --confirm-live-deploy "{LIVE_DEPLOY_CONFIRMATION}".')
        return 0

    env = load_env()
    import paramiko

    print(f"\n[sftp] connecting to {env['SFTP_HOST']}:{env['SFTP_PORT']}")
    transport = paramiko.Transport((env["SFTP_HOST"], int(env["SFTP_PORT"])))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(transport)

    uploaded, failed = 0, []
    for item in plan:
        try:
            sftp.put(str(ROOT / item.local), item.remote)
            uploaded += 1
            print(f"[up] {item.remote}")
        except Exception as e:  # noqa: BLE001
            failed.append((str(item.local), str(e)))
            print(f"[err] {item.local}: {e}")
    sftp.close()
    transport.close()
    print(f"\n[done] uploaded {uploaded}/{len(plan)} ({len(failed)} failed)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
