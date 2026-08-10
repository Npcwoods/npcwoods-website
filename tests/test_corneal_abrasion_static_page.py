from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "html" / "corneal-abrasion-eye-scratch" / "index.html"
ROUTER = ROOT / "php" / "npcwoods-corneal-abrasion-post.php"


class CornealAbrasionStaticPageTests(unittest.TestCase):
    def test_live_route_has_a_standalone_search_safe_blog_page(self):
        self.assertTrue(PAGE.exists(), "standalone blog page source is missing")
        self.assertTrue(ROUTER.exists(), "standalone blog route is missing")
        page = PAGE.read_text(encoding="utf-8")
        router = ROUTER.read_text(encoding="utf-8")
        self.assertIn("scratched-eye-corneal-abrasion-care", router)
        self.assertIn("corneal-abrasion-eye-scratch/index.html", router)
        self.assertIn("ob_start('npcwoods_corneal_remove_meta_pixel')", router)
        self.assertIn("<title>Scratched Your Eye? Here’s What to Do Next | NPCWoods</title>", page)
        self.assertIn('rel="canonical" href="https://npcwoods.com/scratched-eye-corneal-abrasion-care/"', page)
        self.assertIn('rel="stylesheet" href="https://npcwoods.com/wp-content/uploads/2026/08/corneal-abrasion-eye-scratch.css"', page)
        self.assertIn('data-npcwoods-tracking="enabled"', page)
        self.assertIn('http-equiv="Content-Security-Policy"', page)
        self.assertIn("https://analytics.google.com", page)
        self.assertIn("https://googleads.g.doubleclick.net", page)
        self.assertIn("GTM-59QSWZRC", page)
        self.assertNotIn("window.fbq", page)
        self.assertIn("The short version", page)
        self.assertLess(
            page.index('alt="Adult gently shielding one watery eye in soft daylight"'),
            page.index("The short version"),
        )
        self.assertGreaterEqual(page.count("sms:4806394722"), 2)
        self.assertIn('"@type":"FAQPage"', page)
        self.assertNotRegex(page, re.compile(r"connect\.facebook\.net|facebook\.com/tr|fbq\s*\(", re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
