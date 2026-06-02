from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def sitemap_exclusion_block() -> str:
    php = read("php/npcwoods-faq-schema.php")
    match = re.search(
        r"wpseo_exclude_from_sitemap_by_post_ids'.*?return array\((.*?)\);\s*\}\);",
        php,
        re.S,
    )
    assert match, "Yoast sitemap exclusion block not found"
    return match.group(1)


class SeoAuditFixTests(unittest.TestCase):
    def test_llmseo_routes_nested_uti_pages_by_request_path(self):
        php = read("php/npcwoods-llmseo-pages.php")
        self.assertIn("$path_map", php)
        self.assertIn("parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH)", php)
        self.assertIn("'/uti-treatment/mesa-az/'", php)
        self.assertNotIn("'/sinus-infection-treatment/mesa-az/'", php)

    def test_sitemap_exclusions_match_current_index_strategy(self):
        block = sitemap_exclusion_block()
        self.assertRegex(block, r"\b23\b", "bad Mesa sinus URL should be excluded")
        self.assertRegex(block, r"\b192\b", "old /ear-infection/ service page should be excluded")
        self.assertRegex(block, r"\b329\b", "orphan static Albuquerque blog page should be excluded")
        self.assertNotRegex(block, r"\b407\b", "/faq/ should not be excluded")
        self.assertNotRegex(block, r"\b408\b", "/about/ should not be excluded")

    def test_blog_meta_map_covers_recent_posts_and_will_rerun(self):
        php = read("php/npcwoods-faq-schema.php")
        self.assertIn("npcwoods_blog_metas_set_v3", php)
        for post_id in (696, 673, 668, 730, 700):
            self.assertIn(f"{post_id} => array(", php)

    def test_redirects_consolidate_ear_infection_and_keep_faq_live(self):
        php = read("php/npcwoods-redirects.php")
        self.assertIn('"/ear-infection/"', php)
        self.assertIn('"/ear-infection-treatment/"', php)
        self.assertNotIn('"/faq/"                      => "/#faq"', php)

    def test_physical_ear_infection_page_points_to_current_hub(self):
        html = read("landing-pages/ear-infection/index.html")
        self.assertIn('<meta name="robots" content="noindex, follow">', html)
        self.assertIn('<link rel="canonical" href="https://npcwoods.com/ear-infection-treatment/">', html)
        self.assertIn('content="0; url=https://npcwoods.com/ear-infection-treatment/"', html)

    def test_static_source_links_to_current_ear_infection_hub(self):
        offenders = []
        for folder in ("html", "landing-pages"):
            for path in (ROOT / folder).rglob("*.html"):
                text = path.read_text(errors="ignore")
                if "https://npcwoods.com/ear-infection/" in text:
                    offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual([], offenders)

    def test_medication_pages_have_single_h1(self):
        pages = {
            "landing-pages/medications/ondansetron/index.html": "Ondansetron (Zofran) Patient Guide",
            "landing-pages/medications/polytrim/index.html": "Polytrim Eye Drops Patient Guide",
            "landing-pages/medications/oseltamivir/index.html": "Oseltamivir (Tamiflu) Patient Guide",
        }
        for rel, heading in pages.items():
            with self.subTest(rel=rel):
                html = read(rel)
                h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, flags=re.I | re.S)
                self.assertEqual([heading], [re.sub(r"\s+", " ", h).strip() for h in h1s])

    def test_targeted_pages_avoid_ad_risky_terms(self):
        term_checks = {
            "landing-pages/faq/index.html": ("insurance",),
            "landing-pages/telehealth-vs-urgent-care/index.html": ("insurance",),
            "landing-pages/murphy-nc/index.html": ("online doctor", "text a doctor"),
            "landing-pages/blairsville-ga/index.html": ("online doctor", "text a doctor"),
            "landing-pages/blue-ridge-ga/index.html": ("online doctor", "text a doctor"),
        }
        for rel, terms in term_checks.items():
            text = read(rel).lower()
            for term in terms:
                with self.subTest(rel=rel, term=term):
                    self.assertNotIn(term, text)

    def test_targeted_metadata_lengths_are_search_friendly(self):
        pages = [
            "html/pharmacy/index.html",
            "html/review/index.html",
            "landing-pages/trust-video/index.html",
            "landing-pages/strep-throat-treatment/index.html",
            "landing-pages/murphy-nc/index.html",
            "landing-pages/blairsville-ga/index.html",
            "landing-pages/telehealth-vs-urgent-care/index.html",
            "landing-pages/blue-ridge-ga/index.html",
            "landing-pages/credentials/index.html",
            "landing-pages/uti-treatment/surprise-az/index.html",
            "landing-pages/learn/skin-infection/index.html",
            "landing-pages/learn/ingrown-toenail/index.html",
            "landing-pages/learn/tooth-infection/index.html",
            "landing-pages/learn/yeast-infection/index.html",
            "landing-pages/ear-infection-treatment/index.html",
            "landing-pages/faq/index.html",
            "landing-pages/pricing/index.html",
            "landing-pages/medications/cephalexin/index.html",
            "landing-pages/medications/amoxicillin/index.html",
            "landing-pages/medications/hydroxyzine/index.html",
            "landing-pages/learn/bronchitis/index.html",
            "landing-pages/learn/stomach-bug/index.html",
            "landing-pages/learn/strep-throat/index.html",
        ]
        for rel in pages:
            html = read(rel)
            title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
            desc = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.I)
            with self.subTest(rel=rel, field="title"):
                self.assertIsNotNone(title)
                self.assertLessEqual(len(re.sub(r"\s+", " ", title.group(1)).strip()), 60)
            with self.subTest(rel=rel, field="description"):
                self.assertIsNotNone(desc)
                self.assertLessEqual(len(desc.group(1).strip()), 155)

    def test_old_banned_word_pricing_url_is_noindex_handoff(self):
        html = read("landing-pages/affordable-telemedicine-arizona-no-insurance/index.html")
        self.assertIn('<meta name="robots" content="noindex, follow">', html)
        self.assertIn('<link rel="canonical" href="https://npcwoods.com/pricing/">', html)
        self.assertIn('content="0; url=https://npcwoods.com/pricing/"', html)
        self.assertNotIn("insurance", html.lower())

    def test_public_source_has_no_banned_word_copy(self):
        offenders = []
        for folder in ("html", "landing-pages"):
            for path in (ROOT / folder).rglob("*.html"):
                if "shared" in path.parts or path.name.startswith("test-"):
                    continue
                text = path.read_text(errors="ignore").lower()
                if "insurance" in text:
                    offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual([], offenders)

    def test_hidden_tracking_pixels_have_empty_alt_text(self):
        offenders = []
        for folder in ("html", "landing-pages"):
            for path in (ROOT / folder).rglob("*.html"):
                if path.name.startswith("test-"):
                    continue
                html = path.read_text(errors="ignore")
                for tag in re.findall(r"<img\b[^>]*>", html, re.I):
                    if 'facebook.com/tr?' in tag and not re.search(r"\salt=", tag, re.I):
                        offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual([], sorted(set(offenders)))


if __name__ == "__main__":
    unittest.main()
