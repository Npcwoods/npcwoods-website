#!/usr/bin/env python3
"""Verify an immutable preview manifest; never publish or change the website."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from page_verification import browser_proof
from website_policy import headings


def verify_preview(manifest_path, base_url, browser_check=browser_proof):
    manifest_path = Path(manifest_path).resolve()
    base = urlsplit(base_url)
    local = base.scheme == 'http' and base.hostname in ('127.0.0.1', 'localhost')
    hosted = base.scheme == 'https' and (base.hostname or '').endswith('.vercel.app')
    if not (local or hosted) or base.username or base.password or base.query or base.fragment or base.path not in ('', '/'):
        raise ValueError('expected an unprotected Vercel preview origin or local test origin')
    data = json.loads(manifest_path.read_text())
    output = manifest_path.parent
    if data.get('schema_version') != 1 or Path(data.get('output', '')).resolve() != output or not data.get('pages'):
        raise ValueError('invalid preview manifest')
    spec = importlib.util.spec_from_file_location('preview_deploy_verifier', Path(__file__).with_name('deploy.py'))
    deploy = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = deploy
    spec.loader.exec_module(deploy)
    # Validate every bundle entry before making any network requests.
    plans, seen = [], set()
    for entry in data['pages']:
        route = entry['route']
        destination = (output / entry['destination']).resolve()
        if not re.fullmatch(r'/(?:[a-z0-9][a-z0-9_-]*/)*', route) or route in seen:
            raise ValueError('invalid or duplicate preview route')
        seen.add(route)
        if not destination.is_relative_to(output) or destination != output / route.strip('/') / 'index.html':
            raise ValueError('preview path escaped its route')
        if hashlib.sha256(destination.read_bytes()).hexdigest() != entry['preview_sha256']:
            raise ValueError('preview changed after it was prepared')
        values = headings(destination.read_text())
        if values != {'title': [entry['title']], 'h1': [entry['h1']]}:
            raise ValueError('manifest headings do not match the preview')
        plans.append(deploy.PagePlan(route.strip('/') or 'home', destination, '', base_url.rstrip('/') + route))
    results = []
    for item in plans:
        problem = deploy.verify_http(item)
        if problem:
            results.append({'url': item.url, 'ok': False, 'detail': problem, 'screenshots': []})
            continue
        try:
            ok, detail, screenshots = browser_check(item.local, item.url, output.parent / 'proof')
        except Exception as exc:
            ok, detail, screenshots = False, f'browser verification failed: {exc}', []
        results.append({'url': item.url, 'ok': ok, 'detail': detail, 'screenshots': screenshots})
    return {'ok': all(p['ok'] for p in results), 'pages': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        result = verify_preview(args.manifest, args.base_url)
    except Exception as exc:
        result = {'ok': False, 'error': str(exc), 'pages': []}
    print(json.dumps(result))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
