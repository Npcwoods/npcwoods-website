"""Paid-pages mu-plugin must route the four Ads + HIPAA start doors."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "php" / "npcwoods-paid-pages.php"


class AdsHipaaPaidPagesRouterTest(unittest.TestCase):
    def test_start_doors_are_mapped(self):
        text = PLUGIN.read_text(encoding="utf-8")
        for slug in ("start-uti", "start-sinus", "start-dental", "start-uri"):
            with self.subTest(slug=slug):
                self.assertIn(f"'/{slug}/' => '{slug}/index.html'", text)
                self.assertIn(f"'{slug}' => '{slug}/index.html'", text)
        self.assertIn("'/t/click/'", text)
        self.assertIn("npcwoods_ads_click_ingest", text)
        self.assertIn("gclid", text)
        self.assertNotIn("phone", text.lower().split("npcwoods_ads_click_ingest")[1][:800])


if __name__ == "__main__":
    unittest.main()
