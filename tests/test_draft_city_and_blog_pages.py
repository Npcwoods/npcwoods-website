"""Lock Chris-approved drafts: 5 city pages + 2 blog posts. Git only. Not live."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMS = "sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit"
LOCKED_911 = (
    "Text-based telehealth is not for emergencies. "
    "If you have chest pain, trouble breathing, or other emergency symptoms, call 911."
)
FOOTER_MARK = "<!-- ===== NPCWOODS SITE FOOTER (Shared Component) ===== -->"
HIPAA = "GTM, GA4, and Google Ads stay off this health-condition page (no BAA)."


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def body_only(html: str) -> str:
    return html.split(FOOTER_MARK, 1)[0] if FOOTER_MARK in html else html


CITY_PAGES = {
    "landing-pages/uti-treatment/phoenix-az/index.html": {
        "title": "UTI Treatment in Phoenix, AZ | $59 Text Visit",
        "h1": "UTI in Phoenix and you don’t want the Banner waiting room? Text Chris.",
        "url": "https://npcwoods.com/uti-treatment/phoenix-az/",
        "local": "Banner",
        "forbidden_cities": ("Atlanta", "Tucson", "Chandler"),
        "min_bytes": 50000,
        "plugin": "php/npcwoods-uti-phoenix.php",
        "route": "/uti-treatment/phoenix-az/",
        "html_rel": "uti-treatment/phoenix-az/index.html",
    },
    "landing-pages/uti-treatment/tucson-az/index.html": {
        "title": "UTI Treatment in Tucson, AZ | $59 Text Visit",
        "h1": "Burning through a Tucson afternoon? Text Chris.",
        "url": "https://npcwoods.com/uti-treatment/tucson-az/",
        "local": "Banner University",
        "forbidden_cities": ("Atlanta", "Phoenix", "Chandler"),
        "min_bytes": 50000,
        "plugin": "php/npcwoods-uti-tucson.php",
        "route": "/uti-treatment/tucson-az/",
        "html_rel": "uti-treatment/tucson-az/index.html",
    },
    "landing-pages/sinus-infection-treatment/mesa-az/index.html": {
        "title": "Sinus Treatment in Mesa, AZ | $59 Text Visit",
        "h1": "East Valley sinus pressure and you don’t want Banner Desert? Text Chris.",
        "url": "https://npcwoods.com/sinus-infection-treatment/mesa-az/",
        "local": "Banner Desert",
        "forbidden_cities": ("Phoenix", "Tucson", "Chandler", "Scottsdale"),
        "min_bytes": 50000,
        "plugin": "php/npcwoods-sinus-mesa.php",
        "route": "/sinus-infection-treatment/mesa-az/",
        "html_rel": "sinus-infection-treatment/mesa-az/index.html",
    },
    "landing-pages/sinus-infection-treatment/chandler-az/index.html": {
        "title": "Sinus Treatment in Chandler, AZ | $59 Text Visit",
        "h1": "Chandler sinus squeeze after a dusty commute? Text Chris.",
        "url": "https://npcwoods.com/sinus-infection-treatment/chandler-az/",
        "local": "Chandler Regional",
        "forbidden_cities": ("Phoenix", "Tucson", "Mesa", "Scottsdale"),
        "min_bytes": 50000,
        "plugin": "php/npcwoods-sinus-chandler.php",
        "route": "/sinus-infection-treatment/chandler-az/",
        "html_rel": "sinus-infection-treatment/chandler-az/index.html",
    },
    "landing-pages/sinus-infection-treatment/scottsdale-az/index.html": {
        "title": "Sinus Treatment in Scottsdale, AZ | $59 Text Visit",
        "h1": "Scottsdale sinus pressure that will not quit? Text Chris.",
        "url": "https://npcwoods.com/sinus-infection-treatment/scottsdale-az/",
        "local": "HonorHealth",
        "forbidden_cities": ("Phoenix", "Tucson", "Mesa", "Chandler"),
        "min_bytes": 50000,
        "plugin": "php/npcwoods-sinus-scottsdale.php",
        "route": "/sinus-infection-treatment/scottsdale-az/",
        "html_rel": "sinus-infection-treatment/scottsdale-az/index.html",
    },
}

BLOGS = {
    "blog/can-nurse-practitioner-prescribe-antibiotics-by-text/index.html": {
        "title": "Can a nurse practitioner prescribe antibiotics by text?",
        "h1": "Can a nurse practitioner prescribe antibiotics by text?",
        "must": (
            "https://npcwoods.com/uti-treatment/",
            "https://npcwoods.com/sinus-infection-treatment/",
            "not a guarantee",
            "clinically appropriate",
        ),
        "plugin": "php/npcwoods-blog-np-antibiotics-text.php",
        "route": "/blog/can-nurse-practitioner-prescribe-antibiotics-by-text/",
    },
    "blog/dental-pain-cant-get-a-dentist/index.html": {
        "title": "Dental pain when you cannot get a dentist this week",
        "h1": "Dental pain when you cannot get a dentist this week.",
        "must": (
            "https://npcwoods.com/dental-pain/",
            "not a replacement for a dentist",
            "in-person dental care",
        ),
        "plugin": "php/npcwoods-blog-dental-pain-dentist.php",
        "route": "/blog/dental-pain-cant-get-a-dentist/",
    },
}


class DraftCityAndBlogPageTests(unittest.TestCase):
    def test_city_pages_are_real_and_unique(self):
        h1s = []
        titles = []
        for rel, spec in CITY_PAGES.items():
            path = ROOT / rel
            with self.subTest(rel=rel):
                self.assertTrue(path.exists())
                self.assertGreaterEqual(path.stat().st_size, spec["min_bytes"])
                html = read(rel)
                page = body_only(html)
                self.assertIn(f"<title>{spec['title']}</title>", html)
                self.assertIn(spec["h1"], html)
                self.assertIn(spec["url"], html)
                self.assertIn(spec["local"], page)
                self.assertIn(SMS, html)
                self.assertIn("Hi Chris, I'd like to start a $59 visit", html)
                self.assertIn("$59", html)
                self.assertIn("Chris Woods, MSN, APRN, FNP-C", html)
                self.assertIn(LOCKED_911, html)
                self.assertIn("notice-of-privacy-practices", html)
                self.assertIn(HIPAA, html)
                self.assertIn("This is not a", page)
                self.assertIn("Arizona", page)
                self.assertNotIn("Antibiotics without leaving home", html)
                self.assertNotIn("tracking.js", html)
                self.assertNotIn("aggregateRating", html)
                self.assertNotIn("googletagmanager.com", html)
                self.assertNotRegex(html, r"GTM-[A-Z0-9]+|G-[A-Z0-9]+|AW-\d+")
                self.assertIsNone(re.search(r"fbq\s*\(\s*['\"]init['\"]", html))
                self.assertNotRegex(page, r"(?i)\b(doctor|physician|insurance)\b")
                self.assertNotRegex(page, r"\bMD\b")
                self.assertNotIn("geoCoordinates", html)
                for city in spec["forbidden_cities"]:
                    self.assertNotIn(city, page)
                h1s.append(spec["h1"])
                titles.append(spec["title"])
        self.assertEqual(len(h1s), len(set(h1s)))
        self.assertEqual(len(titles), len(set(titles)))

    def test_city_plugins_are_path_only(self):
        for spec in CITY_PAGES.values():
            php = read(spec["plugin"])
            with self.subTest(plugin=spec["plugin"]):
                self.assertIn("parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH )", php)
                self.assertIn(f"'{spec['route']}'", php)
                self.assertIn(spec["html_rel"], php)
                self.assertNotIn("get_post_field", php)
                self.assertEqual(php.count("=>"), 1)

    def test_blog_pages_follow_pocket_pattern(self):
        for rel, spec in BLOGS.items():
            html = read(rel)
            page = body_only(html)
            with self.subTest(rel=rel):
                self.assertIn(f"<title>{spec['title']}</title>", html)
                self.assertIn(f"<h1>{spec['h1']}</h1>", html)
                self.assertIn(SMS, html)
                self.assertIn("$59", html)
                self.assertIn("Chris Woods, MSN, APRN, FNP-C", page)
                self.assertIn(LOCKED_911, html)
                self.assertIn("notice-of-privacy-practices", html)
                self.assertIn(HIPAA, html)
                self.assertNotRegex(page, r"(?i)\b(doctor|physician|insurance)\b")
                self.assertNotRegex(page, r"\bMD\b")
                self.assertNotIn("Text a Doctor", html)
                for token in spec["must"]:
                    self.assertIn(token, page)
                php = read(spec["plugin"])
                self.assertIn(f"'{spec['route']}'", php)
                self.assertIn("parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH )", php)

    def test_llmseo_adds_phoenix_tucson_uti_not_sinus_cities(self):
        php = read("php/npcwoods-llmseo-pages.php")
        self.assertIn("'/uti-treatment/phoenix-az/'", php)
        self.assertIn("'/uti-treatment/tucson-az/'", php)
        self.assertNotIn("'/sinus-infection-treatment/mesa-az/'", php)
        self.assertNotIn("'/sinus-infection-treatment/chandler-az/'", php)
        self.assertNotIn("'/sinus-infection-treatment/scottsdale-az/'", php)

    def test_sitemap_lists_new_uti_cities_not_unpublished_sinus_cities(self):
        html = read("landing-pages/sitemap/index.html")
        self.assertIn("https://npcwoods.com/uti-treatment/phoenix-az/", html)
        self.assertIn("https://npcwoods.com/uti-treatment/tucson-az/", html)
        self.assertNotIn("https://npcwoods.com/sinus-infection-treatment/mesa-az/", html)
        self.assertNotIn("https://npcwoods.com/sinus-infection-treatment/chandler-az/", html)
        self.assertNotIn("https://npcwoods.com/sinus-infection-treatment/scottsdale-az/", html)

    def test_uti_and_blog_drafts_use_red_charcoal_not_hospital_blue(self):
        """Phoenix/Tucson UTI + both blogs must match live sinus red (#9B1C1C), not #2563EB."""
        surfaces = [
            "landing-pages/uti-treatment/phoenix-az/index.html",
            "landing-pages/uti-treatment/tucson-az/index.html",
            "blog/can-nurse-practitioner-prescribe-antibiotics-by-text/index.html",
            "blog/can-nurse-practitioner-prescribe-antibiotics-by-text.html",
            "blog/dental-pain-cant-get-a-dentist/index.html",
            "blog/dental-pain-cant-get-a-dentist.html",
        ]
        hospital_blue = (
            "#2563EB",
            "#2563eb",
            "rgba(37,99,235",
            "rgba(37, 99, 235",
            "#1D4ED8",
            "#EFF6FF",
            "#DBEAFE",
        )
        for rel in surfaces:
            html = read(rel)
            with self.subTest(rel=rel):
                self.assertIn("#9B1C1C", html)
                for token in hospital_blue:
                    self.assertNotIn(token, html)
                if rel.startswith("landing-pages/"):
                    self.assertIn("--brand: #9B1C1C;", html)
                    self.assertIn("theme-color\" content=\"#9B1C1C\"", html)
                    self.assertIn("background: #9B1C1C !important;", html)

    def test_legacy_redirects_point_at_new_city_pages(self):
        redirects = read("php/npcwoods-redirects.php")
        cleanup = read("php/npcwoods-redirects-404-cleanup.php")
        self.assertIn('"/tucson-az-uti/"            => "/uti-treatment/tucson-az/"', redirects)
        self.assertIn('"/phoenix-uti-treatment/"           => "/uti-treatment/phoenix-az/"', cleanup)
        self.assertIn('"/mesa-sinus-infection/"            => "/sinus-infection-treatment/mesa-az/"', cleanup)
        self.assertIn('"/chandler-sinus-infection/"        => "/sinus-infection-treatment/chandler-az/"', cleanup)
        self.assertIn('"/scottsdale-sinus-infection/"      => "/sinus-infection-treatment/scottsdale-az/"', cleanup)


if __name__ == "__main__":
    unittest.main()
