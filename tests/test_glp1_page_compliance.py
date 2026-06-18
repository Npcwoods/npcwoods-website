import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "landing-pages" / "glp1-weight-loss" / "index.html"


class Glp1PageComplianceTest(unittest.TestCase):
    def setUp(self):
        self.text = PAGE.read_text(encoding="utf-8")

    def test_glp1_page_uses_consult_forward_copy(self):
        self.assertIn("$59 GLP-1 consult by text", self.text)
        self.assertIn("oral GLP-1 options", self.text)
        self.assertIn("health history, safety factors, and fit", self.text)

    def test_glp1_page_avoids_blocked_and_high_risk_public_terms(self):
        blocked_patterns = [
            r"\binsurance\b",
            r"\bdoctor(s)?\b",
            r"\bsubscription(s)?\b|\bmembership(s)?\b",
            r"\bprescription(s)?\b|\bprescribe(s|d)?\b",
            r"\bmedication(s)?\b|\bmeds\b",
            r"\bsemaglutide\b|\btirzepatide\b",
            r"\bguarantee(d|s)?\b|\bresults?\b",
            r"\bweight loss\b",
            r"\bboard-certified\b",
        ]
        for pattern in blocked_patterns:
            self.assertIsNone(re.search(pattern, self.text, re.IGNORECASE), pattern)

    def test_glp1_page_has_smart_content_after_tracking_js(self):
        tracking = '<script src="/tracking.js?v=20260528-no-phi"></script>'
        smart = '<script src="/smart-content.js?v=20260531"></script>'

        self.assertIn(tracking, self.text)
        self.assertIn(smart, self.text)
        self.assertLess(self.text.index(tracking), self.text.index(smart))
        self.assertIn('data-npc-personalize="headline"', self.text)
        self.assertIn('data-npc-personalize="subheadline"', self.text)
        self.assertIn('data-npc-personalize="cta-text"', self.text)

    def test_glp1_page_uses_verified_google_review_snippets(self):
        self.assertIn("Mary W.", self.text)
        self.assertIn("Dana H.", self.text)
        self.assertIn("Tori D.", self.text)
        self.assertIn(
            "Even though the visit was online, I felt that all of my concerns were addressed",
            self.text,
        )
        self.assertIn("Quick, professional and convenient", self.text)
        self.assertIn("It was so simple and doing it from my house", self.text)

    def test_glp1_json_ld_is_valid(self):
        scripts = re.findall(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            self.text,
            flags=re.DOTALL,
        )

        self.assertGreaterEqual(len(scripts), 4)
        for script in scripts:
            json.loads(script)


if __name__ == "__main__":
    unittest.main()
