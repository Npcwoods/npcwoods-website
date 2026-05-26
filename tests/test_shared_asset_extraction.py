import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "extract-shared-css-js.py"


def load_module():
    spec = importlib.util.spec_from_file_location("extract_shared_assets", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SharedAssetExtractionTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_asset_comment_does_not_count_as_real_stylesheet(self):
        html = "<body>\n<!-- nav CSS: now in /assets/css/site.css -->\n</body>"

        self.assertFalse(self.module.has_real_css_link(html))
        self.assertIn(self.module.CSS_LINK, self.module.inject_css_link(html))

    def test_asset_comment_does_not_count_as_real_script(self):
        html = "<body>\n<!-- nav JS: now in /assets/js/site.js -->\n</body>"

        self.assertFalse(self.module.has_real_js_script(html))
        self.assertIn(self.module.JS_SCRIPT, self.module.inject_js_script(html))

    def test_existing_real_asset_tags_are_not_duplicated(self):
        html = (
            "<body>\n"
            f"{self.module.CSS_LINK}\n"
            f"{self.module.JS_SCRIPT}\n"
            "</body>"
        )

        self.assertEqual(1, self.module.inject_css_link(html).count(self.module.CSS_LINK))
        self.assertEqual(1, self.module.inject_js_script(html).count(self.module.JS_SCRIPT))

    def test_previously_migrated_page_comments_are_repaired(self):
        html = (
            "<html><body>\n"
            "<!-- nav CSS: now in /assets/css/site.css -->\n"
            "<nav class=\"npc-nav\"></nav>\n"
            "<!-- nav JS: now in /assets/js/site.js -->\n"
            "</body></html>"
        )

        content, stats = self.module.ensure_shared_assets(html, {})

        self.assertIn(self.module.CSS_LINK, content)
        self.assertIn(self.module.JS_SCRIPT, content)
        self.assertTrue(stats["css_link"])
        self.assertTrue(stats["js_script"])


if __name__ == "__main__":
    unittest.main()
