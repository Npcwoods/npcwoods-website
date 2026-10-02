"""Las Vegas sinus draft + SEO orphan / internal-link locks. Git only. Not live."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMS = "sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit"
FOOTER_MARK = "<!-- ===== NPCWOODS SITE FOOTER (Shared Component) ===== -->"
HIPAA = "GTM, GA4, and Google Ads stay off this health-condition page (no BAA)."
LV_HTML = "landing-pages/sinus-infection-treatment/las-vegas-nv/index.html"
LV_PLUGIN = "php/npcwoods-sinus-las-vegas.php"
LV_URL = "https://npcwoods.com/sinus-infection-treatment/las-vegas-nv/"
LOCKED_911 = (
    "Text-based telehealth is not for emergencies. "
    "If you have chest pain, trouble breathing, or other emergency symptoms, call 911."
)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def body_only(html: str) -> str:
    return html.split(FOOTER_MARK, 1)[0] if FOOTER_MARK in html else html


class LasVegasSinusDraftTests(unittest.TestCase):
    def test_lv_sinus_page_is_a_real_city_plate(self):
        path = ROOT / LV_HTML
        self.assertTrue(path.exists())
        self.assertGreaterEqual(path.stat().st_size, 50000)
        html = read(LV_HTML)
        page = body_only(html)
        title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        desc = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.I)
        self.assertIsNotNone(title)
        self.assertIsNotNone(desc)
        self.assertEqual(
            "Sinus Treatment in Las Vegas, NV | $59 Text Visit",
            re.sub(r"\s+", " ", title.group(1)).strip(),
        )
        self.assertLessEqual(len(re.sub(r"\s+", " ", title.group(1)).strip()), 60)
        self.assertEqual(
            "Online sinus care in Las Vegas. Text Chris Woods, NP. $59. Same-day pharmacy when it is safe. You only pay if he can treat you.",
            desc.group(1).strip(),
        )
        self.assertLessEqual(len(desc.group(1).strip()), 155)
        self.assertIn("Sinus infection in Las Vegas and you don’t want the waiting room? Text Chris.", html)
        self.assertIn(LV_URL, html)
        self.assertIn("Summerlin", page)
        self.assertIn("Nevada", page)
        self.assertIn(SMS, html)
        self.assertIn("Hi Chris, I'd like to start a $59 visit", html)
        self.assertIn("$59", html)
        self.assertIn("Chris Woods, MSN, APRN, FNP-C", html)
        self.assertIn("npc-clinician-byline", html)
        self.assertIn("<!-- ===== NPCWOODS SITE HEADER (Shared Component) ===== -->", html)
        self.assertIn(FOOTER_MARK, html)
        self.assertIn(LOCKED_911, html)
        self.assertIn("notice-of-privacy-practices", html)
        self.assertIn(HIPAA, html)
        self.assertIn("window.fbq = function", html)
        self.assertIn("--brand: #9B1C1C;", html)
        self.assertNotIn("Antibiotics without leaving home", html)
        self.assertNotIn("tracking.js", html)
        self.assertNotIn("aggregateRating", html)
        self.assertNotIn("googletagmanager.com", html)
        self.assertNotRegex(html, r"GTM-[A-Z0-9]+|G-[A-Z0-9]+|AW-\d+")
        self.assertIsNone(re.search(r"fbq\s*\(\s*['\"]init['\"]", html))
        self.assertNotRegex(page, r"(?i)\b(doctor|physician|insurance)\b")
        self.assertNotRegex(page, r"\bMD\b")
        self.assertNotIn("geoCoordinates", html)
        for city in ("Mesa", "Tucson", "Chandler", "Banner"):
            self.assertNotIn(city, page)
        # Shared CSS comment says "Phoenix-style"; story copy must not.
        # Shared footer mailing line names Scottsdale. That is the live snippet.

    def test_lv_footer_matches_shared_snippet_once(self):
        html = read(LV_HTML)
        snippet = read("html/shared/footer-snippet.html")
        self.assertEqual(html.count("<!-- ===== NPCWOODS SITE FOOTER (Shared Component) ===== -->"), 1)
        self.assertEqual(html.count("&copy; 2026"), 1)
        self.assertEqual(html.count("npc-site-footer"), 1)
        self.assertIn(
            "Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT",
            html,
        )
        self.assertEqual(
            html.count("Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT"),
            1,
        )
        self.assertNotIn("Licensed in NV, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT", html)
        # Exact shared trust/copyright block, so the plate cannot drift again.
        self.assertIn(
            "<span>&copy; 2026 NPCWoods Telehealth. All rights reserved.</span>",
            html,
        )
        self.assertIn(
            snippet.split("<!-- ===== NPCWOODS SITE FOOTER", 1)[1].split(
                "<!-- ===== END SITE FOOTER ===== -->", 1
            )[0],
            html,
        )

    def test_lv_sinus_plugin_matches_full_path_and_blocks_uti_canonical(self):
        php = read(LV_PLUGIN)
        self.assertIn("parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH )", php)
        self.assertIn("'/sinus-infection-treatment/las-vegas-nv/'", php)
        self.assertIn("sinus-infection-treatment/las-vegas-nv/index.html", php)
        self.assertIn("redirect_canonical", php)
        self.assertIn("return false", php)
        self.assertNotIn("get_post_field", php)
        self.assertEqual(php.count("=>"), 1)
        self.assertNotIn("'/uti-treatment/las-vegas-nv/'", php)

    def test_redirect_maps_do_not_send_lv_sinus_to_uti(self):
        redirects = read("php/npcwoods-redirects.php")
        cleanup = read("php/npcwoods-redirects-404-cleanup.php")
        self.assertNotIn('"/sinus-infection-treatment/las-vegas-nv/"', redirects)
        self.assertNotIn(
            '"/sinus-infection-treatment/las-vegas-nv/" => "/uti-treatment/las-vegas-nv/"',
            cleanup,
        )
        self.assertNotRegex(
            cleanup,
            r'"/sinus-infection-treatment/las-vegas-nv/"\s*=>',
        )
        self.assertIn("npcwoods-sinus-las-vegas.php", cleanup)


class SeoOrphanAndInternalLinkTests(unittest.TestCase):
    def test_html_sitemap_lists_former_yoast_orphans(self):
        html = read("landing-pages/sitemap/index.html")
        for url in (
            "https://npcwoods.com/uti-treatment/tucson-az/",
            "https://npcwoods.com/sinus-infection-treatment/chandler-az/",
            "https://npcwoods.com/sinus-infection-treatment/mesa-az/",
            "https://npcwoods.com/sinus-infection-treatment/scottsdale-az/",
            "https://npcwoods.com/sinus-infection-treatment/tucson-az/",
            LV_URL,
        ):
            self.assertIn(url, html)

    def test_sinus_hub_lists_tucson_east_valley_and_las_vegas(self):
        html = read("landing-pages/sinus-infection-treatment/index.html")
        self.assertIn("CITY SINUS DOORS", html)
        self.assertIn('href="https://npcwoods.com/sinus-infection-treatment/phoenix-az/"', html)
        self.assertIn('href="https://npcwoods.com/sinus-infection-treatment/tucson-az/"', html)
        self.assertIn('href="https://npcwoods.com/sinus-infection-treatment/mesa-az/"', html)
        self.assertIn('href="https://npcwoods.com/sinus-infection-treatment/chandler-az/"', html)
        self.assertIn('href="https://npcwoods.com/sinus-infection-treatment/scottsdale-az/"', html)
        self.assertIn(f'href="{LV_URL}"', html)

    def test_arizona_uti_hub_links_city_plates(self):
        html = read("landing-pages/arizona-uti-treatment/index.html")
        for url in (
            "https://npcwoods.com/uti-treatment/phoenix-az/",
            "https://npcwoods.com/uti-treatment/tucson-az/",
            "https://npcwoods.com/uti-treatment/mesa-az/",
            "https://npcwoods.com/uti-treatment/scottsdale-az/",
            "https://npcwoods.com/uti-treatment/chandler-az/",
            "https://npcwoods.com/uti-treatment/gilbert-az/",
            "https://npcwoods.com/uti-treatment/tempe-az/",
            "https://npcwoods.com/uti-treatment/glendale-az/",
            "https://npcwoods.com/uti-treatment/surprise-az/",
        ):
            self.assertIn(f'href="{url}"', html)
        self.assertNotIn('href="https://npcwoods.com/uti-treatment/flagstaff-az/"', html)


if __name__ == "__main__":
    unittest.main()
