"""Kitchen checks for the generic condition series (screening-labs, mastitis).

Run: python3 -m unittest tests.test_condition_series
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERIES_IDS = ("screening-labs", "mastitis")
MED_NAME_RE = re.compile(
    r"""amoxicillin|amoxil|augmentin|clavulanate|penicillin|dicloxacillin|
    clindamycin|cleocin|metronidazole|flagyl|cephalexin|keflex|cefadroxil|
    azithromycin|zithromax|z-pak|doxycycline|ciprofloxacin|\bcipro\b|
    levofloxacin|bactrim|septra|sulfamethoxazole|trimethoprim|linezolid|
    ibuprofen|advil|motrin|acetaminophen|tylenol|naproxen|\baleve\b|\baspirin\b|
    hydrocodone|oxycodone|tramadol|\bcodeine\b|lidocaine|prednisone|
    nystatin|fluconazole|diflucan|lecithin|biotin|
    statins?\b|atorvastatin|lipitor|rosuvastatin|crestor|simvastatin|
    levothyroxine|synthroid|methimazole|insulin|metformin|
    ozempic|wegovy|mounjaro|semaglutide|tirzepatide|antibiotics?|antibacterial""",
    re.I | re.X,
)
TRACKER_RE = re.compile(
    r"googletagmanager|google-analytics|googleadservices|connect\.facebook\.net|"
    r"facebook\.com/tr|analytics\.ahrefs|/tracking\.js|gtag\(|fbq\(",
    re.I,
)
BANNED_RE = re.compile(r"\bdoctors?\b|\bdocs?\b|\bphysicians?\b|\bM\.?D\.?\b|insurance|appointments?|florida[- ]licensed|guaranteed", re.I)


def series(sid: str) -> dict:
    return json.loads((ROOT / "landing-pages" / "learn" / sid / "series.json").read_text(encoding="utf-8"))


def pages(sid: str) -> list[Path]:
    data = series(sid)
    base = ROOT / "landing-pages" / "learn" / sid
    out = [base / (s["slug"] + "/index.html" if s["slug"] else "index.html") for s in data["stops"]]
    out.append(ROOT / "landing-pages" / data["one_pager"]["path"].strip("/") / "index.html")
    return out


def visible(text: str) -> str:
    text = text.split('<main id="main">', 1)[-1].split("<footer", 1)[0]
    text = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", " ", text, flags=re.S)
    return re.sub(r"<[^>]+>", " ", text)


class ConditionSeriesTest(unittest.TestCase):
    def test_built_with_schema_bubbles_roadmap_and_footer(self):
        footer = (ROOT / "html" / "shared" / "footer-snippet.html").read_text(encoding="utf-8").strip()
        for sid in SERIES_IDS:
            for path in pages(sid):
                text = path.read_text(encoding="utf-8")
                with self.subTest(page=str(path.relative_to(ROOT))):
                    self.assertGreater(len(text), 20_000)
                    for needle in ('"@type": "MedicalWebPage"', '"@type": "FAQPage"', '"@type": "BreadcrumbList"',
                                   "bubble-blue", "bubble-black", "series-sticky", "sms:4806394722", "$59",
                                   "14 states, including Florida by telehealth registration", "911",
                                   'property="og:image:width" content="1200"', 'name="twitter:card" content="summary_large_image"'):
                        self.assertIn(needle, text)
                    self.assertEqual(text.count(footer), 1)
                    self.assertIsNone(TRACKER_RE.search(re.sub(r"<!--.*?-->", "", text, flags=re.S)))
                    self.assertNotIn("noindex", text.lower())

    def test_zero_medication_or_class_names(self):
        for sid in SERIES_IDS:
            roots = [ROOT / "landing-pages" / "learn" / sid, pages(sid)[-1].parent]
            hits = []
            for root in roots:
                for path in root.rglob("*"):
                    if path.suffix.lower() not in {".html", ".json", ".css", ".svg"}:
                        continue
                    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                        if MED_NAME_RE.search(line):
                            hits.append(f"{path.relative_to(ROOT)}:{i}")
            self.assertEqual(hits, [], "\n".join(hits))

    def test_banned_words_in_page_copy(self):
        for sid in SERIES_IDS:
            for path in pages(sid):
                with self.subTest(page=str(path.relative_to(ROOT))):
                    self.assertIsNone(BANNED_RE.search(visible(path.read_text(encoding="utf-8"))))

    def test_explainers_have_real_cutout_ghost_figure_and_og(self):
        for sid in SERIES_IDS:
            for path in pages(sid)[:-1]:
                text = path.read_text(encoding="utf-8")
                main = text.split('<main id="main">', 1)[1]
                with self.subTest(page=str(path.relative_to(ROOT))):
                    self.assertIn('class="hero-cutout" src="/assets/img/people/chris-cutout-600.webp"', main)
                    ghost = main.split('<svg class="hero-ghost"', 1)[1].split("</svg>", 1)[0]
                    self.assertNotIn("<text", ghost)
                    self.assertIn('class="art-fig"', main)
                    for src in re.findall(r'<figure class="art-fig"><img src="([^"?]+)', main):
                        self.assertTrue((ROOT / "landing-pages" / src.lstrip("/")).exists(), src)
            for path in pages(sid):
                text = path.read_text(encoding="utf-8")
                og = re.search(r'<meta property="og:image" content="https://npcwoods.com/([^"?]+)', text).group(1)
                with self.subTest(og=og):
                    local = ROOT / "landing-pages" / og
                    self.assertTrue(local.exists(), og)
                    self.assertLess(local.stat().st_size, 150_000)

    def test_one_series_accent(self):
        for sid in SERIES_IDS:
            css = (ROOT / "landing-pages" / "learn" / sid / "_shared" / "series.css").read_text(encoding="utf-8")
            self.assertIn(f"--accent: {series(sid)['accent']['hex']};", css)
            self.assertNotIn("#f5a524", css.lower())

    def test_rebuild_matches_kitchen_pages(self):
        for sid in SERIES_IDS:
            spec = importlib.util.spec_from_file_location(f"ccs_{sid}", ROOT / "scripts" / "build-condition-series.py")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.SERIES_DIR = ROOT / "landing-pages" / "learn" / sid
            built = {}
            mod.write = lambda path, text: built.__setitem__(Path(path), text)
            mod.main()
            self.assertEqual(len(built), len(pages(sid)))
            for path, text in built.items():
                with self.subTest(page=str(path.relative_to(ROOT))):
                    self.assertEqual(text, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
