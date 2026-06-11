#!/usr/bin/env python3
"""Strip the hardcoded Meta pixel from the remaining health-condition pages.

For each target page:
  1. Remove the inline Meta Pixel block (<!-- Meta Pixel Code --> ... <!-- End Meta
     Pixel Code -->), which kills both the fbevents.js loader and the <noscript>
     facebook.com/tr beacon.
  2. Insert the proven fbq no-op stub at the very top of <head> (before the GTM
     loader) so any GTM-injected Meta pixel also short-circuits.

This is the SAME transform applied to the 6 UTI pages on 2026-06-10, extended to
the 14 health pages that never got it. HIPAA: no BAA with Meta; health-condition
pages must not send PageView there.

Idempotent. Edits the working tree only — does NOT deploy. Run with --check to
verify without writing.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    "landing-pages/uti-treatment/index.html",
    "landing-pages/uti-treatment/albuquerque-nm/index.html",
    "landing-pages/uti-treatment/mesa-az/index.html",
    "landing-pages/uti-treatment/scottsdale-az/index.html",
    "landing-pages/uti-treatment/surprise-az/index.html",
    "landing-pages/uti-care/index.html",
    "landing-pages/uti-treatment-online/index.html",
    "landing-pages/dental-pain/index.html",
    "landing-pages/ear-infection-treatment/index.html",
    "landing-pages/ed-treatment/index.html",
    "landing-pages/glp1-weight-loss/index.html",
    "landing-pages/sinus-infection-treatment/index.html",
    "landing-pages/strep-throat-treatment/index.html",
    "landing-pages/conditions/index.html",
]

# Byte-for-byte identical to the stub already live on the 6 UTI pages.
STUB = """<!-- Meta Pixel disabled 2026-06-10: no BAA with Meta — health-condition pages must not send PageView there.
     The stub below also blocks the GTM-injected pixel: Meta's base code starts with `if(f.fbq)return;`,
     so predefining a no-op fbq means fbevents.js never loads on this page. -->
<script>
window.fbq = function () {};
window.fbq.queue = [];
window.fbq.loaded = true;
window.fbq.version = '2.0';
window._fbq = window.fbq;
</script>"""

BLOCK_RE = re.compile(
    r"[ \t]*<!-- Meta Pixel Code -->.*?<!-- End Meta Pixel Code -->[ \t]*\n?",
    re.DOTALL,
)
HEAD_RE = re.compile(r"(<head>\s*?\n)")

# Strings that must NOT survive in a cleaned page.
FORBIDDEN = ['connect.facebook.net', 'facebook.com/tr', 'fbq("init"', "fbq('init'"]
STUB_MARKER = "Meta Pixel disabled 2026-06-10"


def transform(html: str) -> str:
    out = BLOCK_RE.sub("", html, count=1)
    if STUB_MARKER not in out:
        new, n = HEAD_RE.subn(lambda m: m.group(1) + STUB + "\n", out, count=1)
        if n != 1:
            raise RuntimeError("could not locate a single <head> to insert the stub")
        out = new
    return out


def verify(rel: str, html: str) -> None:
    for bad in FORBIDDEN:
        if bad in html:
            raise RuntimeError(f"{rel}: forbidden marker still present: {bad}")
    if STUB_MARKER not in html:
        raise RuntimeError(f"{rel}: stub marker missing after transform")
    if html.count(STUB_MARKER) != 1:
        raise RuntimeError(f"{rel}: stub inserted {html.count(STUB_MARKER)}x (expected 1)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify only, do not write")
    args = ap.parse_args((argv or sys.argv)[1:])

    changed, clean, errors = 0, 0, 0
    for rel in PAGES:
        path = ROOT / rel
        if not path.exists():
            print(f"[MISS] {rel} — file not found")
            errors += 1
            continue
        html = path.read_text()
        new = transform(html)
        try:
            verify(rel, new)
        except RuntimeError as e:
            print(f"[FAIL] {e}")
            errors += 1
            continue
        if new == html:
            print(f"[ok-already] {rel}")
            clean += 1
            continue
        if args.check:
            print(f"[would-change] {rel}")
            changed += 1
            continue
        path.write_text(new)
        print(f"[stripped] {rel}")
        changed += 1

    print(f"\n{'CHECK' if args.check else 'DONE'}: {changed} changed, {clean} already-clean, {errors} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
