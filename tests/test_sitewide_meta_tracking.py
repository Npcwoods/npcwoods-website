import base64
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "php" / "npcwoods-tracking.php"
FALLBACK_PLUGIN = ROOT / "php" / "npcwoods-sitewide-meta-pixel.php"
PUBLIC_SOURCE_ROOTS = ("html", "landing-pages", "blog")
META_MARKERS = (
    "connect.facebook.net/en_US/fbevents.js",
    "facebook.com/tr",
    "fbq('init'",
    'fbq("init"',
)
THIRD_PARTY_TRACKER_MARKERS = META_MARKERS + (
    "googletagmanager.com",
    "google-analytics.com",
    "googleadservices.com",
    "doubleclick.net",
    "/tracking.js",
)

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


def transform(
    document: str,
    plugin: Path = PLUGIN,
    function_name: str = "npcwoods_tracking_rewrite_document",
) -> str:
    payload = base64.b64encode(document.encode("utf-8")).decode("ascii")
    harness = (
        "function add_action(...$args) {}\n"
        "require $argv[1];\n"
        f"echo {function_name}(base64_decode($argv[2]));\n"
    )
    completed = subprocess.run(
        ["php", "-r", harness, str(plugin), payload],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    return completed.stdout


def homepage_output_buffer_level(plugin: Path) -> int:
    """Return the number of buffers a homepage request adds via the plugin."""
    harness = """
$callbacks = array();
function add_action($hook, $callback, $priority = 10) {
    global $callbacks;
    $callbacks[$hook][] = $callback;
}
function is_admin() { return false; }
function is_front_page() { return true; }
require $argv[1];
foreach ($callbacks['template_redirect'] as $callback) {
    $callback();
}
fwrite(STDERR, (string) ob_get_level());
"""
    completed = subprocess.run(
        ["php", "-r", harness, str(plugin)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    return int(completed.stderr)


def transform_homepage_head(document: str) -> str:
    payload = base64.b64encode(document.encode("utf-8")).decode("ascii")
    harness = (
        "function add_action(...$args) {}\n"
        "require $argv[1];\n"
        "if (function_exists('npcwoods_tracking_rewrite_homepage_head')) { "
        "echo npcwoods_tracking_rewrite_homepage_head(base64_decode($argv[2])); }\n"
    )
    completed = subprocess.run(
        ["php", "-r", harness, str(PLUGIN), payload],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    return completed.stdout


OFFICIAL_PIXEL_ID = "1558261907814968"
INJECTED_PIXEL_ID = "1428464038973925"
HOMEPAGE_TEMPLATE = ROOT / "homepage" / "page-npcwoods-home.php"


class SitewideMetaTrackingTest(unittest.TestCase):
    def test_public_html_sources_do_not_embed_third_party_tracking(self):
        pattern = "|".join(re.escape(marker) for marker in THIRD_PARTY_TRACKER_MARKERS)
        result = subprocess.run(
            [
                "rg", "-l", "-i", "--glob", "*.html",
                "--glob", "!_archive/**", "--glob", "!content-output/**",
                "--glob", "!output/**", "--glob", "!node_modules/**",
                pattern, *(str(ROOT / source_root) for source_root in PUBLIC_SOURCE_ROOTS),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertIn(result.returncode, (0, 1), result.stderr)
        self.assertFalse(result.stdout.strip(), f"Third-party tracking found in:\n{result.stdout}")

    def test_homepage_embeds_official_pixel_pageview_and_contact_after_wp_head(self):
        source = HOMEPAGE_TEMPLATE.read_text(encoding="utf-8")
        wp_head = re.search(r"wp_head\s*\(", source)
        self.assertIsNotNone(wp_head)

        init = re.search(r"fbq\(\s*['\"]init['\"]\s*,\s*['\"]%s['\"]" % OFFICIAL_PIXEL_ID, source)
        pageview = re.search(r"fbq\(\s*['\"]track['\"]\s*,\s*['\"]PageView['\"]", source)
        contact = re.search(r"fbq\(\s*['\"]track['\"]\s*,\s*['\"]Contact['\"]", source)
        contact_custom = re.search(r"fbq\(\s*['\"]trackCustom['\"]\s*,\s*['\"]ContactSent['\"]", source)
        sms_bind = re.search(r"a\[href\^=['\"]sms:", source)

        self.assertIsNotNone(init, "homepage must init official Meta Pixel 1558261907814968")
        self.assertIsNotNone(pageview, "homepage must fire PageView")
        self.assertIsNotNone(contact, "homepage must fire Contact")
        self.assertIsNotNone(contact_custom, "homepage must also fire custom Contact so the beacon is sendable")
        self.assertIsNotNone(sms_bind, "Contact must bind to sms: clicks")
        self.assertIn("connect.facebook.net/en_US/fbevents.js", source)
        self.assertIn(f"facebook.com/tr?id={OFFICIAL_PIXEL_ID}", source)
        site_pixel = re.search(r"fbq\(\s*['\"]init['\"]\s*,\s*['\"]%s['\"]" % INJECTED_PIXEL_ID, source)
        self.assertIsNotNone(site_pixel, "homepage must also init site pixel 1428464038973925")
        self.assertGreater(init.start(), wp_head.start())
        self.assertGreater(site_pixel.start(), wp_head.start())
        self.assertGreater(pageview.start(), wp_head.start())
        self.assertGreater(contact.start(), wp_head.start())
        self.assertIn(f"facebook.com/tr?id={INJECTED_PIXEL_ID}", source)
        self.assertNotIn("GTM-59QSWZRC", source)
        self.assertNotRegex(source, r"fbq\(\s*['\"]track['\"]\s*,\s*['\"]Lead['\"]")

    def test_homepage_bypasses_response_rewriters_to_preserve_its_template(self):
        self.assertEqual(homepage_output_buffer_level(PLUGIN), 0)
        self.assertEqual(homepage_output_buffer_level(FALLBACK_PLUGIN), 0)

    def test_homepage_head_rewriter_removes_injected_meta_pixel_but_keeps_head_content(self):
        head = """<style id=\"plugin-style\">.plugin{display:block}</style>
<!-- Meta Pixel Code --><script>fbq('init', '1428464038973925');</script><noscript><img src=\"https://www.facebook.com/tr?id=1428464038973925\"></noscript><!-- End Meta Pixel Code -->
<script type=\"application/ld+json\">{\"@type\":\"MedicalBusiness\"}</script>"""

        transformed = transform_homepage_head(head)

        self.assertIn('id="plugin-style"', transformed)
        self.assertIn('application/ld+json', transformed)
        self.assertNotIn('1428464038973925', transformed)
        self.assertNotIn('facebook.com/tr', transformed)

    def test_filter_replaces_legacy_trackers_with_site_pixel(self):
        transformed = transform(SAMPLE_DOCUMENT)

        self.assertEqual(transformed.count("1428464038973925"), 2)
        self.assertIn("connect.facebook.net/en_US/fbevents.js", transformed)
        self.assertIn("fbq('init', '1428464038973925')", transformed)
        self.assertIn("fbq('track', 'PageView')", transformed)
        self.assertIn("facebook.com/tr?id=1428464038973925", transformed)
        self.assertNotIn("1558261907814968", transformed)
        self.assertNotIn("googletagmanager.com", transformed)
        self.assertNotIn("google-analytics.com", transformed)
        self.assertNotIn("/tracking.js", transformed)
        self.assertIn("fonts.googleapis.com", transformed)
        self.assertIn("analytics.ahrefs.com", transformed)

    def test_fallback_mu_plugin_replaces_legacy_trackers_with_site_pixel(self):
        transformed = transform(
            SAMPLE_DOCUMENT,
            FALLBACK_PLUGIN,
            "npcwoods_sitewide_meta_pixel_rewrite_document",
        )

        self.assertIn("fbq('init', '1428464038973925')", transformed)
        self.assertIn("connect.facebook.net/en_US/fbevents.js", transformed)
        self.assertNotIn("1558261907814968", transformed)
        self.assertNotIn("googletagmanager.com", transformed)


if __name__ == "__main__":
    unittest.main()
