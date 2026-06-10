#!/usr/bin/env python3
"""Deploy the June 10 2026 discovery-audit week-one fixes (commit f9a2d94).

Covers: edited static HTML pages, llms.txt/llms-full.txt, the rescued ABQ blog,
and the 3 mu-plugins the audit actually modified (eeat, faq-schema, dental-pages).
The other synced mu-plugins already match production, so they are intentionally
NOT pushed.

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
COMMIT = "f9a2d94"
MU_REMOTE = "html/wp-content/mu-plugins"

# mu-plugins the audit modified vs production. The rest of the changed php/ files
# either match the server byte-for-byte or were pulled FROM the server in this commit.
PHP_TO_DEPLOY = {
    "php/npcwoods-eeat.php",
    "php/npcwoods-faq-schema.php",
    "php/npcwoods-dental-pages.php",
}


def load_env():
    env = {}
    for raw in ENV_PATH.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def changed_files() -> list[str]:
    out = subprocess.run(
        ["git", "show", "--name-status", "--format=", COMMIT],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    files = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        # For renames (R100) take the new path (last column)
        path = parts[-1]
        if status.startswith("D"):
            continue
        files.append(path)
    return files


def remote_for(rel: str) -> str | None:
    """Map a repo-relative path to its production path, or None if not deployable."""
    if "/.bak" in rel or rel.endswith(".bak") or "_archive/" in rel:
        return None
    if rel.startswith("scripts/"):
        return None
    if rel == "llms.txt":
        return "html/llms.txt"
    if rel == "llms-full.txt":
        return "html/llms-full.txt"
    if rel.startswith("php/"):
        return f"{MU_REMOTE}/{Path(rel).name}" if rel in PHP_TO_DEPLOY else None
    if rel.startswith("html/"):
        return rel
    if rel.startswith("landing-pages/"):
        return "html/" + rel[len("landing-pages/"):]
    return None


def build_plan() -> list[DeployPlanItem]:
    items = []
    for rel in changed_files():
        remote = remote_for(rel)
        if remote is None:
            continue
        items.append(DeployPlanItem(local=Path(rel), remote=remote))
    return sorted(items, key=lambda i: i.remote)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Deploy discovery-audit fixes. Dry-run by default.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-live-deploy")
    args = parser.parse_args((argv or sys.argv)[1:])

    plan = build_plan()
    html = [i for i in plan if i.remote.endswith(".html") or i.remote.endswith("index.html")]
    php = [i for i in plan if i.remote.startswith(MU_REMOTE)]
    other = [i for i in plan if i not in html and i not in php]
    print(f"[plan] {len(plan)} files: {len(html)} HTML, {len(php)} mu-plugins, {len(other)} root files")
    for i in php + other:
        print(f"  [up] {i.local} -> {i.remote}")
    print(f"  [up] ...+{len(html)} HTML pages")

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

    def mkdir_safe(path: str):
        try:
            sftp.mkdir(path)
        except IOError:
            pass

    uploaded, failed = 0, []
    for item in plan:
        local = ROOT / item.local
        remote = item.remote
        parts = remote.split("/")
        for i in range(1, len(parts)):
            mkdir_safe("/".join(parts[:i]))
        try:
            sftp.put(str(local), remote)
            uploaded += 1
        except Exception as e:  # noqa: BLE001
            failed.append((str(item.local), str(e)))
            print(f"[err] {item.local}: {e}")
    sftp.close()
    transport.close()
    print(f"\n[done] uploaded {uploaded}/{len(plan)} ({len(failed)} failed)")
    if failed:
        return 1

    # IndexNow ping for the HTML + llms surfaces
    paths = [str(ROOT / i.local) for i in plan if i.remote.endswith(".html") or i.remote.endswith(".txt")]
    if paths:
        print("\n[indexnow] pinging...")
        subprocess.run([sys.executable, str(ROOT / "scripts" / "indexnow-submit.py")] + paths, check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
