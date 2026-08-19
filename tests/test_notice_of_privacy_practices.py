"""Live-ready checks for the Notice of Privacy Practices page."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "landing-pages" / "notice-of-privacy-practices" / "index.html"
FOOTER = ROOT / "html" / "shared" / "footer-snippet.html"
SITEMAP = ROOT / "landing-pages" / "sitemap" / "index.html"
ROUTE = ROOT / "php" / "npcwoods-static-pages.php"
COMPLIANCE = ROOT / "php" / "npcwoods-compliance-footer.php"

LEDE = (
    "This notice describes how medical information about you may be used "
    "and disclosed and how you can get access to this information. "
    "Please review it carefully."
)
DRAFT_MARKERS = (
    "draft for review",
    "this page is a draft",
    "not published",
    "not the notice currently in effect",
    "not legal advice",
)
FORBIDDEN = (
    "doctor",
    "doctors",
    "physician",
    "physicians",
    "insurance",
    "noindex",
)


class NoticeOfPrivacyPracticesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = PAGE.read_text(encoding="utf-8")
        cls.footer = FOOTER.read_text(encoding="utf-8")
        cls.sitemap = SITEMAP.read_text(encoding="utf-8")
        cls.route = ROUTE.read_text(encoding="utf-8")
        cls.compliance = COMPLIANCE.read_text(encoding="utf-8")
        cls.lower = cls.page.lower()

    def test_page_is_indexable_with_locked_title_and_h1(self):
        self.assertIn('<meta name="robots" content="index, follow">', self.page)
        self.assertNotRegex(self.page, re.compile(r"noindex", re.I))
        self.assertIn("<title>Notice of Privacy Practices</title>", self.page)
        self.assertIn("<h1>Notice of Privacy Practices</h1>", self.page)
        self.assertIn(
            '<link rel="canonical" href="https://npcwoods.com/notice-of-privacy-practices/">',
            self.page,
        )

    def test_locked_facts_and_standard_sections(self):
        self.assertIn("Effective date: August 19, 2026", self.page)
        self.assertIn(LEDE, self.page)
        self.assertIn("NPCWoods Telemedicine", self.page)
        self.assertIn("Chris Woods, MSN, APRN, FNP-C", self.page)
        self.assertIn("nurse practitioner", self.lower)
        self.assertIn("$59 cash", self.page)
        self.assertIn("cwoods@npcwoods.com", self.page)
        self.assertIn("(480) 639-4722", self.page)
        self.assertIn("https://www.hhs.gov/hipaa/filing-a-complaint/", self.page)
        self.assertIn("We do not sell", self.page)
        self.assertIn("Filing a complaint will not change your care.", self.page)
        self.assertIn("We may revise this notice.", self.page)
        for state in ("Arizona", "Colorado", "Georgia", "Idaho", "Iowa",
                      "Montana", "Nevada", "New Mexico", "North Carolina",
                      "Oregon", "Utah"):
            self.assertIn(state, self.page)

    def test_no_draft_language_or_forbidden_words(self):
        for marker in DRAFT_MARKERS:
            self.assertNotIn(marker, self.lower)
        for word in FORBIDDEN:
            self.assertIsNone(
                re.search(rf"\b{re.escape(word)}\b", self.lower),
                f"forbidden word present: {word}",
            )
        self.assertNotIn("not legal advice", self.lower)
        self.assertIn("&copy; 2026 NPCWoods", self.page)

    def test_uses_shared_header_and_footer(self):
        self.assertIn("NPCWOODS SITE HEADER (Shared Component)", self.page)
        self.assertIn("NPCWOODS SITE FOOTER (Shared Component)", self.page)
        self.assertIn('href="/assets/css/site.css"', self.page)
        self.assertIn('src="/assets/js/site.js" defer', self.page)
        self.assertIn('class="npc-site-footer"', self.page)
        self.assertIn("/notice-of-privacy-practices/", self.footer)
        self.assertIn("Notice of Privacy Practices", self.footer)

    def test_route_sitemap_and_footer_link(self):
        self.assertIn(
            '"notice-of-privacy-practices" => "notice-of-privacy-practices/index.html"',
            self.route,
        )
        self.assertNotIn('"/npp/"', self.route)
        self.assertNotIn('"/hipaa/"', self.route)
        self.assertIn(
            'href="https://npcwoods.com/notice-of-privacy-practices/"',
            self.sitemap,
        )
        self.assertIn(
            'href="/notice-of-privacy-practices/">Notice of Privacy Practices</a>',
            self.compliance,
        )

    def test_no_npp_or_hipaa_aliases(self):
        self.assertNotIn("npcwoods.com/npp/", self.page)
        self.assertNotIn("npcwoods.com/hipaa/", self.page)
        self.assertNotIn('href="/npp/"', self.page)
        self.assertNotIn('href="/hipaa/"', self.page)
        self.assertNotIn("/npp/", self.route)
        self.assertNotIn("/hipaa/", self.route)

    def test_google_and_meta_pixels_are_absent(self):
        for token in (
            "GTM-59QSWZRC",
            "G-EFFRQMG8TC",
            "AW-610222919",
            "googletagmanager.com",
            "google-site-verification",
            "connect.facebook.net",
            "facebook.com/tr",
            "fbq(",
            "fbq ('",
        ):
            self.assertNotIn(token, self.page)


if __name__ == "__main__":
    unittest.main()
