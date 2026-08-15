"""Regression checks for the telehealth-vs-urgent-care story page."""

from pathlib import Path
import unittest


PAGE = (
    Path(__file__).resolve().parents[1]
    / "landing-pages"
    / "telehealth-vs-urgent-care"
    / "index.html"
)


class TelehealthVsUrgentCarePageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = PAGE.read_text(encoding="utf-8")
        cls.lower_page = cls.page.lower()

    def test_story_keeps_the_promise_about_time_back_not_a_stopwatch(self):
        self.assertIn("Two ways to start care.", self.page)
        self.assertIn("One lets you keep your morning.", self.page)
        self.assertIn("Your part is done", self.page)
        for disallowed in ("four minutes", ">4m<", "same-day response"):
            self.assertNotIn(disallowed, self.lower_page)

    def test_page_has_no_prohibited_or_placeholder_marketing_copy(self):
        for disallowed in (
            "insurance",
            "subscription",
            "membership",
            "[your",
            "[states]",
            "[turnaround]",
            "[refund",
            "todo",
        ):
            self.assertNotIn(disallowed, self.lower_page)

    def test_page_uses_shared_site_shell_without_third_party_tracking(self):
        self.assertIn('href="/assets/css/site.css"', self.page)
        self.assertIn('src="/assets/js/site.js" defer', self.page)
        self.assertIn('class="npc-site-footer"', self.page)
        self.assertIn('https://npcwoods.com/medical-disclaimer/', self.page)
        for tracker in ("googletagmanager", "facebook.net", "analytics.ahrefs"):
            self.assertNotIn(tracker, self.lower_page)

    def test_story_has_accessible_motion_fallback_and_primary_sms_cta(self):
        self.assertIn('id="care-story"', self.page)
        self.assertIn("prefers-reduced-motion: reduce", self.page)
        self.assertIn(".stage{position:sticky;top:65px", self.page)
        self.assertIn("height:calc(100svh - 65px)", self.page)
        self.assertIn(".stage{position:sticky;top:57px", self.page)
        self.assertIn('href="sms:4806394722?', self.page)


if __name__ == "__main__":
    unittest.main()
