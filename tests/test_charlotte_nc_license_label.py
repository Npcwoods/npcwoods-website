"""Charlotte UTI is an NC plate. Clone leftovers from Atlanta must not survive."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHARLOTTE = ROOT / "landing-pages/uti-treatment/charlotte-nc/index.html"
FOOTER_MARK = "<!-- ===== NPCWOODS SITE FOOTER (Shared Component) ===== -->"


class CharlotteNcLicenseLabelTests(unittest.TestCase):
    def test_page_body_says_nc_not_ga(self):
        html = CHARLOTTE.read_text(encoding="utf-8")
        page = html.split(FOOTER_MARK, 1)[0]
        self.assertIn("Licensed in North Carolina", page)
        self.assertIn("Licensed in NC", page)
        self.assertNotIn("Licensed in GA", page)
        self.assertNotIn("Charlotte GA", page)
        self.assertNotIn("an Charlotte", page)
        self.assertIn("a Charlotte waiting room", page)
        self.assertIn("Chris Woods, NP &middot; MSN, APRN, FNP-C &middot; Licensed in NC", page)


if __name__ == "__main__":
    unittest.main()
