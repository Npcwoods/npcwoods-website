import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build-vercel-preview-site.py"


def load_module():
    spec = importlib.util.spec_from_file_location("vercel_preview_builder", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class VercelPreviewBuilderTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def write_fixture_site(self, root: Path, export_root: Path) -> None:
        (root / "landing-pages" / "local-page").mkdir(parents=True)
        (root / "landing-pages" / "local-page" / "index.html").write_text(
            "<!doctype html><html><head><title>Local</title></head>"
            "<body><h1>Local</h1></body></html>",
            encoding="utf-8",
        )
        (root / "assets" / "css").mkdir(parents=True)
        (root / "assets" / "css" / "site.css").write_text("body{color:green}", encoding="utf-8")

        (export_root / "blog" / "sample-post").mkdir(parents=True)
        (export_root / "assets" / "uploads" / "2026" / "01").mkdir(parents=True)
        (export_root / "assets" / "uploads" / "2026" / "01" / "hero.jpg").write_bytes(b"fixture-image")
        (export_root / "blog" / "sample-post" / "index.html").write_text(
            """<!doctype html>
<html><head>
<title>Sample post</title>
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="canonical" href="https://npcwoods.com/sample-post/">
<link rel="stylesheet" href="https://npcwoods.com/assets/css/site.css">
<meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/01/hero.jpg">
<script type="application/ld+json">{"url":"https://npcwoods.com/sample-post/","image":"https://npcwoods.com/wp-content/uploads/2026/01/hero.jpg"}</script>
<script>(function(){var x='GTM-TEST'; window.dataLayer=[];})();</script>
<script src="https://www.googletagmanager.com/gtag/js?id=G-TEST"></script>
<script src="https://npcwoods.com/tracking.js"></script>
</head><body>
<img src="https://npcwoods.com/wp-content/uploads/2026/01/hero.jpg"
     srcset="https://npcwoods.com/wp-content/uploads/2026/01/hero.jpg 800w">
<img src="https://npcwoods.com/wp-content/uploads/2026/01/missing.jpg">
<a href="sms:4806394722?body=Hello">Text Chris</a>
<a href="https://external.example/cta">External CTA</a>
</body></html>""",
            encoding="utf-8",
        )

    def build(self, root: Path, export_root: Path | None):
        output = root / "content-output" / "previews" / "vercel-review-site"
        args = ["--output", str(output)]
        if export_root is not None:
            args.extend(["--export-root", str(export_root)])
        with tempfile.TemporaryDirectory() as temp_dir:
            # Keep the fixture root independent from the temporary directory used
            # by the unittest harness while exercising the real CLI entrypoint.
            _ = temp_dir
            original_root = self.module.ROOT
            try:
                self.module.ROOT = root
                return self.module.main(args), output
            finally:
                self.module.ROOT = original_root

    def test_export_blog_route_is_flattened_to_live_url(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            export_root = Path(temp_dir) / "export"
            self.write_fixture_site(root, export_root)

            code, output = self.build(root, export_root)

            self.assertEqual(code, 0)
            self.assertTrue((output / "sample-post" / "index.html").is_file())
            self.assertFalse((output / "blog" / "sample-post" / "index.html").exists())

    def test_export_assets_are_copied_and_only_matching_asset_urls_are_localized(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            export_root = Path(temp_dir) / "export"
            self.write_fixture_site(root, export_root)

            _, output = self.build(root, export_root)
            html = (output / "sample-post" / "index.html").read_text(encoding="utf-8")

            self.assertEqual(
                (output / "wp-content" / "uploads" / "2026" / "01" / "hero.jpg").read_bytes(),
                b"fixture-image",
            )
            self.assertIn('src="/wp-content/uploads/2026/01/hero.jpg"', html)
            self.assertIn('srcset="/wp-content/uploads/2026/01/hero.jpg 800w"', html)
            self.assertIn('src="https://npcwoods.com/wp-content/uploads/2026/01/missing.jpg"', html)
            self.assertIn('href="/assets/css/site.css"', html)
            self.assertIn('href="https://npcwoods.com/sample-post/"', html)
            self.assertIn('href="sms:4806394722?body=Hello"', html)
            self.assertIn('href="https://external.example/cta"', html)

    def test_absent_export_root_is_a_successful_local_only_build(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            self.write_fixture_site(root, Path(temp_dir) / "unused-export")

            code, output = self.build(root, Path(temp_dir) / "does-not-exist")

            self.assertEqual(code, 0)
            self.assertTrue((output / "local-page" / "index.html").is_file())
            self.assertFalse((output / "sample-post" / "index.html").exists())

    def test_preview_removes_production_trackers_and_stripe_navigation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            export_root = Path(temp_dir) / "export"
            self.write_fixture_site(root, export_root)
            pay_dir = root / "landing-pages" / "pay"
            pay_dir.mkdir(parents=True)
            (pay_dir / "index.html").write_text(
                """<!doctype html><html><head><script>
const stripeBaseUrl = 'https://buy.stripe.com/test';
form.addEventListener('submit', () => window.location.replace(stripeBaseUrl));
</script><meta http-equiv="refresh" content="0; url=https://external.example/redirect"></head><body><form><button>Pay</button></form></body></html>""",
                encoding="utf-8",
            )

            _, output = self.build(root, export_root)
            post_html = (output / "sample-post" / "index.html").read_text(encoding="utf-8")
            pay_html = (output / "pay" / "index.html").read_text(encoding="utf-8")
            tracking = (output / "tracking.js").read_text(encoding="utf-8")

            self.assertNotIn("googletagmanager.com", post_html)
            self.assertNotIn("GTM-TEST", post_html)
            self.assertNotIn("npcwoods.com/tracking.js", post_html)
            self.assertIn('src="/tracking.js"', post_html)
            self.assertNotIn("buy.stripe.com", pay_html)
            self.assertNotIn("window.location.replace(stripeBaseUrl)", pay_html)
            self.assertNotIn('http-equiv="refresh"', pay_html)
            self.assertIn("production tracking disabled", tracking)
            self.assertIn("window.fbq", tracking)

    def test_preview_robots_and_headers_remain_noindex(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            self.write_fixture_site(root, Path(temp_dir) / "unused-export")

            _, output = self.build(root, None)
            config = json.loads((output / "vercel.json").read_text(encoding="utf-8"))
            headers = {header["key"]: header["value"] for header in config["headers"][0]["headers"]}

            self.assertEqual((output / "robots.txt").read_text(encoding="utf-8"), "User-agent: *\nDisallow: /\n")
            self.assertEqual(headers["X-Robots-Tag"], "noindex, nofollow, noarchive")


if __name__ == "__main__":
    unittest.main()
