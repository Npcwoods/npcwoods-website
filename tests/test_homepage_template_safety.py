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

    def test_homepage_uses_shared_header_and_footer_snippets_when_available(self):
        self.assertIn("shared/header-snippet.html", self.text)
        self.assertIn("shared/footer-snippet.html", self.text)
        self.assertIn("npcwoods_shared_footer_rendered", self.text)

    def test_homepage_fallback_footer_includes_emergency_blurb(self):
        locked = (
            "Text-based telehealth is not for emergencies. "
            "If you have chest pain, trouble breathing, or other emergency symptoms, call 911."
        )
        self.assertIn(locked, self.text)

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


if __name__ == "__main__":
    unittest.main()
