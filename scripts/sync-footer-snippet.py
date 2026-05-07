#!/usr/bin/env python3
"""Propagate html/shared/footer-snippet.html into every page that inlined it.

SAFE two-mode replacement:

  Mode A (marker mode) — page has BOTH:
    <!-- ===== NPCWOODS SITE FOOTER ... -->
    <!-- ===== END SITE FOOTER ===== -->
  → replace the entire region between markers (CSS + footer) with the canonical snippet.

  Mode B (html mode) — page has the <footer class="npc-site-footer"> element but no markers:
  → replace only the <footer>...</footer> HTML element with the snippet's <footer>...</footer>,
    leaving page-level <style> blocks untouched. This avoids the v1 bug where a too-greedy
    regex grabbed page-level CSS and the entire page body.

Idempotent. Writes a `.footer-synced.bak` only on first sync per file.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SNIPPET = ROOT / "html" / "shared" / "footer-snippet.html"
SCAN_DIRS = [ROOT / "html", ROOT / "landing-pages"]

# Mode A boundaries
START_MARKER_RE = re.compile(r"<!--\s*=+\s*NPCWOODS SITE FOOTER.*?-->", re.DOTALL)
END_MARKER = "<!-- ===== END SITE FOOTER ===== -->"
MODE_A_RE = re.compile(
    r"<!--\s*=+\s*NPCWOODS SITE FOOTER.*?<!--\s*=+\s*END SITE FOOTER\s*=+\s*-->",
    re.DOTALL,
)

# Mode B: just the <footer class="npc-site-footer">...</footer> HTML element
MODE_B_RE = re.compile(
    r'<footer class="npc-site-footer">.*?</footer>',
    re.DOTALL,
)

# From the snippet: extract just the <footer>...</footer> HTML for Mode B
SNIPPET_FOOTER_RE = re.compile(
    r'<footer class="npc-site-footer">.*?</footer>',
    re.DOTALL,
)


def main() -> int:
    if not SNIPPET.exists():
        print(f"[fatal] canonical snippet missing: {SNIPPET}", file=sys.stderr)
        return 1
    canonical_full = SNIPPET.read_text(encoding="utf-8").rstrip("\n")
    footer_only_match = SNIPPET_FOOTER_RE.search(canonical_full)
    if not footer_only_match:
        print("[fatal] could not extract <footer> from snippet", file=sys.stderr)
        return 1
    canonical_footer_html = footer_only_match.group(0)

    changed_a = 0
    changed_b = 0
    untouched = 0
    no_match = []

    targets = []
    for root in SCAN_DIRS:
        for html in root.rglob("index.html"):
            if html.name.endswith(".bak"):
                continue
            targets.append(html)

    for path in sorted(targets):
        text = path.read_text(encoding="utf-8")

        # Try Mode A first (full marker-bounded replace)
        if MODE_A_RE.search(text):
            new_text = MODE_A_RE.sub(lambda _: canonical_full, text, count=1)
            mode = "A"
        elif MODE_B_RE.search(text):
            # Mode B: just swap the <footer> HTML element
            new_text = MODE_B_RE.sub(lambda _: canonical_footer_html, text, count=1)
            mode = "B"
        else:
            no_match.append(path)
            continue

        # Sanity: file size should not collapse > 30%
        if len(new_text) < len(text) * 0.7:
            print(f"[ABORT-SAFETY] {path.relative_to(ROOT)}: size would shrink {len(text)}->{len(new_text)} (>30%); skipping")
            continue

        if new_text == text:
            untouched += 1
            continue

        bak = path.with_suffix(path.suffix + ".footer-synced.bak")
        if not bak.exists():
            bak.write_text(text, encoding="utf-8")
        path.write_text(new_text, encoding="utf-8")
        if mode == "A":
            changed_a += 1
        else:
            changed_b += 1
        print(f"[sync:{mode}] {path.relative_to(ROOT)}")

    print()
    print(f"  changed (mode A, full-snippet): {changed_a}")
    print(f"  changed (mode B, footer-only):  {changed_b}")
    print(f"  up-to-date:                      {untouched}")
    print(f"  no match:                        {len(no_match)}")
    for p in no_match[:10]:
        print(f"    - {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
