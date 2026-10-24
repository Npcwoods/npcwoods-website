"""Safety + behavior tests for scripts/deploy.py (the unified guarded deploy tool).

Run: python3 -m unittest tests/test_deploy_tool.py -v

Nothing here touches the network, SFTP, or WordPress: paramiko and playwright
are mocked, load_env is asserted untouched in every guard test. The git guard
tests build throwaway repos in a temp folder (local file remotes only).
Run with a timeout, e.g.  perl -e 'alarm 300; exec @ARGV' python3 -m unittest tests/test_deploy_tool.py
"""
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from datetime import datetime
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "deploy.py"
LEDGER = REPO / "facts" / "practice.json"
CONFIRM = "CHRIS APPROVED LIVE DEPLOY"
PAGE = "uti-treatment/mesa-az/search-safe"  # real kitchen file; kitchen HTML must stay pixel-free
CLEAN_PAGE = "clean-plate"
CLEAN_HTML = (
    "<!DOCTYPE html><html><head><title>Clean plate</title></head>"
    "<body><h1>Text Chris</h1></body></html>"
)


def load_module():
    spec = importlib.util.spec_from_file_location("deploy_tool", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses needs the module registered
    spec.loader.exec_module(module)
    return module


def write_ledger(root: Path) -> None:
    (root / "facts").mkdir(parents=True, exist_ok=True)
    shutil.copy(LEDGER, root / "facts" / "practice.json")


def write_clean_landing(root: Path, page: str = CLEAN_PAGE, html: str = CLEAN_HTML) -> str:
    write_ledger(root)
    page_dir = root / "landing-pages" / page
    page_dir.mkdir(parents=True)
    (page_dir / "index.html").write_text(html)
    return page


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
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root)
            with mock.patch.object(self.m, "ROOT", root), \
                 mock.patch.object(self.m, "load_env") as load_env, \
                 mock.patch.dict(sys.modules, {"paramiko": fake_paramiko}):
                out = io.StringIO()
                with redirect_stdout(out):
                    code = self.m.main(["deploy.py", "--pages", CLEAN_PAGE])
        self.assertEqual(code, 0)
        load_env.assert_not_called()
        fake_paramiko.Transport.assert_not_called()
        text = out.getvalue()
        self.assertIn("[dry-run] nothing uploaded", text)
        self.assertIn(f"html/{CLEAN_PAGE}/index.html", text)
        self.assertRegex(text, r"sha256 [0-9a-f]{12}")  # checksum shown in the plan

    def test_mesa_search_safe_kitchen_file_is_not_blocked_by_pixel_markers(self):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self.m.main(["deploy.py", "--pages", PAGE])
        self.assertEqual(code, 0, err.getvalue())
        self.assertNotIn("forbidden marker", err.getvalue())
        self.assertIn("[dry-run] nothing uploaded", out.getvalue())

    def test_dry_run_blocks_on_forbidden_meta_pixel_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad_root = Path(tmp)
            write_ledger(bad_root)
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

    def _run(self, argv, stdin_tty=False, typed=None, root=None):
        fake_paramiko = mock.MagicMock()
        out, err = io.StringIO(), io.StringIO()
        with ExitStack() as stack:
            load_env = stack.enter_context(mock.patch.object(self.m, "load_env"))
            # These tests are about the confirmation phrase; the git guard has its own tests.
            stack.enter_context(mock.patch.object(self.m, "preflight_block", return_value=(None, "abc123")))
            stack.enter_context(mock.patch.dict(sys.modules, {"paramiko": fake_paramiko}))
            stack.enter_context(mock.patch.object(self.m.sys.stdin, "isatty", return_value=stdin_tty))
            if root is not None:
                stack.enter_context(mock.patch.object(self.m, "ROOT", root))
            if typed is not None:
                stack.enter_context(mock.patch("builtins.input", return_value=typed))
            with redirect_stdout(out), redirect_stderr(err):
                code = self.m.main(argv)
        return code, load_env, fake_paramiko, out.getvalue(), err.getvalue()

    def test_live_without_confirmation_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root)
            code, load_env, paramiko_mock, _, err = self._run(
                ["deploy.py", "--pages", CLEAN_PAGE, "--live"], root=root)
        self.assertEqual(code, 2)
        load_env.assert_not_called()
        paramiko_mock.Transport.assert_not_called()
        self.assertIn("[blocked]", err)

    def test_live_with_wrong_flag_phrase_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root)
            code, load_env, paramiko_mock, _, err = self._run(
                ["deploy.py", "--pages", CLEAN_PAGE, "--live",
                 "--confirm-live-deploy", "yes please"], root=root)
        self.assertEqual(code, 2)
        load_env.assert_not_called()
        paramiko_mock.Transport.assert_not_called()
        self.assertIn("wrong confirmation phrase", err)

    def test_live_with_wrong_typed_phrase_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root)
            code, load_env, paramiko_mock, _, err = self._run(
                ["deploy.py", "--pages", CLEAN_PAGE, "--live"],
                stdin_tty=True, typed="sure", root=root)
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
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root)
            code, load_env, _, _, err = self._run(
                ["deploy.py", "--pages", CLEAN_PAGE, "--live", "--verify-only",
                 "--confirm-live-deploy", "CHRIS APPROVED LIVE DEPLOY"], root=root)
        self.assertEqual(code, 2)
        load_env.assert_not_called()
        self.assertIn("mutually exclusive", err)


class VerifyOnlyTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_verify_only_writes_timestamped_proof_report(self):
        fixed_now = datetime(2026, 6, 18, 8, 45, 12)

        class FixedDatetime:
            @classmethod
            def now(cls):
                return fixed_now

        fake_paramiko = mock.MagicMock()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root)
            with mock.patch.object(self.m, "ROOT", root), \
                 mock.patch.object(self.m, "hq_root", return_value=Path(tmp)), \
                 mock.patch.object(self.m, "datetime", FixedDatetime), \
                 mock.patch.object(self.m, "load_env") as load_env, \
                 mock.patch.dict(sys.modules, {"paramiko": fake_paramiko}), \
                 mock.patch.object(self.m, "run_verification",
                                   return_value={CLEAN_PAGE: "PASS (HTTP markers only)"}) as rv:
                out = io.StringIO()
                with redirect_stdout(out):
                    code = self.m.main(["deploy.py", "--pages", CLEAN_PAGE, "--verify-only"])

            report = (Path(tmp) / "content-output" / "reports" / "deploy-verify" /
                      "deploy-verify-20260618-084512.md")
            self.assertEqual(code, 0)
            load_env.assert_not_called()
            fake_paramiko.Transport.assert_not_called()
            rv.assert_called_once()
            self.assertTrue(report.exists())
            text = report.read_text()
            self.assertIn("# Deploy Verification Proof", text)
            self.assertIn("Mode: verify-only", text)
            self.assertIn(CLEAN_PAGE, text)
            self.assertIn(f"https://npcwoods.com/{CLEAN_PAGE}/", text)
            self.assertIn("PASS (HTTP markers only)", text)
            self.assertIn("Screenshots: none", text)
            self.assertIn(str(report), out.getvalue())

    def test_verification_proof_report_includes_playwright_screenshot_paths(self):
        fixed_now = datetime(2026, 6, 18, 9, 10, 11)

        class FixedDatetime:
            @classmethod
            def now(cls):
                return fixed_now

        plan = [self.m.PagePlan(
            page=PAGE,
            local=self.m.ROOT / "landing-pages" / PAGE / "index.html",
            remote=f"html/{PAGE}/index.html",
            url=f"https://npcwoods.com/{PAGE}/",
        )]
        result = self.m.VerificationResult(
            "FAIL",
            "GTM=False GA4=False MetaPixel=0",
            screenshots=["/tmp/deploy-proof/mobile-before.png", "/tmp/deploy-proof/mobile-after.png"],
        )
        with tempfile.TemporaryDirectory() as tmp, \
             mock.patch.object(self.m, "hq_root", return_value=Path(tmp)), \
             mock.patch.object(self.m, "datetime", FixedDatetime):
            report = self.m.write_verification_proof_report(
                plan, {PAGE: result}, mode="verify-only")

            text = report.read_text()
        self.assertEqual(report.name, "deploy-verify-20260618-091011.md")
        self.assertIn("FAIL", text)
        self.assertIn("GTM=False GA4=False MetaPixel=0", text)
        self.assertIn("/tmp/deploy-proof/mobile-before.png", text)
        self.assertIn("/tmp/deploy-proof/mobile-after.png", text)

    def test_verify_only_runs_verification_without_sftp_or_credentials(self):
        fake_paramiko = mock.MagicMock()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root)
            with mock.patch.object(self.m, "ROOT", root), \
                 mock.patch.object(self.m, "load_env") as load_env, \
                 mock.patch.dict(sys.modules, {"paramiko": fake_paramiko}), \
                 mock.patch.object(self.m, "run_verification",
                                   return_value={CLEAN_PAGE: "PASS (HTTP markers only)"}) as rv:
                out = io.StringIO()
                with redirect_stdout(out):
                    code = self.m.main(["deploy.py", "--pages", CLEAN_PAGE, "--verify-only"])
        self.assertEqual(code, 0)
        load_env.assert_not_called()
        fake_paramiko.Transport.assert_not_called()
        rv.assert_called_once()
        self.assertIn("1/1 pages passed", out.getvalue())

    def test_verify_only_reports_failure_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root)
            with mock.patch.object(self.m, "ROOT", root), \
                 mock.patch.object(self.m, "run_verification",
                                   return_value={CLEAN_PAGE: "FAIL: bad status 404"}):
                with redirect_stdout(io.StringIO()):
                    code = self.m.main(["deploy.py", "--pages", CLEAN_PAGE, "--verify-only"])
        self.assertEqual(code, 1)


class CleanUrlVerifyTest(unittest.TestCase):
    """Done check is the ordinary public address, not a cache-bust query."""

    def setUp(self):
        self.m = load_module()

    def test_verify_http_requests_the_ordinary_public_address(self):
        item = self.m.PagePlan(
            page=PAGE,
            local=Path("/tmp/unused"),
            remote=f"html/{PAGE}/index.html",
            url=f"https://npcwoods.com/{PAGE}/",
        )
        captured = {}

        class Resp:
            status = 200

            def read(self):
                return (
                    b"<!DOCTYPE html><html><head><title>UTI</title></head>"
                    b"<body><h1>Text Chris</h1></body></html>"
                )

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        def fake_urlopen(req, timeout=30):
            captured["url"] = req.full_url
            return Resp()

        with mock.patch.object(self.m.urllib.request, "urlopen", fake_urlopen):
            problem = self.m.verify_http(item)
        self.assertIsNone(problem)
        self.assertEqual(captured["url"], item.url)
        self.assertNotIn("?", captured["url"])


class ContentBlockTest(unittest.TestCase):
    """Banned words, Ahrefs, and facts drift BLOCK (exit 2) before any server contact."""

    def setUp(self):
        self.m = load_module()

    def _run_live(self, html):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root, html=html)
            fake_paramiko = mock.MagicMock()
            err = io.StringIO()
            with mock.patch.object(self.m, "ROOT", root), \
                 mock.patch.object(self.m, "load_env") as load_env, \
                 mock.patch.object(self.m, "sftp_connect") as sftp_connect, \
                 mock.patch.object(self.m, "preflight_block", return_value=(None, "abc123")), \
                 mock.patch.dict(sys.modules, {"paramiko": fake_paramiko}), \
                 redirect_stdout(io.StringIO()), redirect_stderr(err):
                code = self.m.main(["deploy.py", "--pages", CLEAN_PAGE, "--live",
                                    "--confirm-live-deploy", CONFIRM])
        return code, load_env, sftp_connect, fake_paramiko, err.getvalue()

    def _assert_blocked(self, html, needle):
        code, load_env, sftp_connect, fake_paramiko, err = self._run_live(html)
        self.assertEqual(code, 2, err)
        load_env.assert_not_called()
        sftp_connect.assert_not_called()
        fake_paramiko.Transport.assert_not_called()
        self.assertIn(needle, err)

    def page(self, body, head=""):
        return f"<!DOCTYPE html><html><head><title>t</title>{head}</head><body>{body}</body></html>"

    def test_each_banned_word_blocks(self):
        for word in ("appointment", "Appointments", "physician", "Doctor", "INSURANCE", "MD"):
            with self.subTest(word=word):
                self._assert_blocked(self.page(f"<p>No {word} needed.</p>"), "banned word")

    def test_md_is_case_sensitive_and_whole_word(self):
        self.assertEqual(self.m.load_practice_facts().banned_word_hits(
            self.page('<p>md cmd MDN RMD markdown</p>')), [])
        self.assertTrue(self.m.load_practice_facts().banned_word_hits(self.page("<p>Not an MD.</p>")))

    def test_urls_and_slugs_do_not_trip_banned_words(self):
        html = self.page(
            '<p><a class="doctor-card" href="https://doctor.webmd.com/doctor/christopher-woods">WebMD profile</a> '
            '<a href="/insurance-free-care/">price</a> see /appointment-free/ and '
            '<img src="/img/physician.png" alt="Chris"> https://example.com/md/insurance</p>'
            '<style>.md{color:red}</style><!-- doctor note -->')
        self.assertEqual(self.m.load_practice_facts().banned_word_hits(html), [])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root, html=html)
            err = io.StringIO()
            with mock.patch.object(self.m, "ROOT", root), \
                 redirect_stdout(io.StringIO()), redirect_stderr(err):
                code = self.m.main(["deploy.py", "--pages", CLEAN_PAGE])  # dry-run
        self.assertEqual(code, 0, err.getvalue())

    def test_ahrefs_script_blocks(self):
        for head in ('<script src="https://analytics.ahrefs.com/analytics.js" data-key="x" async></script>',
                     '<script async src="https://ahrefs.com/analytics.js"></script>'):
            with self.subTest(head=head):
                self._assert_blocked(self.page("<p>Text Chris.</p>", head), "forbidden marker")

    def test_eleven_states_facts_drift_blocks(self):
        self._assert_blocked(self.page("<p>Licensed in 11 states.</p>"), "facts drift")

    def test_licensed_in_12_states_blocks(self):
        self._assert_blocked(self.page("<p>Licensed in 12 states, plus a Florida telehealth registration (TPAN3355).</p>"), "facts drift")

    def test_verify_only_is_not_blocked_by_words(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root, html=self.page("<p>No appointment.</p>"))
            with mock.patch.object(self.m, "ROOT", root), \
                 mock.patch.object(self.m, "run_verification",
                                   return_value={CLEAN_PAGE: "PASS (HTTP markers only)"}), \
                 redirect_stdout(io.StringIO()):
                code = self.m.main(["deploy.py", "--pages", CLEAN_PAGE, "--verify-only"])
        self.assertEqual(code, 0)

    def test_allowed_disclosure_passes_but_bare_physician_blocks(self):
        ok = self.page("<p>Chris practices in Georgia under a collaborative agreement with a "
                       "Georgia-licensed physician. He is a nurse practitioner, not a physician.</p>"
                       "<li>American Academy of Family Physicians (AAFP), Acute Otitis Media</li>")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_clean_landing(root, html=ok)
            err = io.StringIO()
            with mock.patch.object(self.m, "ROOT", root), \
                 redirect_stdout(io.StringIO()), redirect_stderr(err):
                code = self.m.main(["deploy.py", "--pages", CLEAN_PAGE])  # dry-run
        self.assertEqual(code, 0, err.getvalue())
        self._assert_blocked(ok.replace("</body>", "<p>A physician checks every chart.</p></body>"),
                             "banned word 'physician'")

    def test_deploy_banned_words_are_in_the_ledger(self):
        ledger = json.loads(LEDGER.read_text())
        facts = self.m.load_practice_facts()
        for word in facts.BANNED_WORDS_ANY_CASE + facts.BANNED_WORDS_EXACT_CASE:
            self.assertIn(word, ledger["forbidden_words"])
        self.assertIn("appointment", ledger["forbidden_words"])


GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "Guard Test", "GIT_AUTHOR_EMAIL": "guard@example.com",
    "GIT_COMMITTER_NAME": "Guard Test", "GIT_COMMITTER_EMAIL": "guard@example.com",
    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0",
}


def g(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, env=GIT_ENV, check=True, capture_output=True,
                          text=True, timeout=60).stdout.strip()


class GitGuardTest(unittest.TestCase):
    """Plate only from the counter, on main, clean, fetched, HEAD == origin/main."""

    def setUp(self):
        self.m = load_module()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        tmp = Path(self._tmp.name).resolve()
        self.env_patch = mock.patch.dict(os.environ, {k: v for k, v in GIT_ENV.items()
                                                       if k.startswith("GIT_")})
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)
        self.bare = tmp / "origin.git"
        g(tmp, "init", "-q", "--bare", "-b", "main", str(self.bare))
        seed = tmp / "seed"
        g(tmp, "init", "-q", "-b", "main", str(seed))
        write_clean_landing(seed)
        g(seed, "add", "-A")
        g(seed, "commit", "-q", "-m", "seed")
        g(seed, "remote", "add", "origin", str(self.bare))
        g(seed, "push", "-q", "origin", "main")
        self.kitchen = tmp / "kitchen"
        self.kitchen.mkdir()
        self.counter = self.kitchen / "npcwoods-website"
        g(tmp, "clone", "-q", str(self.bare), str(self.counter))
        self.card = self.kitchen / "KITCHEN-COUNTERS.json"
        self.card.write_text(json.dumps({"counters": [
            {"folder": "npcwoods-website", "plate": True},
            {"folder": "npcwoods-website-old-uti-branch", "plate": False}]}))
        for name, value in (("KITCHEN", self.kitchen), ("COUNTER_CARD", self.card),
                            ("SCRIPT_ROOT", self.counter), ("ROOT", self.counter)):
            patcher = mock.patch.object(self.m, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def run_live(self):
        fake_paramiko = mock.MagicMock()
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(self.m, "load_env") as load_env, \
             mock.patch.object(self.m, "sftp_connect") as sftp_connect, \
             mock.patch.dict(sys.modules, {"paramiko": fake_paramiko}), \
             redirect_stdout(out), redirect_stderr(err):
            code = self.m.main(["deploy.py", "--pages", CLEAN_PAGE, "--live",
                                "--confirm-live-deploy", CONFIRM])
        return code, load_env, sftp_connect, fake_paramiko, out.getvalue(), err.getvalue()

    def assert_blocked(self, needle):
        code, load_env, sftp_connect, fake_paramiko, out, err = self.run_live()
        self.assertEqual(code, 2, err)
        load_env.assert_not_called()
        sftp_connect.assert_not_called()
        fake_paramiko.Transport.assert_not_called()
        self.assertIn(needle, err)
        self.assertNotIn("[about to upload]", out)

    def test_clean_main_passes_and_prints_head_before_upload(self):
        blocked, head = self.m.preflight_block()
        self.assertIsNone(blocked)
        self.assertEqual(head, g(self.counter, "rev-parse", "HEAD"))

        class Reached(Exception):
            pass

        out = io.StringIO()
        with mock.patch.object(self.m, "load_env", side_effect=Reached), \
             redirect_stdout(out), redirect_stderr(io.StringIO()):
            with self.assertRaises(Reached):
                self.m.main(["deploy.py", "--pages", CLEAN_PAGE, "--live", "--confirm-live-deploy", CONFIRM])
        self.assertIn(f"[about to upload] main @ {head}", out.getvalue())
        self.assertIn(f"landing-pages/{CLEAN_PAGE}/index.html -> html/{CLEAN_PAGE}/index.html", out.getvalue())

    def test_deploy_backups_do_not_count_as_dirty(self):
        (self.counter / "deploy-backups").mkdir()
        (self.counter / "deploy-backups" / "x.remote-backup").write_text("x")
        self.assertIsNone(self.m.preflight_block()[0])

    def test_behind_origin_main_by_one_is_blocked(self):
        other = Path(self._tmp.name).resolve() / "other"
        g(other.parent, "clone", "-q", str(self.bare), str(other))
        (other / "landing-pages" / CLEAN_PAGE / "index.html").write_text(CLEAN_HTML.replace("Clean", "Newer"))
        g(other, "commit", "-q", "-am", "newer")
        g(other, "push", "-q", "origin", "main")
        self.assert_blocked("behind 1")

    def test_ahead_of_origin_main_is_blocked(self):
        (self.counter / "landing-pages" / CLEAN_PAGE / "index.html").write_text(CLEAN_HTML.replace("Clean", "Local"))
        g(self.counter, "commit", "-q", "-am", "local only")
        self.assert_blocked("ahead 1")

    def test_dirty_tracked_file_is_blocked(self):
        (self.counter / "landing-pages" / CLEAN_PAGE / "index.html").write_text(CLEAN_HTML.replace("Clean", "Dirty"))
        self.assert_blocked("Uncommitted changes")

    def test_untracked_file_is_blocked(self):
        (self.counter / "stray.txt").write_text("x")
        self.assert_blocked("Uncommitted changes")

    def test_wrong_branch_is_blocked(self):
        g(self.counter, "checkout", "-q", "-b", "feat/something")
        self.assert_blocked("not main")

    def test_failed_fetch_is_blocked(self):
        g(self.counter, "remote", "set-url", "origin", str(self.bare) + "-missing")
        self.assert_blocked("fetch origin main failed")

    def test_spare_folder_is_blocked_even_when_clean(self):
        spare = self.kitchen / "npcwoods-website-old-uti-branch"
        g(self.kitchen, "clone", "-q", str(self.bare), str(spare))
        with mock.patch.object(self.m, "SCRIPT_ROOT", spare), mock.patch.object(self.m, "ROOT", spare):
            self.assert_blocked("not the kitchen counter")

    def test_remote_diff_is_guarded_too(self):
        g(self.counter, "checkout", "-q", "-b", "feat/something")
        with mock.patch.object(self.m, "load_env") as load_env, \
             mock.patch.object(self.m, "sftp_connect") as sftp_connect, \
             redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = self.m.main(["deploy.py", "--pages", CLEAN_PAGE, "--remote-diff"])
        self.assertEqual(code, 2)
        load_env.assert_not_called()
        sftp_connect.assert_not_called()

    def test_no_bypass_flag_exists(self):
        src = SCRIPT.read_text()
        self.assertNotRegex(src, r"--(skip|no|bypass|force)[-_]?(git|guard|counter|preflight)")


class KitchenCounterTest(unittest.TestCase):
    """The real card on the Mini names exactly one counter: Desktop/Chris-HQ/npcwoods-website."""

    SPARES = (
        Path("/Users/macmini/Desktop/Chris-HQ/npcwoods-website-old-uti-branch"),
        Path("/Users/macmini/Desktop/Chris-HQ/npcwoods-website-postlaunch-wt"),
        Path("/Users/macmini/Desktop/Chris-HQ/postlaunch-fix-2026-10-06"),
        Path("/Users/macmini/Desktop/Chris-HQ/npcwoods-web-vp-platform"),
        Path("/Users/macmini/.config/superpowers/worktrees/npcwoods-website/washington-state-hub"),
        Path("/Users/macmini/pinkeye-v2-wt"),
    )

    def setUp(self):
        self.m = load_module()
        if not self.m.COUNTER_CARD.is_file():
            self.skipTest("real kitchen counter card only exists on the home Mac Mini")

    def test_real_counter_is_allowed(self):
        self.assertIsNone(self.m.kitchen_counter_block(self.m.KITCHEN / "npcwoods-website"))

    def test_spare_copies_are_blocked(self):
        for spare in self.SPARES:
            blocked = self.m.kitchen_counter_block(spare)
            self.assertIsNotNone(blocked, spare)
            self.assertIn("not the kitchen counter", blocked)

    def test_card_names_one_counter_and_points_at_the_ledger(self):
        card = json.loads(self.m.COUNTER_CARD.read_text(encoding="utf-8"))
        plating = [row for row in card["counters"] if row.get("plate") is True]
        self.assertEqual([row["folder"] for row in plating], ["npcwoods-website"])
        self.assertEqual(card["practice_facts"], "npcwoods-website/facts/practice.json")
        for row in card.get("outside", []):
            self.assertIs(row["plate"], False, row)


if __name__ == "__main__":
    unittest.main()
