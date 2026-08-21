"""Health-condition HTML must not ship live Meta / GTM / GA4 / Ads pixels.

Chris approved removing advertising/analytics pixels from health pages
(no BAA). Homepage PHP stays out of this commit. Public snippet is disabled.

Run: python3 -m unittest tests.test_health_page_trackers
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "strip_health_page_ad_pixels.py"

# Import the same classifier the strip script uses.
import importlib.util

spec = importlib.util.spec_from_file_location("strip_health_page_ad_pixels", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
LIVE_TOKENS = (
    "GTM-59QSWZRC",
    "G-EFFRQMG8TC",
    "AW-610222919",
)
FBQ_INIT_RE = re.compile(r"""fbq\s*\(\s*['\"]init['\"]""")


def uncommented(html: str) -> str:
    return COMMENT_RE.sub("", html)


class HealthPageTrackerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.health_files = mod.health_html_files()
        if not cls.health_files:
            raise AssertionError("strip script found no health HTML files")

    def test_health_pages_have_no_live_ad_or_analytics_pixels(self):
        for path in self.health_files:
            rel = path.relative_to(ROOT).as_posix()
            with self.subTest(page=rel):
                html = path.read_text(encoding="utf-8")
                live = uncommented(html)
                for token in LIVE_TOKENS:
                    self.assertNotIn(token, live, f"{rel} still has live {token}")
                self.assertIsNone(
                    FBQ_INIT_RE.search(live), f"{rel} still has live fbq init"
                )
                self.assertNotIn(
                    "facebook.com/tr", live, f"{rel} still has a live Meta noscript"
                )
                self.assertIn(
                    "GTM, GA4, and Google Ads stay off",
                    html,
                    f"{rel} is missing the HIPAA-off comment",
                )

    def test_homepage_file_was_not_stripped(self):
        homepage = ROOT / "homepage" / "page-npcwoods-home.php"
        self.assertTrue(homepage.exists())
        text = homepage.read_text(encoding="utf-8")
        self.assertNotIn("GTM, GA4, and Google Ads stay off", text)
        # Homepage tracking rides on wp_head(); this file must stay untouched.

    def test_marketing_snippet_is_disabled(self):
        snippet = ROOT / "html" / "shared" / "tracking-snippet.html"
        text = snippet.read_text(encoding="utf-8")
        self.assertNotIn("fbq('init'", text)
        self.assertNotIn("GTM-59QSWZRC", text)
        self.assertIn("intentionally disabled", text)

    def test_executive_false_positive_is_not_treated_as_health(self):
        self.assertFalse(
            mod.is_health_html("landing-pages/executive/index.html"),
            "executive contains the letters 'uti' but is not a condition page",
        )


if __name__ == "__main__":
    unittest.main()
