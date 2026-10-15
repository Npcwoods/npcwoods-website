import base64
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "php" / "npcwoods-tracking.php"

SAMPLE_DOCUMENT = """<!doctype html>
<html lang="en">
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <script>window.fbq = function () {};</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-EFFRQMG8TC"></script>
  <script>window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('config', 'G-EFFRQMG8TC');</script>
  <script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){};t=b.createElement(e);t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','1558261907814968');</script>
  <noscript><img src="https://www.facebook.com/tr?id=1558261907814968&amp;ev=PageView&amp;noscript=1"></noscript>
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-59QSWZRC"></iframe></noscript>
  <script src="/tracking.js?v=20260528-no-phi"></script>
  <script src="https://analytics.ahrefs.com/analytics.js" data-key="keep-me"></script>
  <main>Care when you need it.</main>
</body>
</html>"""


def transform(document: str) -> str:
    payload = base64.b64encode(document.encode("utf-8")).decode("ascii")
    harness = """
function add_action(...$args) {}
require $argv[1];
echo npcwoods_tracking_rewrite_document(base64_decode($argv[2]));
"""
    completed = subprocess.run(
        ["php", "-r", harness, str(PLUGIN), payload],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    return completed.stdout


class SitewideMetaTrackingTest(unittest.TestCase):
    def test_filter_replaces_google_and_legacy_meta_tracking_with_requested_pixel(self):
        transformed = transform(SAMPLE_DOCUMENT)

        self.assertIn("fbq('init', '1428464038973925');", transformed)
        self.assertIn(
            'src="https://www.facebook.com/tr?id=1428464038973925&ev=PageView&noscript=1"',
            transformed,
        )
        self.assertEqual(transformed.count("connect.facebook.net/en_US/fbevents.js"), 1)
        self.assertEqual(transformed.count("fbq('init', '1428464038973925');"), 1)
        self.assertNotIn("1558261907814968", transformed)
        self.assertNotIn("googletagmanager.com", transformed)
        self.assertNotIn("google-analytics.com", transformed)
        self.assertNotIn("/tracking.js", transformed)
        self.assertIn("fonts.googleapis.com", transformed)
        self.assertIn("analytics.ahrefs.com", transformed)


if __name__ == "__main__":
    unittest.main()
