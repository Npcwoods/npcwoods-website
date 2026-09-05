#!/usr/bin/env python3
"""Inject llms.txt alternate + above-the-fold answer block on Wave A money plates.

Kitchen cook. Does not SFTP. Chris yes already given for the inject drafts.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LLMS = (
    '<link rel="alternate" type="application/llms.txt" href="https://npcwoods.com/llms.txt">\n'
    '<link rel="alternate" type="application/llms-full.txt" href="https://npcwoods.com/llms-full.txt">'
)

ATF_STYLE = """<style>
  .npc-atf-answer {
    margin: 16px auto 24px;
    max-width: 65ch;
    padding: 18px 22px;
    border: 1px solid #dbe5f5;
    border-radius: 12px;
    background: #f8fbff;
    font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 1rem;
    line-height: 1.6;
    color: #25364f;
  }
  .npc-atf-answer p { margin: 0; }
  .npc-atf-answer a { color: #1d4ed8; font-weight: 600; }
</style>
"""

GENERIC_ATF = """<div class="npc-atf-answer" data-npc-aeo="atf-answer">
  <p>
    <strong>NPCWoods</strong> is a $59 text visit with Chris Woods, MSN, APRN, FNP-C, a licensed Nurse Practitioner.
    Text <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">(480) 639-4722</a>.
    No video. No app. No chatbot. You must be physically in a licensed state at the time of the visit.
    A prescription is not promised. You only pay if he can treat you.
  </p>
</div>
"""

CITY = {
    "uti-treatment/phoenix-az": ("UTIs", "Phoenix", "Arizona"),
    "uti-treatment/tucson-az": ("UTIs", "Tucson", "Arizona"),
    "uti-treatment/mesa-az": ("UTIs", "Mesa", "Arizona"),
    "uti-treatment/scottsdale-az": ("UTIs", "Scottsdale", "Arizona"),
    "uti-treatment/surprise-az": ("UTIs", "Surprise", "Arizona"),
    "uti-treatment/chandler-az": ("UTIs", "Chandler", "Arizona"),
    "uti-treatment/gilbert-az": ("UTIs", "Gilbert", "Arizona"),
    "uti-treatment/glendale-az": ("UTIs", "Glendale", "Arizona"),
    "uti-treatment/tempe-az": ("UTIs", "Tempe", "Arizona"),
    "uti-treatment/atlanta-ga": ("UTIs", "Atlanta", "Georgia"),
    "uti-treatment/charlotte-nc": ("UTIs", "Charlotte", "North Carolina"),
    "uti-treatment/woodstock-ga": ("UTIs", "Woodstock", "Georgia"),
    "uti-treatment/albuquerque-nm": ("UTIs", "Albuquerque", "New Mexico"),
    "uti-treatment/denver-co": ("UTIs", "Denver", "Colorado"),
    "uti-treatment/reno-nv": ("UTIs", "Reno", "Nevada"),
    "sinus-infection-treatment/phoenix-az": ("sinus infections", "Phoenix", "Arizona"),
    "sinus-infection-treatment/tucson-az": ("sinus infections", "Tucson", "Arizona"),
    "sinus-infection-treatment/mesa-az": ("sinus infections", "Mesa", "Arizona"),
    "sinus-infection-treatment/scottsdale-az": ("sinus infections", "Scottsdale", "Arizona"),
    "sinus-infection-treatment/chandler-az": ("sinus infections", "Chandler", "Arizona"),
    "dental-pain/gainesville-ga": ("dental pain", "Gainesville", "Georgia"),
}


STATE = {
    "arizona-telemedicine": "Arizona",
    "colorado-telemedicine": "Colorado",
    "georgia-telemedicine": "Georgia",
    "idaho-telemedicine": "Idaho",
    "iowa-telemedicine": "Iowa",
    "montana-telemedicine": "Montana",
    "nevada-telemedicine": "Nevada",
    "new-mexico-telemedicine": "New Mexico",
    "north-carolina-telemedicine": "North Carolina",
    "oregon-telemedicine": "Oregon",
    "utah-telemedicine": "Utah",
}

WAVE_B = [
    "landing-pages/uti-treatment/denver-co/index.html",
    "landing-pages/uti-treatment/reno-nv/index.html",
    "landing-pages/pink-eye-treatment/index.html",
    "landing-pages/conditions/index.html",
    "html/about/index.html",
    "landing-pages/arizona-telemedicine/index.html",
    "landing-pages/colorado-telemedicine/index.html",
    "landing-pages/georgia-telemedicine/index.html",
    "landing-pages/idaho-telemedicine/index.html",
    "landing-pages/iowa-telemedicine/index.html",
    "landing-pages/montana-telemedicine/index.html",
    "landing-pages/nevada-telemedicine/index.html",
    "landing-pages/new-mexico-telemedicine/index.html",
    "landing-pages/north-carolina-telemedicine/index.html",
    "landing-pages/oregon-telemedicine/index.html",
    "landing-pages/utah-telemedicine/index.html",
]

HERO_SECTION_RE = re.compile(
    r'(<section\b[^>]*class="[^"]*(?:nl-hero|about-hero|(?<![\w-])hero(?![\w-]))[^"]*"[^>]*>'
    r"[\s\S]*?</section>)",
    re.I,
)

CONDITION = {
    "pink-eye-treatment": "pink eye",
}


def city_atf(cond: str, city: str, state: str) -> str:
    return f"""<div class="npc-atf-answer" data-npc-aeo="atf-answer">
  <p>
    <strong>NPCWoods Telemedicine</strong> reviews {cond} in {city}, {state} for <strong>$59</strong> by text.
    You must be physically in {state} or another licensed state at the time of the visit.
    Text <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">(480) 639-4722</a>.
    A prescription is not promised. You only pay if he can treat you.
  </p>
</div>
"""


def wave_a() -> list[Path]:
    roots = [
        ROOT / "landing-pages" / "uti-treatment",
        ROOT / "landing-pages" / "sinus-infection-treatment",
        ROOT / "landing-pages" / "strep-throat-treatment",
        ROOT / "landing-pages" / "ear-infection-treatment",
        ROOT / "landing-pages" / "dental-pain",
        ROOT / "landing-pages" / "ed-treatment",
        ROOT / "landing-pages" / "glp1-weight-loss",
        ROOT / "landing-pages" / "how-it-works",
        ROOT / "landing-pages" / "pricing",
        ROOT / "landing-pages" / "credentials",
        ROOT / "landing-pages" / "faq",
    ]
    out: list[Path] = []
    for root in roots:
        if root.is_file():
            continue
        if (root / "index.html").exists():
            out.append(root / "index.html")
        if root.is_dir():
            for child in sorted(root.glob("*/index.html")):
                if "search-safe" in child.as_posix() or "_search-safe" in child.as_posix():
                    continue
                out.append(child)
    return out


def inject_llms(html: str) -> str:
    if "application/llms.txt" in html:
        return html
    if "</head>" not in html:
        return html
    return html.replace("</head>", LLMS + "\n</head>", 1)


def inject_atf(html: str, block: str) -> str:
    if 'data-npc-aeo="atf-answer"' in html:
        return html
    insert = ATF_STYLE + block
    m = HERO_SECTION_RE.search(html)
    if m:
        return html[: m.end()] + "\n" + insert + html[m.end() :]
    m = re.search(r"(<h1[\s\S]*?</section>)", html, re.I)
    if not m:
        return html
    return html[: m.end()] + "\n" + insert + html[m.end() :]


def state_atf(state: str) -> str:
    return f"""<div class="npc-atf-answer" data-npc-aeo="atf-answer">
  <p>
    <strong>NPCWoods</strong> is a $59 text visit with Chris Woods, MSN, APRN, FNP-C, a licensed Nurse Practitioner.
    Licensed in {state}. Text <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">(480) 639-4722</a>.
    No video. No app. No chatbot. You must be physically in {state} or another licensed state at the time of the visit.
    A prescription is not promised. You only pay if he can treat you.
  </p>
</div>
"""


def condition_atf(cond: str) -> str:
    return f"""<div class="npc-atf-answer" data-npc-aeo="atf-answer">
  <p>
    <strong>NPCWoods Telemedicine</strong> reviews {cond} for <strong>$59</strong> by text.
    You must be physically in a licensed state at the time of the visit.
    Text <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">(480) 639-4722</a>.
    A prescription is not promised. You only pay if he can treat you.
  </p>
</div>
"""


def byline_html() -> str:
    raw = (ROOT / "html" / "shared" / "eeat-clinician-byline.html").read_text(encoding="utf-8")
    start = raw.find("<style>")
    end = raw.rfind("</section>") + len("</section>")
    chunk = raw[start:end]
    chunk = chunk.replace("2026-06-24", "2026-09-04")
    chunk = chunk.replace("June 24, 2026", "September 4, 2026")
    return chunk + "\n"


def inject_byline(html: str) -> str:
    if "npc-clinician-byline" in html:
        return html
    block = byline_html()
    m = re.search(r'(<div class="npc-atf-answer"[^>]*>[\s\S]*?</div>)', html)
    if m:
        return html[: m.end()] + "\n" + block + html[m.end() :]
    m = HERO_SECTION_RE.search(html)
    if m:
        return html[: m.end()] + "\n" + block + html[m.end() :]
    return html


def rel_key(path: Path) -> str:
    try:
        return path.relative_to(ROOT / "landing-pages").as_posix().replace("/index.html", "")
    except ValueError:
        return path.relative_to(ROOT).as_posix().replace("/index.html", "")


def atf_for(rel: str) -> str:
    if rel in CITY:
        return city_atf(*CITY[rel])
    if rel in STATE:
        return state_atf(STATE[rel])
    if rel in CONDITION:
        return condition_atf(CONDITION[rel])
    return GENERIC_ATF


def load_strip():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "strip_health_page_ad_pixels",
        ROOT / "scripts" / "strip_health_page_ad_pixels.py",
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    n_llms = n_atf = 0
    for path in wave_a():
        html = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT / "landing-pages").as_posix().replace("/index.html", "")
        new = inject_llms(html)
        if new != html:
            n_llms += 1
            html = new
        block = atf_for(rel)
        new = inject_atf(html, block)
        if new != html:
            n_atf += 1
            html = new
        if html != path.read_text(encoding="utf-8"):
            path.write_text(html, encoding="utf-8")
            print(f"[ok] {rel}")
    print(f"[done] llms={n_llms} atf={n_atf}")
    return 0


def main_wave_b() -> int:
    strip = load_strip()
    n_llms = n_atf = n_byline = n_pixel = 0
    for rel in WAVE_B:
        path = ROOT / rel
        html = path.read_text(encoding="utf-8")
        original = html
        stripped = strip.transform(html)
        if stripped != html:
            n_pixel += 1
            html = stripped
        key = rel_key(path)
        new = inject_llms(html)
        if new != html:
            n_llms += 1
            html = new
        new = inject_atf(html, atf_for(key))
        if new != html:
            n_atf += 1
            html = new
        new = inject_byline(html)
        if new != html:
            n_byline += 1
            html = new
        if html != original:
            path.write_text(html, encoding="utf-8")
            print(f"[ok] {rel}")
        else:
            print(f"[skip] {rel}")
    print(f"[done] pixel={n_pixel} llms={n_llms} atf={n_atf} byline={n_byline}")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--wave-b", action="store_true", help="Denver/Reno/state hubs/about/conditions/pink-eye")
    args = parser.parse_args()
    raise SystemExit(main_wave_b() if args.wave_b else main())
