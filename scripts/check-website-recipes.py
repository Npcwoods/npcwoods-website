#!/usr/bin/env python3
"""Read-only drift check: source policy, generated pages, and active recipes."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from replace_sitewide_tracking import target_paths
from website_policy import POLICY_VERSION, tracker_markers


def check(hq_root=None):
    problems = []
    pages = target_paths(ROOT)
    for page in pages:
        markers = tracker_markers(page.read_text())
        if markers:
            problems.append(f'{page.relative_to(ROOT)}: forbidden tracking: {", ".join(markers)}')
    spec = importlib.util.spec_from_file_location('city_recipe_check', ROOT / 'scripts/build-search-safe-pages.py')
    recipe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recipe)
    template = (recipe.TEMPLATE_DIR / 'template.html').read_text()
    cities = json.loads((recipe.TEMPLATE_DIR / 'cities.json').read_text())
    for city in cities:
        rendered = recipe.render(template, city)
        problems.extend(f'city recipe {city["slug"]}: {p}' for p in recipe.check_page(city, rendered))
        dest = recipe.out_path(recipe.DEFAULT_OUT_ROOT, city['slug'])
        if not dest.is_file() or dest.read_text() != rendered:
            problems.append(f'city recipe {city["slug"]}: source differs from generated output')
    docs = [ROOT / p for p in ('AGENTS.md', 'CLAUDE.md', 'scripts/README-deploy.md',
                               'landing-pages/uti-treatment/_search-safe-template/README.md')]
    if hq_root:
        docs.extend(Path(hq_root) / p for p in ('.agents/skills/page-build/SKILL.md',
                                               'skills/page-build/SKILL.md',
                                               '.agents/skills/deploy-and-verify/SKILL.md'))
    stale = ('Preserve all existing tracking codes', 'Add all tracking codes',
             'Tracking codes (do NOT omit any)', 'tracking.js loads (check network',
             'tracking.js/GTM present', 'GTM + GA4 requests fire', 'GTM/tracking.js missing',
             'python3 scripts/sftp-upload.py', 'python3 npcwoods-website/scripts/sftp-upload.py',
             'python3 scripts/deploy-changed-pages.py')
    for doc in docs:
        if not doc.is_file():
            problems.append(f'missing active recipe: {doc.name}')
            continue
        content = doc.read_text()
        if 'WEBSITE-RECIPES.md' not in content:
            problems.append(f'{doc}: missing current recipe pointer')
        for phrase in stale:
            if phrase in content:
                problems.append(f'{doc}: retired instruction: {phrase}')
    return {'ok': not problems, 'policy_version': POLICY_VERSION,
            'source_documents_checked': len(pages), 'city_recipes_checked': len(cities),
            'active_recipes_checked': len(docs), 'problems': problems}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hq-root', type=Path, help='Also check the three active HQ skill copies')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    result = check(args.hq_root)
    if args.json:
        print(json.dumps(result))
    else:
        print(f'{"PASS" if result["ok"] else "FAIL"}: policy {POLICY_VERSION}; '
              f'{result["source_documents_checked"]} public sources; {result["city_recipes_checked"]} city recipes')
        for problem in result['problems']:
            print('  ' + problem)
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
