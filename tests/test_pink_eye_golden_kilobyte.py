"""Pink-eye hub must match UTI chrome depth and stay clinically honest."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "landing-pages/pink-eye-treatment/index.html"
UTI = ROOT / "landing-pages/uti-treatment/index.html"
HEADER_MARK = "<!-- ===== NPCWOODS SITE HEADER (Shared Component) ===== -->"
FOOTER_MARK = "<!-- ===== NPCWOODS SITE FOOTER (Shared Component) ===== -->"


class PinkEyeGoldenKilobyteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.size = PAGE.stat().st_size

    def test_page_is_uti_scale_not_a_thin_card(self):
        uti_size = UTI.stat().st_size
        self.assertGreaterEqual(
            self.size,
            80_000,
            f"pink-eye is {self.size} bytes; UTI gold is {uti_size}. Need golden-kilobyte depth.",
        )
        self.assertGreaterEqual(
            self.size,
            int(uti_size * 0.80),
            f"pink-eye {self.size} is under 80% of UTI {uti_size}",
        )

    def test_shared_chrome_and_thread_ui(self):
        self.assertIn(HEADER_MARK, self.html)
        self.assertIn(FOOTER_MARK, self.html)
        self.assertIn("imsg-bubble", self.html)
        self.assertIn("Three texts", self.html)
        self.assertIn("not a chatbot", self.html.lower())

    def test_9_0_signals_and_no_banned_tracking(self):
        html = self.html
        self.assertIn("$59", html)
        self.assertIn("sms:4806394722", html)
        self.assertIn("1285125468", html)
        self.assertIn("Last reviewed", html)
        self.assertIn("MedicalWebPage", html)
        self.assertIn("FAQPage", html)
        self.assertIn("911", html)
        self.assertIn("how-it-works", html)
        self.assertNotIn("/tracking.js", html)
        self.assertNotRegex(html, r"(?i)\binsurance\b")
        self.assertNotIn('"@type": "Physician"', html)
        self.assertNotIn('"@type":"Physician"', html)
        self.assertNotRegex(html, r"fbq\(['\"]init")
        self.assertNotIn("googletagmanager.com", html)

    def test_clinical_holds_are_on_the_plate(self):
        html = self.html.lower()
        self.assertRegex(html, r"viral")
        self.assertRegex(html, r"bacterial")
        self.assertRegex(html, r"allerg")
        self.assertRegex(html, r"contact[- ]lens")
        self.assertRegex(html, r"in-person")
        self.assertRegex(html, r"newborn")
        self.assertRegex(html, r"polytrim|polymyxin")
        self.assertRegex(html, r"erythromycin")
        self.assertRegex(html, r"not automatic|not every case|do not (automatically )?need antibiotic")
        self.assertIn("cdc.gov/conjunctivitis", html)
        self.assertRegex(html, r"photophobia|light sensitivity")
        self.assertRegex(html, r"keratitis")


if __name__ == "__main__":
    unittest.main()
