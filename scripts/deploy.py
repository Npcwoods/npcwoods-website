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

ASSETS (--asset assets/<path>, repeatable; added 2026-11-02): repo files under
assets/ go to public_html/assets/<path> over the same SFTP session, BEFORE any
page. NEW files only: if the remote file already exists it is never
overwritten (reported "matching" when its sha equals the kitchen copy,
otherwise SKIPPED, and then no page in that run is uploaded because pages may
point at it). Uploaded/matching assets are purged and their public URL sha
verified exactly like pages. Same guards; nothing is ever deleted.

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
  python3 scripts/deploy.py --pages learn/ear-infection \
      --asset assets/img/share/learn-ear-infection-v2-1200x630.jpg
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
ASSETS_DIR = "assets"  # --asset files must live under <repo>/assets/
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
class AssetPlan:
    rel: str                      # repo-relative, e.g. assets/img/share/x-1200x630.jpg
    local: Path                   # absolute local file
    remote: str                   # public_html/assets/...
    url: str                      # https://npcwoods.com/assets/...
    size: int = 0
    sha256: str = ""


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


def normalize_asset(raw: str) -> str:
    """Repo-relative path under assets/ (leading slash tolerated). Refuses
    anything else, traversal, and directories-by-name."""
    p = raw.strip().lstrip("/")
    parts = p.split("/")
    if ".." in parts or "." in parts or "" in parts:
        raise ValueError(f"refusing odd or traversing asset path: {raw!r}")
    if parts[0] != ASSETS_DIR or len(parts) < 2:
        raise ValueError(f"--asset must be a file under {ASSETS_DIR}/ in the repo, got {raw!r}")
    return p


def collect_assets(args) -> list[str]:
    seen, out = set(), []
    for chunk in getattr(args, "asset", None) or []:
        for r in chunk.split(","):
            if not r.strip():
                continue
            a = normalize_asset(r)
            if a not in seen:
                seen.add(a)
                out.append(a)
    return out


def build_asset_plan(assets: list[str]) -> list[AssetPlan]:
    plan, problems = [], []
    base = (ROOT / ASSETS_DIR).resolve()
    for rel in assets:
        local = ROOT / rel
        item = AssetPlan(rel=rel, local=local, remote=f"{REMOTE_PREFIX}/{rel}", url=f"{SITE}/{rel}")
        try:
            local.resolve().relative_to(base)
        except ValueError:
            problems.append(f"{rel}: resolves outside {ASSETS_DIR}/ (symlink?)")
            continue
        if not local.is_file():
            problems.append(f"{rel}: local file missing: {local}")
            continue
        data = local.read_bytes()
        item.size = len(data)
        item.sha256 = hashlib.sha256(data).hexdigest()
        plan.append(item)
    if problems:
        raise RuntimeError("asset plan blocked:\n  " + "\n  ".join(problems))
    return plan


def print_asset_plan(assets: list[AssetPlan]) -> None:
    if not assets:
        return
    print(f"Asset plan — {len(assets)} file(s) (new files only, never overwritten):")
    for a in assets:
        print(f"  [asset] {a.rel}")
        print(f"       -> {a.remote}  ({a.size:,} bytes, sha256 {a.sha256[:12]}…)")


def check_remote_assets(sftp, assets: list[AssetPlan]) -> dict[str, str]:
    """Read-only. {rel: 'new' | 'matching' | 'differs <sha12> (<bytes> bytes)'}"""
    out = {}
    for a in assets:
        try:
            with sftp.file(a.remote, "rb") as rf:
                data = rf.read()
        except IOError:
            out[a.rel] = "new"
            continue
        sha = hashlib.sha256(data).hexdigest()
        out[a.rel] = "matching" if sha == a.sha256 else f"differs {sha[:12]} ({len(data):,} bytes)"
    return out


def upload_assets(sftp, assets: list[AssetPlan], state: dict[str, str]) -> dict[str, str]:
    """Upload only assets whose remote state is 'new'. Never overwrites, never deletes.
    Returns {rel: 'uploaded' | 'matching (already live, not re-uploaded)' |
    'SKIPPED: ...' | 'FAILED: ...'}"""
    results = {}
    for a in assets:
        st = state.get(a.rel, "")
        if st == "matching":
            results[a.rel] = "matching (already on server, not re-uploaded)"
            print(f"  [asset] {a.remote}: already on server with matching sha, not re-uploaded")
            continue
        if st != "new":
            results[a.rel] = f"SKIPPED: remote exists and {st}; not overwritten"
            print(f"  [asset] {a.remote}: SKIPPED, remote exists and {st}; not overwritten", file=sys.stderr)
            continue
        try:
            sftp_mkdirs(sftp, posixpath.dirname(a.remote))
            sftp.put(str(a.local), a.remote)
            size = sftp.stat(a.remote).st_size
            if size != a.size:
                results[a.rel] = f"FAILED: remote size {size} != local {a.size}"
                print(f"  [err] {a.remote}: {results[a.rel]}")
                continue
            results[a.rel] = "uploaded"
            print(f"  [up] {a.remote} ({size:,} bytes)")
        except Exception as e:  # noqa: BLE001 — report at the end
            results[a.rel] = f"FAILED: {e}"
            print(f"  [err] {a.rel}: {e}")
    return results



# --------------------------------------------------------------------------
# --file: a FIXED allow-list of non-page files (homepage template, four
# mu-plugins, the menu script, llms*.txt, the shared header/footer snippets).
# Chris approved adding this to the house tools on 2026-11-02 13:59 ET:
# "Add homepage/menu/footer/llms.txt upload to the house tools with backups".
# Overwrite in place only: the server file must already exist. Never creates,
# never deletes, never renames. One PHP file per run.
# --------------------------------------------------------------------------

MU_PLUGINS_REMOTE = f"{REMOTE_PREFIX}/wp-content/mu-plugins"
HOMEPAGE_TEMPLATE_REMOTE = f"{REMOTE_PREFIX}/wp-content/themes/twentytwentyfour/page-npcwoods-home.php"
FILE_TARGETS = {
    # repo-relative path -> server path (relative to the SFTP home)
    "homepage/page-npcwoods-home.php": HOMEPAGE_TEMPLATE_REMOTE,
    "php/npcwoods-compliance-footer.php": f"{MU_PLUGINS_REMOTE}/npcwoods-compliance-footer.php",
    "php/npcwoods-eeat.php": f"{MU_PLUGINS_REMOTE}/npcwoods-eeat.php",
    "php/npcwoods-faq-schema.php": f"{MU_PLUGINS_REMOTE}/npcwoods-faq-schema.php",
    "php/npcwoods-sitemap-hygiene.php": f"{MU_PLUGINS_REMOTE}/npcwoods-sitemap-hygiene.php",
    "php/npcwoods-robots-extras.php": f"{MU_PLUGINS_REMOTE}/npcwoods-robots-extras.php",
    # Route map for static landing pages. Chris OK'd 2026-11-04 13:32 ET ("Tidy and push it live").
    "php/npcwoods-static-pages.php": f"{MU_PLUGINS_REMOTE}/npcwoods-static-pages.php",
    "assets/js/npc-menu.js": f"{REMOTE_PREFIX}/assets/js/npc-menu.js",
    "llms.txt": f"{REMOTE_PREFIX}/llms.txt",
    "llms-full.txt": f"{REMOTE_PREFIX}/llms-full.txt",
    "html/shared/footer-snippet.html": f"{REMOTE_PREFIX}/shared/footer-snippet.html",
    "html/shared/header-snippet.html": f"{REMOTE_PREFIX}/shared/header-snippet.html",
}
# Files whose public URL serves the exact bytes (sha-checked after purge).
FILE_PUBLIC_URLS = {
    "assets/js/npc-menu.js": f"{SITE}/assets/js/npc-menu.js",
    "llms.txt": f"{SITE}/llms.txt",
    "llms-full.txt": f"{SITE}/llms-full.txt",
    "html/shared/footer-snippet.html": f"{SITE}/shared/footer-snippet.html",
    "html/shared/header-snippet.html": f"{SITE}/shared/header-snippet.html",
}
# Rendered pages to check after a file that changes PHP output (or that the
# homepage template reads, like the shared footer snippet). The homepage is
# always checked; a PHP error or a lost template restores the backup.
# WP_RENDERED_CHECK_URL: a page WordPress itself renders through the block
# theme (date archive), so mu-plugin output (compliance footer, schema) shows up.
WP_RENDERED_CHECK_URL = f"{SITE}/2026/"
RENDER_CHECK_URLS = {
    "homepage/page-npcwoods-home.php": [f"{SITE}/"],
    "php/npcwoods-compliance-footer.php": [f"{SITE}/", WP_RENDERED_CHECK_URL],
    "php/npcwoods-eeat.php": [f"{SITE}/", WP_RENDERED_CHECK_URL],
    "php/npcwoods-faq-schema.php": [f"{SITE}/", WP_RENDERED_CHECK_URL],
    "php/npcwoods-sitemap-hygiene.php": [f"{SITE}/", WP_RENDERED_CHECK_URL, f"{SITE}/page-sitemap.xml"],
    "php/npcwoods-robots-extras.php": [f"{SITE}/", f"{SITE}/robots.txt"],
    "php/npcwoods-static-pages.php": [f"{SITE}/", f"{SITE}/travel-telehealth-text-visit/",
                                      f"{SITE}/sick-on-vacation-text-visit/",
                                      f"{SITE}/out-of-town-medication-refill/",
                                      f"{SITE}/boise-county-text-visit/", f"{SITE}/baca-county-text-visit/"],
    "html/shared/footer-snippet.html": [f"{SITE}/"],
    "html/shared/header-snippet.html": [f"{SITE}/"],
}
PHP_ERROR_MARKERS = (
    b"Parse error", b"Fatal error", b"There has been a critical error",
    b"Warning</b>:", b"Notice</b>:", b"Deprecated</b>:",
)


@dataclass
class FilePlan:
    rel: str            # repo-relative, e.g. php/npcwoods-eeat.php
    local: Path
    remote: str
    size: int = 0
    sha256: str = ""

    @property
    def is_php(self) -> bool:
        return self.rel.endswith(".php")

    @property
    def is_mu_plugin(self) -> bool:
        return self.remote.startswith(MU_PLUGINS_REMOTE + "/")


def normalize_file(raw: str) -> str:
    p = raw.strip().lstrip("/")
    if ".." in p.split("/"):
        raise ValueError(f"refusing path traversal in --file: {raw!r}")
    if p not in FILE_TARGETS:
        allowed = ", ".join(sorted(FILE_TARGETS))
        raise ValueError(f"--file {raw!r} is not on the allow-list. Allowed: {allowed}")
    return p


def collect_files(args) -> list[str]:
    seen, out = set(), []
    for chunk in getattr(args, "file", None) or []:
        for r in chunk.split(","):
            if r.strip():
                f = normalize_file(r)
                if f not in seen:
                    seen.add(f)
                    out.append(f)
    return out


def php_function_names(php: str) -> set[str]:
    """Named PHP functions (same rule county_ship.py uses for mu-plugins)."""
    return set(re.findall(r"^\s*function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", php, re.M))


def php_lint(path: Path) -> str | None:
    """`php -l`; None when clean, else the reason. A missing php CLI blocks."""
    try:
        proc = subprocess.run(["php", "-l", str(path)], capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        return "php CLI not found; cannot lint"
    if proc.returncode != 0:
        return (proc.stdout + proc.stderr).strip()[:400]
    return None


def build_file_plan(files: list[str]) -> list[FilePlan]:
    plan, problems = [], []
    if sum(f.endswith(".php") for f in files) > 1:
        problems.append("one PHP file per run (ship the homepage template, verify, then each mu-plugin)")
    for rel in files:
        local = ROOT / rel
        item = FilePlan(rel=rel, local=local, remote=FILE_TARGETS[rel])
        try:
            local.resolve().relative_to(ROOT.resolve())
        except ValueError:
            problems.append(f"{rel}: resolves outside the repo (symlink?)")
            continue
        if not local.is_file():
            problems.append(f"{rel}: local file missing: {local}")
            continue
        data = local.read_bytes()
        item.size, item.sha256 = len(data), hashlib.sha256(data).hexdigest()
        if item.is_php:
            lint = php_lint(local)
            if lint:
                problems.append(f"{rel}: php -l failed: {lint}")
        else:
            lower = data.decode("utf-8", errors="replace").lower()
            for bad in FORBIDDEN_MARKERS:
                if bad.lower() in lower:
                    problems.append(f"{rel}: contains forbidden marker {bad!r}")
        plan.append(item)
    if problems:
        raise RuntimeError("file plan blocked:\n  " + "\n  ".join(problems))
    return plan


def print_file_plan(files: list[FilePlan]) -> None:
    if not files:
        return
    print(f"File plan — {len(files)} allow-listed file(s) (overwrite in place only, backup first):")
    for f in files:
        print(f"  [file] {f.rel}")
        print(f"       -> {f.remote}  ({f.size:,} bytes, sha256 {f.sha256[:12]}…)")


def remote_file_state(sftp, item: FilePlan) -> str:
    """Read-only. 'missing' | 'same' | 'differs <sha12> (<bytes> bytes)'."""
    try:
        with sftp.file(item.remote, "rb") as rf:
            data = rf.read()
    except IOError:
        return "missing"
    sha = hashlib.sha256(data).hexdigest()
    return "same" if sha == item.sha256 else f"differs {sha[:12]} ({len(data):,} bytes)"


def duplicate_function_problem(item: FilePlan, other_php: dict[str, str]) -> str | None:
    """other_php: {server filename: text} of every OTHER .php in mu-plugins.
    Refuse if the file we are about to upload defines a function another
    mu-plugin already defines (two definitions = site-wide 500)."""
    mine = php_function_names(item.local.read_text(errors="replace"))
    clashes = {}
    for name, text in other_php.items():
        both = mine & php_function_names(text)
        if both:
            clashes[name] = sorted(both)
    if clashes:
        return f"{item.rel}: functions already defined in other mu-plugins: {clashes}"
    return None


def read_other_mu_plugins(sftp, skip_remote: str) -> dict[str, str]:
    out = {}
    skip = posixpath.basename(skip_remote)
    for name in sftp.listdir(MU_PLUGINS_REMOTE):
        if not name.endswith(".php") or name == skip:
            continue
        with sftp.file(f"{MU_PLUGINS_REMOTE}/{name}", "rb") as rf:
            out[name] = rf.read().decode("utf-8", errors="replace")
    return out


def render_check(url: str, title_before: str | None = None) -> tuple[bool, str, dict]:
    """Clean-URL GET of a rendered page after a PHP/snippet change."""
    proc = subprocess.run(["curl", "-s", "-A", UA, "--max-time", "45", "-w", "\n%{http_code}", url],
                          capture_output=True, timeout=60)
    body, _, code = (proc.stdout or b"").rpartition(b"\n")
    status = int(code or 0) if code.strip().isdigit() else 0
    info = {"status": status, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
    if status != 200:
        return False, f"HTTP {status}", info
    hits = [m.decode() for m in PHP_ERROR_MARKERS if m in body]
    if hits:
        return False, f"PHP error text in page: {hits}", info
    if url.rstrip("/") == SITE:
        if not (b'class="hero' in body and b"wp-site-blocks" not in body):
            return False, "homepage lost the custom PHP template (hero missing / wp-site-blocks present)", info
        m = re.search(rb"<title>([^<]*)</title>", body)
        title = m.group(1).decode("utf-8", "replace") if m else ""
        if title_before is not None and title != title_before:
            return False, f"homepage title changed: {title_before!r} -> {title!r}", info
    return True, "ok", info


def run_file_deploy(args, files: list[FilePlan], head: str | None) -> int:
    """Live path for --file. Same guards as pages (clean main == origin/main,
    confirmation phrase, key-only SFTP, one attempt)."""
    if not confirm_live(args.confirmation):
        return 2
    print(f"\n[about to upload] main @ {head} from {SCRIPT_ROOT}")
    for f in files:
        print(f"  {f.rel} -> {f.remote}  (overwrite in place, sha256 {f.sha256[:12]}…)")
    env = load_env()
    missing = [k for k in ("ROCKET_SFTP_HOST", "ROCKET_SFTP_USER", "ROCKET_SFTP_KEY_PATH") if not env.get(k)]
    if missing:
        print(f"[blocked] .env is missing {', '.join(missing)}. Nothing uploaded.", file=sys.stderr)
        return 2
    homepage_before = homepage_snapshot(f"{SITE}/")
    print(f"[homepage before] {homepage_before['status']} {homepage_before['bytes']:,} bytes "
          f"sha256 {homepage_before['sha256'][:12]}… title {homepage_before['title']!r}")
    if homepage_before["status"] != 200 or not homepage_before["custom_hero"]:
        print("[blocked] homepage is not healthy BEFORE deploy. Nothing uploaded.", file=sys.stderr)
        return 2

    print(f"\n[sftp] connecting to Rocket {env['ROCKET_SFTP_HOST']}:{env.get('ROCKET_SFTP_PORT') or 22}")
    sftp, transport = sftp_connect(env)
    uploaded, backups, results = [], {}, {}
    try:
        # every check happens before the first byte is written
        problems = []
        for f in files:
            state = remote_file_state(sftp, f)
            if state == "missing":
                problems.append(f"{f.rel}: {f.remote} does not exist on the server; --file only overwrites "
                                f"in place (never creates{' mu-plugins' if f.is_mu_plugin else ''} files)")
            elif state == "same":
                results[f.rel] = "same (already live, not re-uploaded)"
            if f.is_php:
                others = read_other_mu_plugins(sftp, f.remote if f.is_mu_plugin else "")
                dup = duplicate_function_problem(f, others)
                if dup:
                    problems.append(dup)
        if problems:
            print("[blocked] nothing uploaded:\n  " + "\n  ".join(problems), file=sys.stderr)
            return 2
        for f in files:
            if f.rel in results:
                print(f"  [same] {f.remote} already matches kitchen; not re-uploaded")
                continue
            bak = sftp_backup(sftp, f.remote)
            if not bak:
                print(f"[blocked] backup of {f.remote} failed; stopping before upload", file=sys.stderr)
                break
            backups[f.rel] = bak
            print(f"  [backup] {f.remote} -> {bak}")
            sftp.put(str(f.local), f.remote)
            with sftp.file(f.remote, "rb") as rf:
                ok = hashlib.sha256(rf.read()).hexdigest() == f.sha256
            print(f"  [up] {f.remote} ({f.size:,} bytes) server copy matches kitchen: {ok}")
            if not ok:
                results[f.rel] = "FAILED: server copy does not match kitchen after upload"
                sftp.put(str(bak), f.remote)
                print(f"  [restore] {f.remote} <- {bak}", file=sys.stderr)
                break
            uploaded.append(f)

        # purge: exact public URLs, plus a full-site purge when PHP output or the
        # snippets the PHP templates read could change rendered pages
        if uploaded and not args.skip_flush:
            exact = {FILE_PUBLIC_URLS[f.rel]: f.sha256 for f in uploaded if f.rel in FILE_PUBLIC_URLS}
            rendered = [f for f in uploaded if f.rel in RENDER_CHECK_URLS]
            if exact:
                for url, st in purge_and_confirm(env, exact).items():
                    rel = next(f.rel for f in uploaded if FILE_PUBLIC_URLS.get(f.rel) == url)
                    results[rel] = st
            if rendered:
                rocket_purge_everything(env)
                time.sleep(10)

        # rendered-page checks; a failure restores the backup we just took and stops
        for f in uploaded:
            failed = None
            for url in RENDER_CHECK_URLS.get(f.rel, []):
                ok, why, info = render_check(url, homepage_before["title"])
                print(f"  [render] {url}: {'ok' if ok else 'FAIL — ' + why} "
                      f"(HTTP {info['status']}, {info['bytes']:,} bytes, sha256 {info['sha256'][:12]}…)")
                if not ok:
                    bak = backups[f.rel]
                    sftp.put(str(bak), f.remote)
                    print(f"  [restore] {f.remote} <- {bak} (render check failed)", file=sys.stderr)
                    rocket_purge_everything(env)
                    time.sleep(10)
                    ok2, why2, info2 = render_check(f"{SITE}/", homepage_before["title"])
                    print(f"  [after restore] homepage {'ok' if ok2 else 'STILL BAD — ' + why2} "
                          f"(HTTP {info2['status']}, {info2['bytes']:,} bytes)")
                    results[f.rel] = f"RESTORED from backup: {why}"
                    failed = why
                    break
            if failed:
                break
            results.setdefault(f.rel, "ok (uploaded; render checks passed)")
    finally:
        sftp.close()
        transport.close()

    homepage_after = homepage_snapshot(f"{SITE}/")
    print("\n" + "=" * 70)
    print(f"FILE DEPLOY REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for f in files:
        print(f"    {f.rel}")
        print(f"      remote:  {f.remote}")
        print(f"      backup:  {backups.get(f.rel, '(none)')}")
        print(f"      result:  {results.get(f.rel, 'not attempted')}")
    print(f"  homepage before: {homepage_before['status']} {homepage_before['bytes']:,} bytes "
          f"sha256 {homepage_before['sha256']}")
    print(f"  homepage after:  {homepage_after['status']} {homepage_after['bytes']:,} bytes "
          f"sha256 {homepage_after['sha256']} title {homepage_after['title']!r}")
    bad = [r for r in results.values() if not r.startswith(("ok", "same"))]
    attempted = all(f.rel in results for f in files)
    ok = attempted and not bad and homepage_after["status"] == 200 and homepage_after["custom_hero"]
    print(f"  result: {'ALL GOOD' if ok else 'ATTENTION NEEDED'}")
    print("=" * 70)
    return 0 if ok else 1


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
    # Per-page exceptions: {repo-relative file: [exact sentence, ...]}. Each
    # sentence must appear exactly once on that one page; nowhere else counts.
    by_page = ledger.get("banned_word_allowed_phrases_by_page", {})
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
        page_allowed = list(by_page.get(rel, []))
        for phrase in page_allowed:
            n = len(re.findall(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", html, re.IGNORECASE))
            if n != 1:
                problems.append(f"{page}: per-page allowed sentence must appear exactly once "
                                f"(found {n}): {phrase!r} — refusing to deploy")
        content_problems = [f"banned word {h}" for h in
                            facts.banned_word_hits(html, list(allowed_phrases) + page_allowed)]
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


def rocket_purge_everything(env: dict) -> bool:
    """Full-site Rocket CDN purge. Used only as the automatic fallback when a
    single-URL purge leaves the old copy at the edge."""
    token = rocket_token(env)
    if not token:
        return False
    site_id = env.get("ROCKET_SITE_ID") or ROCKET_SITE_ID_DEFAULT
    status, payload = _curl_json(f"{ROCKET_API}/sites/{site_id}/cache/purge_everything",
                                 method="POST", body={}, token=token)
    ok = status == 200 and bool(payload is None or payload.get("success", True))
    print(f"  [cache] Rocket FULL-SITE purge: {'ok' if ok else f'FAILED (HTTP {status})'}")
    return ok


def live_fetch(url: str) -> dict:
    """Read-only clean-URL GET (no cache-busting query, no compression) the way
    a patient hits it. Returns status, sha256 of the body, bytes, cf-cache-status, age."""
    proc = subprocess.run(["curl", "-s", "-A", UA, "--max-time", "45", "-D", "-", url],
                          capture_output=True, timeout=60)
    raw = proc.stdout or b""
    # curl -D - writes every header block (redirects too) before the body
    head, body = b"", raw
    while body.startswith(b"HTTP/") and b"\r\n\r\n" in body:
        head, body = body.split(b"\r\n\r\n", 1)
    hdrs = {}
    status = 0
    for i, line in enumerate(head.decode("latin-1").split("\r\n")):
        if i == 0:
            parts = line.split()
            status = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        elif ":" in line:
            k, v = line.split(":", 1)
            hdrs[k.strip().lower()] = v.strip()
    return {"status": status, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
            "cf_cache": hdrs.get("cf-cache-status", ""), "age": hdrs.get("age", "")}


def _stale(expected: dict, fetch) -> dict:
    out = {}
    for url, sha in expected.items():
        live = fetch(url)
        if live["status"] != 200 or live["sha256"] != sha:
            out[url] = live
    return out


def purge_and_confirm(env: dict, expected: dict, *, fetch=None, sleep=None,
                      purge=None, purge_all=None, settle_s: int = 8, rechecks: int = 3) -> dict:
    """Purge, then PROVE the edge serves the kitchen bytes.

    expected: {live_url: kitchen_sha256}. Single-URL purge first. Rocket's
    partial purge (files and tags) has been reporting success while the
    Cloudflare edge keeps the old copy (seen 2026-10-28 on /pharmacy/, /faq/,
    /arizona-uti-treatment/), so if any clean URL still serves a different sha
    we fall back to a full-site purge automatically and re-check. Returns
    {url: "ok ..." | "STALE ..."}; callers must treat STALE as a failed deploy."""
    fetch = fetch or live_fetch
    sleep = sleep or time.sleep
    purge = purge or rocket_purge
    purge_all = purge_all or rocket_purge_everything
    results = {}
    if not expected:
        return results
    purge(env, list(expected))
    sleep(settle_s)
    stale = _stale(expected, fetch)
    for url in expected:
        if url not in stale:
            results[url] = "ok (single-URL purge; live sha matches kitchen)"
    if not stale:
        return results
    for url, live in stale.items():
        print(f"  [cache] {url} still stale after single-URL purge "
              f"(live {live['sha256'][:12]} cf={live['cf_cache'] or '-'} age={live['age'] or '-'}) "
              f"-> full-site purge")
    purge_all(env)
    remaining = dict(stale)
    for _ in range(rechecks):
        sleep(settle_s)
        remaining = _stale({u: expected[u] for u in remaining}, fetch)
        if not remaining:
            break
    for url in stale:
        if url in remaining:
            live = remaining[url]
            results[url] = (f"STALE: live sha {live['sha256'][:12]} != kitchen {expected[url][:12]} "
                            f"(HTTP {live['status']}, cf={live['cf_cache'] or '-'}, age={live['age'] or '-'}) "
                            f"even after full-site purge")
            print(f"  [cache] {url}: {results[url]}", file=sys.stderr)
        else:
            results[url] = "ok (full-site purge fallback; live sha matches kitchen)"
    return results


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
            raw = resp.read()
            hdrs = getattr(resp, "headers", None) or {}
            cf_cache = hdrs.get("cf-cache-status", "-")
            age = hdrs.get("age", "-")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        return f"request failed: {e}"
    if status != 200:
        return f"bad status {status}"
    if item.sha256:
        live_sha = hashlib.sha256(raw).hexdigest()
        if live_sha != item.sha256:
            return (f"live sha {live_sha[:12]} != kitchen {item.sha256[:12]} "
                    f"(cf-cache-status={cf_cache}, age={age}) — edge is serving a stale copy")
    html = raw.decode("utf-8", errors="replace")
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


def main_files(args, file_names: list[str]) -> int:
    """--file mode: dry-run plan by default; --remote-diff reads server state
    and runs the duplicate-function check read-only; --live uploads."""
    try:
        files = build_file_plan(file_names)
    except RuntimeError as e:
        print(f"[blocked] {e}", file=sys.stderr)
        return 2
    if args.verify_only:
        failed = 0
        for f in files:
            url = FILE_PUBLIC_URLS.get(f.rel)
            if url:
                live = live_fetch(url)
                ok = live["status"] == 200 and live["sha256"] == f.sha256
                failed += not ok
                print(f"  [verify] {url}: {'PASS' if ok else 'FAIL'} (HTTP {live['status']}, "
                      f"live sha {live['sha256'][:12]} vs kitchen {f.sha256[:12]})")
            for url in RENDER_CHECK_URLS.get(f.rel, []):
                ok, why, info = render_check(url)
                failed += not ok
                print(f"  [render] {url}: {'ok' if ok else 'FAIL — ' + why} (HTTP {info['status']}, "
                      f"{info['bytes']:,} bytes, sha256 {info['sha256'][:12]}…)")
        return 1 if failed else 0
    head = None
    if args.live or args.remote_diff:
        blocked, head = preflight_block()
        if blocked:
            print(blocked, file=sys.stderr)
            return 2
    print_file_plan(files)
    print(f"  target: Rocket.net site {ROCKET_SITE_ID_DEFAULT} SFTP (key auth), web root {REMOTE_PREFIX}/")
    if not args.live:
        if args.remote_diff:
            env = load_env()
            sftp, transport = sftp_connect(env)
            try:
                print("\nRemote file check (read-only):")
                for f in files:
                    state = remote_file_state(sftp, f)
                    note = " — would be REFUSED (overwrite in place only)" if state == "missing" else ""
                    print(f"  [{state.split()[0]}] {f.remote}{note}" + ("" if state in ("missing", "same") else f" — remote {state}"))
                    if f.is_php:
                        dup = duplicate_function_problem(
                            f, read_other_mu_plugins(sftp, f.remote if f.is_mu_plugin else ""))
                        print(f"  [functions] {f.rel}: {dup or 'no clash with other mu-plugins'}")
            finally:
                sftp.close()
                transport.close()
        print("\n[dry-run] nothing uploaded. Add --live (and Chris\'s confirmation phrase) to deploy.")
        return 0
    return run_file_deploy(args, files, head)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Unified guarded deploy for NPCWoods landing pages. DRY-RUN BY DEFAULT.")
    parser.add_argument("--pages", action="append",
                        help="comma-separated page paths relative to landing-pages/ (repeatable)")
    parser.add_argument("--manifest", help="text file of page paths, one per line, # comments OK")
    parser.add_argument("--asset", action="append",
                        help="repo-relative file under assets/ to upload as a NEW file to "
                             "public_html/assets/... (repeatable; never overwrites)")
    parser.add_argument("--file", action="append",
                        help="allow-listed non-page file to overwrite in place (homepage template, "
                             "five mu-plugins, npc-menu.js, llms*.txt, shared snippets); "
                             "one PHP file per run; cannot be combined with --pages/--asset")
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
        asset_names = collect_assets(args)
        file_names = collect_files(args)
    except (ValueError, OSError) as e:
        print(f"[err] {e}", file=sys.stderr)
        return 2
    if file_names:
        if pages or asset_names:
            print("[err] --file runs alone: ship pages/assets in a separate run", file=sys.stderr)
            return 2
        return main_files(args, file_names)
    if not pages and not asset_names:
        parser.print_usage()
        print("[err] nothing given — use --pages, --manifest, --asset or --file", file=sys.stderr)
        return 2

    try:
        plan = build_plan(pages, strict=not args.verify_only)
        assets = build_asset_plan(asset_names)
    except RuntimeError as e:
        print(f"[blocked] {e}", file=sys.stderr)
        return 2

    stub_table = load_stub_table()

    # ---- verify-only -----------------------------------------------------
    if args.verify_only:
        print(f"[verify-only] checking {len(plan)} live page(s), {len(assets)} asset(s), no upload")
        failed = []
        if plan:
            results = run_verification(plan)
            proof_report = write_verification_proof_report(plan, results, mode="verify-only")
            failed = [p for p, r in results.items() if r.startswith("FAIL")]
            print(f"[proof] wrote verification report: {proof_report}")
        for a in assets:
            live = live_fetch(a.url)
            ok = live["status"] == 200 and live["sha256"] == a.sha256
            print(f"  [verify] {a.url}: {'PASS' if ok else 'FAIL'} (HTTP {live['status']}, "
                  f"live sha {live['sha256'][:12]} vs kitchen {a.sha256[:12]})")
            if not ok:
                failed.append(a.rel)
        label = "pages" if not assets else "pages+assets"
        print(f"\n[done] {len(plan) + len(assets) - len(failed)}/{len(plan) + len(assets)} {label} passed verification")
        return 1 if failed else 0

    # ---- counter + git guard: before .env loads, before any server contact --
    head = None
    if args.live or args.remote_diff:
        blocked, head = preflight_block()
        if blocked:
            print(blocked, file=sys.stderr)
            return 2

    print_plan(plan, stub_table, head)
    print_asset_plan(assets)
    print(f"  target: Rocket.net site {ROCKET_SITE_ID_DEFAULT} SFTP (key auth), web root {REMOTE_PREFIX}/")
    purge_urls = [a.url for a in assets] + [i.url for i in plan]
    print(f"  after upload: Rocket CDN purge of {len(purge_urls)} URL(s): " + ", ".join(purge_urls))

    # ---- dry-run (default) ----------------------------------------------
    if not args.live:
        if args.remote_diff:
            env = load_env()
            sftp, transport = sftp_connect(env)
            try:
                remote_diff(sftp, plan)
                if assets:
                    print("\nRemote asset check (read-only):")
                    for rel, st in check_remote_assets(sftp, assets).items():
                        print(f"  [{st.split()[0]}] {rel}" + ("" if st in ("new", "matching") else f" — remote {st}; would be SKIPPED"))
            finally:
                sftp.close()
                transport.close()
        print(f'\n[dry-run] nothing uploaded. Add --live (and Chris\'s confirmation phrase) to deploy.')
        return 0

    # ---- live ------------------------------------------------------------
    if not confirm_live(args.confirmation):
        return 2

    print(f"\n[about to upload] main @ {head} from {SCRIPT_ROOT}")
    for a in assets:
        print(f"  {a.rel} -> {a.remote}  (asset, new-only, sha256 {a.sha256[:12]}…)")
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
    asset_results: dict[str, str] = {}
    hold_pages = False
    try:
        if assets:
            asset_state = check_remote_assets(sftp, assets)
            asset_results = upload_assets(sftp, assets, asset_state)
            bad = [r for r, v in asset_results.items() if v.startswith(("SKIPPED", "FAILED"))]
            if bad and plan:
                hold_pages = True
                print(f"  [hold] {len(bad)} asset(s) not live as planned; no page uploaded this run "
                      f"(pages may point at them): {', '.join(bad)}", file=sys.stderr)
        for item in ([] if hold_pages else plan):
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
    stale_pages = []
    live_assets = [a for a in assets if asset_results.get(a.rel, "").startswith(("uploaded", "matching"))]
    asset_cache: dict[str, str] = {}
    if not args.skip_flush and (uploaded or live_assets):
        expected = {a.url: a.sha256 for a in live_assets}
        expected.update({item.url: item.sha256 for item in uploaded})
        confirmed = purge_and_confirm(env, expected)
        for item in uploaded:
            flush_results[item.page] = confirmed.get(item.url, "not checked")
            if not flush_results[item.page].startswith("ok"):
                stale_pages.append(item.page)
        for a in live_assets:
            asset_cache[a.rel] = confirmed.get(a.url, "not checked")
            if not asset_cache[a.rel].startswith("ok"):
                stale_pages.append(a.rel)

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
    for a in assets:
        print(f"    asset {a.rel}")
        print(f"      remote:  {a.remote}")
        print(f"      result:  {asset_results.get(a.rel, 'not attempted')}")
        print(f"      cache:   {asset_cache.get(a.rel, 'skipped')}")
    if hold_pages:
        print("  pages HELD: an asset was skipped or failed, so no page was uploaded")
    print(f"  uploaded: {len(uploaded)}/{len(plan)} page(s)")
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
    if stale_pages:
        print(f"  STALE AT EDGE (live sha != kitchen): {', '.join(stale_pages)}")
    bad_assets = [r for r, v in asset_results.items() if v.startswith(("SKIPPED", "FAILED"))]
    ok = (not failed_uploads and not failed_verify and not hp_problem and not stale_pages
          and not bad_assets and not hold_pages)
    print(f"  result: {'ALL GOOD' if ok else 'ATTENTION NEEDED'}")
    print("=" * 70)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
