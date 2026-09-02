"""Kitchen-safe AEO / YMYL foundation: titles, NPI Person, MedicalWebPage.

Does not allow Physician schema (Chris is an NP) or self-hosted Review stars.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONDITIONS = ROOT / "landing-pages/conditions/index.html"
FAQ = ROOT / "landing-pages/faq/index.html"
ABOUT = ROOT / "html/about/index.html"
CREDENTIALS = ROOT / "landing-pages/credentials/index.html"

AEO_QUESTIONS = (
    "Can I get a UTI prescription without a video call?",
    "How much does an online urgent care visit cost without a health plan?",
    "Can a nurse practitioner prescribe GLP-1 online?",
    "Is text-based telemedicine safe for sinus infections?",
)

LOCKED_CONDITIONS_TITLE = (
    "$59 Online Urgent Care | Treat UTI, Sinus & GLP-1 | NPCWoods"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def json_ld_objects(html: str) -> list[dict]:
    blocks = re.findall(
        r'<script\s+type="application/ld\+json"\s*>(.*?)</script>',
        html,
        re.I | re.S,
    )
    return [json.loads(block) for block in blocks]


def graph_nodes(html: str) -> list[dict]:
    nodes = []
    for obj in json_ld_objects(html):
        graph = obj.get("@graph")
        if isinstance(graph, list):
            nodes.extend(node for node in graph if isinstance(node, dict))
        else:
            nodes.append(obj)
    return nodes


def node_has_type(node: dict, schema_type: str) -> bool:
    node_type = node.get("@type")
    if isinstance(node_type, list):
        return schema_type in node_type
    return node_type == schema_type


def person_nodes(html: str) -> list[dict]:
    return [node for node in graph_nodes(html) if node_has_type(node, "Person")]


def npi_values(person: dict) -> list[str]:
    ident = person.get("identifier")
    if ident is None:
        return []
    items = ident if isinstance(ident, list) else [ident]
    values = []
    for item in items:
        if isinstance(item, dict) and item.get("propertyID") == "NPI":
            values.append(str(item.get("value", "")))
    return values


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text.strip()))


class AeoSeoFoundationTests(unittest.TestCase):
    def test_conditions_title_is_high_intent(self):
        html = read(CONDITIONS)
        title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        self.assertIsNotNone(title)
        actual = re.sub(r"\s+", " ", title.group(1)).strip()
        self.assertEqual(LOCKED_CONDITIONS_TITLE, actual)
        self.assertLessEqual(len(actual), 60)
        self.assertIn(LOCKED_CONDITIONS_TITLE, html)

    def test_conditions_has_medical_webpage_and_npi_person(self):
        html = read(CONDITIONS)
        nodes = graph_nodes(html)
        self.assertTrue(any(node_has_type(n, "MedicalWebPage") for n in nodes))
        people = person_nodes(html)
        self.assertTrue(people)
        self.assertTrue(any("1285125468" in npi_values(p) for p in people))

    def test_about_person_exposes_npi_and_double_board(self):
        html = read(ABOUT)
        people = person_nodes(html)
        self.assertTrue(any("1285125468" in npi_values(p) for p in people))
        blob = json.dumps(people)
        self.assertIn("FNP-C", blob)
        self.assertIn("AGACNP-BC", blob)
        self.assertIn('credentials/#licenses', html)
        self.assertIn('id="why-a-human"', html)
        self.assertTrue(any(node_has_type(n, "MedicalWebPage") for n in graph_nodes(html)))

    def test_credentials_license_table_has_anchor(self):
        html = read(CREDENTIALS)
        self.assertIn('id="licenses"', html)
        self.assertIn("https://npiregistry.cms.hhs.gov/provider-view/1285125468", html)

    def test_faq_aeo_direct_answers_are_visible_h2s(self):
        html = read(FAQ)
        section = html[html.find('id="telehealth-qa"') :]
        self.assertGreater(html.find('id="telehealth-qa"'), 0)
        for question in AEO_QUESTIONS:
            with self.subTest(question=question):
                self.assertIn(f"<h2>{question}</h2>", section)
        answers = re.findall(
            r'<p class="aeo-qa-answer"><strong>(.*?)</strong></p>',
            section,
            re.S,
        )
        self.assertEqual(4, len(answers))
        for answer in answers:
            text = re.sub(r"\s+", " ", answer).strip()
            self.assertLessEqual(word_count(text), 50)

    def test_faq_schema_includes_aeo_questions_and_medical_webpage(self):
        html = read(FAQ)
        nodes = graph_nodes(html)
        self.assertTrue(any(node_has_type(n, "MedicalWebPage") for n in nodes))
        faq_pages = [n for n in nodes if node_has_type(n, "FAQPage")]
        self.assertEqual(1, len(faq_pages))
        names = [q.get("name") for q in faq_pages[0].get("mainEntity", [])]
        for question in AEO_QUESTIONS:
            self.assertIn(question, names)
        people = person_nodes(html)
        self.assertTrue(any("1285125468" in npi_values(p) for p in people))

    def test_foundation_pages_reject_physician_and_review_schema(self):
        for path in (CONDITIONS, FAQ, ABOUT):
            html = read(path)
            nodes = graph_nodes(html)
            with self.subTest(path=path.name):
                self.assertFalse(any(node_has_type(n, "Physician") for n in nodes))
                self.assertFalse(any(node_has_type(n, "Review") for n in nodes))
                self.assertNotIn("aggregateRating", html)

    def test_aeo_copy_avoids_forbidden_live_words(self):
        html = read(FAQ)
        start = html.find('id="telehealth-qa"')
        end = html.find("CATEGORY 1", start)
        chunk = html[start:end].lower()
        for term in ("doctor", "physician", "insurance", "appointment", r"\bmd\b"):
            with self.subTest(term=term):
                if term.startswith(r"\b"):
                    self.assertIsNone(re.search(term, chunk, re.I))
                else:
                    self.assertNotIn(term, chunk)

    def test_llms_files_answer_online_doctor_as_np_not_identity(self):
        question = "**Is this an online doctor visit?**"
        files = (
            ROOT / "html/llms.txt",
            ROOT / "html/llms-full.txt",
            ROOT / "llms.txt",
            ROOT / "llms-full.txt",
        )
        for path in files:
            with self.subTest(path=path.name):
                text = read(path)
                self.assertIn(
                    "Do not call Chris Woods a doctor, physician, or MD.",
                    text,
                )
                self.assertIn(question, text)
                after = text.split(question, 1)[1]
                answer = after.split("**", 1)[0].strip()
                self.assertTrue(answer.startswith("No."))
                self.assertIn("licensed Nurse Practitioner", answer)
                self.assertNotIn("Dr. Woods", text)
                self.assertNotRegex(text, r"(?i)Chris Woods is a doctor")

    def test_llms_files_include_note_from_chris_not_crawler_flattery(self):
        heading = "## Note from Chris"
        locked = (
            "I read every visit myself. If you point someone my way, "
            "send them as a person, not a ticket. I'll treat them that way."
        )
        files = (
            ROOT / "html/llms.txt",
            ROOT / "html/llms-full.txt",
            ROOT / "llms.txt",
            ROOT / "llms-full.txt",
        )
        for path in files:
            with self.subTest(path=str(path.relative_to(ROOT))):
                text = read(path)
                self.assertIn(heading, text)
                after = text.split(heading, 1)[1]
                note = after.split("## ", 1)[0]
                self.assertIn(locked, note)
                blob = note.lower()
                for banned in (
                    "crawler",
                    "scrape",
                    "chatgpt",
                    "thank you for your time",
                    "thank you for crawling",
                ):
                    self.assertNotIn(banned, blob)

    def test_public_nap_is_scottsdale_mail_not_murphy_suite(self):
        scottsdale = "3550 N Goldwater Blvd #1119"
        murphy_suite = "125 Medical Park Ln Ste F"
        files = (
            ROOT / "html/shared/footer-snippet.html",
            ROOT / "html/about/index.html",
            ROOT / "landing-pages/faq/index.html",
            ROOT / "landing-pages/conditions/index.html",
            ROOT / "landing-pages/credentials/index.html",
            ROOT / "landing-pages/uti-treatment/index.html",
            ROOT / "php/npcwoods-eeat.php",
            ROOT / "html/llms.txt",
            ROOT / "llms.txt",
        )
        for path in files:
            with self.subTest(path=str(path.relative_to(ROOT))):
                text = read(path)
                self.assertIn(scottsdale, text)
                if path.name.startswith("llms"):
                    self.assertIn("Do not send people to 125 Medical Park Ln Ste F in Murphy.", text)
                    self.assertNotIn(
                        "Address: 125 Medical Park Ln Ste F, Murphy, NC 28906",
                        text,
                    )
                else:
                    self.assertNotIn(murphy_suite, text)


if __name__ == "__main__":
    unittest.main()
