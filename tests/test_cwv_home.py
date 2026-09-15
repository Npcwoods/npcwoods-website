import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "php" / "npcwoods-cwv.php"
SAVE_CONTACT = ROOT / "php" / "npcwoods-save-contact.php"


class CoreWebVitalsHomeTest(unittest.TestCase):
    def setUp(self):
        self.plugin = PLUGIN.read_text(encoding="utf-8") if PLUGIN.exists() else ""
        self.save = SAVE_CONTACT.read_text(encoding="utf-8")

    def test_cwv_plugin_exists_with_unique_prefix(self):
        self.assertTrue(PLUGIN.exists(), "php/npcwoods-cwv.php must exist")
        self.assertIn("function npcwoods_cwv_is_custom_plate", self.plugin)
        self.assertNotIn("function npcwoods_speed_hints", self.plugin)

    def test_plugin_strips_customizer_css_on_custom_plates(self):
        self.assertIn("wp_get_custom_css", self.plugin)
        self.assertIn("npcwoods_cwv_strip_custom_css", self.plugin)

    def test_plugin_dequeues_homepage_bloat(self):
        for handle in (
            "wp-block-library",
            "global-styles",
            "trustedsite-badge-js",
            "googlesitekit-events-provider-content-events",
        ):
            self.assertIn(handle, self.plugin)

    def test_plugin_strips_site_designer_and_wpcode_from_html(self):
        self.assertIn("wp-site-designer-contrast-fallback", self.plugin)
        self.assertIn("wpcode-css-snippet", self.plugin)
        self.assertIn("print_emoji_detection_script", self.plugin)
        self.assertIn("Professional Redesign", self.plugin)
        self.assertIn("wp_custom_css_cb", self.plugin)
        self.assertIn("wsimg", self.plugin)
        self.assertIn("fonts\\.googleapis\\.com", self.plugin)
        self.assertIn("dns-prefetch", self.plugin)

    def test_plugin_skips_save_contact_widget_on_homepage(self):
        self.assertIn("npcwoods_save_contact_button", self.plugin)
        self.assertIn("remove_action", self.plugin)

    def test_save_contact_uses_tiny_webp_not_megabyte_png(self):
        self.assertIn("chris-woods-headshot-160.webp", self.save)
        self.assertNotIn("chris-woods-headshot.png", self.save)
