import unittest
from pathlib import Path


PAGE = Path(__file__).resolve().parents[1] / "landing-pages" / "real-care" / "index.html"
ROUTER = Path(__file__).resolve().parents[1] / "php" / "npcwoods-static-pages.php"
OG_IMAGE = Path(__file__).resolve().parents[1] / "landing-pages" / "real-care" / "assets" / "real-care-og.png"


class RealCarePageTests(unittest.TestCase):
    def setUp(self):
        self.html = PAGE.read_text(encoding="utf-8")
        self.lower_html = self.html.lower()

    def test_is_a_headerless_facebook_landing_page_with_a_complete_footer(self):
        self.assertNotIn("<nav", self.lower_html)
        self.assertIn('<footer class="npc-site-footer">', self.html)
        self.assertIn("Conditions We Treat", self.html)
        self.assertIn("States We Serve", self.html)
        self.assertIn("Medical Disclaimer", self.html)
        self.assertIn("Privacy Policy", self.html)
        self.assertIn("Terms of Service", self.html)

    def test_has_working_contact_and_facebook_metadata(self):
        sms = "sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit"
        self.assertIn(sms, self.html)
        self.assertIn('href="tel:4806394722"', self.html)
        self.assertIn('<link rel="canonical" href="https://npcwoods.com/real-care/">', self.html)
        self.assertIn('<meta property="og:url" content="https://npcwoods.com/real-care/">', self.html)
        self.assertIn('https://npcwoods.com/real-care/assets/real-care-og.png', self.html)
        self.assertIn('<meta property="og:image:width" content="1200">', self.html)
        self.assertIn('<meta property="og:image:height" content="630">', self.html)
        self.assertTrue(OG_IMAGE.is_file())
        self.assertNotIn("noindex", self.lower_html)

    def test_keeps_required_safety_and_marketing_guardrails(self):
        self.assertIn("Not for emergencies", self.html)
        self.assertNotIn("insurance", self.lower_html)
        self.assertNotIn("subscription", self.lower_html)
        self.assertNotIn("<title>npcwoods — real care, on your time</title>", self.lower_html)

    def test_is_registered_with_the_static_page_router(self):
        router = ROUTER.read_text(encoding="utf-8")
        self.assertRegex(router, r'"real-care"\s*=>\s*"real-care/index\.html"')


if __name__ == "__main__":
    unittest.main()
