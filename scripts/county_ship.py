#!/usr/bin/env python3
"""Shared ship helper for the daily HPSA county page — Rocket.net target.

Replaces the per-county content-output/<county>-YYYYMMDD/preship_readonly.py
and ship_pieces.py copies (those targeted GoDaddy html/ with password SFTP and
a WP stub-touch flush; do not use them since 2026-10-26).

The page HTML and /sitemap/ still go up with scripts/deploy.py. This helper
does the pieces deploy.py does not: the county's NEW photo/mark/share-card
files, the one new route line in npcwoods-static-pages.php, the WP stub, and
a Rocket CDN purge of every uploaded URL.

Target: Rocket.net site 354775, SFTP key login (ROCKET_SFTP_* in
Chris-HQ/.env), web root public_html/. Secrets load only from that .env
via deploy.py; nothing secret is printed.

Usage (run from the counter, on main):
  # 1. read-only pre-ship snapshot (route file, sitemap, mu-plugins, asset existence)
  python3 scripts/county_ship.py snapshot --slug rich-county-text-visit \
      --work ../content-output/rich-county-20261028 \
      --asset landing-pages/rich-county-text-visit/mark.png \
      --asset landing-pages/rich-county-text-visit/<photo>.jpg \
      --asset assets/img/share/rich-county-1200x630.jpg

  # 2. plan (DEFAULT = dry-run, no server contact)
  python3 scripts/county_ship.py ship --slug rich-county-text-visit --title "Rich County text visit" \
      --work ../content-output/rich-county-20261028 --asset ... (same list)

  # 3. live (standing daily-county go-ahead only; same phrase gate as deploy.py)
  ... ship ... --live --confirm-live-deploy "CHRIS APPROVED LIVE DEPLOY"

Safety (unchanged from the GoDaddy-era helpers):
  - assets are NEW files only: refuses if any already exists on the server
  - route file: live copy must equal the pre-ship snapshot; local file must
    keep every live route and add exactly one ("<slug>" => "<slug>/index.html");
    php -l must pass; no duplicate function names across mu-plugins
  - backups before overwrite: local content-output/deploy-backups/<date>/ and
    a remote <route>.bak-<ts>-<county> next to the route file
  - never deletes anything on the server; one SFTP attempt, stop on failure
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # npcwoods-website
HQ = ROOT.parent                                        # Chris-HQ
SITE = "https://npcwoods.com"
ROUTE_FILE = "npcwoods-static-pages.php"
LIVE_DEPLOY_CONFIRMATION = "CHRIS APPROVED LIVE DEPLOY"


def deploy_module():
    spec = importlib.util.spec_from_file_location("npcw_deploy", ROOT / "scripts" / "deploy.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


D = deploy_module()
WEB_ROOT = D.REMOTE_PREFIX                              # "public_html"
ROUTE_REMOTE = f"{WEB_ROOT}/wp-content/mu-plugins/{ROUTE_FILE}"
ROUTE_LOCAL = ROOT / "php" / ROUTE_FILE
SITEMAP_REMOTE = f"{WEB_ROOT}/sitemap/index.html"


def remote_for(local_rel: str) -> str:
    """landing-pages/<slug>/x -> public_html/<slug>/x ; assets/... -> public_html/assets/..."""
    rel = local_rel.strip("/")
    if rel.startswith("landing-pages/"):
        rel = rel[len("landing-pages/"):]
    if ".." in rel.split("/"):
        raise ValueError(f"path traversal: {local_rel}")
    return f"{WEB_ROOT}/{rel}"


def url_for(remote: str) -> str:
    return f"{SITE}/{remote[len(WEB_ROOT) + 1:]}"


def county_tag(slug: str) -> str:
    return slug.replace("-county-text-visit", "").replace("-text-visit", "")


def routes(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if "=>" in line]


def function_names(php: str) -> set[str]:
    return set(re.findall(r"^\s*function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", php, re.M))


def duplicate_functions(mu_dir: Path, local_route: Path) -> dict[str, list[str]]:
    seen: dict[str, list[str]] = {}
    files = {p.name: p.read_text(errors="replace") for p in mu_dir.glob("*.php") if p.name != ROUTE_FILE}
    files[ROUTE_FILE] = local_route.read_text(errors="replace")
    for name, text in files.items():
        for fn in function_names(text):
            seen.setdefault(fn, []).append(name)
    return {fn: names for fn, names in seen.items() if len(names) > 1}


def route_check(live_text: str, local_text: str, slug: str) -> str | None:
    old, new = routes(live_text), routes(local_text)
    missing = [r for r in old if r not in new]
    added = [r for r in new if r not in old]
    expected = [f'"{slug}" => "{slug}/index.html",']
    print(f"[route] live {len(old)} lines, local {len(new)}, missing {len(missing)}, added {added}")
    if missing:
        return f"local route file drops live routes: {missing[:5]}"
    if added != expected:
        return f"route diff must be exactly {expected}, got {added}"
    return None


# --------------------------------------------------------------------------

def cmd_snapshot(args) -> int:
    work = Path(args.work).resolve()
    live = work / "live"
    (live / "mu").mkdir(parents=True, exist_ok=True)
    env = D.load_env()
    sftp, client = D.sftp_connect(env)
    try:
        for remote, local in [(ROUTE_REMOTE, live / ROUTE_FILE), (SITEMAP_REMOTE, live / "sitemap-index.html")]:
            with sftp.file(remote, "rb") as rf:
                local.write_bytes(rf.read())
            print("[pulled]", remote, local.stat().st_size)
        checks = [f"{WEB_ROOT}/{args.slug}", f"{WEB_ROOT}/{args.slug}/index.html"] + [remote_for(a) for a in args.asset]
        for p in checks:
            try:
                sftp.stat(p)
                print("[EXISTS]", p)
            except IOError:
                print("[absent]", p)
        mu = f"{WEB_ROOT}/wp-content/mu-plugins"
        names = sorted(sftp.listdir(mu))
        for n in names:
            if n.endswith(".php"):
                with sftp.file(f"{mu}/{n}", "rb") as rf:
                    (live / "mu" / n).write_bytes(rf.read())
        print(f"[mu-plugins] {len(names)} entries, {sum(n.endswith('.php') for n in names)} .php pulled")
    finally:
        sftp.close()
        client.close()
    return 0


def cmd_ship(args) -> int:
    work = Path(args.work).resolve()
    snap_route = work / "live" / ROUTE_FILE
    if not snap_route.exists():
        print(f"[blocked] no pre-ship snapshot at {snap_route}. Run `snapshot` first.", file=sys.stderr)
        return 2
    assets = []
    for a in args.asset:
        local = ROOT / a
        if not local.is_file():
            print(f"[blocked] local asset missing: {local}", file=sys.stderr)
            return 2
        assets.append((local, remote_for(a)))

    # local guards (no server contact)
    subprocess.run(["php", "-l", str(ROUTE_LOCAL)], check=True)
    problem = route_check(snap_route.read_text(), ROUTE_LOCAL.read_text(), args.slug)
    if problem:
        print(f"[blocked] {problem}", file=sys.stderr)
        return 2
    dups = duplicate_functions(work / "live" / "mu", ROUTE_LOCAL)
    if dups:
        print(f"[blocked] duplicate PHP functions across mu-plugins: {dups}", file=sys.stderr)
        return 2
    print("[dup-functions] none")

    page_url = f"{SITE}/{args.slug}/"
    purge = [page_url] + [url_for(r) for _, r in assets]
    print(f"\nCounty ship plan — {args.slug} (Rocket.net, web root {WEB_ROOT}/)")
    for local, remote in assets:
        print(f"  [new]   {local.relative_to(ROOT)} -> {remote}  ({local.stat().st_size:,} bytes)")
    print(f"  [route] php/{ROUTE_FILE} -> {ROUTE_REMOTE}  (backup first, +1 route)")
    print(f"  [stub]  WP page '{args.slug}' (find or create)")
    print(f"  [purge] Rocket CDN: {', '.join(purge)}")

    if not args.live:
        print("\n[dry-run] nothing uploaded. Add --live and the confirmation phrase to ship.")
        return 0
    if args.confirmation != LIVE_DEPLOY_CONFIRMATION:
        print(f'[blocked] --live needs --confirm-live-deploy "{LIVE_DEPLOY_CONFIRMATION}".', file=sys.stderr)
        return 2

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    env = D.load_env()
    sftp, client = D.sftp_connect(env)
    try:
        for local, remote in assets:          # pre-check ALL before writing ANY
            try:
                sftp.stat(remote)
                print("[STOP] already exists, not overwriting:", remote)
                return 3
            except IOError:
                pass
        with sftp.file(ROUTE_REMOTE, "rb") as rf:
            live = rf.read()
        if live != snap_route.read_bytes():
            print("[STOP] live route file changed since the pre-ship snapshot")
            return 4
        for local, remote in assets:
            D.sftp_mkdirs(sftp, remote.rsplit("/", 1)[0])
            sftp.put(str(local), remote)
            print("[upload new]", remote, sftp.stat(remote).st_size, "local", local.stat().st_size)
        local_bak = HQ / "content-output" / "deploy-backups" / datetime.now().strftime("%Y-%m-%d") / \
            f"{ROUTE_FILE}.remote-backup-{ts}"
        local_bak.parent.mkdir(parents=True, exist_ok=True)
        local_bak.write_bytes(live)
        print("[backup local]", local_bak)
        bak_remote = f"{ROUTE_REMOTE}.bak-{ts}-{county_tag(args.slug)}"
        with sftp.file(bak_remote, "wb") as wf:
            wf.write(live)
        print("[backup remote]", bak_remote, sftp.stat(bak_remote).st_size)
        sftp.put(str(ROUTE_LOCAL), ROUTE_REMOTE)
        with sftp.file(ROUTE_REMOTE, "rb") as rf:
            chk = rf.read()
        print("[upload route]", ROUTE_REMOTE, len(chk), "matches local:", chk == ROUTE_LOCAL.read_bytes())
    finally:
        sftp.close()
        client.close()

    dp_spec = importlib.util.spec_from_file_location("npcw_deploy_page", ROOT / "scripts" / "deploy-page.py")
    dp = importlib.util.module_from_spec(dp_spec)
    sys.modules[dp_spec.name] = dp
    dp_spec.loader.exec_module(dp)
    pid = dp.get_or_create_stub(env, args.slug, args.title)
    ok = D.rocket_purge(env, purge)
    print("STUB_ID", pid, "TS", ts, "PURGE", "ok" if ok else "FAILED")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Daily county page pieces -> Rocket.net. DRY-RUN BY DEFAULT.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("snapshot", "ship"):
        p = sub.add_parser(name)
        p.add_argument("--slug", required=True, help="e.g. rich-county-text-visit")
        p.add_argument("--work", required=True, help="content-output/<county>-YYYYMMDD work dir")
        p.add_argument("--asset", action="append", default=[], help="repo-relative NEW file (repeatable)")
        if name == "ship":
            p.add_argument("--title", required=True, help="WP stub title")
            p.add_argument("--live", action="store_true")
            p.add_argument("--confirm-live-deploy", dest="confirmation", default=None)
    args = ap.parse_args(argv)
    if not re.fullmatch(r"[a-z0-9-]+-text-visit", args.slug):
        print("[blocked] slug must look like <county>-county-text-visit", file=sys.stderr)
        return 2
    return cmd_snapshot(args) if args.cmd == "snapshot" else cmd_ship(args)


if __name__ == "__main__":
    sys.exit(main())
