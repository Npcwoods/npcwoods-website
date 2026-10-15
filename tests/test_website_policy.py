import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WebsitePolicyTest(unittest.TestCase):
    def test_all_static_page_tools_share_one_policy(self):
        policy = ROOT / 'scripts/website_policy.py'
        self.assertTrue(policy.is_file(), 'missing executable policy shared by the recipes')
        for name in ['scripts/deploy.py', 'scripts/build-search-safe-pages.py', 'tests/guardian/guardian.py']:
            with self.subTest(tool=name):
                self.assertIn('website_policy', (ROOT / name).read_text())

    def test_city_recipe_does_not_require_a_forbidden_script(self):
        spec = importlib.util.spec_from_file_location('recipe', ROOT / 'scripts/build-search-safe-pages.py')
        recipe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(recipe)
        self.assertNotIn('tracking.js', recipe.REQUIRED_MARKERS)

