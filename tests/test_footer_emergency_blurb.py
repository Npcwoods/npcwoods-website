import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCKED = (
    "Text-based telehealth is not for emergencies. "
    "If you have chest pain, trouble breathing, or other emergency symptoms, call 911."
)
SNIPPET = ROOT / "html" / "shared" / "footer-snippet.html"
HOMEPAGE = ROOT / "homepage" / "page-npcwoods-home.php"


class FooterEmergencyBlurbTest(unittest.TestCase):
    def test_shared_footer_has_locked_sentence_once(self):
        text = SNIPPET.read_text(encoding="utf-8")
        self.assertEqual(1, text.count(LOCKED))
        self.assertIn('class="npc-footer-emergency"', text)

    def test_homepage_fallback_has_locked_sentence(self):
        text = HOMEPAGE.read_text(encoding="utf-8")
        self.assertIn("shared/footer-snippet.html", text)
        self.assertIn(LOCKED, text)


if __name__ == "__main__":
    unittest.main()
