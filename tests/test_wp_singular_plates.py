"""WP singular plates: unbreak blank posts/legal without calling the broken canvas."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "php" / "npcwoods-wp-singular-plates.php"


class WpSingularPlatesTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(PLUGIN.exists())
        self.php = PLUGIN.read_text(encoding="utf-8")

    def test_skips_static_html_and_homepage(self):
        self.assertIn("index.html", self.php)
        self.assertIn("file_exists", self.php)
        self.assertIn("is_front_page", self.php)
        self.assertIn("is_singular", self.php)

    def test_does_not_call_wp_head_or_wp_footer(self):
        # wp_head currently dies mid-callback on singular WP templates.
        self.assertNotIn("wp_head(", self.php)
        self.assertNotIn("wp_footer(", self.php)
        self.assertNotIn("get_header(", self.php)

    def test_plate_has_food(self):
        self.assertIn("$59", self.php)
        self.assertIn("sms:4806394722", self.php)
        self.assertIn("the_content", self.php)
        self.assertIn("<title>", self.php)

    def test_no_forbidden_chrome(self):
        self.assertNotRegex(self.php, r"\binsurance\b")
        self.assertNotRegex(self.php, r"@type\":\s*\"Physician\"")
        self.assertNotIn("Text a Doctor", self.php)

    def test_unique_function_names(self):
        self.assertIn("npcwoods_singular_plate_", self.php)
        self.assertIn("template_redirect", self.php)


if __name__ == "__main__":
    unittest.main()
