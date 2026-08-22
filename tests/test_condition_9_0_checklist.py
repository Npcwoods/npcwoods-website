"""9.0 condition-hub checklist. Pink eye, sinus, strep, ear must match UTI-grade signals."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "pink-eye": ROOT / "landing-pages/pink-eye-treatment/index.html",
    "sinus": ROOT / "landing-pages/sinus-infection-treatment/index.html",
    "strep": ROOT / "landing-pages/strep-throat-treatment/index.html",
    "ear": ROOT / "landing-pages/ear-infection-treatment/index.html",
}


class ConditionNineChecklistTests(unittest.TestCase):
    def test_each_money_condition_has_uti_grade_signals(self):
        for name, path in PAGES.items():
            html = path.read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertIn("$59", html)
                self.assertIn("sms:4806394722", html)
                self.assertIn("1285125468", html)
                self.assertIn("Last reviewed", html)
                self.assertIn("MedicalWebPage", html)
                self.assertIn("FAQPage", html)
                self.assertIn("not a chatbot", html.lower())
                self.assertIn("911", html)
                self.assertRegex(html, r"(?i)(er if|emergency|in-person)")
                self.assertNotRegex(html, r"(?i)\binsurance\b")
                self.assertNotIn('"@type": "Physician"', html)
                self.assertNotIn('"@type":"Physician"', html)
                self.assertIn("how-it-works", html)


if __name__ == "__main__":
    unittest.main()
