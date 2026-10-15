"""Practice facts ledger. The named surfaces must match it.

Does not edit pages, skills, or spare website copies.
Run: python3 tests/test_practice_facts.py -v
"""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "practice_facts.py"
LEDGER = ROOT / "facts" / "practice.json"

STATES = ["AZ", "CO", "FL", "GA", "ID", "IA", "MT", "NV", "NM", "NC", "OR", "UT", "WA"]
LICENSES = ["AZ", "CO", "GA", "ID", "IA", "MT", "NV", "NM", "NC", "OR", "UT", "WA"]


def load_module():
    spec = importlib.util.spec_from_file_location("practice_facts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PracticeFactsTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()
        self.ledger = self.m.load_ledger(LEDGER)

    def test_locks_price_states_florida_and_credentials(self):
        self.assertEqual(self.ledger["price_usd"], 59)
        self.assertIs(self.ledger["pay_only_if_text_care_is_safe"], True)
        self.assertIs(self.ledger["no_subscription"], True)
        self.assertEqual(self.ledger["states_served"], STATES)
        self.assertEqual(self.ledger["aprn_licenses"], LICENSES)
        self.assertNotIn("FL", self.ledger["aprn_licenses"])
        florida = self.ledger["florida"]
        self.assertEqual(florida["id"], "TPAN3355")
        self.assertEqual(florida["kind"], "out-of-state telehealth registration")
        self.assertEqual(florida["not"], "Florida APRN license")
        self.assertEqual(florida["public_url"], "https://flhealthsource.gov/telehealth/")
        self.assertEqual(
            self.ledger["washington_public_page"]["rule"],
            "Do not print the Washington license number.",
        )
        self.assertEqual(self.ledger["credentials_confirmed"], ["MSN", "APRN", "FNP-C"])
        self.assertEqual(self.ledger["npi"], "1285125468")
        self.assertEqual(
            self.ledger["forbidden_words"],
            ["doctor", "Dr.", "physician", "MD", "insurance", "appointment"],
        )

    def test_acute_care_credential_stays_open(self):
        acute = self.ledger["acute_care_credential"]
        self.assertEqual(acute["status"], "open")
        self.assertEqual(acute["seen_as"], ["AGACNP-BC", "ACNP-BC"])
        self.assertIn("Do not pick a winner", acute["rule"])
        self.assertIn("Do not rewrite the site", acute["rule"])

    def test_named_surfaces_match_the_ledger(self):
        self.assertEqual(
            self.ledger["surfaces"],
            [
                "homepage/page-npcwoods-home.php",
                "php/npcwoods-robots-extras.php",
                "landing-pages/executive/index.html",
                "landing-pages/credentials/index.html",
            ],
        )
        self.assertEqual(self.ledger["surface_must_contain"], ["13 states", "TPAN3355"])
        self.assertEqual(self.ledger["surface_must_not_contain"], ["11 states"])
        self.assertEqual(self.m.surface_mismatches(ROOT, self.ledger), [])

    def test_eleven_state_copy_is_a_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = Path("homepage/page-npcwoods-home.php")
            (root / rel).parent.mkdir(parents=True)
            (root / rel).write_text("Licensed in 11 states.", encoding="utf-8")
            ledger = dict(self.ledger)
            ledger["surfaces"] = [str(rel)]
            problems = self.m.surface_mismatches(root, ledger)
        self.assertTrue(any("11 states" in problem for problem in problems))


class PageChecksTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()
        self.ledger = self.m.load_ledger(LEDGER)

    def test_page_drift_flags_old_and_overclaimed_state_counts(self):
        self.assertTrue(self.m.page_drift("landing-pages/x/index.html", "Licensed in 11 states", self.ledger))
        self.assertTrue(self.m.page_drift("landing-pages/x/index.html", "Licensed in 13 states", self.ledger))
        self.assertEqual(self.m.page_drift("landing-pages/x/index.html", "Serving 13 states", self.ledger), [])

    def test_surface_pages_must_carry_roster(self):
        problems = self.m.page_drift("landing-pages/credentials/index.html", "Serving 13 states", self.ledger)
        self.assertTrue(any("TPAN3355" in p for p in problems))

    ALLOWED = [
        "not a physician",
        "Collaborative Agreement with GA-Licensed Physician",
        "Collaborative Agreement with NC-Licensed Physician",
        "collaborative agreement with a Georgia-licensed physician",
        "collaborative agreement with a North Carolina-licensed physician",
        "collaborative agreement with an NC physician",
        "American Academy of Family Physicians",
        "American College of Physicians",
        "American College of Emergency Physicians",
        "American Family Physician",
    ]

    def test_allowed_phrases_are_exactly_chris_approved_list(self):
        self.assertEqual(self.ledger["banned_word_allowed_phrases"], self.ALLOWED)

    def test_no_allowed_phrase_is_a_bare_word_or_covers_another_banned_word(self):
        for phrase in self.ledger["banned_word_allowed_phrases"]:
            words = phrase.split()
            self.assertGreaterEqual(len(words), 3, phrase)
            for other in ("appointment", "doctor", "insurance"):
                self.assertNotIn(other, phrase.lower(), phrase)
            self.assertNotRegex(phrase, r"\bMD\b")
            # take out the one word the phrase exists for; nothing banned may remain
            rest = " ".join(w for w in words if not w.lower().startswith("physician")
                            and not w.lower().endswith("physician"))
            self.assertEqual(self.m.banned_word_hits(rest), [], phrase)

    def test_each_allowed_phrase_passes_in_page_text(self):
        allowed = self.ledger["banned_word_allowed_phrases"]
        for phrase in allowed:
            html = f"<p>Chris Woods, MSN, APRN, FNP-C. {phrase}.</p>"
            self.assertEqual(self.m.banned_word_hits(html, allowed), [], phrase)
        self.assertEqual(self.m.banned_word_hits(
            "<li><strong>American Academy of Family Physicians (AAFP)</strong>, Cellulitis</li>", allowed), [])
        self.assertEqual(self.m.banned_word_hits(
            '{"description":"Not a chatbot. Not an AI clinician. Not a physician."}', allowed), [])

    def test_same_word_outside_an_allowed_phrase_still_blocks(self):
        allowed = self.ledger["banned_word_allowed_phrases"]
        for html in (
            "<p>Talk to a physician today.</p>",
            "<p>Our physicians reply fast.</p>",
            "<p>He works with a Georgia-licensed physician.</p>",           # disclosure cut short
            "<p>American Family Physicians recommend this.</p>",           # not the journal name
            "<p>He is not a physician. A physician reviews every chart.</p>",  # second use is bare
        ):
            self.assertTrue(self.m.banned_word_hits(html, allowed), html)
        for html in ("<p>Book an appointment.</p>", "<p>Ask your doctor.</p>",
                     "<p>We take insurance.</p>", "<p>Seen by an MD.</p>"):
            self.assertTrue(self.m.banned_word_hits(html, allowed), html)

    def test_allowed_phrase_mechanism(self):
        html = "<p>American Academy of Family Physicians</p>"
        self.assertTrue(self.m.banned_word_hits(html))
        self.assertEqual(self.m.banned_word_hits(html, ["American Academy of Family Physicians"]), [])


if __name__ == "__main__":
    unittest.main()
