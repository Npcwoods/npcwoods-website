"""deploy.purge_and_confirm: single-URL purge, sha proof, automatic full-site
fallback, loud STALE failure. No network: fetch/purge/sleep are injected."""
from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def _load():
    spec = importlib.util.spec_from_file_location("npcw_deploy_purge_test", SCRIPTS / "deploy.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


D = _load()
URL = "https://npcwoods.com/faq/"
NEW, OLD = "a" * 64, "b" * 64


class Harness:
    def __init__(self, served):
        self.served = list(served)  # sha served per fetch call, last one repeats
        self.calls = []

    def fetch(self, url):
        sha = self.served.pop(0) if len(self.served) > 1 else self.served[0]
        self.calls.append(("fetch", url))
        return {"status": 200, "sha256": sha, "bytes": 1, "cf_cache": "HIT", "age": "300"}

    def purge(self, env, urls):
        self.calls.append(("purge", tuple(urls)))
        return True

    def purge_all(self, env):
        self.calls.append(("purge_all",))
        return True

    def run(self):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            res = D.purge_and_confirm({}, {URL: NEW}, fetch=self.fetch, sleep=lambda s: None,
                                      purge=self.purge, purge_all=self.purge_all)
        return res, err.getvalue()


class PurgeAndConfirmTests(unittest.TestCase):
    def test_single_purge_enough_no_full_purge(self):
        h = Harness([NEW])
        res, _ = h.run()
        self.assertTrue(res[URL].startswith("ok (single-URL"))
        self.assertNotIn(("purge_all",), h.calls)

    def test_stale_after_single_purge_falls_back_to_full_purge(self):
        h = Harness([OLD, NEW])
        res, _ = h.run()
        self.assertIn(("purge_all",), h.calls)
        self.assertTrue(res[URL].startswith("ok (full-site"))

    def test_still_stale_after_full_purge_is_loud_failure(self):
        h = Harness([OLD])
        res, err = h.run()
        self.assertTrue(res[URL].startswith("STALE"))
        self.assertIn("STALE", err)
        self.assertIn(("purge_all",), h.calls)

    def test_empty_expected_does_nothing(self):
        self.assertEqual(D.purge_and_confirm({}, {}, fetch=None, purge=lambda *a: 1 / 0), {})


class VerifyHttpShaTests(unittest.TestCase):
    def test_stale_edge_copy_fails_verification(self):
        import hashlib
        from unittest import mock
        body = b"<!DOCTYPE html><html>old</html>"

        class Resp:
            status = 200
            headers = {"cf-cache-status": "HIT", "age": "120"}
            def read(self): return body
            def __enter__(self): return self
            def __exit__(self, *a): return False

        item = D.PagePlan(page="faq", local=Path("x"), remote="public_html/faq/index.html",
                          url=URL, sha256=hashlib.sha256(b"new").hexdigest())
        with mock.patch.object(D.urllib.request, "urlopen", return_value=Resp()):
            problem = D.verify_http(item)
        self.assertIsNotNone(problem)
        self.assertIn("stale", problem)


if __name__ == "__main__":
    unittest.main()
