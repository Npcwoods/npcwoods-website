from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "landing-pages/pink-eye-treatment/index.html"
ROUTER = ROOT / "php/npcwoods-static-pages.php"


class PinkEyeTreatmentPageTest(unittest.TestCase):
    def test_page_and_route_are_present_and_compliant(self):
        html = PAGE.read_text(encoding="utf-8")
        router = ROUTER.read_text(encoding="utf-8")

        self.assertIn('"pink-eye-treatment"', router)
        self.assertIn('href="https://npcwoods.com/pink-eye-treatment/"', html)
        self.assertIn('src="/tracking.js"', html)
        self.assertIn('application/ld+json', html)
        self.assertIn('Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT', html)
        self.assertNotRegex(
            html,
            re.compile(r"\binsurance\b|\bdoctor\b|\bsubscription\b", re.I),
        )
