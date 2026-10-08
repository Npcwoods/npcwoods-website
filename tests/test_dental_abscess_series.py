"""Kitchen checks for the dental-abscess mini-series and PMax offer page."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERIES_DIR = ROOT / "landing-pages" / "learn" / "dental-abscess"
OFFER = ROOT / "landing-pages" / "dental-abscess-treatment" / "index.html"
SERIES_JSON = SERIES_DIR / "series.json"
EDU = ROOT / "php" / "npcwoods-education-pages.php"
DENTAL = ROOT / "php" / "npcwoods-dental-pages.php"

MED_NAME_RE = re.compile(
    r"""
    amoxicillin|amoxil|augmentin|clavulanate|penicillin|pen-vk|
    clindamycin|cleocin|metronidazole|flagyl|cephalexin|keflex|
    azithromycin|zithromax|z-pak|\bzpak\b|doxycycline|ciprofloxacin|
    \bcipro\b|levofloxacin|levaquin|ibuprofen|advil|motrin|
    acetaminophen|tylenol|naproxen|\baleve\b|\baspirin\b|
    hydrocodone|oxycodone|vicodin|percocet|\bnorco\b|tramadol|
    \bcodeine\b|lidocaine|benzocaine|orajel|chlorhexidine|
    prednisone|macrobid|nitrofurantoin|bactrim|septra|
    phenazopyridine|pyridium|ozempic|wegovy|mounjaro
    """,
    re.I | re.X,
)
TRACKER_RE = re.compile(
    r"googletagmanager|google-analytics|googleadservices|connect\.facebook\.net|"
    r"facebook\.com/tr|analytics\.ahrefs|/tracking\.js",
    re.I,
)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def series() -> dict:
    return json.loads(SERIES_JSON.read_text(encoding="utf-8"))


def html_files() -> list[Path]:
    files = [SERIES_DIR / "index.html", OFFER]
    for stop in series()["stops"]:
        if stop["slug"]:
            files.append(SERIES_DIR / stop["slug"] / "index.html")
    return files


class DentalAbscessSeriesTest(unittest.TestCase):
    def test_series_json_accent_and_stops(self):
        data = series()
        self.assertEqual(data["accent"]["name"], "red")
        self.assertEqual(data["accent"]["hex"].lower(), "#b42318")
        self.assertEqual(len(data["stops"]), 10)
        self.assertEqual(data["stops"][0]["path"], "/learn/dental-abscess/")
        self.assertEqual(data["one_pager"]["path"], "/dental-abscess-treatment/")
        self.assertIn("Florida by telehealth registration", data["license_line"])
        self.assertEqual(data["sms"]["number"], "4806394722")

    def test_all_pages_built(self):
        for path in html_files():
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertTrue(path.exists(), f"missing {path}")
                self.assertGreater(path.stat().st_size, 20_000)

    def test_pages_have_schema_bubbles_and_roadmap(self):
        for path in html_files():
            text = path.read_text(encoding="utf-8")
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertIn('"@type": "MedicalWebPage"', text)
                self.assertIn('"@type": "FAQPage"', text)
                self.assertIn('"@type": "BreadcrumbList"', text)
                self.assertIn("bubble-blue", text)
                self.assertIn("bubble-black", text)
                self.assertIn("#007AFF", text)
                self.assertIn("series-sticky", text)
                self.assertIn("GTM, GA4, and Google Ads stay off", text)
                self.assertIn("13 states, including Florida by telehealth registration", text)
                self.assertIn("does not guarantee a prescription", text.lower())
                self.assertNotIn("Florida-licensed", text)
                self.assertNotIn("Florida licensed", text)

    def test_offer_links_into_series(self):
        text = OFFER.read_text(encoding="utf-8")
        self.assertIn("https://npcwoods.com/learn/dental-abscess/", text)
        self.assertIn("Explained plainly", text)
        self.assertIn("$59", text)
        self.assertIn("sms:4806394722", text)

    def test_hub_has_you_are_here_roadmap(self):
        text = (SERIES_DIR / "index.html").read_text(encoding="utf-8")
        self.assertIn("You are here", text)
        self.assertIn("roadmap-list", text)

    def test_zero_medication_names_in_series_build(self):
        roots = [SERIES_DIR, OFFER.parent]
        hits = []
        for root in roots:
            for path in root.rglob("*"):
                if path.suffix.lower() not in {".html", ".json", ".css"}:
                    continue
                if path.name == "README.md":
                    continue
                for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    if MED_NAME_RE.search(line):
                        hits.append(f"{path.relative_to(ROOT)}:{i}:{line.strip()}")
        self.assertEqual(hits, [], "medication names in series build:\n" + "\n".join(hits))

    def test_zero_antibiotic_class_word_in_series_build(self):
        # PMax / Site Audit restricted class word. Fail everywhere in the
        # series HTML/JSON/CSS build. The real CDC source URL may keep
        # /antibiotic-use/ in the path; display titles must stay soft.
        allowed_url = "https://www.cdc.gov/antibiotic-use/index.html"
        class_word = re.compile(r"antibiotics?", re.I)
        roots = [SERIES_DIR, OFFER.parent]
        hits = []
        for root in roots:
            for path in root.rglob("*"):
                if path.suffix.lower() not in {".html", ".json", ".css"}:
                    continue
                scrubbed = path.read_text(encoding="utf-8").replace(allowed_url, "")
                for i, line in enumerate(scrubbed.splitlines(), 1):
                    if class_word.search(line):
                        hits.append(f"{path.relative_to(ROOT)}:{i}:{line.strip()}")
        self.assertEqual(
            hits, [], "antibiotic class word in series build:\n" + "\n".join(hits)
        )

    def test_no_ad_trackers_in_live_markup(self):
        for path in html_files():
            live = COMMENT_RE.sub("", path.read_text(encoding="utf-8"))
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertIsNone(TRACKER_RE.search(live))
                self.assertNotIn("no tracking", live.lower())
                self.assertNotIn("noindex", live.lower())

    def test_mu_plugin_routes(self):
        edu = EDU.read_text(encoding="utf-8")
        dental = DENTAL.read_text(encoding="utf-8")
        for stop in series()["stops"]:
            self.assertIn(f"'{stop['path']}'", edu.replace(" ", ""))
            self.assertIn(stop["path"], edu)
        self.assertIn("/dental-abscess-treatment/", dental)
        self.assertIn("dental-abscess-treatment/index.html", dental)

    def test_forbidden_marketing_words_in_series_copy(self):
        # Shared footer says "No appointment." Ignore that chrome.
        for path in html_files():
            text = path.read_text(encoding="utf-8")
            main = text.split('<main id="main">', 1)[-1]
            main = main.split('<footer', 1)[0]
            lower = main.lower()
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertNotIn("physician", lower)
                self.assertNotRegex(lower, r"\bdoctors?\b")
                self.assertNotIn("insurance", lower)
                self.assertNotIn("guaranteed results", lower)


    def test_background_matches_glp1_per_page_type(self):
        # Hub copies /learn/glp1/ (vertical night -> neon blue -> cream -> white
        # body gradient). Stops copy /learn/glp1/<stop>/ (dark neon-glow hero
        # band on a white page). Offer copies /glp1-weight-loss/ (blue hero band
        # on a white page).
        css = (SERIES_DIR / "_shared" / "series.css").read_text(encoding="utf-8")
        for stop in (
            "#05060a 10%", "#071a3a 18%", "#0a84ff 34%", "#0a84ff 48%",
            "#5eb8ff 58%", "#F6F3EE 72%", "#FFFFFF 100%",
        ):
            self.assertIn(stop, css)
        self.assertIn("rgba(0,113,227,.42)", css)
        hub = (SERIES_DIR / "index.html").read_text(encoding="utf-8")
        self.assertIn('<body class="series-page series-hub">', hub)
        self.assertIn('<body class="series-page series-offer">', OFFER.read_text(encoding="utf-8"))
        for stop in series()["stops"]:
            if not stop["slug"]:
                continue
            text = (SERIES_DIR / stop["slug"] / "index.html").read_text(encoding="utf-8")
            with self.subTest(page=stop["slug"]):
                self.assertIn('<body class="series-page series-stop">', text)

    def test_one_accent_only(self):
        css = (SERIES_DIR / "_shared" / "series.css").read_text(encoding="utf-8")
        self.assertIn("--accent: #B42318;", css)
        # No second series accent hue snuck in with the background work.
        for other in ("#f5a524", "#F5A524", "#19a463"):
            self.assertNotIn(other, css)


if __name__ == "__main__":
    unittest.main()
