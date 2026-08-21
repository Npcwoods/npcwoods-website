"""FAQ sinus antibiotics follow CDC/IDSA, not leftover azithromycin."""
from __future__ import annotations

import unittest
from pathlib import Path

FAQ = Path(__file__).resolve().parents[1] / "landing-pages/faq/index.html"


class FaqSinusAntibioticListTests(unittest.TestCase):
    def test_sinus_answer_uses_doxy_not_azithro(self):
        html = FAQ.read_text(encoding="utf-8")
        start = html.find("Sinus infections are one of the top conditions")
        self.assertGreater(start, 0)
        chunk = html[start : html.find("How much do medications cost", start)]
        self.assertIn("doxycycline", chunk)
        self.assertIn("amoxicillin-clavulanate", chunk)
        self.assertNotIn("azithromycin", chunk.lower())


if __name__ == "__main__":
    unittest.main()
