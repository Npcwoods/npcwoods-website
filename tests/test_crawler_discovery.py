"""Kitchen tests for crawler discovery files.

The files are already live on the apex host. A 301 from /sitemap.xml to
/sitemap_index.xml is success. www /sitemap.xml was the leftover 404.
robots.txt / sitemaps stay noindex — they do not need a canonical URL.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests" / "guardian"))

from guardian import sitemap_xml_redirect_ok  # noqa: E402


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class CrawlerDiscoveryTests(unittest.TestCase):
    def test_apex_llms_files_exist_and_lead_with_practice_name(self):
        for rel in ("html/llms.txt", "llms.txt", "html/llms-full.txt", "llms-full.txt"):
            with self.subTest(rel=rel):
                text = read(rel)
                self.assertTrue(text.startswith("# NPCWoods Telemedicine"))
                self.assertIn("Last updated: September 1, 2026", text)
                self.assertIn("$59", text)
                self.assertIn("11", text)

    def test_robots_extras_points_at_yoast_index_not_sitemap_xml(self):
        php = read("php/npcwoods-robots-extras.php")
        self.assertIn("Sitemap: https://npcwoods.com/sitemap_index.xml", php)
        self.assertNotIn("Sitemap: https://npcwoods.com/sitemap.xml", php)
        self.assertIn("/sitemap.xml 301s here", php)

    def test_www_and_apex_sitemap_xml_301_to_apex_index(self):
        php = read("php/npcwoods-redirects.php")
        self.assertIn('"/sitemap.xml"', php)
        self.assertIn("https://npcwoods.com/sitemap_index.xml", php)
        self.assertIn("www.npcwoods.com/sitemap.xml", php)
        self.assertRegex(
            php,
            r'header\(\s*"Location:\s*https://npcwoods.com/sitemap_index.xml"',
        )

    def test_llms_files_are_listed_in_a_sitemap(self):
        php = read("php/npcwoods-robots-extras.php")
        static = read("html/llms-sitemap.xml")
        self.assertIn("https://npcwoods.com/llms.txt", php)
        self.assertIn("https://npcwoods.com/llms-full.txt", php)
        self.assertIn("https://npcwoods.com/llms-sitemap.xml", php)
        self.assertIn("wpseo_sitemap_index", php)
        self.assertIn("wpseo_sitemap_page_content", php)
        self.assertIn("X-Robots-Tag: noindex, follow", php)
        self.assertNotIn("rel=\"canonical\"", php)
        self.assertIn("<loc>https://npcwoods.com/llms.txt</loc>", static)
        self.assertIn("<loc>https://npcwoods.com/llms-full.txt</loc>", static)

    def test_guardian_treats_sitemap_xml_301_as_success(self):
        self.assertTrue(
            sitemap_xml_redirect_ok(301, "https://npcwoods.com/sitemap_index.xml")
        )
        self.assertTrue(
            sitemap_xml_redirect_ok(308, "https://www.npcwoods.com/sitemap_index.xml")
        )
        self.assertFalse(sitemap_xml_redirect_ok(404, None))
        self.assertFalse(sitemap_xml_redirect_ok(200, None))
        self.assertFalse(
            sitemap_xml_redirect_ok(301, "https://npcwoods.com/sitemap.xml")
        )

    def test_guardian_does_not_require_canonical_on_discovery_files(self):
        guardian = read("tests/guardian/guardian.py")
        self.assertIn("No canonical required", guardian)
        self.assertIn("check_discovery_files", guardian)
        self.assertIn("do not report a Yoast 301 as a missing sitemap", guardian)


if __name__ == "__main__":
    unittest.main()
