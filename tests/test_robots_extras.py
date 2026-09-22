"""robots.txt extras: no advertised backend dirs; bak rules are end-anchored."""

import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1] / "php" / "npcwoods-robots-extras.php"


class RobotsExtrasTest(unittest.TestCase):
    def setUp(self):
        self.text = PLUGIN.read_text(encoding="utf-8")

    def test_does_not_advertise_backend_folders(self):
        for path in ("/automation-output/", "/backups/", "/scripts/"):
            self.assertNotIn(f"Disallow: {path}", self.text)

    def test_bak_rules_are_end_anchored(self):
        self.assertIn("'/*.bak$'", self.text)
        self.assertIn("'/*.meta-bak$'", self.text)
        self.assertIn("'/*.synced.bak$'", self.text)
        self.assertNotIn("'/*.bak'", self.text.replace("'/*.bak$'", ""))

    def test_keeps_llms_and_sitemap(self):
        self.assertIn("/llms.txt", self.text)
        self.assertIn("/llms-full.txt", self.text)
        self.assertIn("sitemap_index.xml", self.text)

    def test_scope_comment_excludes_hrt(self):
        self.assertIn("does not offer hormone replacement", self.text.lower())
        self.assertIn("HRT", self.text)


if __name__ == "__main__":
    unittest.main()
