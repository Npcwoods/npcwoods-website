#!/usr/bin/env python3
"""Regenerate the search-safe UTI city landing pages from a single template.

Template:   landing-pages/uti-treatment/_search-safe-template/template.html
City data:  landing-pages/uti-treatment/_search-safe-template/cities.json
Output:     landing-pages/uti-treatment/<slug>/search-safe/index.html  (only)

Usage:
    python3 scripts/build-search-safe-pages.py              # all cities
    python3 scripts/build-search-safe-pages.py --city mesa-az
    python3 scripts/build-search-safe-pages.py --check      # verify, write nothing

Supersedes scripts/build-uti-search-safe-cities-2026-06-11.py (which spliced
the design from the live surprise-az page at runtime; this one uses a frozen
template so output never drifts when other pages change).

This script does NOT deploy anything. Deploys go through the guarded deploy
flow and require Chris's explicit approval.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "landing-pages" / "uti-treatment" / "_search-safe-template"
DEFAULT_OUT_ROOT = ROOT / "landing-pages" / "uti-treatment"

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_FIELDS = ("slug", "city", "state", "state_abbr", "state_page")

# Guardrails carried over from the original build script.
REQUIRED_MARKERS = [
    "GTM-59QSWZRC",
    "gtag/js?id=G-EFFRQMG8TC",
    "AW-610222919",
    "window.NPCWoodsPaidSurface = true",
    "tracking.js",
    'content="noindex,follow"',
    "Most patients hear back the same day, usually within a few hours.",
]
FORBIDDEN_MARKERS = [
    "connect.facebook.net",
    "facebook.com/tr",
    "fbevents.js",
    "nitrofurantoin",
    "trimethoprim",
    "macrobid",
    "bactrim",
    "cephalexin",
    "phenazopyridine",
    "nystatin",
    "antibiotic",
    "prescription",
    "insurance",
]


def render(template: str, city: dict) -> str:
    return (
        template.replace("{{SLUG}}", city["slug"])
        .replace("{{CITY}}", city["city"])
        .replace("{{STATE_PAGE}}", city["state_page"])
        .replace("{{STATE}}", city["state"])
        .replace("{{ST}}", city["state_abbr"])
    )


def check_page(city: dict, html: str) -> list[str]:
    problems = []
    lower = html.lower()
    for marker in REQUIRED_MARKERS:
        if marker not in html:
            problems.append(f"missing required marker: {marker}")
    for bad in FORBIDDEN_MARKERS:
        if bad.lower() in lower:
            problems.append(f"contains forbidden marker: {bad}")
    if "{{" in html:  # note: literal "}}" exists in nested JSON-LD, so only check "{{"
        problems.append("unrendered placeholder")
    if f"/uti-treatment/{city['slug']}/search-safe/" not in html:
        problems.append("canonical URL not rendered")
    return problems


def out_path(out_root: Path, slug: str) -> Path:
    """The ONLY path this script ever writes: <out_root>/<slug>/search-safe/index.html."""
    if not SLUG_RE.match(slug):
        raise SystemExit(f"refusing unsafe slug: {slug!r}")
    dest = (out_root / slug / "search-safe" / "index.html").resolve()
    if not dest.is_relative_to(out_root.resolve()):
        raise SystemExit(f"refusing to write outside {out_root}: {dest}")
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--city", help="build a single city slug (e.g. mesa-az)")
    ap.add_argument("--check", action="store_true",
                    help="render and compare against files on disk; write nothing")
    ap.add_argument("--out-root", type=Path, default=DEFAULT_OUT_ROOT,
                    help="output root (tests only; default: landing-pages/uti-treatment)")
    args = ap.parse_args()

    template = (TEMPLATE_DIR / "template.html").read_text()
    cities = json.loads((TEMPLATE_DIR / "cities.json").read_text())

    for city in cities:
        missing = [f for f in REQUIRED_FIELDS if not city.get(f)]
        if missing:
            print(f"[FAIL] cities.json entry {city.get('slug', '?')}: missing {missing}")
            return 1

    if args.city:
        cities = [c for c in cities if c["slug"] == args.city]
        if not cities:
            print(f"[FAIL] no city with slug {args.city!r} in cities.json")
            return 1

    failures = 0
    for city in cities:
        html = render(template, city)
        problems = check_page(city, html)
        if problems:
            failures += 1
            for p in problems:
                print(f"[FAIL] {city['slug']}: {p}")
            continue
        dest = out_path(args.out_root, city["slug"])
        if args.check:
            if dest.exists() and dest.read_text() == html:
                print(f"[ok] {city['slug']}: matches {dest}")
            else:
                failures += 1
                print(f"[DIFF] {city['slug']}: rendered output differs from {dest}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html)
        print(f"[ok] wrote {dest}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
