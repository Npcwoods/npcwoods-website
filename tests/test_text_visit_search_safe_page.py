"""Guardrails for the paid text-visit urgent-care landing page."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "landing-pages" / "online-urgent-care-info" / "search-safe" / "index.html"
ROUTER = ROOT / "php" / "npcwoods-paid-pages.php"


def live_markup(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).lower()


def page_text() -> str:
    if not PAGE.exists():
        raise AssertionError("paid text-visit page is missing")
    return PAGE.read_text(encoding="utf-8")


class TextVisitSearchSafePageTest(unittest.TestCase):
    def test_page_exists_and_has_search_safe_metadata(self):
        text = page_text()
        self.assertIn(
            '<link rel="canonical" href="https://npcwoods.com/online-urgent-care-info/search-safe/">',
            text,
        )
        self.assertRegex(text, r'<meta name="robots" content="[^"]*noindex[^"]*">')
        self.assertIn("window.NPCWoodsPaidSurface = true", text)
        self.assertIn("npc_attribution_last", text)

    def test_page_leads_with_visit_price_and_not_walk_in(self):
        text = page_text()
        for required in (
            "Skip the lobby. Text Chris, NP.",
            "$59 flat fee",
            "not charged if",
            "Not a walk-in",
            "sprains",
            "Call 911",
            "sms:+14806394722",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_live_markup_has_no_medication_sales_language_or_health_pixels(self):
        text = live_markup(page_text())
        forbidden = (
            "clindamycin",
            "amoxicillin",
            "penicillin",
            "antibiotic",
            "prescription",
            "connect.facebook.net",
            "facebook.com/tr",
            "googletagmanager.com",
            "google-analytics.com",
            "googleadservices.com",
            "doubleclick.net",
            "/tracking.js",
        )
        for marker in forbidden:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, text)

    def test_forbidden_marketing_words_are_absent(self):
        text = live_markup(page_text())
        for pattern in (r"\bdoctor\b", r"\bphysician\b", r"\bmd\b", r"\bappointment\b", r"\binsurance\b"):
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, text, flags=re.I))

    def test_router_maps_exact_clean_url(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn(
            "'/online-urgent-care-info/search-safe/' => 'online-urgent-care-info/search-safe/index.html'",
            text,
        )


if __name__ == "__main__":
    unittest.main()
