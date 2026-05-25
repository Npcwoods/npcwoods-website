#!/usr/bin/env python3
"""
CWV batch fixes for the top 3 templates.

Idempotent by design: reads every target from its `.cwv-bak` on each run, so re-running
produces the same output. Mirrors the pattern in scripts/update-meta-descriptions.py.

Changes applied per file:
  1. Move the GTM IIFE + gtag/config block out of <head> to just before </body>.
     The <noscript> GTM iframe inside <body> is left alone — it's non-blocking.
  2. Add two preconnects inside <head> right after the fonts.gstatic preconnect:
       - <link rel="preconnect" href="https://npcwoods.com">
       - <link rel="preconnect" href="https://www.googletagmanager.com">

Hero <img> srcset was considered but skipped: the only WP-generated variant for
chris-*.webp is chris-400.webp (verified via curl 2026-04-21). No 768w exists to
populate srcset with, so adding it would create a 404 on larger viewports.

Usage:
    python3 scripts/cwv-batch-fixes.py --dry-run
    python3 scripts/cwv-batch-fixes.py
"""

import argparse
import pathlib
import re
import shutil
import sys
from dataclasses import dataclass, field

REPO = pathlib.Path(__file__).resolve().parent.parent

TARGETS = [
    REPO / "homepage/page-npcwoods-home.php",
    REPO / "landing-pages/uti-treatment/index.html",
    REPO / "landing-pages/uti-treatment/mesa-az/index.html",
]

# Match the GTM IIFE block (multi-line <script>...</script> containing GTM-59QSWZRC).
GTM_IIFE_RE = re.compile(
    r"<script>\(function\(w,d,s,l,i\)\{.*?GTM-59QSWZRC'\);</script>",
    re.DOTALL,
)

# Match the gtag.js async loader + its config block.
GTAG_BLOCK_RE = re.compile(
    r"<script async src=\"https://www\.googletagmanager\.com/gtag/js\?id=G-EFFRQMG8TC\"></script>\s*"
    r"<script>\s*window\.dataLayer.*?gtag\('config', 'AW-610222919'\);\s*</script>",
    re.DOTALL,
)

FONTS_GSTATIC_RE = re.compile(
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>'
)

BODY_CLOSE_RE = re.compile(r"</body>")

EXTRA_PRECONNECTS = (
    '<link rel="preconnect" href="https://npcwoods.com">\n'
    '<link rel="preconnect" href="https://www.googletagmanager.com">'
)

# Marker comment the script inserts along with the GTM block at </body> — lets us
# identify already-moved GTM on re-runs without false matches.
RELOCATED_MARKER = "<!-- NPCWoods CWV: GTM relocated to end of <body> by cwv-batch-fixes.py -->"


@dataclass
class Report:
    file: str
    gtm_moved: bool = False
    preconnects_added: bool = False
    skipped: list = field(default_factory=list)


def ensure_backup(path: pathlib.Path) -> pathlib.Path:
    bak = path.with_suffix(path.suffix + ".cwv-bak")
    if not bak.exists():
        shutil.copy2(path, bak)
    return bak


def apply_fixes(path: pathlib.Path, dry_run: bool) -> Report:
    r = Report(file=str(path.relative_to(REPO)))
    bak = ensure_backup(path)
    original = bak.read_text(encoding="utf-8")
    out = original

    # --- 1. Move GTM IIFE + gtag block to just before </body>
    gtm_match = GTM_IIFE_RE.search(out)
    gtag_match = GTAG_BLOCK_RE.search(out)

    if gtm_match and gtag_match:
        gtm_html = gtm_match.group(0)
        gtag_html = gtag_match.group(0)

        # Remove both blocks from their current position (first occurrence each).
        out = GTM_IIFE_RE.sub("", out, count=1)
        out = GTAG_BLOCK_RE.sub("", out, count=1)

        # Clean up any leftover HTML comment pointer (e.g. "<!-- NPCWoods Tracking: GTM -->")
        # that would otherwise dangle above an empty block.
        out = re.sub(
            r"<!-- NPCWoods Tracking: GTM -->\s*\n",
            "",
            out,
            count=1,
        )

        # Reinsert just before </body>
        body_close = BODY_CLOSE_RE.search(out)
        if body_close:
            insertion = f"\n{RELOCATED_MARKER}\n{gtm_html}\n{gtag_html}\n"
            out = out[: body_close.start()] + insertion + out[body_close.start() :]
            r.gtm_moved = True
        else:
            r.skipped.append("no </body> tag — GTM not relocated")
            return r
    else:
        r.skipped.append("GTM IIFE or gtag block not matched (already moved or markup drifted)")

    # --- 2. Add self-origin + GTM preconnects
    head_fragment = out.split("</head>", 1)[0] if "</head>" in out else out
    already_has_self = 'href="https://npcwoods.com"' in head_fragment and 'rel="preconnect"' in head_fragment
    already_has_gtm = 'href="https://www.googletagmanager.com"' in head_fragment and 'rel="preconnect"' in head_fragment

    if FONTS_GSTATIC_RE.search(out) and not (already_has_self and already_has_gtm):
        out = FONTS_GSTATIC_RE.sub(
            lambda m: m.group(0) + "\n" + EXTRA_PRECONNECTS,
            out,
            count=1,
        )
        r.preconnects_added = True
    elif already_has_self and already_has_gtm:
        r.skipped.append("preconnects already present")
    else:
        r.skipped.append("fonts.gstatic anchor missing — preconnects not added")

    if not dry_run and out != original:
        path.write_text(out, encoding="utf-8")
    return r


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="Report what would change without writing")
    args = ap.parse_args()

    reports = [apply_fixes(p, args.dry_run) for p in TARGETS]
    any_unexpected_skip = False
    for rep in reports:
        print(f"\n=== {rep.file} ===")
        print(f"  GTM moved:        {rep.gtm_moved}")
        print(f"  Preconnects:      {rep.preconnects_added}")
        for msg in rep.skipped:
            print(f"  SKIP: {msg}")
            if "already" not in msg:
                any_unexpected_skip = True

    if args.dry_run:
        print("\n(dry-run: no files written)")
    return 0 if not any_unexpected_skip else 3


if __name__ == "__main__":
    sys.exit(main())
