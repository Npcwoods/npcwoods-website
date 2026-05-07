#!/usr/bin/env python3
"""
fix-h2-ratings-banner.py

Fixes the H2-before-H1 heading hierarchy bug across all landing pages.

The `Over 50 Five Star Ratings` banner is currently marked up as an <h2>
that renders before each page's actual <h1>, violating Google's heading
structure guidance and WCAG. It's a visual banner label, not a section
heading, so we demote it to a <p> with a new class.

Two edits per file:
  1. HTML tag: <h2>...</h2> -> <p class="reviews-banner-title">...</p>
  2. CSS selector: `.reviews-banner-header h2` -> `.reviews-banner-header .reviews-banner-title`
     (+ add `margin:0` to neutralize <p>'s default margin)

Safe by design:
  - Creates a .bak sibling file for every modified file
  - Idempotent: skips files already patched
  - --dry-run shows unified diffs without writing
  - Uses anchored regex so it can never close the wrong </h2>

Usage:
  ./fix-h2-ratings-banner.py --dry-run                  # preview all changes
  ./fix-h2-ratings-banner.py --dry-run --file <path>    # preview one file
  ./fix-h2-ratings-banner.py                            # apply to all landing-pages/
  ./fix-h2-ratings-banner.py --restore                  # restore from .bak files
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGET = REPO_ROOT / "landing-pages"

# Files to NEVER touch, even if they match the pattern.
# dental-pain is the golden template: its H1 already comes before the H2,
# so it does not have the heading-hierarchy bug. It also backs an active
# Google Ads campaign — zero-risk deploys only.
SKIP_LIST = {
    (REPO_ROOT / "landing-pages" / "dental-pain" / "index.html").resolve(),
}

# --- Edit 1: CSS selector swap -------------------------------------------------
# Two known variants in the codebase:
#   - MINIFIED: single-line, used in 53 files
#   - PRETTY:   multi-line, used in dental-pain/index.html only
# Both are handled as deterministic exact-string replacements so every byte
# of change is auditable.
CSS_VARIANTS = [
    # MINIFIED (single line)
    (
        ".reviews-banner-header h2{font-family:'DM Serif Display',serif;"
        "font-size:clamp(1.5rem,3.5vw,2.2rem);color:#1a1a2e;display:inline-flex;"
        "align-items:center;gap:10px;justify-content:center;flex-wrap:wrap}",
        ".reviews-banner-header .reviews-banner-title{font-family:'DM Serif Display',serif;"
        "font-size:clamp(1.5rem,3.5vw,2.2rem);color:#1a1a2e;display:inline-flex;"
        "align-items:center;gap:10px;justify-content:center;flex-wrap:wrap;margin:0}",
    ),
    # PRETTY (dental-pain/index.html only)
    (
        "    .reviews-banner-header h2 {\n"
        "      font-family: 'DM Serif Display', serif;\n"
        "      font-size: clamp(1.5rem, 3.5vw, 2.2rem);\n"
        "      color: #1a1a2e;\n"
        "      display: inline-flex;\n"
        "      align-items: center;\n"
        "      gap: 10px;\n"
        "      justify-content: center;\n"
        "      flex-wrap: wrap;\n"
        "    }",
        "    .reviews-banner-header .reviews-banner-title {\n"
        "      font-family: 'DM Serif Display', serif;\n"
        "      font-size: clamp(1.5rem, 3.5vw, 2.2rem);\n"
        "      color: #1a1a2e;\n"
        "      display: inline-flex;\n"
        "      align-items: center;\n"
        "      gap: 10px;\n"
        "      justify-content: center;\n"
        "      flex-wrap: wrap;\n"
        "      margin: 0;\n"
        "    }",
    ),
]

# --- Edit 2: HTML tag swap ----------------------------------------------------
# Anchored pattern: matches ONLY the ratings-banner <h2>, never any other <h2>.
# The \s* allows the newlines between `Ratings`, the <span>, and the closing tag.
HTML_PATTERN = re.compile(
    r'<h2>Over 50 Five Star Ratings\s*'
    r'(<span class="reviews-banner-stars">.*?</span>)\s*'
    r'</h2>',
    re.DOTALL,
)
HTML_REPLACE = r'<p class="reviews-banner-title">Over 50 Five Star Ratings \1</p>'

# Sentinel: if this string is already in the file, we've already patched it.
IDEMPOTENCY_MARKER = 'class="reviews-banner-title"'


def classify(path: Path) -> str:
    """Bucket each file for the summary report."""
    parts = path.parts
    if "medications" in parts:
        return "medication"
    if "learn" in parts:
        return "education"
    if any(p.endswith("-telemedicine") for p in parts):
        return "state"
    if "uti-treatment" in parts and len(parts) > parts.index("uti-treatment") + 2:
        return "city"
    if any(
        p in parts
        for p in (
            "uti-treatment",
            "sinus-infection-treatment",
            "dental-pain",
            "ed-treatment",
            "glp1-weight-loss",
        )
    ):
        return "condition"
    return "other"


def process_file(path: Path, dry_run: bool) -> dict:
    """
    Returns a dict describing what happened:
      status: 'patched' | 'already-patched' | 'no-h2-ratings' | 'css-mismatch' | 'html-mismatch' | 'error'
      diff:   unified diff string (only in dry-run mode when patched)
    """
    if path.resolve() in SKIP_LIST:
        return {"status": "skipped"}

    try:
        original = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"status": "error", "error": str(e)}

    # Idempotency: if the file already has the new class, skip it.
    if IDEMPOTENCY_MARKER in original:
        return {"status": "already-patched"}

    # Quick check: does this file even have the ratings H2?
    if "Over 50 Five Star Ratings" not in original:
        return {"status": "no-h2-ratings"}

    # Apply Edit 1: CSS (try each known variant; first hit wins)
    step1 = None
    for css_old, css_new in CSS_VARIANTS:
        if css_old in original:
            step1 = original.replace(css_old, css_new, 1)
            break
    if step1 is None:
        return {"status": "css-mismatch"}

    # Apply Edit 2: HTML
    match = HTML_PATTERN.search(step1)
    if not match:
        return {"status": "html-mismatch"}
    step2 = HTML_PATTERN.sub(HTML_REPLACE, step1, count=1)

    if step2 == original:
        return {"status": "no-change"}

    # Sanity: the file should now contain the marker and NOT contain the old
    # CSS selector or the old H2 opening tag for this banner.
    if IDEMPOTENCY_MARKER not in step2:
        return {"status": "error", "error": "post-patch sanity check failed (marker missing)"}
    for css_old, _ in CSS_VARIANTS:
        if css_old in step2:
            return {"status": "error", "error": "post-patch sanity check failed (old CSS still present)"}
    if "<h2>Over 50 Five Star Ratings" in step2:
        return {"status": "error", "error": "post-patch sanity check failed (old H2 still present)"}

    diff_text = ""
    if dry_run:
        diff_text = "".join(
            difflib.unified_diff(
                original.splitlines(keepends=True),
                step2.splitlines(keepends=True),
                fromfile=str(path),
                tofile=str(path) + " (patched)",
                n=3,
            )
        )
    else:
        # Write .bak then overwrite. Atomic-ish.
        bak = path.with_suffix(path.suffix + ".bak")
        if not bak.exists():
            bak.write_text(original, encoding="utf-8")
        path.write_text(step2, encoding="utf-8")

    return {"status": "patched", "diff": diff_text}


def restore_from_backups(target: Path) -> None:
    """Undo: copy every *.html.bak back over its *.html sibling."""
    restored = 0
    for bak in target.rglob("*.html.bak"):
        original = bak.with_suffix("")  # strip .bak
        original.write_text(bak.read_text(encoding="utf-8"), encoding="utf-8")
        bak.unlink()
        restored += 1
        print(f"  restored {original.relative_to(REPO_ROOT)}")
    print(f"\nRestored {restored} files.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="Show diffs without writing anything")
    ap.add_argument("--file", type=Path, help="Operate on a single file (path)")
    ap.add_argument("--target", type=Path, default=DEFAULT_TARGET, help=f"Directory to scan (default: {DEFAULT_TARGET})")
    ap.add_argument("--restore", action="store_true", help="Restore all files from their .bak siblings and exit")
    args = ap.parse_args()

    if args.restore:
        restore_from_backups(args.target)
        return 0

    if args.file:
        files = [args.file.resolve()]
    else:
        files = sorted(args.target.resolve().rglob("index.html"))

    if not files:
        print(f"No index.html files found under {args.target}")
        return 1

    mode = "DRY RUN" if args.dry_run else "APPLY"
    print(f"=== fix-h2-ratings-banner [{mode}] ===")
    print(f"Scanning {len(files)} file(s) under {args.target}\n")

    buckets = {
        "patched": [],
        "already-patched": [],
        "no-h2-ratings": [],
        "css-mismatch": [],
        "html-mismatch": [],
        "no-change": [],
        "error": [],
    }

    for f in files:
        result = process_file(f, dry_run=args.dry_run)
        status = result["status"]
        buckets.setdefault(status, []).append((f, result))
        rel = f.relative_to(REPO_ROOT)
        category = classify(f)
        if status == "patched":
            if args.dry_run:
                print(f"[{category:10s}] WOULD PATCH  {rel}")
                if args.file:  # only print the full diff when targeting one file
                    print(result["diff"])
            else:
                print(f"[{category:10s}] PATCHED      {rel}")
        elif status == "already-patched":
            print(f"[{category:10s}] already ok   {rel}")
        elif status == "no-h2-ratings":
            print(f"[{category:10s}] no banner    {rel}")
        elif status in ("css-mismatch", "html-mismatch"):
            print(f"[{category:10s}] MISMATCH ({status})  {rel}")
        elif status == "skipped":
            print(f"[{category:10s}] SKIPPED      {rel} (explicit skip list)")
        elif status == "error":
            print(f"[{category:10s}] ERROR        {rel} -- {result.get('error', '?')}")

    # Summary
    print("\n=== summary ===")
    for name, items in buckets.items():
        if items:
            print(f"  {name}: {len(items)}")

    if buckets["error"] or buckets["css-mismatch"] or buckets["html-mismatch"]:
        print("\n⚠️  Some files could not be patched. Inspect them before re-running.")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
