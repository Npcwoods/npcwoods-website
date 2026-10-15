"""Exercise the actual HTTP verifier against a local server, never the clinic."""
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

from tests.test_deploy_tool import load_module


GOOD = '<!doctype html><html><head><title>Local &amp; checked</title></head><body><h1>A <span>real</span> page</h1><p>' + 'content ' * 700 + '</p></body></html>'


class CleanPageVerificationTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()
        self.temp = tempfile.TemporaryDirectory()
        self.local = Path(self.temp.name) / 'index.html'
        self.local.write_text(GOOD)
        self.document = GOOD
        self.redirect = False
        self.requests = []
        fixture = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                fixture.requests.append(self.path)
                if fixture.redirect and self.path == '/page/':
                    self.send_response(302)
                    self.send_header('Location', '/login/')
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                # The cache-busting response deliberately lies: it always looks good.
                self.wfile.write((GOOD if '?' in self.path else fixture.document).encode())

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.item = self.m.PagePlan('page', self.local, 'html/page/index.html',
                                   f'http://127.0.0.1:{self.server.server_port}/page/',
                                   size=len(GOOD.encode()))

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def test_success_checks_only_the_clean_url(self):
        self.assertIsNone(self.m.verify_http(self.item))
        self.assertEqual(self.requests, ['/page/'])

    def test_blank_clean_shell_cannot_be_rescued_by_cache_buster(self):
        self.document = '<!doctype html><html><head></head><body>WordPress shell</body></html>'
        self.assertIsNotNone(self.m.verify_http(self.item))
        self.assertEqual(self.requests, ['/page/'])

    def test_wrong_title_and_h1_fail_even_with_large_real_html(self):
        for before, after in [('Local &amp; checked', 'Wrong title'), ('A <span>real</span> page', 'Wrong page')]:
            with self.subTest(before=before):
                self.document = GOOD.replace(before, after)
                self.assertIsNotNone(self.m.verify_http(self.item))

    def test_same_headings_but_missing_body_fails(self):
        self.document = GOOD.replace('content ' * 700, 'empty')
        self.assertIsNotNone(self.m.verify_http(self.item))

    def test_redirect_to_other_route_fails_even_with_correct_html(self):
        self.redirect = True
        self.assertIsNotNone(self.m.verify_http(self.item))

    def test_forbidden_tracker_in_returned_document_fails(self):
        self.document = GOOD.replace('</head>', '<script src="https://connect.facebook.net/en_US/fbevents.js"></script></head>')
        self.assertIsNotNone(self.m.verify_http(self.item))

    def test_unverifiable_local_document_fails_closed(self):
        self.local.write_text('<!doctype html><html><body>no title or h1</body></html>')
        self.assertIsNotNone(self.m.verify_http(self.item))

    def test_missing_browser_cannot_report_full_verification_pass(self):
        with mock.patch.dict('sys.modules', {'playwright': None}):
            result = self.m.run_verification([self.item])['page']
        self.assertTrue(result.startswith('FAIL'), str(result))
