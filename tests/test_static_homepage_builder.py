import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build-vercel-preview-site.py"


def load_module():
    spec = importlib.util.spec_from_file_location("vercel_preview_builder_home", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class StaticHomepageBuilderTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_homepage_php_template_becomes_static_html(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            export_root = Path(temp_dir) / "export"
            (root / "homepage").mkdir(parents=True)
            (root / "assets").mkdir()
            (root / "html" / "shared").mkdir(parents=True)
            (export_root / "assets" / "uploads" / "2026" / "01").mkdir(parents=True)
            (export_root / "assets" / "uploads" / "2026" / "01" / "hero.jpg").write_bytes(b"hero")
            (root / "homepage" / "page-npcwoods-home.php").write_text(
                """<?php\nheader\n?>\n<!doctype html><html><head>\n<?php if (function_exists('wp_head')) { wp_head(); } ?>\n</head><body>\n<?php $npcwoods_header_rendered = false; readfile('header-snippet.html'); if (!$npcwoods_header_rendered): ?>fallback<?php endif; ?>\n<main><h1>Home</h1><img src=\"https://npcwoods.com/wp-content/uploads/2026/01/hero.jpg\"></main>\n<?php $npcwoods_footer_rendered = false; readfile('footer-snippet.html'); if (!$npcwoods_footer_rendered): ?>fallback<?php endif; ?>\n<?php if (function_exists('wp_footer')) { wp_footer(); } ?>\n</body></html>\n""",
                encoding="utf-8",
            )
            (root / "html" / "shared" / "header-snippet.html").write_text(
                '<nav aria-label="Main navigation">Header</nav>', encoding="utf-8"
            )
            (root / "html" / "shared" / "footer-snippet.html").write_text(
                '<footer>Footer</footer>', encoding="utf-8"
            )

            output = root / "content-output" / "previews" / "vercel-review-site"
            original_root = self.module.ROOT
            try:
                self.module.ROOT = root
                code = self.module.main(
                    ["--output", str(output), "--export-root", str(export_root)]
                )
            finally:
                self.module.ROOT = original_root

            self.assertEqual(code, 0)
            html = (output / "index.html").read_text(encoding="utf-8")
            self.assertNotIn("<?php", html)
            self.assertNotIn("wp_head", html)
            self.assertNotIn("wp_footer", html)
            self.assertIn('aria-label="Main navigation"', html)
            self.assertIn("<footer>Footer</footer>", html)
            self.assertIn('src="/wp-content/uploads/2026/01/hero.jpg"', html)

    def test_localization_preserves_json_ld_absolute_urls(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "preview"
            asset = output / "wp-content" / "uploads" / "2026" / "01" / "hero.jpg"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"hero")
            html = (
                '<img src="https://npcwoods.com/wp-content/uploads/2026/01/hero.jpg">'
                '<script type="application/ld+json">'
                '{"image":"https://npcwoods.com/wp-content/uploads/2026/01/hero.jpg"}'
                "</script>"
            )

            localized = self.module.localize_export_asset_urls(html, output)

            self.assertIn('src="/wp-content/uploads/2026/01/hero.jpg"', localized)
            self.assertIn(
                '"image":"https://npcwoods.com/wp-content/uploads/2026/01/hero.jpg"',
                localized,
            )

    def test_export_posts_generate_static_blog_archive(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            export_root = Path(temp_dir) / "export"
            (root / "landing-pages" / "local-page").mkdir(parents=True)
            (root / "landing-pages" / "local-page" / "index.html").write_text(
                "<html><body>local</body></html>", encoding="utf-8"
            )
            for slug, title in (("first-post", "First Post"), ("second-post", "Second Post")):
                post = export_root / "blog" / slug
                post.mkdir(parents=True)
                (post / "index.html").write_text(
                    f'<html><head><title>{title}</title>'
                    f'<meta property="article:published_time" content="2026-01-01T00:00:00+00:00">'
                    f'<link rel="canonical" href="https://npcwoods.com/{slug}/"></head>'
                    "<body>post</body></html>",
                    encoding="utf-8",
                )

            output = root / "content-output" / "previews" / "vercel-review-site"
            original_root = self.module.ROOT
            try:
                self.module.ROOT = root
                code = self.module.main(
                    ["--output", str(output), "--export-root", str(export_root)]
                )
            finally:
                self.module.ROOT = original_root

            self.assertEqual(code, 0)
            archive = (output / "blog" / "index.html").read_text(encoding="utf-8")
            self.assertIn('rel="canonical" href="https://npcwoods.com/blog/"', archive)
            self.assertIn('href="/first-post/"', archive)
            self.assertIn('href="/second-post/"', archive)

    def test_archive_page_two_has_trailing_slash_prev_link(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            export_root = Path(temp_dir) / "export"
            (root / "landing-pages" / "local-page").mkdir(parents=True)
            (root / "landing-pages" / "local-page" / "index.html").write_text(
                "<html><body>local</body></html>", encoding="utf-8"
            )
            for index in range(21):
                post = export_root / "blog" / f"post-{index}"
                post.mkdir(parents=True)
                (post / "index.html").write_text(
                    f'<html><head><title>Post {index}</title>'
                    f'<meta property="article:published_time" content="2026-01-{index + 1:02d}T00:00:00+00:00">'
                    f'<link rel="canonical" href="https://npcwoods.com/post-{index}/"></head>'
                    "<body>post</body></html>",
                    encoding="utf-8",
                )

            output = root / "content-output" / "previews" / "vercel-review-site"
            original_root = self.module.ROOT
            try:
                self.module.ROOT = root
                code = self.module.main(
                    ["--output", str(output), "--export-root", str(export_root)]
                )
            finally:
                self.module.ROOT = original_root

            self.assertEqual(code, 0)
            archive_page_two = (output / "blog" / "page" / "2" / "index.html").read_text(
                encoding="utf-8"
            )
            self.assertIn(
                '<link rel="prev" href="https://npcwoods.com/blog/">',
                archive_page_two,
            )

    def test_preview_config_includes_checked_in_redirect_draft(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            (root / "landing-pages" / "local-page").mkdir(parents=True)
            (root / "landing-pages" / "local-page" / "index.html").write_text(
                "<html><body>local</body></html>", encoding="utf-8"
            )
            (root / "vercel.migration.draft.json").write_text(
                json.dumps(
                    {
                        "redirects": [
                            {"source": "/old/", "destination": "/new/", "statusCode": 301}
                        ]
                    }
                ),
                encoding="utf-8",
            )
            output = root / "content-output" / "previews" / "vercel-review-site"
            original_root = self.module.ROOT
            try:
                self.module.ROOT = root
                code = self.module.main(["--output", str(output)])
            finally:
                self.module.ROOT = original_root

            self.assertEqual(code, 0)
            config = json.loads((output / "vercel.json").read_text(encoding="utf-8"))
            self.assertEqual(config["redirects"][0]["statusCode"], 301)

    def test_exported_homepage_overrides_php_fallback_and_preserves_route(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            export_root = Path(temp_dir) / "export"
            (root / "homepage").mkdir(parents=True)
            (root / "homepage" / "page-npcwoods-home.php").write_text(
                "<?php ?><!doctype html><html><body>PHP fallback</body></html>",
                encoding="utf-8",
            )
            exported_home = export_root / "pages"
            exported_home.mkdir(parents=True)
            (exported_home / "index.html").write_text(
                '<!doctype html><html><head><link rel="canonical" href="https://npcwoods.com/"></head>'
                "<body><h1>Exported homepage</h1></body></html>",
                encoding="utf-8",
            )
            output = root / "content-output" / "previews" / "vercel-review-site"
            original_root = self.module.ROOT
            try:
                self.module.ROOT = root
                code = self.module.main(
                    ["--output", str(output), "--export-root", str(export_root)]
                )
            finally:
                self.module.ROOT = original_root

            self.assertEqual(code, 0)
            homepage = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn("Exported homepage", homepage)
            self.assertNotIn("PHP fallback", homepage)

    def test_patient_experience_source_uses_live_page_route(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            (root / "html" / "experience").mkdir(parents=True)
            (root / "html" / "experience" / "index.html").write_text(
                '<!doctype html><html><head><link rel="canonical" href="https://npcwoods.com/patient-experience/"></head>'
                "<body><h1>Patient Experience</h1></body></html>",
                encoding="utf-8",
            )
            (root / "landing-pages" / "local-page").mkdir(parents=True)
            (root / "landing-pages" / "local-page" / "index.html").write_text(
                "<html><body>local</body></html>", encoding="utf-8"
            )

            output = root / "content-output" / "previews" / "vercel-review-site"
            original_root = self.module.ROOT
            try:
                self.module.ROOT = root
                code = self.module.main(["--output", str(output), "--export-root", str(Path(temp_dir) / "none")])
            finally:
                self.module.ROOT = original_root

            self.assertEqual(code, 0)
            self.assertTrue((output / "patient-experience" / "index.html").is_file())
            self.assertFalse((output / "experience" / "index.html").exists())


if __name__ == "__main__":
    unittest.main()
