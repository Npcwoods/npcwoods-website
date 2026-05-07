#!/usr/bin/env python3
"""Propagate html/shared/header-snippet.html into every page that inlined it.

Idempotent: re-run anytime. Finds the block bounded by the opening
`<!-- ===== NPCWOODS SITE HEADER` comment and `<!-- ===== END SITE HEADER ===== -->`
marker, replaces it with the current canonical snippet.

Skips .bak files. Writes a .bak only on the first sync of a file (never overwrites
an existing .bak).
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SNIPPET = ROOT / "html" / "shared" / "header-snippet.html"
SCAN_DIRS = [ROOT / "html", ROOT / "landing-pages"]
END_MARKER = "<!-- ===== END SITE HEADER ===== -->"
START_RE = re.compile(r"<!--\s*=+\s*NPCWOODS SITE HEADER.*?-->", re.DOTALL)
BLOCK_RE = re.compile(
    r"<!--\s*=+\s*NPCWOODS SITE HEADER.*?<!--\s*=+\s*END SITE HEADER\s*=+\s*-->",
    re.DOTALL,
)
# Mode B fallback: pages that lost the START marker but still have END.
# Match from the SVG icon defs (always the very first element of the header) to END marker.
MODE_B_RE = re.compile(
    r'<svg style="display:none[^"]*"[^>]*>.*?<!--\s*=+\s*END SITE HEADER\s*=+\s*-->',
    re.DOTALL,
)
# From the snippet, extract just the body part (skip the leading comment lines)
SNIPPET_BODY_RE = re.compile(
    r'(<svg style="display:none[^"]*"[^>]*>.*?<!--\s*=+\s*END SITE HEADER\s*=+\s*-->)',
    re.DOTALL,
)


def main() -> int:
    if not SNIPPET.exists():
        print(f"[fatal] canonical snippet missing: {SNIPPET}", file=sys.stderr)
        return 1
    canonical = SNIPPET.read_text(encoding="utf-8").rstrip("\n")
    body_match = SNIPPET_BODY_RE.search(canonical)
    canonical_body = body_match.group(1) if body_match else canonical

    changed_a = 0
    changed_b = 0
    untouched = 0
    no_match = []

    targets = []
    for root in SCAN_DIRS:
        for html in root.rglob("index.html"):
            if html.suffix == ".bak" or html.name.endswith(".bak"):
                continue
            targets.append(html)

    for path in sorted(targets):
        text = path.read_text(encoding="utf-8")
        if BLOCK_RE.search(text):
            new_text = BLOCK_RE.sub(lambda _: canonical, text, count=1)
            mode = "A"
        elif MODE_B_RE.search(text):
            new_text = MODE_B_RE.sub(lambda _: canonical_body, text, count=1)
            mode = "B"
        else:
            no_match.append(path)
            continue

        # Safety: refuse any swap that shrinks the file by more than 30%
        if len(new_text) < len(text) * 0.7:
            print(f"[ABORT-SAFETY] {path.relative_to(ROOT)}: would shrink {len(text)}->{len(new_text)} (>30%); skipping")
            continue

        if new_text == text:
            untouched += 1
            continue
        bak = path.with_suffix(path.suffix + ".synced.bak")
        if not bak.exists():
            bak.write_text(text, encoding="utf-8")
        path.write_text(new_text, encoding="utf-8")
        if mode == "A":
            changed_a += 1
        else:
            changed_b += 1
        print(f"[sync:{mode}] {path.relative_to(ROOT)}")

    print()
    print(f"  changed (mode A, marker-bounded): {changed_a}")
    print(f"  changed (mode B, svg-bounded):    {changed_b}")
    print(f"  up-to-date:                        {untouched}")
    print(f"  no match:                          {len(no_match)}")
    for p in no_match:
        print(f"    - {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
