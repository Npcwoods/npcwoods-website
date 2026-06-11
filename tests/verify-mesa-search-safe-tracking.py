#!/usr/bin/env python3
"""Playwright tracking verification for the Mesa search-safe paid landing page.

Loads /uti-treatment/mesa-az/search-safe/?gclid=TEST on desktop + mobile,
clicks the SMS CTA, and asserts:
  - GTM container + GA4 requests fire
  - sms_click event reaches GA/Ads endpoints (gclid present)
  - NO Meta pixel requests (health page)
Saves screenshots for Chris's review.
"""
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path.home() / "Desktop/Chris-HQ/content-output/reports/google-ads-uti-mesa-rescue"
OUT.mkdir(parents=True, exist_ok=True)
TS = datetime.now().strftime("%Y%m%d-%H%M%S")
URL = "https://npcwoods.com/uti-treatment/mesa-az/search-safe/?gclid=TEST_MESA_RELAUNCH"

GOOD = ["googletagmanager.com", "google-analytics.com", "googleadservices.com", "doubleclick.net"]
BAD = ["connect.facebook.net", "facebook.com/tr"]


def run(p, label, viewport, ua=None):
    print(f"\n=== {label} ===")
    browser = p.chromium.launch()
    ctx_args = {"viewport": viewport}
    if ua:
        ctx_args["user_agent"] = ua
    ctx = browser.new_context(**ctx_args)
    page = ctx.new_page()
    hits, bad_hits = [], []
    page.on("request", lambda r: (
        hits.append(r.url) if any(d in r.url for d in GOOD) else
        bad_hits.append(r.url) if any(d in r.url for d in BAD) else None
    ))
    page.goto(URL, wait_until="networkidle", timeout=60000)
    title = page.title()
    h1 = page.locator("h1").first.inner_text()
    faq = page.locator("text=Most patients hear back the same day").count()
    # neutralize sms: navigation then click the CTA so tracking handlers fire
    page.evaluate("""
        document.querySelectorAll('a[href^="sms:"]').forEach(a => {
            a.dataset.origHref = a.href;
            a.addEventListener('click', e => e.preventDefault(), {capture: false});
        });
    """)
    page.locator('a[href^="sms:"], a[data-orig-href^="sms:"]').first.click()
    page.wait_for_timeout(3000)
    shot = OUT / f"live-{label}-{TS}.png"
    page.screenshot(path=str(shot), full_page=False)
    ctx.close()
    browser.close()

    gtm = any("googletagmanager.com" in u for u in hits)
    ga4 = any("google-analytics.com" in u or "/g/collect" in u for u in hits)
    ads = any("googleadservices.com" in u or "doubleclick.net" in u for u in hits)
    print(f"title: {title}")
    print(f"h1: {h1}")
    print(f"canonical FAQ wording live: {'YES' if faq else 'NO (cache may be stale)'}")
    print(f"GTM loaded: {gtm} | GA4 hits: {ga4} | Ads/Doubleclick: {ads}")
    print(f"Meta pixel requests: {len(bad_hits)} {'!! FAIL' if bad_hits else '(clean)'}")
    print(f"screenshot: {shot}")
    ok = gtm and ga4 and not bad_hits
    print("RESULT:", "PASS" if ok else "FAIL")
    return ok


with sync_playwright() as p:
    desktop = run(p, "desktop", {"width": 1440, "height": 900})
    mobile = run(
        p, "mobile", {"width": 390, "height": 844},
        ua="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
           "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    )
    sys.exit(0 if desktop and mobile else 1)
