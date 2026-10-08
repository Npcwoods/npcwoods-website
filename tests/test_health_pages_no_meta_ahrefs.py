"""Health pages must never carry Meta Pixel or Ahrefs tracker code.

NPCWoods has no BAA with Meta or Ahrefs (HIPAA). Chris approved scrubbing
the repo copies of every health / condition / medication / treatment / blog
page on 2026-10-08. This test fails if any of those pages under
landing-pages/ (plus the root blog/ folder) ships live (uncommented) Meta
Pixel or Ahrefs code again, and requires the no-op fbq stub on every page
that was scrubbed.

Non-health pages (homepage, about, state/place pages, /pay/, employers...)
are intentionally out of scope here.

Run: cd tests && python3 -m unittest test_health_pages_no_meta_ahrefs
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

FORBIDDEN = {
    "Meta site pixel id": re.compile(r"1428464038973925"),
    "Meta ads pixel id": re.compile(r"1558261907814968"),
    "Meta fbevents.js loader": re.compile(r"fbevents\.js", re.I),
    "Meta connect.facebook.net": re.compile(r"connect\.facebook\.net", re.I),
    "Meta noscript facebook.com/tr": re.compile(r"facebook\.com/tr\b", re.I),
    "fbq('init'/'track') call": re.compile(r"""fbq\s*\(\s*['"]"""),
    "Ahrefs analytics.js": re.compile(r"analytics\.ahrefs\.com", re.I),
    "Ahrefs data-key": re.compile(r"1qFceGSHKP6yg4JlSdNJ4Q"),
}

STUB = (
    "<script>\n"
    "window.fbq = function () {};\n"
    "window.fbq.queue = [];\n"
    "window.fbq.loaded = true;\n"
    "window.fbq.version = '2.0';\n"
    "window._fbq = window.fbq;\n"
    "</script>\n"
)

# Path fragments that mark a page as health / condition / medication /
# treatment / patient-education / blog content.
HEALTH_MARKERS = (
    "uti",
    "sinus",
    "strep",
    "ear-infection",
    "tooth",
    "dental",
    "learn/",
    "medications/",
    "ed-treatment",
    "glp1",
    "yeast",
    "antibiotics",
    "conditions/",
    "poison-ivy",
    "cold-sore",
    "pink-eye",
    "impetigo",
    "nausea",
    "albuterol",
    "treatment",
    "blog",
    "llmseo/",
    "faq/",
)

# Contain a marker substring but are not health pages.
NOT_HEALTH = (
    "landing-pages/executive/",          # "executive" contains "uti"
    "landing-pages/homepage-redesign-preview/",
)

# Every page scrubbed on 2026-10-08 must keep the no-op stub as its first script.
SCRUBBED_20261008 = (
    "blog/can-nurse-practitioner-prescribe-antibiotics-by-text/index.html",
    "blog/dental-pain-cant-get-a-dentist/index.html",
    "blog/urgent-care-in-your-pocket/index.html",
    "landing-pages/arizona-uti-treatment/index.html",
    "landing-pages/blog/impetigo-signs-treatment/index.html",
    "landing-pages/blog/index.html",
    "landing-pages/cold-sore-treatment/index.html",
    "landing-pages/conditions/albuterol-inhaler-refill-preview/index.html",
    "landing-pages/conditions/index.html",
    "landing-pages/conditions/nausea-vomiting-treatment/index.html",
    "landing-pages/conditions/poison-ivy-treatment/index.html",
    "landing-pages/dental-pain/gainesville-ga/index.html",
    "landing-pages/dental-pain/index.html",
    "landing-pages/do-i-need-antibiotics-sinus-infection/index.html",
    "landing-pages/ear-infection-treatment/index.html",
    "landing-pages/ed-treatment/index.html",
    "landing-pages/faq/index.html",
    "landing-pages/glp1-weight-loss/index.html",
    "landing-pages/llmseo/blog-burning-when-you-pee-albuquerque.html",
    "landing-pages/medications/index.html",
    "landing-pages/pink-eye-treatment/index.html",
    "landing-pages/poison-ivy/index.html",
    "landing-pages/sinus-infection-treatment/index.html",
    "landing-pages/sinus-infection-treatment/chandler-az/index.html",
    "landing-pages/sinus-infection-treatment/mesa-az/index.html",
    "landing-pages/sinus-infection-treatment/scottsdale-az/index.html",
    "landing-pages/sinus-infection-treatment/tucson-az/index.html",
    "landing-pages/strep-throat-treatment/index.html",
    "landing-pages/uti-care/index.html",
    "landing-pages/uti-treatment-online/index.html",
    "landing-pages/uti-treatment/index.html",
    "landing-pages/uti-treatment/albuquerque-nm/index.html",
    "landing-pages/uti-treatment/atlanta-ga/index.html",
    "landing-pages/uti-treatment/burning-when-i-pee/index.html",
    "landing-pages/uti-treatment/chandler-az/index.html",
    "landing-pages/uti-treatment/charlotte-nc/index.html",
    "landing-pages/uti-treatment/gilbert-az/index.html",
    "landing-pages/uti-treatment/glendale-az/index.html",
    "landing-pages/uti-treatment/is-my-uti-getting-worse/index.html",
    "landing-pages/uti-treatment/mesa-az/index.html",
    "landing-pages/uti-treatment/no-video-uti-treatment/index.html",
    "landing-pages/uti-treatment/scottsdale-az/index.html",
    "landing-pages/uti-treatment/surprise-az/index.html",
    "landing-pages/uti-treatment/tempe-az/index.html",
    "landing-pages/uti-treatment/uti-antibiotics-online/index.html",
    "landing-pages/when-to-see-provider-for-uti/index.html",
)


def is_health_page(rel: str) -> bool:
    rel = rel.lower()
    if any(rel.startswith(skip) for skip in NOT_HEALTH):
        return False
    if rel.startswith("blog/"):
        return True
    return any(marker in rel for marker in HEALTH_MARKERS)


def health_pages() -> list[Path]:
    pages: list[Path] = []
    for base in ("landing-pages", "blog"):
        for path in sorted((ROOT / base).rglob("*.html")):
            rel = path.relative_to(ROOT).as_posix()
            if is_health_page(rel):
                pages.append(path)
    return pages


def live_markers(html: str) -> list[str]:
    live = COMMENT_RE.sub("", html)
    return [name for name, rx in FORBIDDEN.items() if rx.search(live)]


class HealthPagesNoMetaAhrefsTest(unittest.TestCase):
    def test_classifier_finds_the_health_pages(self):
        rels = {p.relative_to(ROOT).as_posix() for p in health_pages()}
        self.assertGreater(len(rels), 100)
        self.assertIn("landing-pages/medications/amoxicillin/index.html", rels)
        self.assertIn("landing-pages/uti-treatment/index.html", rels)
        self.assertIn("landing-pages/llmseo/blog-burning-when-you-pee-albuquerque.html", rels)
        self.assertNotIn("landing-pages/executive/index.html", rels)
        self.assertNotIn("landing-pages/pay/index.html", rels)

    def test_no_health_page_has_meta_or_ahrefs_markers(self):
        offenders = {}
        for path in health_pages():
            hits = live_markers(path.read_text(encoding="utf-8", errors="replace"))
            if hits:
                offenders[path.relative_to(ROOT).as_posix()] = hits
        self.assertFalse(
            offenders,
            "Meta/Ahrefs tracker code found on health pages (no BAA, HIPAA):\n"
            + "\n".join(f"  {k}: {', '.join(v)}" for k, v in sorted(offenders.items())),
        )

    def test_every_medication_page_is_clean_and_stubbed(self):
        meds = sorted((ROOT / "landing-pages" / "medications").rglob("index.html"))
        self.assertGreaterEqual(len(meds), 22)  # 21 drug pages + index
        for path in meds:
            with self.subTest(page=path.relative_to(ROOT).as_posix()):
                html = path.read_text(encoding="utf-8")
                self.assertEqual(live_markers(html), [])
                self.assertIn(STUB, html)

    def test_scrubbed_pages_have_noop_stub_as_first_script(self):
        for rel in SCRUBBED_20261008:
            with self.subTest(page=rel):
                html = (ROOT / rel).read_text(encoding="utf-8")
                first = html.find("<script")
                self.assertNotEqual(first, -1)
                self.assertTrue(
                    html[first:].startswith(STUB),
                    f"{rel}: first <script> must be the no-op fbq stub",
                )

    def test_stub_matches_learn_hub_exactly(self):
        learn = (ROOT / "landing-pages" / "learn" / "index.html").read_text(encoding="utf-8")
        self.assertIn(STUB, learn)

    def test_detector_catches_real_tracker_code(self):
        sample = (
            "<head><script>!function(f,b,e,v,n,t,s){}(window,document,'script',"
            "'https://connect.facebook.net/en_US/fbevents.js');"
            "fbq('init', '1428464038973925');fbq('track', 'PageView');</script>"
            '<noscript><img src="https://www.facebook.com/tr?id=1428464038973925&ev=PageView&noscript=1"/></noscript>'
            '<script src="https://analytics.ahrefs.com/analytics.js" data-key="1qFceGSHKP6yg4JlSdNJ4Q" async></script>'
            "</head>"
        )
        self.assertEqual(set(live_markers(sample)), set(FORBIDDEN) - {"Meta ads pixel id"})
        # Explanatory HTML comments that mention fbevents.js are fine.
        self.assertEqual(live_markers("<!-- fbevents.js never loads -->" + STUB), [])


if __name__ == "__main__":
    unittest.main()
