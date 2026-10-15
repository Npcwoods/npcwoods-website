import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
HTML = '<!doctype html><html><head><title>Review</title></head><body><h1>Real page</h1>' + 'content ' * 300 + '</body></html>'


class PreviewBundleTest(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('preview_builder', ROOT / 'scripts/build-vercel-preview-site.py')
        self.m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = self.m
        spec.loader.exec_module(self.m)
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.m.ROOT = self.root
        self.output = self.root / 'content-output/previews/task/site'
        self.page = self.root / 'landing-pages/about/index.html'
        self.page.parent.mkdir(parents=True)
        self.page.write_text(HTML)

    def tearDown(self):
        self.temp.cleanup()

    def build(self, pages=None):
        args = SimpleNamespace(output=str(self.output), page=pages or ['about'], include_live_tracking=False, json=True)
        with mock.patch.object(self.m, 'parse_args', return_value=args):
            return self.m.main()

    def test_manifest_binds_requested_routes_to_source_and_preview_hashes(self):
        self.assertEqual(self.build(), 0)
        manifest = self.output / 'preview-manifest.json'
        self.assertTrue(manifest.exists(), 'preview needs a structured review manifest')
        data = json.loads(manifest.read_text())
        self.assertEqual([p['route'] for p in data['pages']], ['/about/'])
        self.assertEqual(data['pages'][0]['title'], 'Review')
        self.assertEqual(len(data['pages'][0]['source_sha256']), 64)

    def test_missing_requested_page_fails_before_output_is_created(self):
        with self.assertRaises(SystemExit):
            self.build(['about', 'missing'])
        self.assertFalse(self.output.exists())

    def test_existing_preview_cannot_be_destroyed_by_a_new_build(self):
        self.output.mkdir(parents=True)
        sentinel = self.output / 'keep.txt'
        sentinel.write_text('previous approved preview')
        with self.assertRaises(SystemExit):
            self.build()
        self.assertEqual(sentinel.read_text(), 'previous approved preview')

    def test_inline_trackers_and_php_do_not_escape_into_preview(self):
        self.page.write_text(HTML.replace('</head>', '<script src="https://connect.facebook.net/en_US/fbevents.js"></script></head>'))
        self.build()
        self.assertNotIn('connect.facebook.net', (self.output / 'about/index.html').read_text())
        self.assertNotIn('<?', self.m.strip_php_template_header('<?php x(); ?>' + HTML + '<?php y(); ?>'))

    def test_assets_do_not_copy_secrets_or_executable_server_files(self):
        assets = self.root / 'assets'
        assets.mkdir()
        for name in ['.env', 'private.php', 'credentials.json', 'safe.css']:
            (assets / name).write_text('fixture only')
        self.build()
        self.assertEqual([p.name for p in (self.output / 'assets').iterdir()], ['safe.css'])


    def test_manifest_hash_uses_same_snapshot_as_preview_when_source_changes(self):
        expected = hashlib.sha256(self.page.read_bytes()).hexdigest()
        with mock.patch.object(self.m, 'copy_tree', side_effect=lambda *args: self.page.write_text(HTML.replace('Review', 'Later edit'))):
            self.build()
        manifest = json.loads((self.output / 'preview-manifest.json').read_text())
        self.assertEqual(manifest['pages'][0]['source_sha256'], expected)
        self.assertIn('<title>Review</title>', (self.output / 'about/index.html').read_text())
