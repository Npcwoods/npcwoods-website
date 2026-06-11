#!/usr/bin/env python3
"""Deploy the 2026-06-11 Meta-pixel strip: 14 remaining health-condition pages.

Extends the 2026-06-10 6-page strip to every health-condition page that still
carried the hardcoded inline Meta pixel. Each page now has the pixel block removed
and the fbq no-op stub at the top of <head> (see scripts/strip_meta_pixel_html.py).
Chris approved this go-live bundle on 2026-06-11 ("do all 14").

Dry-run is the default. Live upload requires the standard confirmation phrase.
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

PAGES = [
    "landing-pages/uti-treatment/index.html",
    "landing-pages/uti-treatment/albuquerque-nm/index.html",
    "landing-pages/uti-treatment/mesa-az/index.html",
    "landing-pages/uti-treatment/scottsdale-az/index.html",
    "landing-pages/uti-treatment/surprise-az/index.html",
    "landing-pages/uti-care/index.html",
    "landing-pages/uti-treatment-online/index.html",
    "landing-pages/dental-pain/index.html",
    "landing-pages/ear-infection-treatment/index.html",
    "landing-pages/ed-treatment/index.html",
    "landing-pages/glp1-weight-loss/index.html",
    "landing-pages/sinus-infection-treatment/index.html",
    "landing-pages/strep-throat-treatment/index.html",
    "landing-pages/conditions/index.html",
]

FORBIDDEN = ['connect.facebook.net', 'facebook.com/tr', 'fbq("init"', "fbq('init'"]
STUB_MARKER = "Meta Pixel disabled 2026-06-10"


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
        for bad in FORBIDDEN:
            if bad in html:
                raise RuntimeError(f"{rel} still contains an active Meta pixel marker ({bad}) — refusing to deploy")
        if STUB_MARKER not in html:
            raise RuntimeError(f"{rel} is missing the fbq stub — run strip_meta_pixel_html.py first")
        items.append(DeployPlanItem(local=Path(rel), remote="html/" + rel[len("landing-pages/"):]))
    return items


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Deploy 14-page Meta-pixel strip. Dry-run by default.")
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
