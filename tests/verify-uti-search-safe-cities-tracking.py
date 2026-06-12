#!/usr/bin/env python3
"""Playwright tracking verification for the search-safe UTI city pages.

Multi-city version of verify-mesa-search-safe-tracking.py. For each city,
loads /uti-treatment/{slug}/search-safe/?gclid=TEST on mobile, clicks the
SMS CTA, and asserts:
  - GTM container + GA4 requests fire
  - NO Meta pixel requests (health page)
Run after scripts/deploy-uti-search-safe-cities-2026-06-12.py --execute.
Pass slugs as args to limit, e.g.:
    python3 tests/verify-uti-search-safe-cities-tracking.py chandler-az
"""
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path.home() / "Desktop/Chris-HQ/content-output/reports/google-ads-uti-city-expansion"
OUT.mkdir(parents=True, exist_ok=True)
TS = datetime.now().strftime("%Y%m%d-%H%M%S")

SLUGS = [
    "scottsdale-az", "surprise-az", "albuquerque-nm",
    "chandler-az", "gilbert-az", "tempe-az", "glendale-az",
]
GOOD = ["googletagmanager.com", "google-analytics.com", "googleadservices.com", "doubleclick.net"]
BAD = ["connect.facebook.net", "facebook.com/tr"]
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)


def run(p, slug):
    url = f"https://npcwoods.com/uti-treatment/{slug}/search-safe/?gclid=TEST_CITY_EXPANSION"
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, user_agent=MOBILE_UA)
    page = ctx.new_page()
    hits, bad_hits = [], []
    page.on("request", lambda r: (
        hits.append(r.url) if any(d in r.url for d in GOOD) else
        bad_hits.append(r.url) if any(d in r.url for d in BAD) else None
    ))
    page.goto(url, wait_until="networkidle", timeout=60000)
    title = page.title()
    page.evaluate("""
        document.querySelectorAll('a[href^="sms:"]').forEach(a => {
            a.addEventListener('click', e => e.preventDefault(), {capture: false});
        });
    """)
    page.locator('a[href^="sms:"]').first.click()
    page.wait_for_timeout(3000)
    shot = OUT / f"live-{slug}-{TS}.png"
    page.screenshot(path=str(shot), full_page=False)
    ctx.close()
    browser.close()

    gtm = any("googletagmanager.com" in u for u in hits)
    ga4 = any("google-analytics.com" in u or "/g/collect" in u for u in hits)
    ok = gtm and ga4 and not bad_hits
    print(f"{'PASS' if ok else 'FAIL'} {slug}: GTM={gtm} GA4={ga4} "
          f"MetaPixel={len(bad_hits)} title=\"{title}\" shot={shot.name}")
    return ok


def main() -> int:
    slugs = sys.argv[1:] or SLUGS
    with sync_playwright() as p:
        results = [run(p, slug) for slug in slugs]
    print(f"\n{sum(results)}/{len(results)} pages passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
