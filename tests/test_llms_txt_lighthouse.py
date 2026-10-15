import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ROOT / "llms.txt",
    ROOT / "html" / "llms.txt",
    ROOT / "llms-full.txt",
    ROOT / "html" / "llms-full.txt",
)

# Lighthouse Agentic Browsing audit (core/audits/agentic/llms-txt.js)
H1_RE = re.compile(r"^\s*#\s+.+", re.M)
MD_LINK_RE = re.compile(r"\[.+\]\(.+\)")


class LlmsTxtLighthouseTest(unittest.TestCase):
    def test_kitchen_and_html_copies_stay_in_sync(self):
        self.assertEqual(
            (ROOT / "llms.txt").read_text(encoding="utf-8"),
            (ROOT / "html" / "llms.txt").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            (ROOT / "llms-full.txt").read_text(encoding="utf-8"),
            (ROOT / "html" / "llms-full.txt").read_text(encoding="utf-8"),
        )

    def test_files_pass_lighthouse_llms_txt_checks(self):
        for path in FILES:
            with self.subTest(path=str(path.relative_to(ROOT))):
                text = path.read_text(encoding="utf-8")
                self.assertRegex(text, H1_RE, "missing H1")
                self.assertRegex(text, MD_LINK_RE, "missing markdown links")
                self.assertGreaterEqual(len(text), 50, "too short")
                self.assertTrue(text.lstrip().startswith("# "), "H1 must be first")
                self.assertNotIn("\n---\n", text, "YAML-looking --- breaks some parsers")
