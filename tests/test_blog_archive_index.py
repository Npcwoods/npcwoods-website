"""Static /blog/ index so nginx does not 403 the archive directory."""
from __future__ import annotations

import unittest
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "landing-pages/blog/index.html"


class BlogArchiveIndexTests(unittest.TestCase):
    def test_archive_plate_has_food(self):
        html = INDEX.read_text(encoding="utf-8")
        self.assertIn("<title>Blog — Health Tips from a Nurse Practitioner | NPCWoods</title>", html)
        self.assertIn("<h1>The Blog</h1>", html)
        self.assertIn("$59", html)
        self.assertIn("sms:4806394722", html)
        self.assertIn("double board-certified", html)
        self.assertGreaterEqual(html.count('class="blog-card'), 10)
        self.assertNotRegex(html, r"(?i)\binsurance\b")
        self.assertNotIn("Text a Doctor", html)


if __name__ == "__main__":
    unittest.main()
