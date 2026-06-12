#!/usr/bin/env python3
"""Generate search-safe UTI city landing pages from the Mesa template.

The Mesa search-safe page (/uti-treatment/mesa-az/search-safe/) is the proven
RESTRICTED_DRUG_TERMS-safe paid destination for the Jun 11 relaunch. This
script clones it for the other live UTI cities (Scottsdale, Surprise,
Albuquerque) and new Phoenix-metro cities (Chandler, Gilbert, Tempe,
Glendale) so campaigns can scale the moment Mesa proves out.

Pages are written to landing-pages/uti-treatment/{slug}/search-safe/index.html.
This script does NOT deploy anything.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "landing-pages/uti-treatment/mesa-az/search-safe/index.html"

# slug, city, state (state only used when it differs from Arizona)
CITIES = [
    ("scottsdale-az", "Scottsdale", "Arizona", "AZ"),
    ("surprise-az", "Surprise", "Arizona", "AZ"),
    ("chandler-az", "Chandler", "Arizona", "AZ"),
    ("gilbert-az", "Gilbert", "Arizona", "AZ"),
    ("tempe-az", "Tempe", "Arizona", "AZ"),
    ("glendale-az", "Glendale", "Arizona", "AZ"),
    ("albuquerque-nm", "Albuquerque", "New Mexico", "NM"),
]

REQUIRED = [
    "GTM-59QSWZRC",
    "gtag/js?id=G-EFFRQMG8TC",
    "AW-610222919",
    "tracking.js",
    'content="noindex,follow"',
    "Most patients hear back the same day, usually within a few hours.",
]
FORBIDDEN = [
    "connect.facebook.net",
    "facebook.com/tr",
    'fbq("init"',
    "fbq('init'",
    "nitrofurantoin",
    "trimethoprim",
    "macrobid",
    "bactrim",
    "cephalexin",
    "antibiotic",
    "prescription drug",
    "insurance",
]


def build_page(template: str, slug: str, city: str, state: str, abbr: str) -> str:
    html = template.replace("mesa-az", slug)
    html = html.replace("Mesa", city)
    if state != "Arizona":
        html = html.replace("Arizona", state)
        html = html.replace(", AZ", f", {abbr}")
    return html


def check_page(slug: str, html: str) -> list[str]:
    problems = []
    lower = html.lower()
    for marker in REQUIRED:
        if marker not in html:
            problems.append(f"missing required marker: {marker}")
    for bad in FORBIDDEN:
        if bad.lower() in lower:
            problems.append(f"contains forbidden marker: {bad}")
    if slug != "mesa-az" and "Mesa" in html:
        problems.append("leftover 'Mesa' reference")
    if slug.endswith("-nm") and ("Arizona" in html or ", AZ" in html):
        problems.append("leftover Arizona reference on NM page")
    if f"/uti-treatment/{slug}/search-safe/" not in html:
        problems.append("canonical URL not updated")
    return problems


def main() -> int:
    template = TEMPLATE.read_text()
    failures = 0
    for slug, city, state, abbr in CITIES:
        html = build_page(template, slug, city, state, abbr)
        problems = check_page(slug, html)
        if problems:
            failures += 1
            for p in problems:
                print(f"[FAIL] {slug}: {p}")
            continue
        dest = ROOT / "landing-pages" / "uti-treatment" / slug / "search-safe" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html)
        print(f"[ok] {dest.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
