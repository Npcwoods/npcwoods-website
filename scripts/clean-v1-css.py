#!/usr/bin/env python3
"""Surgically remove dead v1 CSS from the NPCWoods homepage.

Reads from a pristine backup (NEVER the target file — per
feedback_splice_script_idempotency.md). Reads the audit manifest TSV.
Removes every DELETE row's line range plus every INVESTIGATE row's
line range plus three explicit JS handler ranges. Validates output.
Bails on >30% shrink. Writes to .candidate, not the live file.

Usage:
    python3 scripts/clean-v1-css.py            # write candidate
    python3 scripts/clean-v1-css.py --dry-run  # preview, no write
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOMEPAGE_DIR = ROOT / "homepage"
SOURCE = HOMEPAGE_DIR / "page-npcwoods-home.php.bak-2026-04-30-pre-css-cleanup"
TARGET = HOMEPAGE_DIR / "page-npcwoods-home.php"
CANDIDATE = HOMEPAGE_DIR / "page-npcwoods-home.php.candidate"
MANIFEST = ROOT / "scripts" / "v1-css-cleanup-manifest-2026-04-30.tsv"

# JS handler ranges to delete in the same pass (per Phase 2 plan)
# Line ranges are 1-indexed, inclusive on both ends.
JS_DELETIONS = [
    (3691, 3703),  # IntersectionObserver for .reveal (handler is dead)
    (3708, 3712),  # window.addEventListener('scroll') -> .scrolled toggle
    (3721, 3739),  # .faq-question click handler (v2 uses <details>)
]

# Validation: these tokens MUST appear in the output
KEEP_TOKENS = [
    "</style>",
    ":root {",
    ".npc-nav",
    ".btn-primary",
    ".site-footer",
    ".mobile-sticky-cta",
    ".home-v2",                      # v2 namespace block intact
    "<!-- STICKY MOBILE CTA -->",    # near footer markup
    "application/ld+json",           # all 3 JSON-LD blocks intact
    "schema.org",                    # @context uses lowercase
    "tracking.js",                   # tracking.js include intact
    "GTM-",                          # GTM intact
    "gtag",                          # gtag config intact
]

# Validation: these tokens MUST NOT appear in the output (selectors we deleted)
DELETED_TOKENS = [
    ".proof-bar {",
    ".answer-first {",
    ".pain-section {",
    ".compare-section {",
    ".testimonials-section",
    ".faq-list",
    ".cta-section {",
    ".btn-secondary {",
    ".btn-ghost {",
    ".btn-inverted {",
    ".reveal.visible",
    ".section-header {",
]

SHRINK_GUARD_PCT = 30  # bail if output is >30% smaller than input


def read_lines(path: Path) -> list[str]:
    with path.open() as f:
        return f.read().splitlines(keepends=True)


def parse_manifest_ranges(manifest_path: Path) -> list[tuple[int, int, str, str]]:
    """Return list of (start_line, end_line, verdict, selector) tuples.

    Only includes DELETE and INVESTIGATE verdicts. KEEP rows are excluded.
    """
    ranges = []
    with manifest_path.open() as f:
        header = f.readline()
        for line in f:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            selector, line_range, verdict = parts[0], parts[1], parts[2]
            if verdict not in ("DELETE", "INVESTIGATE"):
                continue
            try:
                start_str, end_str = line_range.split("-")
                start = int(start_str)
                end = int(end_str)
            except ValueError:
                print(f"[warn] bad line_range '{line_range}' for {selector}", file=sys.stderr)
                continue
            ranges.append((start, end, verdict, selector))
    return ranges


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping/adjacent (start, end) tuples into minimal coverage."""
    if not ranges:
        return []
    sorted_ranges = sorted(ranges)
    merged = [list(sorted_ranges[0])]
    for start, end in sorted_ranges[1:]:
        if start <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [tuple(r) for r in merged]


def remove_ranges(lines: list[str], ranges: list[tuple[int, int]]) -> list[str]:
    """Return lines with every (start, end) range removed (1-indexed, inclusive)."""
    if not ranges:
        return lines[:]
    delete_set = set()
    for start, end in ranges:
        for ln in range(start, end + 1):
            delete_set.add(ln)
    return [line for i, line in enumerate(lines, start=1) if i not in delete_set]


def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv

    if not SOURCE.exists():
        print(f"[fatal] source backup missing: {SOURCE}", file=sys.stderr)
        return 2
    if not MANIFEST.exists():
        print(f"[fatal] manifest missing: {MANIFEST}", file=sys.stderr)
        return 2

    src_lines = read_lines(SOURCE)
    src_bytes = sum(len(line) for line in src_lines)
    print(f"source: {SOURCE.name} — {len(src_lines)} lines, {src_bytes:,} bytes")

    manifest_rows = parse_manifest_ranges(MANIFEST)
    print(f"manifest: {len(manifest_rows)} DELETE+INVESTIGATE rows")

    # Build the merged delete-range set from manifest + manual JS ranges
    raw_ranges = [(s, e) for (s, e, _, _) in manifest_rows] + JS_DELETIONS
    merged = merge_ranges(raw_ranges)
    total_lines_to_remove = sum(end - start + 1 for start, end in merged)
    print(f"merged ranges: {len(merged)} contiguous blocks, {total_lines_to_remove} lines total")

    out_lines = remove_ranges(src_lines, merged)
    out_bytes = sum(len(line) for line in out_lines)
    delta_lines = len(src_lines) - len(out_lines)
    delta_bytes = src_bytes - out_bytes
    pct_shrink = (delta_bytes / src_bytes) * 100
    print(f"output: {len(out_lines)} lines, {out_bytes:,} bytes")
    print(f"delta: -{delta_lines} lines, -{delta_bytes:,} bytes ({pct_shrink:.1f}% shrink)")

    # Safety guard
    if pct_shrink > SHRINK_GUARD_PCT:
        print(
            f"[fatal] shrink {pct_shrink:.1f}% exceeds {SHRINK_GUARD_PCT}% guard — "
            "refusing to write candidate. Inspect manifest for over-deletion.",
            file=sys.stderr,
        )
        return 3

    # Validation: KEEP tokens must still be present
    out_text = "".join(out_lines)
    missing_keep = [tok for tok in KEEP_TOKENS if tok not in out_text]
    if missing_keep:
        print(
            f"[fatal] validation failed — KEEP tokens missing from output: {missing_keep}",
            file=sys.stderr,
        )
        return 4

    # Validation: 3 JSON-LD blocks intact
    json_ld_count = out_text.count('<script type="application/ld+json">')
    if json_ld_count != 3:
        print(
            f"[fatal] expected 3 JSON-LD blocks, found {json_ld_count}",
            file=sys.stderr,
        )
        return 4

    # Validation: DELETED tokens must NOT remain (we expect 0 hits)
    leftover_deleted = [tok for tok in DELETED_TOKENS if tok in out_text]
    if leftover_deleted:
        print(
            f"[warn] DELETED tokens still present (over-conservative manifest?): {leftover_deleted}",
            file=sys.stderr,
        )
        # warn only — don't fail. Manifest may have missed a follow-on definition.

    # Validation: v2 markup boundary intact
    if '<div class="home-v2">' not in out_text:
        print("[fatal] v2 wrapper div missing", file=sys.stderr)
        return 4

    print()
    print("=== Validation summary ===")
    print(f"  KEEP tokens present: {len(KEEP_TOKENS) - len(missing_keep)}/{len(KEEP_TOKENS)}")
    print(f"  JSON-LD blocks: {json_ld_count}/3")
    print(f"  DELETED tokens leftover: {len(leftover_deleted)} (warn-only)")
    print(f"  v2 wrapper present: yes")
    print()

    if dry_run:
        print("=== DRY RUN — no file written ===")
        print(f"  would write: {CANDIDATE}")
        return 0

    CANDIDATE.write_text(out_text)
    print(f"=== Wrote candidate ===")
    print(f"  {CANDIDATE}")
    print()
    print("Next steps:")
    print(f"  diff -u {SOURCE} {CANDIDATE} | head -60   # spot-check")
    print(f"  python3 -c 'open(\"{TARGET}\").read()'    # sanity")
    print(f"  mv {CANDIDATE} {TARGET}                  # promote when satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
