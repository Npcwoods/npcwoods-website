#!/usr/bin/env python3
"""
Inject Person schema + cite-as link into all 21 medication reference pages.

Why: Education pages have Person schema for Chris, but medication pages don't.
This is the single biggest E-E-A-T / AEO gap on /medications/* — fixing it
strengthens author attribution for AI citation across 21 high-intent URLs.

Idempotent: safe to re-run. Skips files that already contain Person schema.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "landing-pages" / "medications"

PERSON_SCHEMA_BLOCK = '''
  <!-- Schema: Person (Chris Woods) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "@id": "https://npcwoods.com/#chris-woods",
    "url": "https://npcwoods.com/about/",
    "name": "Chris Woods",
    "hasCredential": {
      "@type": "EducationalOccupationalCredential",
      "credentialCategory": "license",
      "name": "MSN, APRN, FNP-C"
    },
    "jobTitle": "Licensed Nurse Practitioner",
    "image": "https://npcwoods.com/wp-content/uploads/2026/03/chris-woods-headshot.png",
    "description": "Chris Woods is a Licensed Nurse Practitioner and founder of NPCWoods Telemedicine. He personally reviews every medication guide on the site.",
    "worksFor": {
      "@id": "https://npcwoods.com/#medical-business"
    }
  }
  </script>

'''

# Anchor: insert Person schema right BEFORE the FAQPage schema block
FAQ_ANCHOR = re.compile(r'(\n  <script type="application/ld\+json">\s*\n\s*\{\s*\n\s*"@context": "https://schema\.org",\s*\n\s*"@type": "FAQPage")')


def inject_person_schema(html: str) -> tuple[str, bool]:
    """Insert Person schema before FAQPage block. Return (new_html, changed)."""
    # Idempotency: skip if Person schema already present
    if '"@id": "https://npcwoods.com/#chris-woods"' in html or '"@type": "Person"' in html:
        return html, False
    new_html, count = FAQ_ANCHOR.subn(PERSON_SCHEMA_BLOCK + r'\1', html, count=1)
    if count == 0:
        return html, False
    return new_html, True


def inject_cite_as(html: str, canonical_url: str) -> tuple[str, bool]:
    """Add <link rel="cite-as"> after the canonical link tag."""
    if 'rel="cite-as"' in html:
        return html, False
    # Insert right after the canonical tag
    pattern = re.compile(r'(<link rel="canonical" href="' + re.escape(canonical_url) + r'">)')
    replacement = r'\1\n  <link rel="cite-as" href="' + canonical_url + '">'
    new_html, count = pattern.subn(replacement, html, count=1)
    return new_html, count > 0


def derive_canonical(file_path: Path) -> str:
    slug = file_path.parent.name
    return f"https://npcwoods.com/medications/{slug}/"


def main() -> None:
    files = sorted(ROOT.glob("*/index.html"))
    if not files:
        print(f"No medication pages found under {ROOT}")
        return

    print(f"Found {len(files)} medication pages")
    person_added = 0
    cite_added = 0
    skipped = 0

    for f in files:
        html = f.read_text(encoding="utf-8")
        canonical = derive_canonical(f)

        new_html, p_changed = inject_person_schema(html)
        new_html, c_changed = inject_cite_as(new_html, canonical)

        if p_changed or c_changed:
            f.write_text(new_html, encoding="utf-8")
            tags = []
            if p_changed:
                tags.append("Person")
                person_added += 1
            if c_changed:
                tags.append("cite-as")
                cite_added += 1
            print(f"  ✓ {f.parent.name}: {' + '.join(tags)}")
        else:
            print(f"  - {f.parent.name}: already done")
            skipped += 1

    print(f"\nDone. Person schema added: {person_added}. cite-as added: {cite_added}. Skipped: {skipped}.")


if __name__ == "__main__":
    main()
