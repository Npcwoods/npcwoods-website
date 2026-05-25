#!/usr/bin/env python3
"""Create a phone-reviewable static preview bundle, optionally deploy to Vercel."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
OUT_ROOT = REPO / "automation-output" / "previews"
BUILD_DIR = OUT_ROOT / "latest-build"

PUBLIC_DIRS = ("assets", "blog", "html", "landing-pages")

EXCLUDE_DIRS = {
    ".git",
    ".vercel",
    ".tmp",
    "__pycache__",
    "automation-output",
    "backups",
    "node_modules",
}

EXCLUDE_SUFFIXES = (
    ".bak",
    ".pyc",
    ".pyo",
    ".pyd",
    ".log",
)

EXCLUDE_NAMES = {
    ".DS_Store",
    ".env",
    ".env.local",
    ".env.production",
}


def run(args: list[str], *, cwd: Path = REPO, check: bool = True) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if check and result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise SystemExit(message or f"Command failed: {' '.join(args)}")
    return result.stdout.strip()


def repo_info() -> dict[str, str]:
    return {
        "branch": run(["git", "branch", "--show-current"], check=False) or "unknown",
        "commit": run(["git", "rev-parse", "--short", "HEAD"], check=False) or "unknown",
        "subject": run(["git", "log", "-1", "--pretty=%s"], check=False) or "unknown",
    }


def changed_files(since: str) -> list[Path]:
    output = run(["git", "diff", "--name-only", f"{since}..HEAD"], check=False)
    files = []
    for line in output.splitlines():
        path = REPO / line
        if path.exists() and path.is_file():
            files.append(path.relative_to(REPO))
    return files


def should_skip(path: Path) -> bool:
    rel_parts = path.relative_to(REPO).parts
    if any("/".join(rel_parts[: i + 1]) in EXCLUDE_DIRS for i in range(len(rel_parts))):
        return True
    if path.name in EXCLUDE_NAMES or path.name.startswith(".env."):
        return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    return False


def copy_public_repo() -> None:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True)

    for dirname in PUBLIC_DIRS:
        item = REPO / dirname
        if not item.exists():
            continue
        if should_skip(item):
            continue
        target = BUILD_DIR / item.name
        shutil.copytree(item, target, ignore=copy_ignore)


def copy_ignore(directory: str, names: list[str]) -> set[str]:
    ignored = set()
    base = Path(directory)
    for name in names:
        path = base / name
        try:
            rel = path.relative_to(REPO)
        except ValueError:
            rel = Path(name)
        if name in EXCLUDE_NAMES or name.startswith(".env.") or name in EXCLUDE_DIRS:
            ignored.add(name)
            continue
        if any("/".join(rel.parts[: i + 1]) in EXCLUDE_DIRS for i in range(len(rel.parts))):
            ignored.add(name)
            continue
        if path.suffix in EXCLUDE_SUFFIXES:
            ignored.add(name)
    return ignored


def preview_link(path: Path) -> str:
    value = path.as_posix()
    if value.endswith("/index.html"):
        return value[: -len("index.html")]
    return value


def write_review_index(info: dict[str, str], files: list[Path]) -> None:
    review_dir = BUILD_DIR / "_preview"
    review_dir.mkdir(parents=True, exist_ok=True)
    html_files = [
        p
        for p in files
        if p.suffix.lower() in {".html", ".htm"}
        and p.parts
        and p.parts[0] in PUBLIC_DIRS
    ]
    skipped_files = [
        p
        for p in files
        if p.suffix.lower() in {".php"}
        or (p.parts and p.parts[0] not in PUBLIC_DIRS)
    ]

    rows = []
    if html_files:
        for path in html_files:
            href = "../" + preview_link(path)
            rows.append(
                f'<li><a href="{html.escape(href)}">{html.escape(path.as_posix())}</a></li>'
            )
    else:
        rows.append("<li>No changed static HTML files detected in the selected commit range.</li>")

    skipped_note = ""
    if skipped_files:
        skipped_items = "".join(
            f"<li>{html.escape(path.as_posix())}</li>" for path in skipped_files[:20]
        )
        if len(skipped_files) > 20:
            skipped_items += f"<li>...and {len(skipped_files) - 20} more</li>"
        skipped_note = f"""
  <h2>Not Included</h2>
  <p>These changed files were left out of the public preview bundle because they are source/tooling files, not static review pages.</p>
  <ul>{skipped_items}</ul>
"""

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NPCWoods Preview {html.escape(info['commit'])}</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f7f3ed; color: #1f2c35; }}
    main {{ max-width: 880px; margin: 0 auto; padding: 40px 20px 64px; }}
    h1 {{ margin: 0 0 12px; font-size: clamp(2rem, 7vw, 4.5rem); line-height: .95; letter-spacing: 0; }}
    p {{ font-size: 1rem; line-height: 1.6; color: #475569; }}
    .meta, ul {{ background: #fff; border: 1px solid rgba(31,44,53,.12); border-radius: 8px; box-shadow: 0 18px 45px rgba(31,44,53,.08); }}
    .meta {{ display: grid; gap: 10px; padding: 18px; margin: 24px 0; }}
    .meta div {{ overflow-wrap: anywhere; }}
    ul {{ list-style: none; padding: 10px; margin: 18px 0 0; }}
    li + li {{ border-top: 1px solid rgba(31,44,53,.1); }}
    a {{ display: block; padding: 14px 12px; color: #0f66a6; font-weight: 700; text-decoration: none; overflow-wrap: anywhere; }}
    a:hover {{ text-decoration: underline; }}
    code {{ font-size: .95em; }}
  </style>
</head>
<body>
<main>
  <h1>Phone Preview</h1>
  <p>This is a temporary static review bundle for the latest website commit. It is for visual review only, not a production deploy.</p>
  <section class="meta">
    <div><strong>Branch:</strong> <code>{html.escape(info['branch'])}</code></div>
    <div><strong>Commit:</strong> <code>{html.escape(info['commit'])}</code></div>
    <div><strong>Message:</strong> {html.escape(info['subject'])}</div>
    <div><strong>Built:</strong> {timestamp}</div>
  </section>
  <h2>Changed Pages</h2>
  <ul>
    {''.join(rows)}
  </ul>
  {skipped_note}
</main>
</body>
</html>
"""
    (review_dir / "index.html").write_text(page)
    (BUILD_DIR / "index.html").write_text(
        '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/_preview/">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>NPCWoods Preview</title><a href="/_preview/">Open preview</a>'
    )
    (BUILD_DIR / "vercel.json").write_text(json.dumps({"cleanUrls": True, "trailingSlash": True}, indent=2))


def deploy(open_browser: bool) -> str:
    vercel = shutil.which("vercel")
    if not vercel:
        raise SystemExit("Vercel CLI is not installed.")
    output = run([vercel, "deploy", str(BUILD_DIR), "-y", "--no-wait"])
    urls = re.findall(r"https://[^\s]+", output)
    url = urls[-1] if urls else output.strip()
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "latest-url.txt").write_text(url + "\n")
    if open_browser and shutil.which("open"):
        subprocess.run(["open", url], check=False)
    return url


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", default="HEAD~1", help="Git ref to compare against, default: HEAD~1")
    parser.add_argument("--deploy", action="store_true", help="Deploy the preview bundle to Vercel")
    parser.add_argument("--open", action="store_true", help="Open the deployed URL in the default browser")
    args = parser.parse_args()

    info = repo_info()
    files = changed_files(args.since)
    copy_public_repo()
    write_review_index(info, files)

    print(f"Preview bundle ready: {BUILD_DIR}")
    print(f"Local review file: {BUILD_DIR / 'index.html'}")
    if args.deploy:
        url = deploy(args.open)
        print(f"Preview URL: {url}")


if __name__ == "__main__":
    main()
