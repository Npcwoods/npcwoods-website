"""Browser proof shared by production and preview verification."""
from pathlib import Path
import os
import uuid

from website_policy import compare_page, tracker_markers


def browser_proof(local, url, report_dir):
    from playwright.sync_api import sync_playwright

    source = Path(local).read_text(encoding='utf-8')
    output = Path(report_dir) / ('page-' + uuid.uuid4().hex)
    output.mkdir(parents=True, exist_ok=False)
    screenshots, problems = [], []
    launch = {}
    channel = os.environ.get('NPCWOODS_BROWSER_CHANNEL')
    if channel:
        if channel not in ('chrome', 'msedge'):
            raise ValueError('unsupported NPCWOODS_BROWSER_CHANNEL')
        launch['channel'] = channel
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(**launch)
        try:
            for name, width, height in [('mobile', 390, 844), ('desktop', 1440, 1000)]:
                context = browser.new_context(viewport={'width': width, 'height': height})
                try:
                    forbidden = []

                    def restrict(route):
                        markers = tracker_markers(route.request.url)
                        if markers or route.request.method not in ('GET', 'HEAD'):
                            forbidden.extend(markers or ['non-read-only request'])
                            route.abort()
                        else:
                            route.continue_()

                    context.route('**/*', restrict)
                    page = context.new_page()
                    response = page.goto(url, wait_until='networkidle', timeout=60000)
                    page.wait_for_timeout(1500)
                    if not response or response.status != 200 or page.url != url:
                        problems.append(f'{name}: wrong status or redirected URL')
                    detail = compare_page(source, page.content())
                    if detail:
                        problems.append(f'{name}: {detail}')
                    if page.locator('h1').count() != 1 or not page.locator('h1').first.is_visible():
                        problems.append(f'{name}: heading is not visible')
                    if forbidden:
                        problems.append(f'{name}: blocked {len(forbidden)} forbidden request(s)')
                    screenshot = output / f'{name}.png'
                    page.screenshot(path=str(screenshot), full_page=True)
                    screenshots.append(str(screenshot))
                finally:
                    context.close()
        finally:
            browser.close()
    return not problems, '; '.join(problems) or 'clean URL, matching title/H1, visible page, no forbidden requests; mobile + desktop', screenshots
