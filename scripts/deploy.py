#!/usr/bin/env python3
"""Unified guarded deploy tool for NPCWoods.com landing pages.

Supersedes the dated one-off deploy scripts (see scripts/README-deploy.md).
Pipeline per page:

  0. Counter + git guard (before .env loads, for --live and --remote-diff):
     only the one folder KITCHEN-COUNTERS.json allows, on main, clean,
     fetched, and HEAD == origin/main. No bypass flag.
  1. Local safety checks that BLOCK: no tracking pixels or Ahrefs, no banned
     words (appointment, physician, doctor, insurance, MD), no facts drift.
  2. Homepage baseline snapshot (https://npcwoods.com/?n=1: status, bytes,
     sha256, <title>) before anything is uploaded.
  3. Timestamped remote backup -> content-output/deploy-backups/<date>/.
  4. SFTP upload (Rocket.net, key auth):
     landing-pages/{path}/index.html -> public_html/{path}/index.html.
  5. Rocket CDN cache purge for exactly the uploaded URLs
     (POST https://api.rocket.net/v1/sites/354775/cache/purge).
  6. Live verification (clean public URL, no query string; full Playwright
     tracking run if playwright is installed), then the homepage is
     re-checked against the step-2 baseline.

HOST: npcwoods.com moved from GoDaddy Managed WordPress to Rocket.net on
2026-10-26 (site id 354775). GoDaddy (html/ prefix, password SFTP, WP stub
touch for Varnish) is kept below as commented fallback only. Do not use it
since 2026-10-26.

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
import re
import subprocess
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
SCRIPT_ROOT = Path(__file__).resolve().parent.parent  # where this script file lives; tests cannot move it
KITCHEN = Path("/Users/macmini/Desktop/Chris-HQ")
COUNTER_CARD = KITCHEN / "KITCHEN-COUNTERS.json"
GIT_TIMEOUT_S = 90
LANDING_DIR = "landing-pages"
# Rocket.net web root, relative to the SFTP home (/home/<user>/public_html).
REMOTE_PREFIX = "public_html"
# REMOTE_PREFIX = "html"  # GoDaddy Managed WP — do not use since 2026-10-26
SITE = "https://npcwoods.com"
HOMEPAGE_CHECK_URL = f"{SITE}/?n=1"
ROCKET_API = "https://api.rocket.net/v1"
ROCKET_SITE_ID_DEFAULT = "354775"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

LIVE_DEPLOY_CONFIRMATION = "CHRIS APPROVED LIVE DEPLOY"

# Kitchen HTML must not contain these. Health/city/search-safe plates keep
# GTM, GA, Ads, tracking.js, and Meta out of the file. The dining-room plugin
# owns the site pixel. Homepage PHP is the exception. "insurance" is a Chris
# hard rule for marketing surfaces.
FORBIDDEN_MARKERS = [
    "connect.facebook.net",
    "facebook.com/tr",
    'fbq("init"',
    "fbq('init'",
    "googletagmanager.com",
    "google-analytics.com",
    "googleadservices.com",
    "doubleclick.net",
    "/tracking.js",
    "analytics.ahrefs.com",
    "ahrefs.com/analytics",
]
WARN_IF_MISSING = []
WARN_IF_PRESENT = []  # "insurance" now BLOCKS via the banned-word check
INTENTIONAL_NO_TRACKING_PAGES = {"pay"}

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
    "/dental-pain/search-safe/": 995,
    "/online-urgent-care-info/": 998,
    "/online-urgent-care-info/search-safe/": 999,
    "/pharmacy/": 334,
    "/pharmacy-partners/": 335,
    "/pay/": 674,
    "/cold-sore-treatment/": 835,
    "/uti-treatment/charlotte-nc/": 284,
    "/uti-treatment/atlanta-ga/": 264,
    "/what-is-async-telemedicine/": 892,
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


def load_practice_facts():
    """scripts/practice_facts.py from this script's own folder."""
    import importlib.util
    path = Path(__file__).resolve().parent / "practice_facts.py"
    spec = importlib.util.spec_from_file_location("npcw_practice_facts", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def deploy_verify_report_dir() -> Path:
    return hq_root() / "content-output" / "reports" / "deploy-verify"


def verification_status_text(result) -> str:
    return str(result)


def verification_result_label(result) -> str:
    text = verification_status_text(result)
    if text.startswith("PASS"):
        return "PASS"
    if text.startswith("FAIL"):
        return "FAIL"
    return text or "unknown"


def verification_marker_tracking_text(result) -> str:
    detail = getattr(result, "marker_tracking_status", "")
    return detail or verification_status_text(result)


def verification_screenshot_paths(result) -> list[str]:
    return [str(path) for path in (getattr(result, "screenshots", []) or [])]


def md_cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def write_verification_proof_report(
    plan: list[PagePlan],
    results: dict[str, object],
    mode: str,
    now: datetime | None = None,
) -> Path:
    now = now or datetime.now()
    out_dir = deploy_verify_report_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"deploy-verify-{now.strftime('%Y%m%d-%H%M%S')}.md"

    lines = [
        "# Deploy Verification Proof",
        "",
        f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Mode: {mode}",
        "",
        "## Page Results",
        "",
        "| Page | URL | Result | Marker/tracking status | Screenshots |",
        "|---|---|---|---|---|",
    ]
    for item in plan:
        result = results.get(item.page, "skipped")
        screenshots = verification_screenshot_paths(result)
        screenshot_text = "<br>".join(screenshots) if screenshots else "Screenshots: none"
        lines.append(
            f"| `{md_cell(item.page)}` | {md_cell(item.url)} | "
            f"{md_cell(verification_result_label(result))} | "
            f"{md_cell(verification_marker_tracking_text(result))} | "
            f"{md_cell(screenshot_text)} |"
        )
    path.write_text("\n".join(lines) + "\n")
    return path


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


@dataclass
class VerificationResult:
    status: str
    marker_tracking_status: str = ""
    screenshots: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        if not self.marker_tracking_status:
            return self.status
        if self.status.startswith("FAIL:"):
            return self.status
        return f"{self.status} ({self.marker_tracking_status})"

    def startswith(self, prefix: str) -> bool:
        return str(self).startswith(prefix)


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

def build_plan(pages: list[str], strict: bool = True) -> list[PagePlan]:
    """strict=True (dry-run, remote-diff, live): banned words and facts drift
    block. strict=False (--verify-only, no upload): they are shown as warnings."""
    plan, problems = [], []
    facts = load_practice_facts()
    ledger_path = ROOT / "facts" / "practice.json"
    try:
        ledger = facts.load_ledger(ledger_path)
    except (OSError, ValueError, KeyError) as e:
        raise RuntimeError(f"facts ledger unreadable at {ledger_path}: {e}")
    allowed_phrases = ledger.get("banned_word_allowed_phrases", [])
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
        try:
            rel = local.resolve().relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            rel = str(local)
        content_problems = [f"banned word {h}" for h in facts.banned_word_hits(html, allowed_phrases)]
        content_problems += [f"facts drift: {d}" for d in facts.page_drift(rel, html, ledger)]
        for cp in content_problems:
            if strict:
                problems.append(f"{page}: {cp} — refusing to deploy")
            else:
                item.warnings.append(cp)
        plan.append(item)
    if problems:
        raise RuntimeError("plan blocked:\n  " + "\n  ".join(problems))
    return plan


def print_plan(plan: list[PagePlan], stub_table: dict, head: str | None = None) -> None:
    print(f"Deploy plan — {len(plan)} page(s):")
    if head:
        print(f"  from {SCRIPT_ROOT} @ main {head}")
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


def confirm_live(confirmation: str | None, prompt=None) -> bool:
    """True only when Chris's confirmation phrase is supplied — via flag or
    typed interactively. Anything else blocks the deploy."""
    if confirmation == LIVE_DEPLOY_CONFIRMATION:
        return True
    if confirmation is not None:
        print(f"[blocked] wrong confirmation phrase. Expected exactly: {LIVE_DEPLOY_CONFIRMATION}",
              file=sys.stderr)
        return False
    if prompt is None and not sys.stdin.isatty():
        print(f'[blocked] non-interactive run. Re-run with --confirm-live-deploy '
              f'"{LIVE_DEPLOY_CONFIRMATION}" after Chris explicitly approves.', file=sys.stderr)
        return False
    prompt = prompt or input  # looked up at call time so tests can patch builtins.input
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
    """Rocket.net SFTP: key auth only (Rocket has no SFTP passwords).
    Host key must already be in ~/.ssh/known_hosts (RejectPolicy).
    ONE attempt. If it fails, stop and tell Chris; never retry in a loop."""
    import os
    import paramiko  # lazy: dry-run must never need it
    client = paramiko.SSHClient()
    client.load_host_keys(os.path.expanduser("~/.ssh/known_hosts"))
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(
        env["ROCKET_SFTP_HOST"],
        port=int(env.get("ROCKET_SFTP_PORT") or 22),
        username=env["ROCKET_SFTP_USER"],
        key_filename=env["ROCKET_SFTP_KEY_PATH"],
        allow_agent=False, look_for_keys=False,
        timeout=60, banner_timeout=60, auth_timeout=60,
    )
    return client.open_sftp(), client


# GoDaddy fallback — do not use since 2026-10-26 (npcwoods.com is on Rocket.net).
# def sftp_connect_godaddy(env):
#     import paramiko
#     transport = paramiko.Transport((env["SFTP_HOST"], int(env["SFTP_PORT"])))  # 1085255.us30.ssh.myftpupload.com
#     transport.banner_timeout = 60
#     transport.auth_timeout = 60
#     transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
#     return paramiko.SFTPClient.from_transport(transport), transport


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
# Rocket CDN cache purge (replaces the GoDaddy WP stub touch since 2026-10-26)
# --------------------------------------------------------------------------
# Rocket's Cloudflare blocks Python urllib, so these calls go through curl.
# Credentials go to curl on stdin (never argv, never printed).

def _curl_json(url: str, *, method: str = "GET", body: dict | None = None,
               token: str | None = None, timeout: int = 60) -> tuple[int, dict | None]:
    """curl with its whole config (URL, headers, token) on stdin and the JSON
    body in a 0600 temp file that is deleted right after. Nothing secret
    reaches argv or stdout."""
    import os
    import tempfile
    cfg = [f'url = "{url}"', f'request = "{method}"', "silent", "show-error",
           'header = "Content-Type: application/json"',
           'header = "Accept: application/json"',
           'write-out = "\\n%{http_code}"', f"max-time = {timeout}"]
    if token:
        cfg.append(f'header = "Authorization: Bearer {token}"')
    body_path = None
    try:
        if body is not None:
            fd, body_path = tempfile.mkstemp(prefix="rocket-", suffix=".json")
            with os.fdopen(fd, "w") as fh:
                json.dump(body, fh)
            cfg.append(f'data-binary = "@{body_path}"')
        proc = subprocess.run(["curl", "-K", "-"], input="\n".join(cfg) + "\n",
                              capture_output=True, text=True, timeout=timeout + 10)
    finally:
        if body_path:
            os.unlink(body_path)
    text, _, code = proc.stdout.rpartition("\n")
    try:
        status = int(code.strip())
    except ValueError:
        return 0, None
    try:
        return status, (json.loads(text) if text.strip() else None)
    except json.JSONDecodeError:
        return status, None


def rocket_token(env: dict) -> str | None:
    status, payload = _curl_json(f"{ROCKET_API}/login", method="POST", body={
        "username": env["ROCKET_API_USERNAME"], "password": env["ROCKET_API_PASSWORD"]})
    if status != 200 or not payload or not payload.get("token"):
        print(f"  [cache] Rocket API login failed (HTTP {status}). Purge manually in the Rocket panel.")
        return None
    return payload["token"]


def rocket_purge(env: dict, urls: list[str]) -> bool:
    """Purge exactly these URLs from Rocket's CDN. Not purge_everything."""
    if not urls:
        return True
    token = rocket_token(env)
    if not token:
        return False
    site_id = env.get("ROCKET_SITE_ID") or ROCKET_SITE_ID_DEFAULT
    status, payload = _curl_json(f"{ROCKET_API}/sites/{site_id}/cache/purge",
                                 method="POST", body={"files": urls}, token=token)
    ok = status == 200 and bool(payload is None or payload.get("success", True))
    print(f"  [cache] Rocket purge {len(urls)} URL(s): {'ok' if ok else f'FAILED (HTTP {status})'}")
    return ok


# --------------------------------------------------------------------------
# Homepage baseline (must be unchanged by any page deploy)
# --------------------------------------------------------------------------

def homepage_snapshot(url: str = HOMEPAGE_CHECK_URL) -> dict:
    """Read-only GET via curl. Returns status, bytes, sha256, title."""
    proc = subprocess.run(["curl", "-s", "-A", UA, "--max-time", "45", url],
                          capture_output=True, timeout=60)
    head = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-A", UA,
                           "--max-time", "45", url], capture_output=True, text=True, timeout=60)
    body = proc.stdout or b""
    m = re.search(rb"<title>([^<]*)</title>", body)
    return {
        "status": int(head.stdout or 0),
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "title": m.group(1).decode("utf-8", "replace") if m else "",
        "custom_hero": b'class="hero' in body and b"wp-site-blocks" not in body,
    }


def homepage_problem(before: dict, after: dict) -> str | None:
    if after["status"] != 200:
        return f"homepage status {after['status']}"
    if not after["custom_hero"]:
        return "homepage lost the custom PHP template (hero missing / wp-site-blocks present)"
    if after["title"] != before["title"]:
        return f"homepage title changed: {before['title']!r} -> {after['title']!r}"
    if after["sha256"] != before["sha256"]:
        return (f"homepage sha changed {before['sha256'][:12]} -> {after['sha256'][:12]} "
                f"({before['bytes']} -> {after['bytes']} bytes)")
    return None


# --------------------------------------------------------------------------
# GoDaddy WP stub-touch cache flush — do not use since 2026-10-26.
# Kept (uncalled) as fallback reference only.
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
    """Clean-URL GET: the ordinary public address patients hit, no query string.
    Cache-bust (`?v=` / `?n=1`) can lie while this URL is still an empty WP
    shell. Returns None on pass, else a problem description."""
    url = item.url
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
        if item.page in INTENTIONAL_NO_TRACKING_PAGES:
            return None
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


def run_verification(plan: list[PagePlan]) -> dict[str, VerificationResult]:
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
            results[item.page] = VerificationResult(f"FAIL: {problem}", problem)
            print(f"  [verify] {item.page}: FAIL ({problem})")
            continue
        if have_playwright:
            try:
                tracking = verify_tracking_playwright(item)
                ok, detail = tracking[0], tracking[1]
                screenshots = list(tracking[2]) if len(tracking) > 2 else []
            except Exception as e:  # noqa: BLE001 — verification must never crash the report
                ok, detail, screenshots = False, f"playwright error: {e}", []
            results[item.page] = VerificationResult("PASS" if ok else "FAIL", detail, screenshots)
            print(f"  [verify] {item.page}: {'PASS' if ok else 'FAIL'} ({detail})")
        else:
            results[item.page] = VerificationResult("PASS", "HTTP markers only")
            print(f"  [verify] {item.page}: PASS (HTTP markers only)")
    return results


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def kitchen_counter_block(script_root: Path | None = None) -> str | None:
    """Refuse unless this script lives in the one folder KITCHEN-COUNTERS.json allows."""
    root = (SCRIPT_ROOT if script_root is None else script_root).resolve()
    if not COUNTER_CARD.is_file():
        return f"[blocked] Missing kitchen counter card: {COUNTER_CARD}"
    try:
        card = json.loads(COUNTER_CARD.read_text(encoding="utf-8"))
        plating = [row for row in card["counters"] if row.get("plate") is True]
    except (OSError, ValueError, KeyError, TypeError) as e:
        return f"[blocked] Kitchen counter card unreadable: {e}"
    if len(plating) != 1:
        return "[blocked] Kitchen counter card must name exactly one folder to plate from."
    allowed = (KITCHEN / plating[0]["folder"]).resolve()
    if root != allowed:
        return (f"[blocked] This copy is not the kitchen counter. "
                f"Plate only from {allowed}. This script is in {root}.")
    return None


def _git(repo: Path, *args: str, timeout: int = GIT_TIMEOUT_S) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          timeout=timeout, stdin=subprocess.DEVNULL)


IGNORED_DIRTY_PREFIXES = ("deploy-backups/", "content-output/deploy-backups/")


def git_state_block(repo: Path) -> tuple[str | None, str | None]:
    """(problem, head_sha). Refuse unless repo is on main, clean, freshly
    fetched, and HEAD == origin/main. No bypass flag on purpose."""
    try:
        top = _git(repo, "rev-parse", "--show-toplevel")
        if top.returncode != 0:
            return f"[blocked] {repo} is not a git checkout.", None
        if Path(top.stdout.strip()).resolve() != repo.resolve():
            return f"[blocked] git toplevel {top.stdout.strip()} is not {repo}.", None
        branch = _git(repo, "symbolic-ref", "--short", "-q", "HEAD").stdout.strip()
        if branch != "main":
            return f"[blocked] Branch is {branch or '(detached HEAD)'}, not main. Plate only from main.", None
        status = _git(repo, "status", "--porcelain", "--untracked-files=all")
        if status.returncode != 0:
            return f"[blocked] git status failed: {status.stderr.strip()}", None
        dirty = []
        for line in status.stdout.splitlines():
            path = line[3:].split(" -> ")[-1].strip('"')
            if not path.startswith(IGNORED_DIRTY_PREFIXES):
                dirty.append(line)
        if dirty:
            shown = "\n    ".join(dirty[:15])
            more = f"\n    … and {len(dirty) - 15} more" if len(dirty) > 15 else ""
            return (f"[blocked] Uncommitted changes. Commit + merge to main first, then plate that SHA:\n"
                    f"    {shown}{more}"), None
        fetch = _git(repo, "fetch", "--quiet", "origin", "main")
        if fetch.returncode != 0:
            return f"[blocked] git fetch origin main failed: {fetch.stderr.strip()[:300]}", None
        head = _git(repo, "rev-parse", "HEAD").stdout.strip()
        remote = _git(repo, "rev-parse", "FETCH_HEAD").stdout.strip()
        if not head or head != remote:
            counts = _git(repo, "rev-list", "--left-right", "--count", f"HEAD...{remote}").stdout.split()
            ahead, behind = (counts + ["?", "?"])[:2]
            return (f"[blocked] HEAD {head[:12]} is not origin/main {remote[:12]} "
                    f"(ahead {ahead}, behind {behind}). Pull main first."), None
        return None, head
    except subprocess.TimeoutExpired:
        return "[blocked] git timed out (iCloud placeholder or network?). Nothing uploaded.", None
    except FileNotFoundError:
        return "[blocked] git is not installed.", None


def preflight_block() -> tuple[str | None, str | None]:
    """Counter + git guard. Runs before .env loads. Returns (problem, head_sha)."""
    blocked = kitchen_counter_block()
    if blocked:
        return blocked, None
    if ROOT.resolve() != SCRIPT_ROOT.resolve():
        return f"[blocked] Pages folder {ROOT} is not the script folder {SCRIPT_ROOT}.", None
    return git_state_block(SCRIPT_ROOT)


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
    parser.add_argument("--skip-flush", action="store_true", help="live mode: skip Rocket CDN purge")
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
        plan = build_plan(pages, strict=not args.verify_only)
    except RuntimeError as e:
        print(f"[blocked] {e}", file=sys.stderr)
        return 2

    stub_table = load_stub_table()

    # ---- verify-only -----------------------------------------------------
    if args.verify_only:
        print(f"[verify-only] checking {len(plan)} live page(s), no upload")
        results = run_verification(plan)
        proof_report = write_verification_proof_report(plan, results, mode="verify-only")
        failed = [p for p, r in results.items() if r.startswith("FAIL")]
        print(f"[proof] wrote verification report: {proof_report}")
        print(f"\n[done] {len(plan) - len(failed)}/{len(plan)} pages passed verification")
        return 1 if failed else 0

    # ---- counter + git guard: before .env loads, before any server contact --
    head = None
    if args.live or args.remote_diff:
        blocked, head = preflight_block()
        if blocked:
            print(blocked, file=sys.stderr)
            return 2

    print_plan(plan, stub_table, head)
    print(f"  target: Rocket.net site {ROCKET_SITE_ID_DEFAULT} SFTP (key auth), web root {REMOTE_PREFIX}/")
    print(f"  after upload: Rocket CDN purge of {len(plan)} URL(s): " + ", ".join(i.url for i in plan))

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

    print(f"\n[about to upload] main @ {head} from {SCRIPT_ROOT}")
    for item in plan:
        print(f"  {item.local.relative_to(ROOT)} -> {item.remote}  (sha256 {item.sha256[:12]}…)")
    env = load_env()
    missing = [k for k in ("ROCKET_SFTP_HOST", "ROCKET_SFTP_USER", "ROCKET_SFTP_KEY_PATH") if not env.get(k)]
    if missing:
        print(f"[blocked] .env is missing {', '.join(missing)}. Nothing uploaded.", file=sys.stderr)
        return 2
    homepage_before = homepage_snapshot()
    print(f"[homepage baseline] {homepage_before['status']} {homepage_before['bytes']:,} bytes "
          f"sha256 {homepage_before['sha256'][:12]}… title {homepage_before['title']!r}")
    if homepage_before["status"] != 200 or not homepage_before["custom_hero"]:
        print("[blocked] homepage is not healthy BEFORE deploy. Nothing uploaded.", file=sys.stderr)
        return 2
    print(f"\n[sftp] connecting to Rocket {env['ROCKET_SFTP_HOST']}:{env.get('ROCKET_SFTP_PORT') or 22}")
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

    # cache flush: Rocket CDN purge of exactly the uploaded URLs.
    flush_results = {}
    if not args.skip_flush and uploaded:
        ok = rocket_purge(env, [item.url for item in uploaded])
        for item in uploaded:
            flush_results[item.page] = "Rocket purge ok" if ok else "Rocket purge FAILED — purge in Rocket panel"

    # GoDaddy fallback — do not use since 2026-10-26.
    # GoDaddy WPaaS ran a FULL-SITE ban on any publish->publish stub update,
    # so one stub touch flushed every page. Kept disabled for reference.
    if False:  # noqa: SIM108 — GoDaddy stub touch, do not use since 2026-10-26
        auth = wp_auth(env)
        flushed_by = None
        for item in uploaded:
            stub = stub_id_for_page(item.page, stub_table)
            if not stub:
                flush_results[item.page] = "no stub (new URL, nothing cached)"
                print(f"  [cache] {item.page}: no stub — new URL, nothing cached")
                continue
            if flushed_by is not None:
                flush_results[item.page] = f"covered by full-site flush via stub {flushed_by}"
                print(f"  [cache] {item.page}: covered by full-site flush via stub {flushed_by}")
                continue
            ok = touch_stub(auth, stub)
            if ok:
                flushed_by = stub
            flush_results[item.page] = f"stub {stub} {'flushed' if ok else 'FAILED — flush manually'}"
            print(f"  [cache] {item.page}: stub {stub} {'ok' if ok else 'FAILED — flush manually'}")
            time.sleep(0.4)

    # verification
    verify_results = {}
    proof_report = None
    if uploaded and not args.skip_verify:
        print("\n[verify] waiting 10s for cache to settle, then checking live URLs")
        time.sleep(10)
        verify_results = run_verification(uploaded)
        proof_report = write_verification_proof_report(uploaded, verify_results, mode="live-post-deploy")
        print(f"  [proof] wrote verification report: {proof_report}")

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
    if proof_report:
        print(f"  proof:   {proof_report}")
    for page, err in failed_uploads:
        print(f"    {page}: UPLOAD FAILED — {err}")
    failed_verify = [p for p, r in verify_results.items() if r.startswith("FAIL")]
    homepage_after = homepage_snapshot()
    hp_problem = homepage_problem(homepage_before, homepage_after)
    print(f"  homepage: {'unchanged vs baseline' if not hp_problem else 'CHANGED — ' + hp_problem}")
    ok = not failed_uploads and not failed_verify and not hp_problem
    print(f"  result: {'ALL GOOD' if ok else 'ATTENTION NEEDED'}")
    print("=" * 70)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
