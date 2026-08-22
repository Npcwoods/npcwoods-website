import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "replace_sitewide_tracking.py"


def load_module():
    spec = importlib.util.spec_from_file_location("replace_sitewide_tracking", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SAMPLE = """<!doctype html>
<html>
<head>
  <link rel="preconnect" href="https://www.googletagmanager.com">
  <!-- Meta Pixel Code -->
  <script>window.fbq = function () {};</script>
  <script>(function(w,d,s,l,i){j.src='https://www.googletagmanager.com/gtm.js?id='+i;})(window,document,'script','dataLayer','GTM-59QSWZRC');</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-EFFRQMG8TC"></script>
  <script>window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('config', 'AW-610222919');</script>
  <!-- Meta Pixel Code --><script>!function(){var x='https://connect.facebook.net/en_US/fbevents.js';}();fbq('init', '1558261907814968');</script><noscript><img src="https://www.facebook.com/tr?id=1558261907814968&ev=PageView&noscript=1"/></noscript><!-- End Meta Pixel Code -->
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-59QSWZRC"></iframe></noscript>
  <script src="/tracking.js?v=20260528-no-phi"></script>
</body>
</html>"""


class ReplaceSitewideTrackingTest(unittest.TestCase):
    def test_transform_removes_meta_without_injecting_a_replacement(self):
        module = load_module()
        transformed = module.transform(SAMPLE)

        self.assertNotIn("connect.facebook.net/en_US/fbevents.js", transformed)
        self.assertNotIn("facebook.com/tr", transformed)
        self.assertNotIn("fbq('init'", transformed)
        self.assertNotIn("1558261907814968", transformed)
        self.assertNotIn("googletagmanager.com", transformed)
        self.assertNotIn("G-EFFRQMG8TC", transformed)
        self.assertNotIn("AW-610222919", transformed)
        self.assertNotIn("/tracking.js", transformed)
        self.assertNotIn("window.fbq = function", transformed)

    def test_transform_is_idempotent(self):
        module = load_module()
        once = module.transform(SAMPLE)

        self.assertEqual(module.transform(once), once)

    def test_shared_assets_do_not_emit_google_or_meta_events(self):
        for relative_path in (
            "assets/js/site.js",
            "html/assets/js/site.js",
            "html/tracking.js",
            "html/shared/tracking.js",
        ):
            source = (ROOT / relative_path).read_text(encoding="utf-8")
            self.assertNotRegex(source, r"\bgtag\s*\(")
            self.assertNotRegex(source, r"\bfbq\s*\(")

    def test_shared_tracking_snippet_contains_no_meta_pixel(self):
        source = (ROOT / "html/shared/tracking-snippet.html").read_text(encoding="utf-8")

        self.assertNotIn("connect.facebook.net/en_US/fbevents.js", source)
        self.assertNotIn("facebook.com/tr", source)
        self.assertNotIn("fbq('init'", source)

    def test_homepage_template_is_not_stripped_by_sitewide_replace(self):
        module = load_module()
        homepage = ROOT / "homepage" / "page-npcwoods-home.php"
        self.assertNotIn(homepage, module.target_paths())


if __name__ == "__main__":
    unittest.main()
