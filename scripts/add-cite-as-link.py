#!/usr/bin/env python3
"""
Add <link rel="cite-as"> to every static HTML page that has a canonical tag
but is missing cite-as. This tells AI crawlers (ChatGPT, Perplexity, Grok)
which URL to attribute when citing the content — improves AI citation
accuracy and helps consolidate signal to the canonical URL.

Idempotent: safe to re-run.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "landing-pages"

CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)"\s*/?>', re.IGNORECASE)


def process(html: str) -> tuple[str, bool]:
    if 'rel="cite-as"' in html:
        return html, False
    m = CANONICAL_RE.search(html)
    if not m:
        return html, False
    canonical = m.group(1)
    cite_tag = f'<link rel="cite-as" href="{canonical}">'
    new_html = html.replace(m.group(0), m.group(0) + "\n  " + cite_tag, 1)
    return new_html, True


def main() -> None:
    files = sorted(ROOT.rglob("index.html"))
    print(f"Scanning {len(files)} HTML files for cite-as injection")
    added = 0
    skipped = 0
    no_canonical = 0

    for f in files:
        html = f.read_text(encoding="utf-8")
        new_html, changed = process(html)
        if changed:
            f.write_text(new_html, encoding="utf-8")
            rel = f.relative_to(ROOT)
            print(f"  ✓ {rel}")
            added += 1
        elif 'rel="cite-as"' in html:
            skipped += 1
        else:
            no_canonical += 1

    print(f"\nDone. Added cite-as: {added}. Already had: {skipped}. No canonical found: {no_canonical}.")


if __name__ == "__main__":
    main()
