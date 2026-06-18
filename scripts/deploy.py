#!/usr/bin/env python3
"""Unified guarded deploy tool for NPCWoods.com landing pages.

Supersedes the dated one-off deploy scripts (see scripts/README-deploy.md).
Pipeline per page:

  1. Local safety checks (no Meta pixel; warn on missing GTM/tracking.js).
  2. Timestamped remote backup -> content-output/deploy-backups/<date>/.
  3. SFTP upload: landing-pages/{path}/index.html -> html/{path}/index.html.
  4. WP stub touch (REST no-op update) to flush GoDaddy Varnish cache.
  5. Live verification (HTTP markers; full Playwright tracking run if
     playwright is installed).

DEFAULT IS DRY-RUN. Nothing goes live without Chris's explicit yes:
--live requires the confirmation phrase, typed interactively or passed
via --confirm-live-deploy.

Usage:
  python3 scripts/deploy.py --pages uti-treatment/mesa-az/search-safe
  python3 scripts/deploy.py --manifest batch.txt --live
  python3 scripts/deploy.py --pages uti-treatment/mesa-az/search-safe --verify-only
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import posixpath
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------------------------
# Layout & constants
# --------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent  # npcwoods-website repo root
LANDING_DIR = "landing-pages"
REMOTE_PREFIX = "html"
SITE = "https://npcwoods.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

LIVE_DEPLOY_CONFIRMATION = "CHRIS APPROVED LIVE DEPLOY"

# Universal content guards (every marketing page, every deploy).
# Meta pixel must never ride along on a health page (see meta-pixel strip,
# 2026-06-10/11); "insurance" is a Chris hard rule for marketing surfaces.
FORBIDDEN_MARKERS = [
    "connect.facebook.net",
    "facebook.com/tr",
    'fbq("init"',
    "fbq('init'",
]
WARN_IF_MISSING = ["GTM-59QSWZRC", "tracking.js"]
WARN_IF_PRESENT = ["insurance"]

# url path -> WP stub ID for the Varnish cache flush. Search-safe child pages
# flush their parent city stub (walk-up logic in stub_id_for_page).
# Extended at runtime by scripts/page-ids-2026-04-22.json if present.
STUB_IDS = {
    "/": 63,
    "/experience/": 310,
    "/blog/": 413,
    "/georgia-telemedicine/": 252,
    "/north-carolina-telemedicine/": 253,
    "/dental-pain/": 336,
    "/pharmacy/": 334,
    "/pharmacy-partners/": 335,
    "/uti-treatment/mesa-az/": 13,
    "/uti-treatment/surprise-az/": 20,
    "/uti-treatment/scottsdale-az/": 17,
    "/uti-treatment/albuquerque-nm/": 411,
    "/uti-care/": 698,
    "/do-i-need-antibiotics-sinus-infection/": 454,
}
STUB_SIDECAR = ROOT / "scripts" / "page-ids-2026-04-22.json"

GOOD_TRACKING_DOMAINS = [
    "googletagmanager.com",
    "google-analytics.com",
    "googleadservices.com",
    "doubleclick.net",
]
BAD_TRACKING_DOMAINS = ["connect.facebook.net", "facebook.com/tr"]
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)


def hq_root() -> Path:
    """Chris-HQ root (holds .env and content-output). Works from worktrees too."""
    fixed = Path.home() / "Desktop" / "Chris-HQ"
    if (fixed / ".env").exists() or fixed.is_dir():
        return fixed
    return ROOT.parent


def backup_root(now: datetime | None = None) -> Path:
    now = now or datetime.now()
    return hq_root() / "content-output" / "deploy-backups" / now.strftime("%Y-%m-%d")


def backup_path_for(remote: str, now: datetime | None = None) -> Path:
    """content-output/deploy-backups/<date>/<remote with __>.remote-backup-<ts>"""
    now = now or datetime.now()
    ts = now.strftime("%Y%m%d-%H%M%S")
    return backup_root(now) / f"{remote.replace('/', '__')}.remote-backup-{ts}"


# --------------------------------------------------------------------------
# Page resolution
# --------------------------------------------------------------------------

@dataclass
class PagePlan:
    page: str                     # normalized page path, e.g. uti-treatment/mesa-az/search-safe
    local: Path                   # absolute local file
    remote: str                   # remote path, e.g. html/uti-treatment/mesa-az/search-safe/index.html
    url: str                      # live URL
    size: int = 0
    sha256: str = ""
    warnings: list = field(default_factory=list)


def normalize_page(raw: str) -> str:
    """Accept 'uti-treatment/mesa-az/search-safe', with/without trailing slash,
    leading slash, 'landing-pages/' prefix, or a trailing 'index.html'."""
    p = raw.strip().strip("/")
    if p.startswith(f"{LANDING_DIR}/"):
        p = p[len(LANDING_DIR) + 1:]
    if p.endswith("/index.html"):
        p = p[: -len("/index.html")]
    elif p == "index.html":
        p = ""
    if not p:
        raise ValueError(f"cannot deploy the bare homepage path from {raw!r}; pass an explicit page dir")
    if ".." in p.split("/"):
        raise ValueError(f"refusing path traversal in page path: {raw!r}")
    return p


def local_path_for(page: str) -> Path:
    primary = ROOT / LANDING_DIR / page / "index.html"
    if primary.exists():
        return primary
    # core pages (about, experience, pharmacy-partners, ...) keep their source under html/
    fallback = ROOT / "html" / page / "index.html"
    if fallback.exists():
        return fallback
    return primary


def remote_path_for(page: str) -> str:
    return f"{REMOTE_PREFIX}/{page}/index.html"


def url_for(page: str) -> str:
    return f"{SITE}/{page}/"


def parse_manifest(path: Path) -> list[str]:
    """One page path per line; blank lines and #-comments ignored."""
    pages = []
    for raw in path.read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            pages.append(line)
    return pages


def collect_pages(args) -> list[str]:
    raw: list[str] = []
    for chunk in args.pages or []:
        raw.extend(p for p in chunk.split(",") if p.strip())
    if args.manifest:
        raw.extend(parse_manifest(Path(args.manifest)))
    seen, out = set(), []
    for r in raw:
        p = normalize_page(r)
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def stub_id_for_page(page: str, stub_ids: dict | None = None) -> int | None:
    """Exact stub match, else the immediate parent only (search-safe child
    pages flush the parent city stub, e.g. /uti-treatment/mesa-az/ id 13).
    No deeper walk-up: distant ancestors don't cache the child URL, and new
    URLs have nothing cached (None), matching the dated city scripts."""
    table = stub_ids if stub_ids is not None else load_stub_table()
    parts = page.strip("/").split("/")
    for candidate in (parts, parts[:-1]):
        if not candidate:
            continue
        key = "/" + "/".join(candidate) + "/"
        if key in table:
            return table[key]
    return None


def load_stub_table() -> dict:
    table = {}
    if STUB_SIDECAR.exists():
        try:
            table.update(json.loads(STUB_SIDECAR.read_text()))
        except (json.JSONDecodeError, OSError):
            pass
    table.update(STUB_IDS)  # inline entries win
    return table


# --------------------------------------------------------------------------
# Plan + safety checks
# --------------------------------------------------------------------------

def build_plan(pages: list[str]) -> list[PagePlan]:
    plan, problems = [], []
    for page in pages:
        local = local_path_for(page)
        item = PagePlan(page=page, local=local, remote=remote_path_for(page), url=url_for(page))
        if not local.exists():
            problems.append(f"{page}: local file missing: {local}")
            continue
        data = local.read_bytes()
        item.size = len(data)
        item.sha256 = hashlib.sha256(data).hexdigest()
        html = data.decode("utf-8", errors="replace")
        lower = html.lower()
        for bad in FORBIDDEN_MARKERS:
            if bad.lower() in lower:
                problems.append(f"{page}: contains forbidden marker {bad!r} — refusing to deploy")
        for marker in WARN_IF_MISSING:
            if marker not in html:
                item.warnings.append(f"missing {marker!r}")
        for word in WARN_IF_PRESENT:
            if word in lower:
                item.warnings.append(f"contains {word!r} — Chris hard rule, double-check before going live")
        plan.append(item)
    if problems:
        raise RuntimeError("plan blocked:\n  " + "\n  ".join(problems))
    return plan


def print_plan(plan: list[PagePlan], stub_table: dict) -> None:
    print(f"Deploy plan — {len(plan)} page(s):")
    for item in plan:
        stub = stub_id_for_page(item.page, stub_table)
        stub_note = f"stub {stub}" if stub else "no stub (new URL, nothing cached)"
        rel = item.local.relative_to(ROOT)
        print(f"  [up] {rel}")
        print(f"       -> {item.remote}  ({item.size:,} bytes, sha256 {item.sha256[:12]}…, {stub_note})")
        for w in item.warnings:
            print(f"       [warn] {w}")


# --------------------------------------------------------------------------
# Credentials & guard
# --------------------------------------------------------------------------

def load_env() -> dict:
    """Secrets live in ~/Desktop/Chris-HQ/.env only. python-dotenv when
    available, manual parse otherwise (same as every prior deploy script)."""
    env_path = hq_root() / ".env"
    if not env_path.exists():
        raise RuntimeError(f".env not found at {env_path}")
    try:
        from dotenv import dotenv_values  # type: ignore
        return {k: v for k, v in dotenv_values(env_path).items() if v is not None}
    except ImportError:
        pass
    env = {}
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def confirm_live(confirmation: str | None, prompt=input) -> bool:
    """True only when Chris's confirmation phrase is supplied — via flag or
    typed interactively. Anything else blocks the deploy."""
    if confirmation == LIVE_DEPLOY_CONFIRMATION:
        return True
    if confirmation is not None:
        print(f"[blocked] wrong confirmation phrase. Expected exactly: {LIVE_DEPLOY_CONFIRMATION}",
              file=sys.stderr)
        return False
    if not sys.stdin.isatty() and prompt is input:
        print(f'[blocked] non-interactive run. Re-run with --confirm-live-deploy '
              f'"{LIVE_DEPLOY_CONFIRMATION}" after Chris explicitly approves.', file=sys.stderr)
        return False
    try:
        typed = prompt(f'Type the confirmation phrase to deploy LIVE ("{LIVE_DEPLOY_CONFIRMATION}"): ')
    except EOFError:
        typed = ""
    if typed.strip() != LIVE_DEPLOY_CONFIRMATION:
        print("[blocked] confirmation phrase did not match. Nothing uploaded.", file=sys.stderr)
        return False
    return True


# --------------------------------------------------------------------------
# SFTP
# --------------------------------------------------------------------------

def sftp_connect(env):
    import paramiko  # lazy: dry-run must never need it
    transport = paramiko.Transport((env["SFTP_HOST"], int(env["SFTP_PORT"])))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    return paramiko.SFTPClient.from_transport(transport), transport


def sftp_mkdirs(sftp, remote_dir: str) -> None:
    path = ""
    for part in remote_dir.split("/"):
        path = f"{path}/{part}" if path else part
        try:
            sftp.stat(path)
        except IOError:
            sftp.mkdir(path)


def sftp_backup(sftp, remote: str) -> Path | None:
    """Download a timestamped copy of the remote file before overwrite.
    Returns the backup path, or None if the remote file doesn't exist yet."""
    dest = backup_path_for(remote)
    try:
        with sftp.file(remote, "rb") as rf:
            data = rf.read()
    except IOError:
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest


def remote_diff(sftp, plan: list[PagePlan]) -> None:
    """Read-only: report whether each remote file differs from local."""
    print("\nRemote diff (read-only):")
    for item in plan:
        try:
            with sftp.file(item.remote, "rb") as rf:
                data = rf.read()
        except IOError:
            print(f"  [new]  {item.remote} — does not exist on server yet")
            continue
        sha = hashlib.sha256(data).hexdigest()
        if sha == item.sha256:
            print(f"  [same] {item.remote} — identical ({len(data):,} bytes)")
        else:
            print(f"  [diff] {item.remote} — remote {len(data):,} bytes sha {sha[:12]}… "
                  f"vs local {item.size:,} bytes sha {item.sha256[:12]}…")


# --------------------------------------------------------------------------
# WP cache flush
# --------------------------------------------------------------------------

def wp_req(url: str, auth: str, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": f"Basic {auth}", "User-Agent": UA}
    if body is not None:
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, json.loads(resp.read() or "null")
    except urllib.error.HTTPError as e:
        return e.code, None
    except urllib.error.URLError:
        return 0, None


def touch_stub(auth: str, stub_id: int) -> bool:
    """No-op REST update -> GoDaddy auto-purges the Varnish cache for the page."""
    for post_type in ("pages", "posts"):
        base = f"{SITE}/wp-json/wp/v2/{post_type}/{stub_id}"
        st, cur = wp_req(f"{base}?_fields=id,content,title,status", auth)
        if st != 200 or not cur:
            continue
        payload = {
            "title": cur.get("title", {}).get("raw") or cur.get("title", {}).get("rendered", ""),
            "content": cur.get("content", {}).get("raw") or cur.get("content", {}).get("rendered", ""),
            "status": cur.get("status", "publish"),
        }
        st2, _ = wp_req(base, auth, method="POST", body=payload)
        return st2 == 200
    return False


def wp_auth(env: dict) -> str:
    return base64.b64encode(f"{env['WP_USERNAME']}:{env['WP_APP_PASSWORD']}".encode()).decode()


# --------------------------------------------------------------------------
# Live verification
# --------------------------------------------------------------------------

def verify_http(item: PagePlan) -> str | None:
    """Cache-busted GET: page loads, looks like our static HTML, carries GTM +
    tracking.js. Returns None on pass, else a problem description."""
    url = f"{item.url}?v={int(time.time())}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            html = resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        return f"request failed: {e}"
    if status != 200:
        return f"bad status {status}"
    if not html.lstrip().lower().startswith("<!doctype html>"):
        return "response is not our static HTML page"
    missing = [m for m in WARN_IF_MISSING if m not in html]
    if missing:
        return f"missing markers: {missing}"
    return None


def verify_tracking_playwright(item: PagePlan) -> tuple[bool, str]:
    """Full tracking run: mobile viewport, ?gclid=TEST, assert GTM + GA4
    requests fire and zero Meta pixel requests (pattern from
    tests/verify-uti-search-safe-cities-tracking.py)."""
    from playwright.sync_api import sync_playwright  # lazy

    url = f"{item.url}?gclid=TEST_DEPLOY_TOOL"
    hits, bad_hits = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, user_agent=MOBILE_UA)
        page = ctx.new_page()
        page.on("request", lambda r: (
            hits.append(r.url) if any(d in r.url for d in GOOD_TRACKING_DOMAINS) else
            bad_hits.append(r.url) if any(d in r.url for d in BAD_TRACKING_DOMAINS) else None
        ))
        page.goto(url, wait_until="networkidle", timeout=60000)
        sms = page.locator('a[href^="sms:"]')
        if sms.count():
            page.evaluate("""
                document.querySelectorAll('a[href^="sms:"]').forEach(a => {
                    a.addEventListener('click', e => e.preventDefault(), {capture: false});
                });
            """)
            sms.first.click()
            page.wait_for_timeout(3000)
        ctx.close()
        browser.close()

    gtm = any("googletagmanager.com" in u for u in hits)
    ga4 = any("google-analytics.com" in u or "/g/collect" in u for u in hits)
    ok = gtm and ga4 and not bad_hits
    return ok, f"GTM={gtm} GA4={ga4} MetaPixel={len(bad_hits)}"


def run_verification(plan: list[PagePlan]) -> dict[str, str]:
    """Returns page -> 'PASS'/'FAIL: reason' map."""
    try:
        import playwright  # noqa: F401
        have_playwright = True
    except ImportError:
        have_playwright = False
        print("[verify] playwright not installed — falling back to HTTP marker checks only")

    results = {}
    for item in plan:
        problem = verify_http(item)
        if problem:
            results[item.page] = f"FAIL: {problem}"
            print(f"  [verify] {item.page}: FAIL ({problem})")
            continue
        if have_playwright:
            try:
                ok, detail = verify_tracking_playwright(item)
            except Exception as e:  # noqa: BLE001 — verification must never crash the report
                ok, detail = False, f"playwright error: {e}"
            results[item.page] = ("PASS" if ok else "FAIL") + f" ({detail})"
            print(f"  [verify] {item.page}: {'PASS' if ok else 'FAIL'} ({detail})")
        else:
            results[item.page] = "PASS (HTTP markers only)"
            print(f"  [verify] {item.page}: PASS (HTTP markers only)")
    return results


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Unified guarded deploy for NPCWoods landing pages. DRY-RUN BY DEFAULT.")
    parser.add_argument("--pages", action="append",
                        help="comma-separated page paths relative to landing-pages/ (repeatable)")
    parser.add_argument("--manifest", help="text file of page paths, one per line, # comments OK")
    parser.add_argument("--live", action="store_true",
                        help="actually deploy (still requires the confirmation phrase)")
    parser.add_argument("--confirm-live-deploy", dest="confirmation", default=None,
                        help='non-interactive confirmation: "CHRIS APPROVED LIVE DEPLOY"')
    parser.add_argument("--verify-only", action="store_true",
                        help="skip upload; just run live verification for the pages")
    parser.add_argument("--remote-diff", action="store_true",
                        help="dry-run extra: read-only SFTP checksum diff vs remote")
    parser.add_argument("--skip-flush", action="store_true", help="live mode: skip WP stub touch")
    parser.add_argument("--skip-verify", action="store_true", help="live mode: skip post-deploy verification")
    args = parser.parse_args((argv or sys.argv)[1:])

    if args.live and args.verify_only:
        print("[err] --live and --verify-only are mutually exclusive", file=sys.stderr)
        return 2

    try:
        pages = collect_pages(args)
    except (ValueError, OSError) as e:
        print(f"[err] {e}", file=sys.stderr)
        return 2
    if not pages:
        parser.print_usage()
        print("[err] no pages given — use --pages and/or --manifest", file=sys.stderr)
        return 2

    try:
        plan = build_plan(pages)
    except RuntimeError as e:
        print(f"[blocked] {e}", file=sys.stderr)
        return 2

    stub_table = load_stub_table()

    # ---- verify-only -----------------------------------------------------
    if args.verify_only:
        print(f"[verify-only] checking {len(plan)} live page(s), no upload")
        results = run_verification(plan)
        failed = [p for p, r in results.items() if r.startswith("FAIL")]
        print(f"\n[done] {len(plan) - len(failed)}/{len(plan)} pages passed verification")
        return 1 if failed else 0

    print_plan(plan, stub_table)

    # ---- dry-run (default) ----------------------------------------------
    if not args.live:
        if args.remote_diff:
            env = load_env()
            sftp, transport = sftp_connect(env)
            try:
                remote_diff(sftp, plan)
            finally:
                sftp.close()
                transport.close()
        print(f'\n[dry-run] nothing uploaded. Add --live (and Chris\'s confirmation phrase) to deploy.')
        return 0

    # ---- live ------------------------------------------------------------
    if not confirm_live(args.confirmation):
        return 2

    env = load_env()
    print(f"\n[sftp] connecting to {env['SFTP_HOST']}:{env['SFTP_PORT']}")
    sftp, transport = sftp_connect(env)
    uploaded, backups, failed_uploads = [], {}, []
    try:
        for item in plan:
            try:
                bak = sftp_backup(sftp, item.remote)
                backups[item.page] = bak
                if bak:
                    print(f"  [backup] {item.remote} -> {bak}")
                else:
                    print(f"  [backup] {item.remote} did not exist (first deploy)")
                sftp_mkdirs(sftp, posixpath.dirname(item.remote))
                sftp.put(str(item.local), item.remote)
                uploaded.append(item)
                print(f"  [up] {item.remote}")
            except Exception as e:  # noqa: BLE001 — keep going, report at the end
                failed_uploads.append((item.page, str(e)))
                print(f"  [err] {item.page}: {e}")
    finally:
        sftp.close()
        transport.close()

    # cache flush
    flush_results = {}
    if not args.skip_flush:
        auth = wp_auth(env)
        for item in uploaded:
            stub = stub_id_for_page(item.page, stub_table)
            if not stub:
                flush_results[item.page] = "no stub (new URL, nothing cached)"
                print(f"  [cache] {item.page}: no stub — new URL, nothing cached")
                continue
            ok = touch_stub(auth, stub)
            flush_results[item.page] = f"stub {stub} {'flushed' if ok else 'FAILED — flush manually'}"
            print(f"  [cache] {item.page}: stub {stub} {'ok' if ok else 'FAILED — flush manually'}")
            time.sleep(0.4)

    # verification
    verify_results = {}
    if uploaded and not args.skip_verify:
        print("\n[verify] waiting 10s for cache to settle, then checking live URLs")
        time.sleep(10)
        verify_results = run_verification(uploaded)

    # ---- final report ------------------------------------------------------
    print("\n" + "=" * 70)
    print(f"DEPLOY REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  uploaded: {len(uploaded)}/{len(plan)}")
    for item in uploaded:
        bak = backups.get(item.page)
        print(f"    {item.page}")
        print(f"      remote:  {item.remote}")
        print(f"      backup:  {bak if bak else '(none — first deploy)'}")
        print(f"      cache:   {flush_results.get(item.page, 'skipped')}")
        print(f"      verify:  {verify_results.get(item.page, 'skipped')}")
    for page, err in failed_uploads:
        print(f"    {page}: UPLOAD FAILED — {err}")
    failed_verify = [p for p, r in verify_results.items() if r.startswith("FAIL")]
    ok = not failed_uploads and not failed_verify
    print(f"  result: {'ALL GOOD' if ok else 'ATTENTION NEEDED'}")
    print("=" * 70)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
