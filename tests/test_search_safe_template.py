"""The search-safe template must regenerate every live city page byte-for-byte.

These pages receive paid ad traffic; any drift between the template system and
the committed HTML means the refactor changed live output. The generator is
run into a temp dir (never touching the real pages) and each output is
compared byte-wise against the committed file.

Run: python3 -m unittest tests.test_search_safe_template
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "build-search-safe-pages.py"
TEMPLATE_DIR = ROOT / "landing-pages" / "uti-treatment" / "_search-safe-template"
PAGES_ROOT = ROOT / "landing-pages" / "uti-treatment"

EXPECTED_SLUGS = {
    "mesa-az", "tempe-az", "chandler-az", "gilbert-az",
    "glendale-az", "scottsdale-az", "surprise-az", "albuquerque-nm",
}


class SearchSafeTemplateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cities = json.loads((TEMPLATE_DIR / "cities.json").read_text())
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out_root = Path(cls.tmp.name)
        result = subprocess.run(
            [sys.executable, str(GENERATOR), "--out-root", str(cls.out_root)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise AssertionError(
                f"generator failed:\n{result.stdout}\n{result.stderr}"
            )

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_cities_json_covers_all_eight_live_pages(self):
        self.assertEqual({c["slug"] for c in self.cities}, EXPECTED_SLUGS)

    def test_generated_pages_are_byte_identical_to_committed_pages(self):
        for city in self.cities:
            slug = city["slug"]
            with self.subTest(city=slug):
                generated = (self.out_root / slug / "search-safe" / "index.html").read_bytes()
                committed = (PAGES_ROOT / slug / "search-safe" / "index.html").read_bytes()
                self.assertEqual(
                    generated, committed,
                    f"{slug}: generated page differs from committed page "
                    f"(template/cities.json drifted from live output)",
                )

    def test_generator_writes_only_search_safe_index_files(self):
        written = sorted(
            p.relative_to(self.out_root).as_posix()
            for p in self.out_root.rglob("*") if p.is_file()
        )
        self.assertEqual(
            written,
            sorted(f"{slug}/search-safe/index.html" for slug in EXPECTED_SLUGS),
        )

    def test_search_safe_pages_are_marked_as_paid_surfaces(self):
        for city in self.cities:
            slug = city["slug"]
            with self.subTest(city=slug):
                generated = (self.out_root / slug / "search-safe" / "index.html").read_text()
                self.assertIn("window.NPCWoodsPaidSurface = true", generated)
                self.assertIn("/tracking.js?v=20260622-paid-surface", generated)


if __name__ == "__main__":
    unittest.main()
