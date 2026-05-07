#!/usr/bin/env python3
"""Convert render-blocking Google Fonts <link rel="stylesheet"> into a
non-blocking loader using the media="print" swap trick.

Before (blocks render until fonts CSS downloads + parsed):
  <link href="https://fonts.googleapis.com/css2?...&display=swap" rel="stylesheet">

After (browser treats as non-blocking print stylesheet, flips to all once loaded):
  <link rel="preload" as="style" href="...">
  <link rel="stylesheet" href="..." media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="..."></noscript>

Idempotent: detects the `media="print"` marker to avoid double-conversion.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
PATTERN = re.compile(
    r'<link\s+href="(https://fonts\.googleapis\.com/css2\?[^"]+)"\s+rel="stylesheet"\s*/?>',
    re.IGNORECASE,
)
GUARD = 'media="print" onload="this.media'


def build_replacement(href: str) -> str:
    return (
        f'<link rel="preload" as="style" href="{href}">\n'
        f'  <link rel="stylesheet" href="{href}" media="print" onload="this.media=\'all\'">\n'
        f'  <noscript><link rel="stylesheet" href="{href}"></noscript>'
    )


def main():
    targets = []
    for pat in ["html/**/*.html", "landing-pages/**/*.html", "homepage/*.php"]:
        for p in ROOT.glob(pat):
            if p.name.endswith(".bak"):
                continue
            targets.append(p)

    changed = 0
    already = 0
    for path in sorted(targets):
        text = path.read_text(encoding="utf-8")
        if GUARD in text:
            already += 1
            continue
        m = PATTERN.search(text)
        if not m:
            continue
        href = m.group(1)
        new_text = PATTERN.sub(lambda _, h=href: build_replacement(h), text, count=1)
        # re-run in case multiple <link> exist on same page (rare)
        while PATTERN.search(new_text):
            m2 = PATTERN.search(new_text)
            if not m2:
                break
            new_text = PATTERN.sub(
                lambda _, h=m2.group(1): build_replacement(h), new_text, count=1
            )
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
            print(f"[unblock] {path.relative_to(ROOT)}")

    print()
    print(f"  unblocked: {changed}")
    print(f"  already:   {already}")


if __name__ == "__main__":
    main()
