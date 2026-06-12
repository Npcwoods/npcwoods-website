#!/usr/bin/env python3
"""Generate INDEXABLE organic UTI city pages for the 4 new Phoenix-metro cities.

Companion to the search-safe paid pages. These are the organic-SEO versions
(indexable, full content, real local detail) for Chandler, Gilbert, Tempe,
and Glendale — the cities that so far only have a noindex /search-safe/ page.

Base template: landing-pages/uti-treatment/surprise-az/index.html — the only
organic city page already on the Apple design. We localize the city-specific
blocks with VERIFIED local content (hospitals confirmed via web search
2026-06-11) so these are genuinely local, not near-duplicate doorway pages.

Output: landing-pages/uti-treatment/{slug}/index.html  (note: NOT /search-safe/)
This script does NOT deploy anything.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "landing-pages/uti-treatment/surprise-az/index.html"

# Per-city verified local content. All four cities are in Arizona.
# er_short = natural short name for the "how is this different from the ER" FAQ.
CITIES = {
    "chandler-az": {
        "city": "Chandler",
        "scene_headline": "Local care for Chandler and the East Valley",
        "scene_para": (
            "Chandler grew from a farm town into the heart of the East Valley's tech corridor "
            "— Intel, the historic downtown square, and Chandler Fashion Center. But when a "
            "UTI hits on a weeknight, the wait at an urgent care near Dobson or Frye can still run "
            "an hour or more. Text a $59 visit from home instead of sitting in a lobby."
        ),
        "er_short": "Chandler Regional",
    },
    "gilbert-az": {
        "city": "Gilbert",
        "scene_headline": "Local care for Gilbert families",
        "scene_para": (
            "Gilbert went from a small farm town to one of the fastest-growing, most family-friendly "
            "communities in the country — the Heritage District, Agritopia, and easy nights out "
            "by the water tower. Between kids, work, and everything in between, nobody has time to sit "
            "in an urgent care lobby. Text a $59 visit from home instead."
        ),
        "er_short": "Mercy Gilbert",
    },
    "tempe-az": {
        "city": "Tempe",
        "scene_headline": "Built for Tempe and ASU life",
        "scene_para": (
            "Tempe moves fast — ASU, Mill Avenue, Tempe Town Lake, and a student crowd that "
            "doesn't keep 9-to-5 hours. Campus health closes, urgent care lines stack up, and a UTI "
            "doesn't wait for business hours. A $59 text visit means care from your dorm, apartment, "
            "or office without crossing town."
        ),
        "er_short": "HonorHealth Tempe",
    },
    "glendale-az": {
        "city": "Glendale",
        "scene_headline": "Local care for Glendale and the West Valley",
        "scene_para": (
            "Glendale is the West Valley's game day — State Farm Stadium, Westgate, and the "
            "antique shops of historic downtown. After a Cardinals Sunday or a long week, the last "
            "thing you want is an urgent care wait near Arrowhead. Text a $59 visit and skip the lobby."
        ),
        "er_short": "Banner Thunderbird",
    },
}

REQUIRED = [
    "GTM-59QSWZRC",
    "gtag/js?id=G-EFFRQMG8TC",
    "AW-610222919",
    "tracking.js",
    "window.fbq = function",          # Meta-pixel no-op stub (health page)
]
FORBIDDEN = [
    "connect.facebook.net",          # actual pixel endpoint (the no-op-stub comment mentions
    "facebook.com/tr",               # fbevents.js by name, which is fine — only real loads matter)
    "insurance",
    "surprise-az",                    # leftover template URL
    "Banner Del E. Webb",             # leftover template ER
    "Adelante",                       # leftover template pharmacy
    "West Valley residents",          # leftover template scene headline
    "/assets/towns/",                 # template image we don't have for new cities
]


def localize(base: str, slug: str, data: dict) -> str:
    city = data["city"]
    html = base

    # 1) Local-specific blocks FIRST (before the global Surprise -> City swap)
    html = html.replace(
        "Local care for West Valley residents",
        data["scene_headline"],
    )
    html = html.replace(
        "Surprise is one of the West Valley's fastest-growing communities — spring training, "
        "new neighborhoods, and desert parks. But urgent care hasn't kept pace with the growth. "
        "Banner Urgent Care on Bell and Reems closes at 8. HonorHealth on West Bell closes at 7. "
        "Text a $59 visit instead of waiting.",
        data["scene_para"],
    )
    # remove the template town image + caption (we have no image for the new cities)
    html = re.sub(
        r'\s*<img src="/assets/towns/surprise-az-stadium\.jpg".*?<p class="caption">[^<]*</p>',
        "",
        html,
        flags=re.DOTALL,
    )
    # pharmacy lists -> generic national chains, city-flavored (longer match first)
    html = html.replace(
        "Adelante Pharmacy on Bell Road, Fry's on Waddell, CVS, Walgreens, Walmart",
        f"your {city} CVS, Walgreens, Fry's, or Walmart",
    )
    html = html.replace(
        "Adelante Pharmacy on Bell Road, Fry's on Waddell, CVS, Walgreens — wherever is closest",
        f"your {city} CVS, Walgreens, Fry's, or Walmart — wherever is closest",
    )
    # urgent-care framing -> generic (no fabricated streets)
    html = html.replace(
        "Unlike urgent care on Bell Road that closes at 8",
        "Unlike a local urgent care that closes in the evening",
    )
    # ER name (appears in schema + FAQ)
    html = html.replace("Banner Del E. Webb", data["er_short"])

    # 2) Global swaps. Case-sensitive: "Surprise" (capital) only, so "No surprise
    #    bills" stays intact. URL slug handled separately.
    html = html.replace("surprise-az", slug)
    html = html.replace("Surprise", city)

    # 3) Freshen the modified date
    html = html.replace("2026-05-26", "2026-06-11").replace("May 26, 2026", "June 11, 2026")

    return html


def check(slug: str, city: str, html: str) -> list[str]:
    problems = []
    low = html.lower()
    for m in REQUIRED:
        if m not in html:
            problems.append(f"missing required: {m}")
    for b in FORBIDDEN:
        if b.lower() in low:
            problems.append(f"contains forbidden: {b}")
    if "noindex" in low:
        problems.append("has noindex (organic pages must stay indexable)")
    if f"https://npcwoods.com/uti-treatment/{slug}/" not in html:
        problems.append("canonical URL not localized")
    if "Surprise" in html:
        problems.append("leftover 'Surprise'")
    # self-canonical must NOT point at the /search-safe/ variant
    if "/search-safe/" in html:
        problems.append("unexpected /search-safe/ reference")
    return problems


def main() -> int:
    base = BASE.read_text()
    failures = 0
    for slug, data in CITIES.items():
        html = localize(base, slug, data)
        problems = check(slug, data["city"], html)
        if problems:
            failures += 1
            for p in problems:
                print(f"[FAIL] {slug}: {p}")
            continue
        dest = ROOT / "landing-pages" / "uti-treatment" / slug / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html)
        print(f"[ok] {dest.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
