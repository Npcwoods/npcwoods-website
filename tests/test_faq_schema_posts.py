from pathlib import Path
import unittest


PLUGIN = Path(__file__).resolve().parents[1] / "php" / "npcwoods-faq-schema.php"


class FaqSchemaPostTests(unittest.TestCase):
    def test_faq_schema_supports_wordpress_posts_as_well_as_pages(self):
        plugin = PLUGIN.read_text(encoding="utf-8")
        self.assertIn("is_singular(array('page', 'post'))", plugin)


if __name__ == "__main__":
    unittest.main()
