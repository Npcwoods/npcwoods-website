"""Regression tests for the Guardian's no-third-party-tracking policy."""
import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "guardian" / "guardian.py"


def load_guardian():
    spec = importlib.util.spec_from_file_location("site_guardian", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Response:
    def __init__(self, html):
        self.status_code = 200
        self.headers = {"Content-Type": "text/html; charset=utf-8"}
        self.text = html


class Session:
    def __init__(self, html):
        self.response = Response(html)

    def request(self, *args, **kwargs):
        return self.response


class GuardianTrackingPolicyTest(unittest.TestCase):
    def setUp(self):
        self.g = load_guardian()
        self.page = {
            "url": "https://npcwoods.com/about/",
            "is_health_page": False,
            "is_paid_lp": False,
        }

    def _audit(self, html):
        return self.g.check_page(Session(html), self.page, set())

    def test_clean_public_page_has_no_tracker_finding(self):
        result = self._audit("<!DOCTYPE html><html><head></head><body>" + "a" * 2100 + "</body></html>")
        self.assertFalse([f for f in result.findings if f.check == "third-party-tracker"])

    def test_google_or_meta_tracker_is_red_on_every_public_page(self):
        html = (
            "<!DOCTYPE html><html><head><script "
            "src='https://connect.facebook.net/en_US/fbevents.js'></script></head><body>"
            + "a" * 2100 + "</body></html>"
        )
        result = self._audit(html)
        trackers = [f for f in result.findings if f.check == "third-party-tracker"]
        self.assertEqual(len(trackers), 1)
        self.assertEqual(trackers[0].severity, "RED")
        self.assertIn("connect.facebook.net", trackers[0].detail)


if __name__ == "__main__":
    unittest.main()
