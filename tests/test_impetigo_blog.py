"""Impetigo blog plate: live slug, $59 text CTA, no forbidden chrome."""
from __future__ import annotations

import unittest
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "landing-pages/blog/impetigo-signs-treatment/index.html"


class ImpetigoBlogTests(unittest.TestCase):
    def test_plate_has_food(self):
        html = INDEX.read_text(encoding="utf-8")
        self.assertIn("<title>Impetigo: What It Looks Like, How It Spreads, and When to Treat It | NPCWoods</title>", html)
        self.assertIn("Impetigo: What It Looks Like", html)
        self.assertIn("$59", html)
        self.assertIn("sms:4806394722", html)
        self.assertIn("https://npcwoods.com/blog/impetigo-signs-treatment/", html)
        self.assertNotIn("npcwoods.com/contact/", html)
        self.assertNotRegex(html, r"(?i)\binsurance\b")
        self.assertNotIn("Text a Doctor", html)


if __name__ == "__main__":
    unittest.main()
