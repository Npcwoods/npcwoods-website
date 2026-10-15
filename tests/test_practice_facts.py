"""Practice facts ledger. Four named surfaces must match it.

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
            ["doctor", "Dr.", "physician", "MD", "insurance"],
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
                "templates/glp1-explainer/partials/site-footer.html",
                "templates/uti-explainer/partials/site-footer.html",
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


if __name__ == "__main__":
    unittest.main()
