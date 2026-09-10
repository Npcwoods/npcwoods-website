"""UTI hub city-doors must point at live Reno + Tucson plates."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "landing-pages/uti-treatment/index.html"


class UtiHubCityDoorsTest(unittest.TestCase):
    def test_hub_hrefs_reno_and_tucson(self):
        html = HUB.read_text(encoding="utf-8")
        self.assertIn("CITY UTI DOORS", html)
        self.assertIn('href="https://npcwoods.com/uti-treatment/reno-nv/"', html)
        self.assertIn(">Reno, NV</a>", html)
        self.assertIn('href="https://npcwoods.com/uti-treatment/tucson-az/"', html)
        self.assertIn(">Tucson, AZ</a>", html)
        self.assertNotIn("marietta-ga", html)
        self.assertNotIn("flagstaff-az", html)
        self.assertNotIn("las-cruces-nm", html)
        self.assertNotIn("yuma-az", html)


if __name__ == "__main__":
    unittest.main()
