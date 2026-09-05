"""Guardrails for the paid-search dental pain landing page."""

import json
import re
import subprocess
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "landing-pages" / "dental-pain" / "search-safe" / "index.html"
ROUTER = ROOT / "php" / "npcwoods-dental-pages.php"
SAVER_MARKERS = (
    "npc_attribution_last",
    "npc_attribution_first",
    "NPCWoodsAttribution",
    "gclid",
    "gbraid",
    "wbraid",
)
SAVER_THIRD_PARTY = (
    "fetch(",
    "sendbeacon",
    "xmlhttprequest",
    "navigator.sendbeacon",
    "gtag(",
    "fbq(",
    "new image",
)


def live_markup(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).lower()


def page_text() -> str:
    if not PAGE.exists():
        raise AssertionError("paid dental page is missing")
    return PAGE.read_text(encoding="utf-8")


class DentalSearchSafePageTest(unittest.TestCase):
    def test_page_exists_and_has_search_safe_metadata(self):
        self.assertTrue(PAGE.exists(), "paid dental page is missing")
        text = page_text()
        self.assertIn(
            '<link rel="canonical" href="https://npcwoods.com/dental-pain/search-safe/">',
            text,
        )
        self.assertRegex(text, r'<meta name="robots" content="[^"]*noindex[^"]*">')
        self.assertIn("window.NPCWoodsPaidSurface = true", text)

    def test_page_leads_with_evaluation_price_and_safety(self):
        text = page_text()
        for required in (
            "Dental pain? Text Chris, NP.",
            "$59 flat fee",
            "not charged if",
            "hands-on dental care",
            "Call 911",
            "sms:+14806394722",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_live_markup_has_no_medication_sales_language_or_health_pixels(self):
        text = live_markup(page_text())
        forbidden = (
            "clindamycin",
            "amoxicillin",
            "penicillin",
            "antibiotic",
            "prescription",
            "fast rx",
            "connect.facebook.net",
            "facebook.com/tr",
            "googletagmanager.com",
            "google-analytics.com",
            "googleadservices.com",
            "doubleclick.net",
            "/tracking.js",
            "/users/",
            "content-output/",
        )
        for marker in forbidden:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, text)

    def test_forbidden_marketing_words_are_absent(self):
        text = live_markup(page_text())
        for pattern in (r"\bdoctor\b", r"\bphysician\b", r"\bmd\b", r"\bappointment\b"):
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, text, flags=re.I))

    def test_page_has_shared_chrome_and_schema(self):
        text = page_text()
        self.assertIn("npc-nav", text)
        self.assertIn("npc-site-footer", text)
        self.assertIn('type="application/ld+json"', text)
        self.assertIn('"@type": "MedicalWebPage"', text)
        self.assertIn('"@type": "FAQPage"', text)

    def test_router_maps_exact_clean_url(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn(
            "'/dental-pain/search-safe/' => 'dental-pain/search-safe/index.html'",
            text,
        )

    def test_first_party_click_id_saver_is_present_and_stays_local(self):
        text = page_text()
        for marker in SAVER_MARKERS:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)
        saver = live_markup(text)
        for marker in SAVER_THIRD_PARTY:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, saver)

    def test_gclid_is_stored_in_pay_page_shape(self):
        stored = run_saver("?gclid=TESTGCLID1234567890")
        last = stored["last"]
        self.assertEqual("google", last["source"])
        self.assertEqual("cpc", last["medium"])
        self.assertEqual("TESTGCLID1234567890", last["click_id"])
        self.assertEqual("gclid", last["click_id_type"])
        self.assertGreater(last["expiresAt"], 0)
        self.assertEqual(last["click_id"], stored["first"]["click_id"])
        self.assertEqual("TESTGCLID1234567890", stored["attribution"]["click_id"])

    def test_utm_campaign_survives_with_click_id(self):
        stored = run_saver(
            "?utm_source=google&utm_medium=cpc&utm_campaign=search-15&gclid=LIVECLICKIDABCDEF"
        )
        last = stored["last"]
        self.assertEqual("search-15", last["campaign"])
        self.assertEqual("LIVECLICKIDABCDEF", last["click_id"])
        self.assertEqual("gclid", last["click_id_type"])

    def test_stored_click_id_folds_into_stripe_reference_on_pay(self):
        from tests.test_pay_attribution import run_pay_submit

        stored = run_saver("?gclid=TESTGCLID1234567890")
        redirect = run_pay_submit("", stored["last"])
        params = redirect["params"]
        self.assertEqual("google", params["utm_source"])
        self.assertEqual("cpc", params["utm_medium"])
        self.assertEqual("TESTGCLID1234567890", params["gclid"])
        self.assertEqual(
            "google-cpc-manual-payment-gclid-TESTGCLID1234567890",
            params["client_reference_id"],
        )


def run_saver(query: str) -> dict:
    runner = textwrap.dedent(
        """
        const fs = require('fs');
        const html = fs.readFileSync(process.argv[1], 'utf8');
        const query = process.argv[2] || '';
        const match = html.match(/<script>\\s*(window\\.NPCWoodsPaidSurface = true;[\\s\\S]*?\\}\\)\\(\\);)\\s*<\\/script>/);
        if (!match) throw new Error('saver script not found');
        const storage = {};
        global.window = {
          location: { search: query, pathname: '/dental-pain/search-safe/' },
          localStorage: {
            getItem(key) { return Object.prototype.hasOwnProperty.call(storage, key) ? storage[key] : null; },
            setItem(key, value) { storage[key] = String(value); },
            removeItem(key) { delete storage[key]; },
          },
        };
        global.URLSearchParams = URLSearchParams;
        eval(match[1]);
        const last = storage.npc_attribution_last ? JSON.parse(storage.npc_attribution_last) : null;
        const first = storage.npc_attribution_first ? JSON.parse(storage.npc_attribution_first) : null;
        console.log(JSON.stringify({
          last,
          first,
          attribution: global.window.NPCWoodsAttribution || {},
        }));
        """
    )
    completed = subprocess.run(
        ["node", "-e", runner, str(PAGE), query],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


if __name__ == "__main__":
    unittest.main()
