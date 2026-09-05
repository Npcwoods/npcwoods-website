"""Wave B AEO inject: ATF answer + llms alternate + EEAT byline."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]

WAVE_B = (
    "landing-pages/uti-treatment/denver-co/index.html",
    "landing-pages/uti-treatment/reno-nv/index.html",
    "landing-pages/pink-eye-treatment/index.html",
    "landing-pages/conditions/index.html",
    "html/about/index.html",
    "landing-pages/arizona-telemedicine/index.html",
    "landing-pages/colorado-telemedicine/index.html",
    "landing-pages/georgia-telemedicine/index.html",
    "landing-pages/idaho-telemedicine/index.html",
    "landing-pages/iowa-telemedicine/index.html",
    "landing-pages/montana-telemedicine/index.html",
    "landing-pages/nevada-telemedicine/index.html",
    "landing-pages/new-mexico-telemedicine/index.html",
    "landing-pages/north-carolina-telemedicine/index.html",
    "landing-pages/oregon-telemedicine/index.html",
    "landing-pages/utah-telemedicine/index.html",
)

CITY_HINTS = {
    "landing-pages/uti-treatment/denver-co/index.html": ("Denver", "Colorado"),
    "landing-pages/uti-treatment/reno-nv/index.html": ("Reno", "Nevada"),
}

STATE_HINTS = {
    "landing-pages/arizona-telemedicine/index.html": "Arizona",
    "landing-pages/colorado-telemedicine/index.html": "Colorado",
    "landing-pages/georgia-telemedicine/index.html": "Georgia",
    "landing-pages/idaho-telemedicine/index.html": "Idaho",
    "landing-pages/iowa-telemedicine/index.html": "Iowa",
    "landing-pages/montana-telemedicine/index.html": "Montana",
    "landing-pages/nevada-telemedicine/index.html": "Nevada",
    "landing-pages/new-mexico-telemedicine/index.html": "New Mexico",
    "landing-pages/north-carolina-telemedicine/index.html": "North Carolina",
    "landing-pages/oregon-telemedicine/index.html": "Oregon",
    "landing-pages/utah-telemedicine/index.html": "Utah",
}


class AeoWaveBInjectTest(unittest.TestCase):
    def test_wave_b_plates_have_llms_atf_and_eeat_byline(self):
        for rel in WAVE_B:
            html = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(page=rel):
                self.assertIn('type="application/llms.txt"', html)
                self.assertIn('type="application/llms-full.txt"', html)
                self.assertIn('data-npc-aeo="atf-answer"', html)
                self.assertIn("npc-clinician-byline", html)
                self.assertIn("$59", html)
                self.assertIn("sms:4806394722", html)
                self.assertIn("https://npcwoods.com/about/", html)
                self.assertIn("https://npcwoods.com/credentials/", html)

    def test_city_and_state_atf_blocks_name_the_place(self):
        for rel, (city, state) in CITY_HINTS.items():
            html = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(page=rel):
                start = html.index('data-npc-aeo="atf-answer"')
                block = html[start : start + 800]
                self.assertIn(city, block)
                self.assertIn(state, block)
        for rel, state in STATE_HINTS.items():
            html = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(page=rel):
                start = html.index('data-npc-aeo="atf-answer"')
                block = html[start : start + 800]
                self.assertIn(state, block)

    def test_arizona_hub_hrefs_tucson_uti_not_a_hash(self):
        html = (ROOT / "landing-pages/arizona-telemedicine/index.html").read_text(encoding="utf-8")
        self.assertIn('href="https://npcwoods.com/uti-treatment/tucson-az/"', html)
        self.assertRegex(
            html,
            r'href="https://npcwoods.com/uti-treatment/tucson-az/"[\s\S]{0,240}<h3>Tucson</h3>',
        )

    def test_nevada_hub_hrefs_reno_uti_not_a_hash(self):
        html = (ROOT / "landing-pages/nevada-telemedicine/index.html").read_text(encoding="utf-8")
        self.assertIn('href="https://npcwoods.com/uti-treatment/reno-nv/"', html)
        self.assertRegex(
            html,
            r'href="https://npcwoods.com/uti-treatment/reno-nv/"[\s\S]{0,240}<h3>Reno</h3>',
        )

    def test_pink_eye_atf_names_the_condition(self):
        html = (ROOT / "landing-pages/pink-eye-treatment/index.html").read_text(encoding="utf-8")
        start = html.index('data-npc-aeo="atf-answer"')
        block = html[start : start + 800]
        self.assertIn("pink eye", block.lower())


if __name__ == "__main__":
    unittest.main()
