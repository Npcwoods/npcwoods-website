"""Lock 2026-08-24 North GA kitchen plates. Git only. Not live."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMS = "sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit"
LOCKED_911 = (
    "Text-based telehealth is not for emergencies. "
    "If you have chest pain, trouble breathing, or other emergency symptoms, call 911."
)
HIPAA = "GTM, GA4, and Google Ads stay off this health-condition page (no BAA)."
FOOTER_MARK = "<!-- ===== NPCWOODS SITE FOOTER (Shared Component) ===== -->"
INSURANCE = re.compile(r"\binsurance\b", re.I)
DOCTOR = re.compile(r"\b(doctor|physician|MD)\b")
# "not a physician" is a credential disclosure already used in grocery copy.
PHYSICIAN_OK = re.compile(r"not a physician", re.I)

PAGES = {
    "landing-pages/uti-treatment/woodstock-ga/index.html": {
        "title": "UTI Treatment in Woodstock, GA | $59 Text Visit",
        "h1": "UTI in Woodstock and you don’t want the waiting room? Text Chris.",
        "url": "https://npcwoods.com/uti-treatment/woodstock-ga/",
        "local": "Highway 92",
        "forbidden": ("Atlanta", "Piedmont", "Grady", "Banner", "Wellstar", "Northside", "Peachtree", "Kennestone"),
        "min_bytes": 50000,
        "health": True,
    },
    "landing-pages/uti-treatment/canton-ga/index.html": {
        "title": "UTI Treatment in Canton, GA | $59 Text Visit",
        "h1": "UTI in Canton and you don’t want the Riverstone waiting room? Text Chris.",
        "url": "https://npcwoods.com/uti-treatment/canton-ga/",
        "local": "Riverstone",
        "forbidden": ("Atlanta", "Piedmont", "Grady", "Banner", "Wellstar", "Northside", "Peachtree", "Kennestone"),
        "min_bytes": 50000,
        "health": True,
    },
    "landing-pages/skip-the-urgent-care-woodstock-ga/index.html": {
        "title": "7 reasons people in Woodstock skip the urgent-care lobby | $59 text visit",
        "h1": "7 reasons people in Woodstock skip the urgent-care lobby",
        "url": "https://npcwoods.com/skip-the-urgent-care-woodstock-ga/",
        "local": "Towne Lake",
        "forbidden": ("Banner", "Wellstar", "Piedmont", "Northside", "Peachtree", "Kennestone"),
        "min_bytes": 8000,
        "health": False,
    },
    "landing-pages/urgent-care-vs-text-visit-cobb-county/index.html": {
        "title": "Urgent care vs a $59 text visit in Cobb County | NPCWoods",
        "h1": "Urgent care vs a $59 text visit in Cobb County",
        "url": "https://npcwoods.com/urgent-care-vs-text-visit-cobb-county/",
        "local": "East Cobb",
        "forbidden": ("Banner", "Wellstar", "Piedmont", "Northside", "Peachtree", "Kennestone"),
        "min_bytes": 8000,
        "health": False,
    },
    "landing-pages/canton-ga-urgent-care-text-visit/index.html": {
        "title": "5 things Canton GA urgent care can treat that you can also text an NP about",
        "h1": "5 things Canton GA urgent care can treat that you can also text an NP about",
        "url": "https://npcwoods.com/canton-ga-urgent-care-text-visit/",
        "local": "Riverstone",
        "forbidden": ("Banner", "Wellstar", "Piedmont", "Northside", "Peachtree", "Kennestone", "CHOA"),
        "min_bytes": 8000,
        "health": False,
    },
    "landing-pages/urgent-care-line-marietta-ga/index.html": {
        "title": "What to do when every urgent care near Marietta has a line | NPCWoods",
        "h1": "What to do when every urgent care near Marietta has a line",
        "url": "https://npcwoods.com/urgent-care-line-marietta-ga/",
        "local": "Delk",
        "forbidden": ("Banner", "Wellstar", "Piedmont", "Northside", "Peachtree", "Kennestone"),
        "min_bytes": 8000,
        "health": False,
    },
    "landing-pages/urgent-care-near-me-cherokee-county/index.html": {
        "title": "Urgent care near me in Cherokee County — and the text option if you cannot leave",
        "h1": "Urgent care near me in Cherokee County",
        "url": "https://npcwoods.com/urgent-care-near-me-cherokee-county/",
        "local": "Holly Springs",
        "forbidden": ("Banner", "Wellstar", "Piedmont", "Northside", "Peachtree", "Kennestone", "CHOA"),
        "min_bytes": 8000,
        "health": False,
    },
}

PLUGIN = ROOT / "php" / "npcwoods-north-ga-pages.php"


class NorthGaKitchenPlateTests(unittest.TestCase):
    def test_plugin_maps_every_plate(self):
        php = PLUGIN.read_text(encoding="utf-8")
        self.assertIn("Serves standalone HTML for Woodstock", php)
        for rel, spec in PAGES.items():
            html_rel = rel.split("landing-pages/", 1)[1]
            self.assertIn(html_rel, php)
            self.assertIn(spec["url"].replace("https://npcwoods.com", "").strip("/").split("/")[-1], php)

    def test_plates_are_real_and_locked(self):
        for rel, spec in PAGES.items():
            path = ROOT / rel
            with self.subTest(rel=rel):
                self.assertTrue(path.exists(), rel)
                self.assertGreaterEqual(path.stat().st_size, spec["min_bytes"])
                html = path.read_text(encoding="utf-8")
                body = html.split(FOOTER_MARK, 1)[0] if FOOTER_MARK in html else html
                self.assertIn(f"<title>{spec['title']}</title>", html)
                self.assertIn(spec["h1"], html)
                self.assertIn(spec["url"], html)
                self.assertIn(spec["local"], body)
                self.assertIn(SMS, html)
                self.assertIn(LOCKED_911, html)
                self.assertIn(FOOTER_MARK, html)
                self.assertTrue(
                    "COOK DRAFT" in html or "Plated 2026-08-28" in html,
                    "kitchen draft mark or plated date",
                )
                self.assertIn("--bg: #05060a", html)
                self.assertIn('class="hero"', html)
                self.assertIn("stats-band", html)
                self.assertIn("bottom-cta", html)
                self.assertNotIn("font-family: Georgia", html)
                self.assertNotRegex(html, INSURANCE)
                leftover = DOCTOR.sub("", PHYSICIAN_OK.sub("", body))
                self.assertNotRegex(leftover, DOCTOR)
                for word in spec["forbidden"]:
                    self.assertNotIn(word, body)
                if spec["health"]:
                    self.assertIn(HIPAA, html)
                    self.assertNotIn("GTM-59QSWZRC", re.sub(r"<!--.*?-->", "", html, flags=re.S))
                self.assertNotIn("content-output/", html)
                self.assertNotIn("/Users/", html)


if __name__ == "__main__":
    unittest.main()
