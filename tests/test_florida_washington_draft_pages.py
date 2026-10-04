"""Draft Florida, Washington, and Athens Saturday pages. Git only. Not live."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "php" / "npcwoods-static-pages.php"
SMS = "sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit"
FOOTER_MARK = "<!-- ===== NPCWOODS SITE FOOTER (Shared Component) ===== -->"
HEADER_MARK = "<!-- ===== NPCWOODS SITE HEADER (Shared Component) ===== -->"

PAGES = {
    "florida-vacation-sick-text-visit": {
        "rel": "landing-pages/florida-vacation-sick-text-visit/index.html",
        "h1": "Don't spend a park day in an urgent care waiting room.",
        "sub": "Feeling sick on your Florida trip? Text a nurse practitioner from your hotel, beach chair, or ride line. $59. No video, no waiting room.",
        "canonical": "https://npcwoods.com/florida-vacation-sick-text-visit/",
    },
    "washington-wait-here-not-there": {
        "rel": "landing-pages/washington-wait-here-not-there/index.html",
        "h1": "You could be waiting in a lobby. Or you could be looking at Rainier.",
        "sub": "Text a Washington-licensed nurse practitioner. $59, no video, and you don't have to sit in a lobby.",
        "canonical": "https://npcwoods.com/washington-wait-here-not-there/",
    },
    "washington-rainier-wait-here": {
        "rel": "landing-pages/washington-rainier-wait-here/index.html",
        "h1": "Paradise meadows. Or a waiting room after the drive.",
        "must": ("14,410 feet", "Paradise", "Sunrise", "trailhead", "most glaciated"),
        "canonical": "https://npcwoods.com/washington-rainier-wait-here/",
    },
    "washington-olympic-wait-here": {
        "rel": "landing-pages/washington-olympic-wait-here/index.html",
        "h1": "Hall of Mosses. Or lose the afternoon to a lobby.",
        "must": ("Hoh Rain Forest", "Rialto Beach", "Ruby Beach", "UNESCO World Heritage Site"),
        "canonical": "https://npcwoods.com/washington-olympic-wait-here/",
    },
    "washington-cascades-wait-here": {
        "rel": "landing-pages/washington-cascades-wait-here/index.html",
        "h1": "Rainier over the city. Turquoise at Diablo. Not fluorescent lights.",
        "must": ("Seattle waterfront", "Diablo Lake", "glacial turquoise", "fluorescent"),
        "canonical": "https://npcwoods.com/washington-cascades-wait-here/",
    },
    "athens-saturday-text-visit": {
        "rel": "landing-pages/athens-saturday-text-visit/index.html",
        "h1": "The wait is over by the 4th quarter.",
        "sub": "Kid gets sick at the gate. Text a Georgia nurse practitioner from the tailgate. $59. Meds on the way home if a prescription fits.",
        "canonical": "https://npcwoods.com/athens-saturday-text-visit/",
    },
}

TRACKERS = (
    "GTM-",
    "G-EFFRQMG8TC",
    "AW-610222919",
    "googletagmanager.com",
    "google-analytics.com",
    "connect.facebook.net",
    "facebook.com/tr",
    "fbq(",
    "/tracking.js",
    "analytics.ahrefs",
)

TRADEMARKS = (
    "disney",
    "walt disney",
    "mickey",
    "magic kingdom",
    "epcot",
    "universal studios",
    "seaworld",
    "busch gardens",
    "legoland",
)

FORBIDDEN_BODY = re.compile(r"(?i)\b(doctor|physician|insurance|appointment)\b")
MD_WORD = re.compile(r"\bMD\b")
TEXT_A_DOCTOR = re.compile(r"(?i)text a doctor")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def body_only(html: str) -> str:
    return html.split(FOOTER_MARK, 1)[0] if FOOTER_MARK in html else html


class FloridaWashingtonDraftPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.router = ROUTER.read_text(encoding="utf-8")
        cls.html = {slug: read(spec["rel"]) for slug, spec in PAGES.items()}

    def test_pages_use_shared_header_footer_and_existing_sms_cta(self):
        for slug, spec in PAGES.items():
            html = self.html[slug]
            with self.subTest(slug=slug):
                self.assertIn(HEADER_MARK, html)
                self.assertIn(FOOTER_MARK, html)
                self.assertIn('href="/assets/css/site.css"', html)
                self.assertIn('src="/assets/js/site.js" defer', html)
                self.assertIn(SMS, html)
                self.assertNotIn("calendly", html.lower())
                self.assertNotIn("book.npcwoods", html.lower())
                self.assertIn(spec["h1"], html)
                self.assertIn(f'<link rel="canonical" href="{spec["canonical"]}">', html)

    def test_static_pages_router_uses_unique_slugs_not_a_new_plugin(self):
        self.assertIn("get_post_field", self.router)
        for slug, spec in PAGES.items():
            mapped = spec["rel"].removeprefix("landing-pages/")
            self.assertIn(f'"{slug}" => "{mapped}"', self.router)
        self.assertEqual(self.router.count("add_action"), 1)
        self.assertNotIn("function npcwoods_", self.router)

    def test_authored_copy_has_no_forbidden_words_or_pixels(self):
        for slug, spec in PAGES.items():
            html = self.html[slug]
            page = body_only(html)
            with self.subTest(slug=slug):
                self.assertIsNone(FORBIDDEN_BODY.search(page), page[FORBIDDEN_BODY.search(page).start() - 20:FORBIDDEN_BODY.search(page).end() + 20] if FORBIDDEN_BODY.search(page) else None)
                self.assertIsNone(MD_WORD.search(page))
                self.assertIsNone(TEXT_A_DOCTOR.search(html))
                for token in TRACKERS:
                    self.assertNotIn(token, html)
                self.assertNotIn("Florida-licensed", html)
                self.assertNotIn("florida-licensed", html.lower())

    def test_florida_page_keeps_visible_compliance_and_avoids_park_trademarks(self):
        html = self.html["florida-vacation-sick-text-visit"]
        page = body_only(html)
        self.assertIn(PAGES["florida-vacation-sick-text-visit"]["sub"], html)
        self.assertIn("physically in Florida", page)
        self.assertIn("not licensed as a Florida APRN", page)
        self.assertIn("TPAN3355", page)
        self.assertIn("Out-of-State Telehealth Provider", page)
        self.assertIn("APRN-RNP 320600", page)
        self.assertIn("No controlled substances", page)
        self.assertIn("no in-person office in florida", page.lower())
        self.assertIn("$59 per text visit", page)
        self.assertIn("call 911 or go to the ER", page)
        self.assertIn("Not for emergencies", page)
        self.assertIn("Orlando", page)
        self.assertIn("Miami Beach", page)
        self.assertIn("Fort Lauderdale", page)
        self.assertIn("Destin", page)
        self.assertIn("Tampa", page)
        self.assertIn("Clearwater", page)
        self.assertIn("Panama City Beach", page)
        self.assertIn("the castle", page)
        self.assertIn("Rope-drop", page)
        lowered = html.lower()
        for mark in TRADEMARKS:
            self.assertNotIn(mark, lowered)

    def test_washington_hub_links_unique_companion_slugs(self):
        hub = self.html["washington-wait-here-not-there"]
        self.assertIn(PAGES["washington-wait-here-not-there"]["sub"], hub)
        self.assertIn("ARNP.AP.61670388-NP", hub)
        self.assertIn("physically in Washington", hub)
        self.assertIn('href="/washington-rainier-wait-here/"', hub)
        self.assertIn('href="/washington-olympic-wait-here/"', hub)
        self.assertIn('href="/washington-cascades-wait-here/"', hub)
        self.assertNotIn("/washington-wait-here-not-there/mount-rainier/", hub)
        self.assertNotIn("road closure", hub.lower())
        self.assertNotIn("closures", hub.lower())

    def test_athens_saturday_page_keeps_georgia_license_and_avoids_school_marks(self):
        html = self.html["athens-saturday-text-visit"]
        page = body_only(html)
        self.assertIn(PAGES["athens-saturday-text-visit"]["sub"], html)
        self.assertIn("<title>The wait is over by the 4th quarter | $59 text visit | NPCWoods</title>", html)
        self.assertIn("Georgia nurse practitioner", page)
        self.assertIn("APRN-NP319386", page)
        self.assertIn("RN319386", page)
        self.assertIn("2027-01-31", page)
        self.assertIn("physically in Georgia", page)
        self.assertIn("No controlled substances", page)
        self.assertIn("Saturday in Athens", page)
        self.assertIn("Between the hedges", page)
        self.assertIn("The Arch", page)
        self.assertIn("parent or guardian", page)
        self.assertIn("Not for emergencies", page)
        self.assertIn("call 911", page)
        lowered = html.lower()
        for mark in (
            "university of georgia",
            "bulldogs",
            "bulldog",
            "uga",
            "sanford",
        ):
            self.assertNotIn(mark, lowered)

    def test_companion_pages_are_not_thin_hub_duplicates(self):
        hub = body_only(self.html["washington-wait-here-not-there"])
        for slug in (
            "washington-rainier-wait-here",
            "washington-olympic-wait-here",
            "washington-cascades-wait-here",
        ):
            page = body_only(self.html[slug])
            with self.subTest(slug=slug):
                self.assertIn("ARNP.AP.61670388-NP", page)
                self.assertIn("physically in Washington", page)
                self.assertIn("Not for emergencies", page)
                self.assertIn(SMS, self.html[slug])
                for token in PAGES[slug]["must"]:
                    self.assertIn(token, page)
                self.assertNotEqual(page, hub)
                self.assertGreater(len(page), 8000)
                self.assertNotIn("road closure", page.lower())


if __name__ == "__main__":
    unittest.main()
