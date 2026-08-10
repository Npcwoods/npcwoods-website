from pathlib import Path
import re
import unittest


ARTICLE = Path(__file__).resolve().parents[1] / "blog" / "corneal-abrasion-eye-scratch.html"


class CornealAbrasionBlogTests(unittest.TestCase):
    def test_answer_first_article_has_required_safety_and_conversion_content(self):
        article = ARTICLE.read_text(encoding="utf-8")
        self.assertIn("Scratched Your Eye?", article)
        self.assertIn("Here’s What to Do Next.", article)
        self.assertLess(
            article.index('alt="Adult gently shielding one watery eye in soft daylight"'),
            article.index("The short version"),
        )
        self.assertIn("Not sure how serious it is? Text us.", article)
        self.assertGreaterEqual(article.count("sms:4806394722"), 2)
        for phrase in (
            "vision changes",
            "chemical exposure",
            "high-speed debris",
            "contact lenses",
            "Do not try to remove an object that is stuck",
            "do not patch your eye",
            "American Academy of Family Physicians",
            "MedlinePlus",
            "Common Questions",
        ):
            self.assertIn(phrase.lower(), article.lower())

    def test_article_avoids_forbidden_and_overreaching_copy(self):
        article = ARTICLE.read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"\binsurance\b", article, re.IGNORECASE))
        self.assertIsNone(re.search(r"\bdoctor\b", article, re.IGNORECASE))
        self.assertNotIn("we can diagnose your corneal abrasion by text", article.lower())
        self.assertNotIn("we treat corneal abrasions by text", article.lower())
        self.assertNotIn("guarantee", article.lower())


if __name__ == "__main__":
    unittest.main()
