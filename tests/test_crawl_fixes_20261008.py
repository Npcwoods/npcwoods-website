"""Guardrails for the 2026-10-08 crawl fixes (canonicals, sitemap, cache warm)."""

import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LP = ROOT / "landing-pages"
PHP = ROOT / "php"
NEW_PLUGINS = ["npcwoods-sitemap-hygiene.php", "npcwoods-cache-warm.php"]
UTI_STATIC = [
    "uti-treatment/how-fast-do-uti-antibiotics-work",
    "uti-treatment/is-my-uti-getting-worse",
    "uti-treatment/no-video-uti-treatment",
    "uti-treatment/uti-antibiotics-online",
]


def head(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("</head>", 1)[0]


class StateHubCanonicalTest(unittest.TestCase):
    def test_every_state_hub_has_exactly_one_self_canonical(self):
        hubs = sorted(LP.glob("*-telemedicine/index.html"))
        self.assertGreaterEqual(len(hubs), 11)
        for hub in hubs:
            slug = hub.parent.name
            self_url = f"https://npcwoods.com/{slug}/"
            h = head(hub)
            canon = re.findall(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', h)
            og = re.findall(r'property="og:url" content="([^"]+)"', h)
            cite = re.findall(r'<link[^>]*rel="cite-as"[^>]*href="([^"]+)"', h)
            with self.subTest(hub=slug):
                self.assertEqual(canon, [self_url])
                self.assertLessEqual(len(og), 1)
                self.assertTrue(all(u == self_url for u in og + cite))

    def test_utah_head_has_no_washington_identity(self):
        h = head(LP / "utah-telemedicine" / "index.html")
        self.assertNotIn("washington-telemedicine", h)


class SitemapHygieneTest(unittest.TestCase):
    src = (PHP / "npcwoods-sitemap-hygiene.php").read_text(encoding="utf-8")

    def test_paid_noindex_landers_are_excluded(self):
        self.assertRegex(self.src, r"\b998,")
        self.assertRegex(self.src, r"\b999,")

    def test_uti_static_pages_are_added_and_indexable(self):
        for rel in UTI_STATIC:
            with self.subTest(page=rel):
                self.assertIn(f"'/{rel}/'", self.src)
                h = head(LP / rel / "index.html")
                self.assertEqual(
                    re.findall(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', h),
                    [f"https://npcwoods.com/{rel}/"],
                )
                self.assertNotRegex(h, r'name="robots"[^>]*noindex')

    def test_uses_yoast_page_content_filter(self):
        self.assertIn("'wpseo_sitemap_page_content'", self.src)
        self.assertIn("'wpseo_exclude_from_sitemap_by_post_ids'", self.src)


class MuPluginSafetyTest(unittest.TestCase):
    def test_new_plugins_lint(self):
        php = shutil.which("php")
        if not php:
            self.skipTest("php not installed")
        for name in NEW_PLUGINS:
            out = subprocess.run([php, "-l", str(PHP / name)], capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)

    def test_no_duplicate_function_names_across_php(self):
        seen = {}
        for f in sorted(PHP.glob("*.php")):
            for fn in re.findall(r"^\s*function\s+([a-zA-Z0-9_]+)\s*\(", f.read_text(encoding="utf-8"), re.M):
                with self.subTest(function=fn):
                    self.assertNotIn(fn, seen, f"{fn} in {f.name} and {seen.get(fn)}")
                seen[fn] = f.name

    def test_cache_warm_is_get_only_and_hooks_ban(self):
        src = (PHP / "npcwoods-cache-warm.php").read_text(encoding="utf-8")
        self.assertIn("'wpaas_cache_banned'", src)
        self.assertNotIn("wp_remote_post", src)
        self.assertNotIn("wp_remote_request", src)

    def test_cache_warm_tuned_for_mwp_cron(self):
        """MWP cron ticks every few minutes and kills a run at ~255s: each run
        must do ~100-120 URLs inside a ~150s cap and back off on timeouts
        instead of aborting the batch."""
        src = (PHP / "npcwoods-cache-warm.php").read_text(encoding="utf-8")

        def ret(fn):
            m = re.search(r"function %s\(\)\s*\{\s*return\s+(\d+);" % fn, src)
            self.assertIsNotNone(m, fn)
            return int(m.group(1))

        self.assertTrue(100 <= ret("npcwoods_cw_batch_size") <= 120)
        cap, timeout = ret("npcwoods_cw_time_cap"), ret("npcwoods_cw_timeout")
        self.assertTrue(120 <= cap <= 160)
        self.assertLess(cap + timeout + 10, 255)
        self.assertIn("npcwoods_cw_backoff(", src)
        self.assertIn("sleep( $sleep )", src)
        self.assertNotIn("$strikes >= 3", src)
        self.assertIn("wp_schedule_single_event( time() + $gap, 'npcwoods_cw_batch', array( $i ) )", src)
        self.assertIn("'npcwoods_cw_lock'", src)


if __name__ == "__main__":
    unittest.main()
