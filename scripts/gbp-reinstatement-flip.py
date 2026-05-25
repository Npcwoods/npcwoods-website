#!/usr/bin/env python3
"""
GBP Reinstatement Flip Script

One-shot idempotent flip from "GBP placeholder" to "GBP live" state
on the NPCWoods homepage, once the Google Business Profile is
publicly visible again.

Usage:
    python3 gbp-reinstatement-flip.py --gbp-url <URL>
    python3 gbp-reinstatement-flip.py --gbp-url <URL> --dry-run

Reads from a pristine backup created on first run (per memory:
feedback_splice_script_idempotency.md) so repeated runs always
start from the same source and remain idempotent.

Aborts if output shrinks by more than 30% of input (per memory:
feedback_safe_html_block_replace.md).

Does NOT deploy. Run the existing SFTP deploy path after this,
then cache-bust verify per memory: feedback_cf_cache_verification.md.
"""

import argparse
import difflib
import os
import re
import shutil
import sys
from pathlib import Path


REPO = Path(os.environ.get(
    "NPCWOODS_WEBSITE_REPO",
    str(Path(__file__).resolve().parent.parent),
))
HOMEPAGE = REPO / "homepage" / "page-npcwoods-home.php"
BACKUP = REPO / "homepage" / "page-npcwoods-home.php.pre-gbp-flip.bak"

SHRINK_GUARD = 0.70


def ensure_backup(src: Path, backup: Path) -> None:
    if not backup.exists():
        shutil.copy2(src, backup)
        print(f"[backup] created {backup}")
    else:
        print(f"[backup] using existing {backup}")


def flip(source: str, gbp_url: str) -> str:
    """Apply every reinstatement flip. Safe to re-run on already-flipped input."""
    out = source

    # 1. Swap the placeholder href on the hidden CTA.
    out = out.replace('href="#gbp-pending"', f'href="{gbp_url}"')

    # 2. Un-hide the CTA row by removing the inline display:none.
    out = re.sub(
        r'(<div class="testi-cta-row" data-gbp-cta="true")\s+style="display:\s*none;?"(\s*>)',
        r'\1\2',
        out,
    )

    # 3. Inject `sameAs` into the standalone MedicalBusiness schema block.
    #    There are two MedicalBusiness declarations: one inside an earlier
    #    @graph (which already has sameAs via the Organization-style block),
    #    and one standalone block near the end of the file. We target the
    #    latter by matching the @context + @type header that only appears
    #    on the standalone script tag.
    mb_block_pattern = re.compile(
        r'("@context":\s*"https://schema\.org",\s*'
        r'"@type":\s*"MedicalBusiness"[\s\S]*?)'
        r'("aggregateRating":\s*\{[^{}]*\})'
        r'(\s*\})',
        re.MULTILINE,
    )
    m = mb_block_pattern.search(out)
    if m and '"sameAs"' not in m.group(1):
        replacement = (
            f'{m.group(1)}{m.group(2)},\n'
            f'  "sameAs": ["{gbp_url}"]'
            f'{m.group(3)}'
        )
        out = out[:m.start()] + replacement + out[m.end():]

    # 4. Append GBP URL to the Organization entity's existing sameAs array
    #    (currently Facebook + LegitScript).
    org_sameas = re.compile(
        r'("sameAs":\s*\[\s*'
        r'"https://www\.facebook\.com/npcwoods",\s*'
        r'"https://www\.legitscript\.com/websites/\?checker_keywords=npcwoods\.com")'
        r'(\s*\])'
    )
    def org_append(match):
        if gbp_url in match.group(0):
            return match.group(0)
        return f'{match.group(1)},\n        "{gbp_url}"{match.group(2)}'
    out = org_sameas.sub(org_append, out, count=1)

    # 5. Wrap the "50+ Five-star reviews" credential-card stat in a link.
    stat_pattern = re.compile(
        r'<div class="cred-stat">'
        r'<div class="n">50\+</div>'
        r'<div class="l">Five-star reviews</div>'
        r'</div>'
    )
    if stat_pattern.search(out):
        wrapped = (
            f'<a class="cred-stat cred-stat-link" href="{gbp_url}" rel="noopener" '
            f'style="text-decoration:none;color:inherit;display:block;">'
            f'<div class="n">50+</div>'
            f'<div class="l">Five-star reviews &rsaquo;</div>'
            f'</a>'
        )
        out = stat_pattern.sub(wrapped, out, count=1)

    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gbp-url", required=True,
                    help='Public GBP URL (prefer short maps.app.goo.gl link, '
                         'e.g. https://maps.app.goo.gl/xxxxxxx)')
    ap.add_argument("--dry-run", action="store_true",
                    help="Print diff; do not write the homepage file.")
    ap.add_argument("--homepage", type=Path, default=HOMEPAGE)
    ap.add_argument("--backup", type=Path, default=BACKUP)
    args = ap.parse_args()

    if not args.gbp_url.startswith(("https://maps.", "https://www.google.",
                                     "https://g.co/", "https://g.page/",
                                     "https://maps.app.goo.gl/",
                                     "https://search.google.")):
        print(f"[warn] --gbp-url does not look like a Google domain: {args.gbp_url}")

    if not args.homepage.exists():
        sys.exit(f"homepage not found: {args.homepage}")

    ensure_backup(args.homepage, args.backup)

    src = args.backup.read_text()
    out = flip(src, args.gbp_url)

    if len(out) < len(src) * SHRINK_GUARD:
        sys.exit(
            f"[abort] size-shrink guard tripped: "
            f"{len(out)} bytes < {int(SHRINK_GUARD * 100)}% of {len(src)}."
        )

    diff_text = "".join(difflib.unified_diff(
        src.splitlines(keepends=True),
        out.splitlines(keepends=True),
        fromfile="pristine",
        tofile="flipped",
        n=2,
    ))

    if not diff_text:
        print("[no-op] no changes — file already matches flipped state.")
        return

    print(diff_text)

    if args.dry_run:
        print("[dry-run] not writing. Re-run without --dry-run to apply.")
        return

    args.homepage.write_text(out)
    print(f"[done] wrote {args.homepage}")
    print("next: deploy via SFTP, then cache-bust verify "
          "(curl 'https://npcwoods.com/?v=$(date +%s)')")


if __name__ == "__main__":
    main()
