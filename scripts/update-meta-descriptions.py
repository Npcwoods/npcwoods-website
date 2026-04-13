#!/usr/bin/env python3
"""
Update <title> and <meta name="description"> on landing pages from a TSV.

Idempotency: always reads from <file>.meta-bak (created on first run from
the original). Re-running with the same TSV produces the same output.

Usage:
    python scripts/update-meta-descriptions.py scripts/meta-rewrites-2026-04-13.tsv [--dry-run]
"""

import argparse
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TITLE_RE = re.compile(r"<title>.*?</title>", re.DOTALL)
META_DESC_RE = re.compile(
    r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>',
    re.DOTALL,
)

TITLE_MAX = 60
DESC_MAX = 160
BANNED = ["doctor", "insurance", "appointment", "board-certified", "Text a Doctor"]


def html_escape_amp(text: str) -> str:
    """Escape bare & to &amp; (don't double-escape)."""
    return re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)", "&amp;", text)


def attr_escape(text: str) -> str:
    """Escape for use inside a double-quoted HTML attribute."""
    return html_escape_amp(text).replace('"', "&quot;")


def validate(title: str, desc: str, path: str) -> list[str]:
    errors = []
    if len(title) > TITLE_MAX:
        errors.append(f"title is {len(title)} chars (max {TITLE_MAX})")
    if len(desc) > DESC_MAX:
        errors.append(f"description is {len(desc)} chars (max {DESC_MAX})")
    haystack = f"{title} {desc}".lower()
    for word in BANNED:
        if word.lower() in haystack:
            errors.append(f"banned word found: {word!r}")
    return errors


def update_file(target: Path, new_title: str, new_desc: str, dry_run: bool):
    bak = target.with_suffix(target.suffix + ".meta-bak")
    if not bak.exists():
        bak.write_bytes(target.read_bytes())
    original = bak.read_text(encoding="utf-8")

    if not TITLE_RE.search(original):
        return "ERROR: no <title> tag found"
    if not META_DESC_RE.search(original):
        return "ERROR: no <meta name=description> tag found"

    new_title_html = html_escape_amp(new_title)
    new_desc_attr = attr_escape(new_desc)

    updated = TITLE_RE.sub(f"<title>{new_title_html}</title>", original, count=1)
    updated = META_DESC_RE.sub(
        f'<meta name="description" content="{new_desc_attr}">',
        updated,
        count=1,
    )

    if updated == original:
        return "no change"

    if dry_run:
        return "would update"

    target.write_text(updated, encoding="utf-8")
    return "updated"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv", help="Path to TSV with columns: path, new_title, new_description")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    tsv_path = Path(args.tsv)
    if not tsv_path.exists():
        print(f"TSV not found: {tsv_path}", file=sys.stderr)
        sys.exit(1)

    rows = list(csv.DictReader(tsv_path.open(encoding="utf-8"), delimiter="\t"))
    print(f"Loaded {len(rows)} rows from {tsv_path}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'WRITE'}\n")

    any_errors = False
    for row in rows:
        path = row["path"].strip()
        title = row["new_title"].strip()
        desc = row["new_description"].strip()

        errs = validate(title, desc, path)
        if errs:
            any_errors = True
            print(f"[FAIL] {path}")
            for e in errs:
                print(f"       - {e}")
            continue

        target = REPO_ROOT / path
        if not target.exists():
            any_errors = True
            print(f"[FAIL] {path} — file not found")
            continue

        result = update_file(target, title, desc, args.dry_run)
        flag = "OK" if result in ("updated", "would update", "no change") else "FAIL"
        if flag == "FAIL":
            any_errors = True
        print(f"[{flag}] {path}")
        print(f"       title ({len(title):>3}): {title}")
        print(f"       desc  ({len(desc):>3}): {desc}")
        print(f"       -> {result}\n")

    if any_errors:
        print("Completed with errors.", file=sys.stderr)
        sys.exit(2)
    print("All rows processed successfully.")


if __name__ == "__main__":
    main()
