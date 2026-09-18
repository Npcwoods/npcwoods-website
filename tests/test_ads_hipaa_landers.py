"""Guardrails for the four Ads + HIPAA look-plate landers."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "uti": ROOT / "landing-pages" / "start-uti" / "index.html",
    "sinus": ROOT / "landing-pages" / "start-sinus" / "index.html",
    "dental": ROOT / "landing-pages" / "start-dental" / "index.html",
    "uri": ROOT / "landing-pages" / "start-uri" / "index.html",
}
HEADLINES = {
    "uti": "UTI treatment by text · $59 · same day",
    "sinus": "Day 5–7 and still getting worse?",
    "dental": "Tooth throbbing. Bridge care only.",
    "uri": "Can't shake this cold?",
}
FLIP = ("start-uti", "start-sinus", "start-dental", "start-uri")
PIXEL_MARKERS = (
    "googletagmanager.com",
    "google-analytics.com",
    "googleadservices.com",
    "doubleclick.net",
    "facebook.com/tr",
    "connect.facebook.net",
    "analytics.ahrefs.com",
    "/tracking.js",
    "GTM-59QSWZRC",
    "G-EFFRQMG8TC",
    "G-0VCC0Z4FD7",
    "AW-610222919",
)
FORBIDDEN_MARKETING = (
    r"\binsurance\b",
    r"\bdoctor\b",
    r"\bphysician\b",
    r"Antibiotics, today",
    r"guaranteed",
    r"no exam needed",
)


def live_markup(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


class AdsHipaaLandersTest(unittest.TestCase):
    def test_four_landers_exist_with_flip_nav_and_click_script(self):
        for slug, path in PAGES.items():
            with self.subTest(slug=slug):
                self.assertTrue(path.exists(), f"missing {path}")
                text = path.read_text(encoding="utf-8")
                self.assertIn(HEADLINES[slug], text)
                self.assertIn("$59", text)
                self.assertIn("sms:+14806394722", text)
                self.assertIn("tel:+14806394722", text)
                self.assertIn("ads-click.js", text)
                self.assertIn("window.NPCWoodsPaidSurface = true", text)
                self.assertIn("GTM, GA4, and Google Ads stay off", text)
                self.assertIn('content="noindex', text)
                self.assertIn("Call 911", text)
                self.assertIn("50+ Five-Star Reviews", text)
                self.assertIn("legitscript.com", text)
                self.assertIn("Arizona", text)
                self.assertIn("North Carolina", text)
                self.assertIn("What you get", text)
                self.assertIn("Double board-certified", text)
                for dest in FLIP:
                    self.assertIn(f"/{dest}/", text)
                self.assertIn("Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit", text)
                self.assertNotIn("I think I have a UTI", text)

    def test_live_markup_has_no_pixels_or_site_kit(self):
        for slug, path in PAGES.items():
            with self.subTest(slug=slug):
                live = live_markup(path.read_text(encoding="utf-8")).lower()
                for marker in PIXEL_MARKERS:
                    self.assertNotIn(marker.lower(), live, marker)

    def test_forbidden_marketing_language_stays_out(self):
        for slug, path in PAGES.items():
            with self.subTest(slug=slug):
                live = live_markup(path.read_text(encoding="utf-8"))
                for pattern in FORBIDDEN_MARKETING:
                    self.assertIsNone(re.search(pattern, live, flags=re.I), pattern)

    def test_dental_says_bridge_care_only(self):
        text = PAGES["dental"].read_text(encoding="utf-8")
        self.assertIn("does not replace a dentist", text.lower())
        self.assertIn("no drainage", text.lower())
        live = live_markup(text).lower()
        for banned in ("macrobid", "amoxicillin", "clindamycin", "z-pack"):
            self.assertNotIn(banned, live)

    def test_sinus_is_honest_about_green_mucus(self):
        text = PAGES["sinus"].read_text(encoding="utf-8").lower()
        self.assertIn("green mucus", text)

    def test_uri_refuses_leftover_meds_without_drug_names(self):
        text = PAGES["uri"].read_text(encoding="utf-8")
        live = live_markup(text).lower()
        self.assertIn("viral", live)
        self.assertIn("do not pay", live.replace("’", "'"))
        self.assertIn("leftover meds", live)
        for banned in ("z-pack", "zpack", "azithromycin", "macrobid", "amoxicillin"):
            self.assertNotIn(banned, live)

    def test_uti_does_not_promise_a_script(self):
        text = PAGES["uti"].read_text(encoding="utf-8")
        self.assertIn("A prescription is not promised", text)
        self.assertNotIn("Sending Macrobid", text)


if __name__ == "__main__":
    unittest.main()
