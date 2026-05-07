#!/usr/bin/env python3
"""Prune non-AZ city links from sitemap + condition pages.

Per 2026-04-22 strategy: redirect plugin now 301s all flat-slug city 404s to
hubs (deployed earlier today). This script strips the user-visible nav so
sitemap + UTI/sinus condition pages no longer advertise GA/NC/NM city
sections to humans. Only AZ city links remain in the user-facing link graph.

Targets:
  - landing-pages/sitemap/index.html
  - landing-pages/sinus-infection-treatment/index.html
  - landing-pages/uti-treatment/index.html

Safety:
  - Writes timestamped backup (.precrawl-bak-YYYYMMDD-HHMMSS) before editing
  - Idempotent: text-pattern based removal; 2nd run finds no matches, no-op
  - Dry-run mode prints what WOULD change without touching files

Usage:
    python3 scripts/prune-non-az-city-links-2026-04-22.py --dry-run
    python3 scripts/prune-non-az-city-links-2026-04-22.py
"""
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Cities to strip from link graph. AZ kept implicit by exclusion.
NON_AZ_CITY_TOKENS = [
    # New Mexico
    "albuquerque", "las-cruces", "santa-fe", "rio-rancho", "farmington", "roswell",
    # Georgia
    "atlanta", "athens", "augusta", "dalton", "gainesville-ga", "gainesville",
    # North Carolina
    "charlotte", "hickory", "asheville", "hendersonville", "boone",
]

# Conditions that combine with city tokens to form flat-slug city pages
CONDITIONS = ["uti-treatment", "sinus-infection", "telemedicine"]

TARGETS = [
    ROOT / "landing-pages" / "sitemap" / "index.html",
    ROOT / "landing-pages" / "sinus-infection-treatment" / "index.html",
    ROOT / "landing-pages" / "uti-treatment" / "index.html",
]

# State-section wrappers in the sitemap that should be removed wholesale
# (and any sister sections that ONLY contain non-AZ city links)
STATE_SECTION_HEADERS = [
    "City-Specific Pages &mdash; New Mexico",
    "City-Specific Pages &mdash; Georgia",
    "City-Specific Pages &mdash; North Carolina",
]

# Condition pages use <div class="city-group"> or <div class="city-state"> + <h3>State</h3>
# Strip those whole blocks for non-AZ states (handles orphans + fallback state-hub links)
CONDITION_PAGE_STATE_HEADERS = ["New Mexico", "Georgia", "North Carolina"]


def build_link_patterns():
    """Return regex patterns matching <li>...</li> blocks for non-AZ cities."""
    patterns = []
    # Pattern A: flat-slug condition pages — /{city}-{condition}/
    for city in NON_AZ_CITY_TOKENS:
        for cond in CONDITIONS:
            slug = f"/{city}-{cond}/"
            # Match the entire <li>...</li> line containing this href
            patterns.append(re.compile(
                r'^[ \t]*<li>[^\n]*href="https://npcwoods\.com'
                + re.escape(slug)
                + r'"[^\n]*</li>[ \t]*\n',
                re.MULTILINE,
            ))
    # Pattern B: nested ed-treatment city pages — /ed-treatment/{city}-{state}/
    for state in ("ga", "nc"):
        patterns.append(re.compile(
            r'^[ \t]*<li>[^\n]*href="https://npcwoods\.com/ed-treatment/[a-z\-]+\-'
            + state
            + r'/"[^\n]*</li>[ \t]*\n',
            re.MULTILINE,
        ))
    return patterns


def build_section_pattern(header_html):
    """Match a <div class="sitemap-section">...<h2>{header}</h2>...</div> block."""
    return re.compile(
        r'\n[ \t]*<div class="sitemap-section">\s*\n'
        r'[ \t]*<h2>'
        + re.escape(header_html)
        + r'</h2>\s*\n'
        r'(?:[ \t]*<ul>\s*\n)?'
        r'(?:[ \t]*<li>[^\n]*</li>\s*\n)*'
        r'(?:[ \t]*</ul>\s*\n)?'
        r'[ \t]*</div>\s*\n',
        re.MULTILINE,
    )


def build_condition_page_state_pattern(state_name):
    """Match condition-page state blocks: <div class="(city-group|city-state)">...<h3>{state}</h3>...</div>.

    Catches orphan empty blocks AND blocks with state-hub fallback links
    (e.g., `<a href="/georgia-telemedicine/">Atlanta</a>` which my city-link
    pattern doesn't match because the URL isn't a city slug).
    """
    return re.compile(
        r'\n?[ \t]*<div class="city-(?:group|state)">\s*\n'
        r'[ \t]*<h3>'
        + re.escape(state_name)
        + r'</h3>\s*\n'
        r'(?:[ \t]*<ul>\s*\n)?'
        r'(?:[ \t]*<li>[^\n]*</li>\s*\n)*'
        r'(?:[ \t]*</ul>\s*\n)?'
        r'[ \t]*</div>\s*\n',
        re.MULTILINE,
    )


def prune_file(path: Path, dry_run: bool) -> tuple[int, int]:
    """Prune one file. Returns (links_removed, sections_removed)."""
    if not path.exists():
        print(f"[skip] not found: {path}")
        return (0, 0)

    original = path.read_text(encoding="utf-8")
    text = original

    # 1) Strip individual non-AZ city <li> links
    link_count = 0
    for pat in build_link_patterns():
        new_text, n = pat.subn("", text)
        text = new_text
        link_count += n

    # 2) Strip whole sitemap state-section blocks
    section_count = 0
    for header in STATE_SECTION_HEADERS:
        pat = build_section_pattern(header)
        new_text, n = pat.subn("\n", text)
        text = new_text
        section_count += n

    # 3) Strip condition-page state blocks (city-group / city-state divs)
    for state in CONDITION_PAGE_STATE_HEADERS:
        pat = build_condition_page_state_pattern(state)
        new_text, n = pat.subn("\n", text)
        text = new_text
        section_count += n

    if text == original:
        print(f"[noop] {path.relative_to(ROOT)} — no non-AZ city links found")
        return (0, 0)

    if dry_run:
        print(f"[dry-run] {path.relative_to(ROOT)}: would remove {link_count} <li> links + {section_count} state sections")
        return (link_count, section_count)

    # Write timestamped backup
    ts = time.strftime("%Y%m%d-%H%M%S")
    backup = path.with_suffix(path.suffix + f".precrawl-bak-{ts}")
    backup.write_text(original, encoding="utf-8")

    path.write_text(text, encoding="utf-8")
    print(f"[ok] {path.relative_to(ROOT)}: removed {link_count} <li> links + {section_count} state sections (backup: {backup.name})")
    return (link_count, section_count)


def main(argv):
    dry_run = "--dry-run" in argv

    print(f"[prune-non-az] dry-run: {dry_run}")
    print(f"[prune-non-az] non-AZ city tokens: {len(NON_AZ_CITY_TOKENS)} cities × {len(CONDITIONS)} conditions = {len(NON_AZ_CITY_TOKENS) * len(CONDITIONS)} flat-slug patterns + ed-treatment nested patterns")
    print()

    total_links = 0
    total_sections = 0
    for path in TARGETS:
        l, s = prune_file(path, dry_run)
        total_links += l
        total_sections += s

    print()
    print(f"[summary] {total_links} <li> links and {total_sections} state-section blocks {'would be' if dry_run else ''} removed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
