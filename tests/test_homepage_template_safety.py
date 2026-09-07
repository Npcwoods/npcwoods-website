import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "homepage" / "page-npcwoods-home.php"


class HomepageTemplateSafetyTest(unittest.TestCase):
    def setUp(self):
        self.text = TEMPLATE.read_text(encoding="utf-8")

    def test_homepage_runs_wordpress_head_and_footer_hooks(self):
        head_hook = re.search(r"wp_head\s*\(", self.text)
        footer_hook = re.search(r"wp_footer\s*\(", self.text)

        self.assertIsNotNone(head_hook)
        self.assertIsNotNone(footer_hook)
        self.assertLess(head_hook.start(), self.text.index("</head>"))
        self.assertLess(footer_hook.start(), self.text.index("</body>"))

    def test_tracking_js_is_owned_by_wordpress_footer_hook(self):
        self.assertNotIn('<script src="/tracking.js"></script>', self.text)

    def test_homepage_has_emergency_911_blurb(self):
        self.assertIn("Call 911", self.text)
        self.assertIn("chest pain", self.text)

    def test_scroll_plate_markers(self):
        self.assertIn("npc-redesign", self.text)
        self.assertIn("You feel awful.", self.text)
        self.assertIn("$59", self.text)
        self.assertIn("sms:+14806394722", self.text)

    def test_homepage_leaves_seo_metadata_to_wordpress(self):
        """Yoast must be the sole owner of description, canonical, and social tags."""
        patterns = (
            r'<meta\b[^>]*name=["\']description["\']',
            r'<link\b[^>]*rel=["\']canonical["\']',
            r'<meta\b[^>]*property=["\']og:',
            r'<meta\b[^>]*name=["\']twitter:',
        )
        for pattern in patterns:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, self.text, re.I))

    def test_homepage_has_one_fallback_title(self):
        """The active WordPress configuration does not emit a title at wp_head()."""
        self.assertEqual(1, len(re.findall(r"<title\b", self.text, re.I)))

    def test_homepage_has_one_business_entity_owner(self):
        """The shared footer owns the site-wide MedicalBusiness entity."""
        self.assertEqual(0, len(re.findall(r'"@type"\s*:\s*"MedicalBusiness"', self.text)))

    def test_eeat_plugin_does_not_emit_medical_business_on_the_front_page(self):
        php = (ROOT / "php" / "npcwoods-eeat.php").read_text(encoding="utf-8")
        self.assertIn("$graph = array($person);", php)
        self.assertIn("if (!$is_home)", php)
        self.assertIn("$graph[] = $business;", php)
        self.assertIn("Ratings live on the Google Business Profile", php)

    def test_homepage_response_time_matches_guardian_canonical(self):
        self.assertIn("Usually within a few hours", self.text)
        self.assertNotIn("Most visits wrap up in under an hour", self.text)

    def test_homepage_fonts_do_not_block_first_paint(self):
        self.assertNotIn("Inter-VariableFont_slnt,wght.woff2", self.text)
        self.assertNotIn(
            'href="https://www.googletagmanager.com"',
            self.text,
        )
        self.assertIn("{ timeout: 8000 }", self.text)

    def test_lcp_hero_image_is_visible_without_javascript(self):
        self.assertIn("fetchpriority=\"high\"", self.text)
        self.assertIn("chris-400.webp", self.text)
        self.assertIn("chris-1000.webp", self.text)
        self.assertIn("imagesrcset", self.text)

    def test_homepage_defers_meta_pixel_until_idle_or_first_input(self):
        self.assertIn("requestIdleCallback", self.text)
        self.assertIn("loadPixel", self.text)
        self.assertIn("connect.facebook.net/en_US/fbevents.js", self.text)
        self.assertIn("1558261907814968", self.text)
        self.assertIn("1428464038973925", self.text)


    def test_save_contact_widget_waits_for_idle(self):
        js = (ROOT / "assets" / "js" / "site.js").read_text(encoding="utf-8")
        live = (ROOT / "html" / "assets" / "js" / "site.js").read_text(encoding="utf-8")
        self.assertEqual(js, live)
        self.assertIn("npcSaveWrap", js)
        self.assertIn("requestIdleCallback", js)
        self.assertIn("bootSaveContact", js)


if __name__ == "__main__":
    unittest.main()
