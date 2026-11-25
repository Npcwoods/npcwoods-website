"""Kitchen checks for the condition series (screening-labs, mastitis) on the gold UTI look.

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
    text = re.split(r'<main[^>]*id="main"[^>]*>', text, maxsplit=1)[-1].split("<footer", 1)[0]
    text = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", " ", text, flags=re.S)
    return re.sub(r"<[^>]+>", " ", text)


def gold_css(path: Path) -> str:
    head = path.read_text(encoding="utf-8").split("</head>", 1)[0]
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", head, re.S))


COMMON = ('"@type": "MedicalWebPage"', '"@type": "FAQPage"', '"@type": "BreadcrumbList"',
          "sms:4806394722", "$59", "14 states, including Florida by telehealth registration", "911",
          'property="og:image:width" content="1200"', 'name="twitter:card" content="summary_large_image"',
          "MSN, APRN, FNP-C, AGACNP-BC")
SERIES_NEEDLES = ('<header class="gh"', 'class="gh-photo"', 'class="ex-byline"', 'class="ex-tldr"',
                  'class="gh-ghost"')
HUB_NEEDLES = ('class="hub-intro"', 'class="stop-list"', 'class="hub-onepager"', 'class="hub-cta"')
STOP_NEEDLES = ('class="ex-faq"', 'class="ex-map"', 'class="ex-intro"', 'class="ex-pn"', 'class="ex-cta"', 'class="ex-src"')
OFFER_NEEDLES = ('class="hero-inner hero-split"', 'class="stats-band"', 'class="vs-section"', '<section class="reviews">',
                 'id="how-it-works"', 'class="bento"', 'id="pricing"', 'class="er-box"', 'class="fit-grid"',
                 'class="faq-list"', 'class="states-pills"', 'class="explained-grid"', 'class="bottom-cta"',
                 'class="clinician-line"', '"@type": "HowTo"')


class ConditionSeriesTest(unittest.TestCase):
    def test_gold_structure_schema_and_footer(self):
        footer = (ROOT / "html" / "shared" / "footer-snippet.html").read_text(encoding="utf-8").strip()
        for sid in SERIES_IDS:
            ps = pages(sid)
            for i, path in enumerate(ps):
                text = path.read_text(encoding="utf-8")
                kind = "offer" if path == ps[-1] else ("hub" if i == 0 else "stop")
                needles = COMMON + {"offer": OFFER_NEEDLES, "hub": SERIES_NEEDLES + HUB_NEEDLES,
                                    "stop": SERIES_NEEDLES + STOP_NEEDLES}[kind]
                with self.subTest(page=str(path.relative_to(ROOT))):
                    self.assertGreater(len(text), 40_000)
                    for needle in needles:
                        self.assertIn(needle, text)
                    self.assertEqual(text.count(footer), 1)
                    self.assertIsNone(TRACKER_RE.search(re.sub(r"<!--.*?-->", "", text, flags=re.S)))
                    self.assertNotIn("noindex", text.lower())
                    self.assertEqual(len(re.findall(r"<h1[ >]", text)), 1)

    def test_pages_carry_the_gold_css_verbatim(self):
        lander = gold_css(ROOT / "landing-pages" / "uti-treatment" / "index.html")
        hub = gold_css(ROOT / "landing-pages" / "learn" / "uti" / "index.html")
        for sid in SERIES_IDS:
            ps = pages(sid)
            for path in ps:
                with self.subTest(page=str(path.relative_to(ROOT))):
                    self.assertIn(lander if path == ps[-1] else hub, gold_css(path))

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

    def test_labs_pricing_is_plain(self):
        text = visible(pages("screening-labs")[-1].read_text(encoding="utf-8"))
        for needle in ("consultation and the lab order", "Results walk-through", "The lab bills its own fee",
                       "A prescription, if needed", "separate fee"):
            self.assertIn(needle, text)
        self.assertNotIn("only pay if a text visit is the right fit", text)

    def test_mastitis_keeps_103_er_line(self):
        for path in pages("mastitis"):
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertIn("103°F", path.read_text(encoding="utf-8"))

    def test_series_pages_have_real_cutout_ghost_figure_and_og(self):
        for sid in SERIES_IDS:
            for path in pages(sid)[:-1]:
                text = path.read_text(encoding="utf-8")
                with self.subTest(page=str(path.relative_to(ROOT))):
                    self.assertIn('<img src="/assets/img/people/chris-cutout-600.webp"', text)
                    ghost = text.split('<svg class="gh-ghost"', 1)[1].split("</svg>", 1)[0]
                    self.assertNotIn("<text", ghost)
                    figs = re.findall(r'<figure class="ex-fig ex-card-fig"><img src="([^"?]+)', text)
                    self.assertTrue(figs)
                    for src in figs:
                        self.assertTrue((ROOT / "landing-pages" / src.lstrip("/")).exists(), src)
            for path in pages(sid):
                text = path.read_text(encoding="utf-8")
                og = re.search(r'<meta property="og:image" content="https://npcwoods.com/([^"?]+)', text).group(1)
                with self.subTest(og=og):
                    local = ROOT / "landing-pages" / og
                    self.assertTrue(local.exists(), og)
                    self.assertLess(local.stat().st_size, 150_000)

    def test_rebuild_matches_kitchen_pages(self):
        spec = importlib.util.spec_from_file_location("ccs_gold", ROOT / "scripts" / "build-condition-series-gold.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for sid in SERIES_IDS:
            built = {}
            mod.ccs.write = lambda path, text: built.__setitem__(Path(path), text)
            old_argv = sys.argv
            sys.argv = ["build", sid]
            try:
                mod.main()
            finally:
                sys.argv = old_argv
            self.assertEqual(len(built), len(pages(sid)))
            for path, text in built.items():
                with self.subTest(page=str(path.relative_to(ROOT))):
                    self.assertEqual(text, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
