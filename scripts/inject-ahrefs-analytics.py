#!/usr/bin/env python3
"""
Inject the Ahrefs Analytics <script> tag immediately before </head> on every
static HTML landing page.

Idempotent: always reads from <file>.ahrefs-bak (created on first run from
the original). If the snippet is already present, skip. Safe to re-run.

Targets:
  - landing-pages/**/index.html
  - html/{about,experience,pharmacy,pharmacy-partners,thank-you}/index.html

Excludes:
  - landing-pages/*.html at the top level (test/standalone fixtures)
  - html/shared/*.html (snippets with no <head>)
  - html/homepage-education-section.html (partial, no <head>)

Usage:
    python3 scripts/inject-ahrefs-analytics.py           # apply
    python3 scripts/inject-ahrefs-analytics.py --dry-run # preview only
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

AHREFS_KEY = "1qFceGSHKP6yg4JlSdNJ4Q"
SNIPPET = (
    f'<script src="https://analytics.ahrefs.com/analytics.js" '
    f'data-key="{AHREFS_KEY}" async></script>'
)
SNIPPET_BLOCK = (
    "<!-- NPCWoods Tracking: Ahrefs Analytics -->\n"
    f"{SNIPPET}\n"
)


def collect_targets() -> list[Path]:
    targets: list[Path] = []
    # 1) every landing-pages/<slug>/index.html
    for p in (REPO_ROOT / "landing-pages").rglob("index.html"):
        targets.append(p)
    # 2) html/<slug>/index.html for the named static-bypass pages
    for slug in ("about", "experience", "pharmacy", "pharmacy-partners", "thank-you"):
        p = REPO_ROOT / "html" / slug / "index.html"
        if p.exists():
            targets.append(p)
    return sorted(set(targets))


def transform(html: str) -> tuple[str, str]:
    """Return (new_html, status).

    status ∈ {"updated", "skip_already_present", "error:<reason>"}.
    """
    if AHREFS_KEY in html:
        return html, "skip_already_present"
    open_count = html.count("<head")
    close_count = html.count("</head>")
    if open_count == 0 or close_count == 0:
        return html, "error:no_head"
    if close_count > 1:
        return html, "error:multiple_head_closes"
    # Preserve surrounding indentation: find the </head> line, inject a
    # matching-indent snippet block before it.
    idx = html.rfind("</head>")
    line_start = html.rfind("\n", 0, idx) + 1
    indent = html[line_start:idx]
    if indent.strip():
        indent = ""
    injection = f"{indent}<!-- NPCWoods Tracking: Ahrefs Analytics -->\n{indent}{SNIPPET}\n"
    new_html = html[:line_start] + injection + html[line_start:]
    return new_html, "updated"


def process(target: Path, dry_run: bool) -> str:
    bak = target.with_suffix(target.suffix + ".ahrefs-bak")
    if not bak.exists():
        bak.write_bytes(target.read_bytes())
    original = bak.read_text(encoding="utf-8")
    new_html, status = transform(original)
    if status.startswith("error:"):
        return status
    if status == "skip_already_present":
        return status
    if new_html == original:
        return "no_change"
    if dry_run:
        return "would_update"
    target.write_text(new_html, encoding="utf-8")
    return "updated"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    targets = collect_targets()
    print(f"Found {len(targets)} target files.")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'WRITE'}\n")

    counts = {"updated": 0, "would_update": 0, "skip_already_present": 0,
              "no_change": 0}
    errors: list[tuple[Path, str]] = []
    for t in targets:
        rel = t.relative_to(REPO_ROOT)
        status = process(t, args.dry_run)
        if status.startswith("error:"):
            errors.append((rel, status))
            print(f"[FAIL] {rel} -> {status}")
            continue
        counts[status] = counts.get(status, 0) + 1
        tag = "OK" if status in ("updated", "would_update", "no_change",
                                 "skip_already_present") else status
        print(f"[{tag}] {rel} -> {status}")

    print()
    print("Summary:")
    for k, v in counts.items():
        print(f"  {k:>22}: {v}")
    print(f"  {'errors':>22}: {len(errors)}")
    if errors:
        print("\nErrors:")
        for rel, status in errors:
            print(f"  {rel}: {status}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
