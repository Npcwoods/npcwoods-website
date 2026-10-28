"""FAQ patient copy (visible text + FAQPage JSON-LD) carries no drug-class words or
medication names (Chris 2026-10-28), and the FAQPage schema matches the visible Q&A."""
from __future__ import annotations

import html as H
import json
import re
import unittest
from pathlib import Path

FAQ = Path(__file__).resolve().parents[1] / "landing-pages/faq/index.html"
BANNED = re.compile(
    r"\b(antibiotics?|rx|prescriptions?|prescrib\w*|meds|medications?|scripts?|opioids?|benzos?|"
    r"stimulants?|amoxicillin\w*|doxycycline|azithromycin)\b", re.I)


def _vis(x: str) -> str:
    return " ".join(H.unescape(re.sub(r"<[^>]+>", " ", x)).split()).replace(" .", ".")


class FaqNoDrugClassWordsTests(unittest.TestCase):
    def setUp(self):
        self.html = FAQ.read_text(encoding="utf-8")

    def _visible_text(self) -> str:
        body = self.html[self.html.find("<body"):]
        body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", body, flags=re.S)
        # footer nav link label to /medications/ is the shared sitewide footer, out of scope here
        body = body.replace('<a href="https://npcwoods.com/medications/">Medications</a>', "")
        return _vis(body)

    def test_visible_copy_has_no_drug_class_words(self):
        hits = sorted({m.group(0).lower() for m in BANNED.finditer(self._visible_text())})
        self.assertEqual(hits, [])

    def test_faq_schema_has_no_drug_class_words_and_matches_visible(self):
        blocks = [json.loads(b) for b in re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', self.html, re.S)]
        faq = next(b for b in blocks if b.get("@type") == "FAQPage")
        schema = [(q["name"], q["acceptedAnswer"]["text"]) for q in faq["mainEntity"]]
        for q, a in schema:
            self.assertIsNone(BANNED.search(q), q)
            self.assertIsNone(BANNED.search(a), a)
        visible = [_vis(m.group(1)) for m in re.finditer(
            r'<button class="accordion-button"[^>]*>(.*?)</button>', self.html, re.S)]
        visible += [_vis(m.group(1)) for m in re.finditer(
            r'<article class="aeo-qa-item"[^>]*>\s*<h2>(.*?)</h2>', self.html, re.S)]
        self.assertEqual(sorted(q for q, _ in schema), sorted(visible))


if __name__ == "__main__":
    unittest.main()
