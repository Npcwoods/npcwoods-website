"""Compliance guard for the /employers/ employer-health landing page.

Keeps the page Google Ads-safe for future employer campaigns: no medication
or drug names, no "antibiotic", never "Florida-licensed", no outcome
promises, no invented prices, no tracking tags in the kitchen file.

Run: python3 tests/test_employers_page.py -v
"""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "landing-pages" / "employers" / "index.html"
ASSETS = ROOT / "landing-pages" / "employers" / "assets"
PLUGIN = ROOT / "php" / "npcwoods-employers-page.php"

MEDICATION_NAMES = [
    # anti-infectives
    "amoxicillin", "augmentin", "amoxicillin-clavulanate", "clavulanate", "penicillin",
    "cephalexin", "keflex", "cefdinir", "cefuroxime", "ceftriaxone", "cefpodoxime",
    "azithromycin", "z-pak", "zpak", "zithromax", "clarithromycin", "erythromycin",
    "doxycycline", "minocycline", "tetracycline", "ciprofloxacin", "cipro",
    "levofloxacin", "levaquin", "moxifloxacin", "nitrofurantoin", "macrobid",
    "macrodantin", "fosfomycin", "monurol", "trimethoprim", "sulfamethoxazole",
    "bactrim", "septra", "clindamycin", "metronidazole", "flagyl", "mupirocin",
    "bacitracin", "neosporin", "polymyxin", "ofloxacin", "tobramycin", "gentamicin",
    "fluconazole", "diflucan", "terbinafine", "nystatin", "clotrimazole", "miconazole",
    "ketoconazole", "valacyclovir", "valtrex", "acyclovir", "famciclovir",
    "oseltamivir", "tamiflu", "paxlovid", "baloxavir", "xofluza", "ivermectin",
    "permethrin",
    # steroids, allergy, pain, stomach
    "prednisone", "prednisolone", "methylprednisolone", "medrol", "dexamethasone",
    "triamcinolone", "hydrocortisone", "fluticasone", "flonase", "mometasone",
    "budesonide", "cetirizine", "zyrtec", "loratadine", "claritin", "fexofenadine",
    "allegra", "diphenhydramine", "benadryl", "hydroxyzine", "montelukast",
    "pseudoephedrine", "sudafed", "phenylephrine", "guaifenesin", "mucinex",
    "benzonatate", "tessalon", "dextromethorphan", "albuterol", "ibuprofen",
    "advil", "motrin", "naproxen", "aleve", "acetaminophen", "tylenol", "tramadol",
    "phenazopyridine", "pyridium", "azo", "ondansetron", "zofran", "omeprazole",
    "famotidine", "meclizine", "cyclobenzaprine", "lidocaine", "benzocaine",
    # ED, weight, other
    "sildenafil", "viagra", "tadalafil", "cialis", "vardenafil", "semaglutide",
    "ozempic", "wegovy", "rybelsus", "tirzepatide", "mounjaro", "zepbound",
    "liraglutide", "saxenda", "metformin", "glp-1", "glp1", "finasteride",
    "minoxidil", "tretinoin", "spironolactone",
]

BANNED_PATTERNS = [
    r"antibiotic",                 # any form: antibiotic, antibiotics
    r"florida[\s\-]+licensed",     # never "Florida-licensed"
    r"\binsurance\b",
    r"\bdoctors?\b",
    r"\bphysicians?\b",
    r"\bM\.?D\.?\b",
    r"\bappointments?\b",
    r"\bguarantee(d|s)?\b",
    r"\bdiscount(s|ed)?\b",
    r"\bgroup rates?\b",
    r"\bfree (month|trial)\b",
    r"\btestimonials?\b",
]

TRACKING_MARKERS = [
    "googletagmanager.com", "google-analytics.com", "googleadservices.com",
    "doubleclick.net", "gtag(", "dataLayer", "connect.facebook.net",
    "facebook.com/tr", "fbq(", "/tracking.js", "analytics.ahrefs.com",
]

STATES = [
    "Arizona", "Colorado", "Georgia", "Idaho", "Iowa", "Montana", "Nevada",
    "New Mexico", "North Carolina", "Oregon", "Utah", "Washington", "Florida",
]


class _Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self._skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


class EmployersPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        p = _Text()
        p.feed(cls.html)
        cls.visible = re.sub(r"\s+", " ", " ".join(p.parts))
        cls.jsonld = [
            json.loads(s)
            for s in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
                                cls.html, flags=re.S)
        ]

    def test_no_medication_names_anywhere(self):
        lower = self.html.lower()
        for name in MEDICATION_NAMES:
            self.assertIsNone(re.search(r"(?<![a-z0-9])" + re.escape(name) + r"(?![a-z0-9])", lower),
                              f"medication name on employer page: {name}")

    def test_no_banned_words(self):
        for pat in BANNED_PATTERNS:
            self.assertIsNone(re.search(pat, self.html, re.I), f"banned pattern: {pat}")

    def test_no_tracking_tags_in_kitchen_file(self):
        for marker in TRACKING_MARKERS:
            self.assertNotIn(marker, self.html)

    def test_only_price_is_59(self):
        prices = set(re.findall(r"\$\s?\d+(?:[.,]\d+)*", self.visible))
        self.assertEqual(prices, {"$59"}, prices)

    def test_states_line_and_exact_list(self):
        self.assertIn("13 states, including Florida by telehealth registration", self.visible)
        for state in STATES:
            self.assertIn(state, self.visible)

    def test_head_seo(self):
        self.assertIn("<title>Employer Health: $59 Text Visits for Your Team | NPCWoods</title>", self.html)
        self.assertIn('<link rel="canonical" href="https://npcwoods.com/employers/">', self.html)
        self.assertIn('property="og:image" content="https://npcwoods.com/employers/assets/employers-og.jpg"', self.html)
        self.assertIn('name="twitter:card" content="summary_large_image"', self.html)
        self.assertRegex(self.html, r'<meta name="description" content="[^"]{110,165}">')
        self.assertEqual(self.html.count("<h1"), 1)

    def test_json_ld_parses_and_has_required_types(self):
        types = {d.get("@type") for d in self.jsonld}
        for t in ("FAQPage", "BreadcrumbList", "MedicalBusiness", "WebPage"):
            self.assertIn(t, types)
        faq = next(d for d in self.jsonld if d["@type"] == "FAQPage")
        self.assertEqual(len(faq["mainEntity"]), self.html.count("<summary>"))
        for q in faq["mainEntity"]:
            self.assertIn(q["name"].replace("'", "&#x27;"), self.html)
        crumbs = next(d for d in self.jsonld if d["@type"] == "BreadcrumbList")
        self.assertEqual(crumbs["itemListElement"][-1]["item"], "https://npcwoods.com/employers/")

    def test_ctas_use_site_text_number(self):
        self.assertIn('href="sms:4806394722?body=', self.html)
        self.assertIn("Start a pilot &middot; Text Chris", self.html)
        self.assertIn("Talk to Chris about a pilot for your team", self.html)

    def test_flyer_link_points_to_real_asset(self):
        self.assertIn("/employers/assets/npcwoods-break-room-flyer.pdf", self.html)
        self.assertTrue((ASSETS / "npcwoods-break-room-flyer.pdf").is_file())
        for name in ("employers-og.jpg", "chris-cutout-600.webp", "chris-cutout-900.webp"):
            self.assertTrue((ASSETS / name).is_file(), name)

    def test_mu_plugin_routes_only_employers_with_no_named_functions(self):
        php = PLUGIN.read_text(encoding="utf-8")
        self.assertIn("'employers' !== $slug", php)
        self.assertIn("ABSPATH . 'employers/index.html'", php)
        self.assertIsNone(re.search(r"^\s*function\s+\w+", php, re.M))


    def test_privacy_line_uses_plain_hipaa_wording(self):
        self.assertNotIn("HIPAA-compliant", self.html)
        self.assertNotIn("Health details stay between", self.html)
        self.assertGreaterEqual(self.visible.count("Your employer never sees your health details. We follow HIPAA."), 2)
        faq = next(d for d in self.jsonld if d["@type"] == "FAQPage")
        answers = [q["acceptedAnswer"]["text"] for q in faq["mainEntity"]]
        self.assertIn("No. Your employer never sees your health details. We follow HIPAA.", answers)

    def test_work_injury_faq_in_visible_and_json_ld(self):
        q = "What about injuries on the job?"
        a = ("On-the-job injuries go through your company's workers' comp process. Chris handles "
             "everyday sickness like colds, UTIs, and rashes. Emergencies, call 911.")
        self.assertIn(q, self.visible)
        self.assertIn(a, self.visible)
        faq = next(d for d in self.jsonld if d["@type"] == "FAQPage")
        pairs = {x["name"]: x["acceptedAnswer"]["text"] for x in faq["mainEntity"]}
        self.assertEqual(pairs.get(q), a)

    def test_pilot_cost_line_matches_member_pays_model(self):
        self.assertIn("No cost to your company to start a pilot. Team members pay $59 per visit.", self.visible)
        self.assertIn("only pays if Chris can treat them", self.visible)

    def test_blue_bubble_contrast_at_least_4_5(self):
        m = re.search(r"\.bubble\.me\{[^}]*background:(#[0-9A-Fa-f]{6})", self.html)
        self.assertIsNotNone(m)
        def lum(hx):
            out = []
            for i in (1, 3, 5):
                c = int(hx[i:i + 2], 16) / 255
                out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
            return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]
        self.assertGreaterEqual(1.05 / (lum(m.group(1)) + 0.05), 4.5)

if __name__ == "__main__":
    unittest.main()
