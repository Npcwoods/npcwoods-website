"""Real browser integration against local fixtures; no clinic/network writes."""
import importlib.util
import hashlib
import json
from pathlib import Path
import unittest

from tests.test_clean_page_verification import CleanPageVerificationTest, GOOD


@unittest.skipUnless(importlib.util.find_spec('playwright'), 'requires the verification Python environment')
class BrowserPageVerificationTest(CleanPageVerificationTest):
    def test_browser_checks_both_viewports_and_writes_proof(self):
        from page_verification import browser_proof
        ok, detail, screenshots = browser_proof(self.local, self.item.url, Path(self.temp.name) / 'proof')
        self.assertTrue(ok, detail)
        self.assertEqual(len(screenshots), 2)
        self.assertTrue(all(Path(p).stat().st_size > 100 for p in screenshots))
        self.assertTrue(all('?' not in path for path in self.requests))

    def test_dynamic_tracker_is_blocked_and_fails_browser_proof(self):
        from page_verification import browser_proof
        script = "<script>fetch('https://www.'+'google-'+'analytics.com/g/collect').catch(()=>{});</script>"
        self.document = GOOD.replace('</body>', script + '</body>')
        ok, detail, screenshots = browser_proof(self.local, self.item.url, Path(self.temp.name) / 'proof')
        self.assertFalse(ok)
        self.assertIn('forbidden request', detail)

    def test_preview_manifest_through_real_http_and_browser(self):
        path = Path(__file__).resolve().parents[1] / 'scripts/verify-preview.py'
        spec = importlib.util.spec_from_file_location('preview_verifier_test', path)
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        output = Path(self.temp.name) / 'bundle'
        dest = output / 'page/index.html'
        dest.parent.mkdir(parents=True)
        dest.write_text(GOOD)
        manifest = output / 'preview-manifest.json'
        data = {'schema_version': 1, 'output': str(output), 'pages': [{
            'route': '/page/', 'destination': 'page/index.html',
            'preview_sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
            'title': 'Local & checked', 'h1': 'A real page'}]}
        manifest.write_text(json.dumps(data))
        result = verifier.verify_preview(manifest, self.item.url.removesuffix('/page/'))
        self.assertTrue(result['ok'], result)
        self.assertEqual(len(result['pages'][0]['screenshots']), 2)
        dest.write_text('changed after review')
        with self.assertRaisesRegex(ValueError, 'changed'):
            verifier.verify_preview(manifest, 'https://fixture.vercel.app')
        with self.assertRaisesRegex(ValueError, 'origin'):
            verifier.verify_preview(manifest, 'https://npcwoods.com')
