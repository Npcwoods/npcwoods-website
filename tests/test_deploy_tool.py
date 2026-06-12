"""Safety + behavior tests for scripts/deploy.py (the unified guarded deploy tool).

Run: python3 -m unittest tests/test_deploy_tool.py -v

Nothing here touches the network, SFTP, or WordPress: paramiko and playwright
are mocked, load_env is asserted untouched in every guard test.
"""
import importlib.util
import io
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "deploy.py"
PAGE = "uti-treatment/mesa-az/search-safe"  # real page in the repo


def load_module():
    spec = importlib.util.spec_from_file_location("deploy_tool", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses needs the module registered
    spec.loader.exec_module(module)
    return module


class PathResolutionTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_normalize_page_variants(self):
        for raw in (
            "uti-treatment/mesa-az/search-safe",
            "/uti-treatment/mesa-az/search-safe/",
            "landing-pages/uti-treatment/mesa-az/search-safe",
            "landing-pages/uti-treatment/mesa-az/search-safe/index.html",
        ):
            self.assertEqual(self.m.normalize_page(raw), PAGE, raw)

    def test_local_and_remote_paths(self):
        self.assertEqual(self.m.local_path_for(PAGE),
                         self.m.ROOT / "landing-pages" / PAGE / "index.html")
        self.assertEqual(self.m.remote_path_for(PAGE), f"html/{PAGE}/index.html")
        self.assertEqual(self.m.url_for(PAGE), f"https://npcwoods.com/{PAGE}/")

    def test_normalize_rejects_traversal_and_bare_root(self):
        with self.assertRaises(ValueError):
            self.m.normalize_page("../../etc/passwd")
        with self.assertRaises(ValueError):
            self.m.normalize_page("/")


class StubResolutionTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()
        self.table = {"/uti-treatment/mesa-az/": 13, "/dental-pain/": 336, "/uti-treatment/": 999}

    def test_exact_match(self):
        self.assertEqual(self.m.stub_id_for_page("dental-pain", self.table), 336)

    def test_search_safe_child_uses_parent_city_stub(self):
        self.assertEqual(self.m.stub_id_for_page("uti-treatment/mesa-az/search-safe", self.table), 13)

    def test_new_city_has_no_stub_despite_grandparent(self):
        # tempe search-safe must NOT walk up to the /uti-treatment/ hub stub
        self.assertIsNone(self.m.stub_id_for_page("uti-treatment/tempe-az/search-safe", self.table))


class ManifestTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_manifest_parsing_skips_comments_and_blanks(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("# june batch\n\nuti-treatment/mesa-az/search-safe\n"
                    "uti-treatment/tempe-az/search-safe  # new city\n\n")
            path = f.name
        self.assertEqual(self.m.parse_manifest(Path(path)), [
            "uti-treatment/mesa-az/search-safe",
            "uti-treatment/tempe-az/search-safe",
        ])

    def test_collect_pages_merges_flags_and_manifest_dedupes(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("uti-treatment/mesa-az/search-safe\nuti-treatment/glendale-az/search-safe\n")
            path = f.name
        args = mock.Mock(pages=["uti-treatment/mesa-az/search-safe,uti-treatment/tempe-az/search-safe"],
                         manifest=path)
        self.assertEqual(self.m.collect_pages(args), [
            "uti-treatment/mesa-az/search-safe",
            "uti-treatment/tempe-az/search-safe",
            "uti-treatment/glendale-az/search-safe",
        ])


class BackupPathTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_backup_path_is_dated_timestamped_and_never_clobbers_remote_name(self):
        now = datetime(2026, 6, 11, 14, 30, 5)
        p = self.m.backup_path_for("html/uti-treatment/mesa-az/search-safe/index.html", now)
        self.assertEqual(p.parent.name, "2026-06-11")
        self.assertEqual(p.parent.parent.name, "deploy-backups")
        self.assertEqual(p.parent.parent.parent.name, "content-output")
        self.assertEqual(
            p.name,
            "html__uti-treatment__mesa-az__search-safe__index.html.remote-backup-20260611-143005",
        )


class DryRunSafetyTest(unittest.TestCase):
    """The default mode must never touch SFTP, WP, or credentials."""

    def setUp(self):
        self.m = load_module()

    def test_dry_run_makes_no_sftp_calls_and_loads_no_credentials(self):
        fake_paramiko = mock.MagicMock()
        with mock.patch.object(self.m, "load_env") as load_env, \
             mock.patch.dict(sys.modules, {"paramiko": fake_paramiko}):
            out = io.StringIO()
            with redirect_stdout(out):
                code = self.m.main(["deploy.py", "--pages", PAGE])
        self.assertEqual(code, 0)
        load_env.assert_not_called()
        fake_paramiko.Transport.assert_not_called()
        text = out.getvalue()
        self.assertIn("[dry-run] nothing uploaded", text)
        self.assertIn(f"html/{PAGE}/index.html", text)
        self.assertRegex(text, r"sha256 [0-9a-f]{12}")  # checksum shown in the plan

    def test_dry_run_blocks_on_forbidden_meta_pixel_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad_root = Path(tmp)
            page_dir = bad_root / "landing-pages" / "evil-page"
            page_dir.mkdir(parents=True)
            (page_dir / "index.html").write_text(
                "<!DOCTYPE html><html><head><script src='https://connect.facebook.net/x.js'>"
                "</script></head><body>GTM-59QSWZRC tracking.js</body></html>")
            with mock.patch.object(self.m, "ROOT", bad_root), \
                 mock.patch.object(self.m, "load_env") as load_env:
                err = io.StringIO()
                with redirect_stdout(io.StringIO()), redirect_stderr(err):
                    code = self.m.main(["deploy.py", "--pages", "evil-page"])
        self.assertEqual(code, 2)
        load_env.assert_not_called()
        self.assertIn("forbidden marker", err.getvalue())


class LiveGuardTest(unittest.TestCase):
    """--live must refuse to deploy without Chris's exact confirmation phrase."""

    def setUp(self):
        self.m = load_module()

    def _run(self, argv, stdin_tty=False, typed=None):
        fake_paramiko = mock.MagicMock()
        patches = [
            mock.patch.object(self.m, "load_env"),
            mock.patch.dict(sys.modules, {"paramiko": fake_paramiko}),
            mock.patch.object(self.m.sys.stdin, "isatty", return_value=stdin_tty),
        ]
        if typed is not None:
            patches.append(mock.patch("builtins.input", return_value=typed))
        out, err = io.StringIO(), io.StringIO()
        with patches[0] as load_env, patches[1], patches[2], \
             (patches[3] if typed is not None else mock.patch.object(self.m, "main", self.m.main)):
            with redirect_stdout(out), redirect_stderr(err):
                code = self.m.main(argv)
        return code, load_env, fake_paramiko, out.getvalue(), err.getvalue()

    def test_live_without_confirmation_is_blocked(self):
        code, load_env, paramiko_mock, _, err = self._run(["deploy.py", "--pages", PAGE, "--live"])
        self.assertEqual(code, 2)
        load_env.assert_not_called()
        paramiko_mock.Transport.assert_not_called()
        self.assertIn("[blocked]", err)

    def test_live_with_wrong_flag_phrase_is_blocked(self):
        code, load_env, paramiko_mock, _, err = self._run(
            ["deploy.py", "--pages", PAGE, "--live", "--confirm-live-deploy", "yes please"])
        self.assertEqual(code, 2)
        load_env.assert_not_called()
        paramiko_mock.Transport.assert_not_called()
        self.assertIn("wrong confirmation phrase", err)

    def test_live_with_wrong_typed_phrase_is_blocked(self):
        code, load_env, paramiko_mock, _, err = self._run(
            ["deploy.py", "--pages", PAGE, "--live"], stdin_tty=True, typed="sure")
        self.assertEqual(code, 2)
        load_env.assert_not_called()
        paramiko_mock.Transport.assert_not_called()
        self.assertIn("did not match", err)

    def test_correct_typed_phrase_unblocks_confirm_helper(self):
        # unit-level: confirm_live accepts the exact phrase typed interactively
        self.assertTrue(self.m.confirm_live(None, prompt=lambda _: "CHRIS APPROVED LIVE DEPLOY"))
        self.assertTrue(self.m.confirm_live("CHRIS APPROVED LIVE DEPLOY"))
        with redirect_stderr(io.StringIO()):
            self.assertFalse(self.m.confirm_live(None, prompt=lambda _: "nope"))

    def test_live_and_verify_only_are_mutually_exclusive(self):
        code, load_env, _, _, err = self._run(
            ["deploy.py", "--pages", PAGE, "--live", "--verify-only",
             "--confirm-live-deploy", "CHRIS APPROVED LIVE DEPLOY"])
        self.assertEqual(code, 2)
        load_env.assert_not_called()
        self.assertIn("mutually exclusive", err)


class VerifyOnlyTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_verify_only_runs_verification_without_sftp_or_credentials(self):
        fake_paramiko = mock.MagicMock()
        with mock.patch.object(self.m, "load_env") as load_env, \
             mock.patch.dict(sys.modules, {"paramiko": fake_paramiko}), \
             mock.patch.object(self.m, "run_verification",
                               return_value={PAGE: "PASS (HTTP markers only)"}) as rv:
            out = io.StringIO()
            with redirect_stdout(out):
                code = self.m.main(["deploy.py", "--pages", PAGE, "--verify-only"])
        self.assertEqual(code, 0)
        load_env.assert_not_called()
        fake_paramiko.Transport.assert_not_called()
        rv.assert_called_once()
        self.assertIn("1/1 pages passed", out.getvalue())

    def test_verify_only_reports_failure_exit_code(self):
        with mock.patch.object(self.m, "run_verification",
                               return_value={PAGE: "FAIL: bad status 404"}):
            with redirect_stdout(io.StringIO()):
                code = self.m.main(["deploy.py", "--pages", PAGE, "--verify-only"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
