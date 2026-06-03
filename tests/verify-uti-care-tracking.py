#!/usr/bin/env python3
"""Playwright pixel verification for /uti-care/ launch.

Three test runs against the LIVE site:
  1. /uti-care/?gclid=TEST   → expect sms_click_source=google + AW conversion pixel
  2. /uti-care/?fbclid=TEST  → expect sms_click_source=facebook + Meta Lead event
  3. /uti-treatment/         → expect sms_click_source=organic (regression check)

Saves HAR + screenshots for Chris's mobile review at
content-output/reports/uti-care-launch/.

Reference: GL-005 (April $138 burn from missing tracking.js).
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path.home() / "Desktop/Chris-HQ/content-output/reports/uti-care-launch"
OUT.mkdir(parents=True, exist_ok=True)
TS = datetime.now().strftime("%Y%m%d-%H%M%S")


def run_test(p, label, url, expected_source, expected_pixels):
    """Load the URL, click the first SMS CTA, capture network traces.

    expected_pixels: list of (substring, description) tuples that MUST be seen.
    """
    print(f"\n=== Test: {label} ===")
    print(f"URL: {url}")
    print(f"Expected sms_click_source: {expected_source}")

    browser = p.chromium.launch()
    har_path = OUT / f"har-{label}-{TS}.har"
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 900},
        record_har_path=str(har_path),
        record_har_url_filter="**/*",
    )
    page = ctx.new_page()

    network_log = []
    def on_request(req):
        u = req.url
        if any(domain in u for domain in [
            "google-analytics.com", "googletagmanager.com",
            "googleadservices.com", "doubleclick.net",
            "facebook.com/tr", "facebook.net",
        ]):
            network_log.append({"method": req.method, "url": u, "post_data": (req.post_data or "")[:600]})
    page.on("request", on_request)

    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(2500)

    # Inspect window state
    attribution = page.evaluate("window.NPCWoodsAttribution")
    paid_surface = page.evaluate("typeof window.NPCWoodsPaidSurface === 'undefined' ? null : window.NPCWoodsPaidSurface")
    print(f"  window.NPCWoodsPaidSurface = {paid_surface}")
    print(f"  attribution.source = {attribution.get('source') if attribution else None}")
    print(f"  attribution.click_id = {attribution.get('click_id') if attribution else None}")
    print(f"  attribution.fbclid = {attribution.get('fbclid') if attribution else None}")

    # Intercept sms: navigation so we don't trigger phone messenger; click the first nav CTA.
    page.evaluate("""
        document.querySelectorAll('a[href^="sms:"]').forEach(a => {
            a.addEventListener('click', e => { e.preventDefault(); window._smsClicked = a.getAttribute('href'); });
        });
    """)
    # Screenshot before click
    page.screenshot(path=str(OUT / f"shot-before-click-{label}-{TS}.png"), full_page=False)
    page.locator("a[href^='sms:']").first.click()
    page.wait_for_timeout(2500)

    sms_href = page.evaluate("window._smsClicked")
    print(f"  clicked SMS link href: {sms_href}")

    # Take screenshot after click
    page.screenshot(path=str(OUT / f"shot-after-click-{label}-{TS}.png"), full_page=False)

    # Search network log for the sms_click event payload
    sms_click_payloads = []
    aw_conversion_hits = []
    fb_lead_hits = []
    for entry in network_log:
        body = entry.get("post_data", "") or ""
        if "en=sms_click" in body or "en=sms_click" in entry["url"]:
            sms_click_payloads.append(entry)
        if "/conversion/610222919/" in entry["url"]:
            aw_conversion_hits.append(entry)
        if "facebook.com/tr" in entry["url"] and ("ev=Lead" in entry["url"] or "ev=Lead" in body):
            fb_lead_hits.append(entry)

    # Check for sms_click_source param
    detected_source = None
    for entry in sms_click_payloads:
        body = entry["post_data"] + " " + entry["url"]
        m = re.search(r"sms_click_source[=:]([a-z_]+)", body)
        if m:
            detected_source = m.group(1)
            break
        # Also check ep.sms_click_source (GA4 event param prefix)
        m2 = re.search(r"ep\.sms_click_source[=:]([a-z_]+)", body)
        if m2:
            detected_source = m2.group(1)
            break

    print(f"  sms_click hits: {len(sms_click_payloads)}")
    print(f"  AW-610222919 conversion hits: {len(aw_conversion_hits)}")
    print(f"  Meta Lead hits: {len(fb_lead_hits)}")
    print(f"  detected sms_click_source: {detected_source}")

    result = {
        "label": label,
        "url": url,
        "expected_source": expected_source,
        "detected_source": detected_source,
        "paid_surface_flag": paid_surface,
        "attribution": attribution,
        "sms_click_hits": len(sms_click_payloads),
        "aw_conversion_hits": len(aw_conversion_hits),
        "fb_lead_hits": len(fb_lead_hits),
        "passes": detected_source == expected_source,
        "har_path": str(har_path.relative_to(OUT.parent.parent.parent)),
    }

    # Save raw network log
    (OUT / f"network-{label}-{TS}.json").write_text(json.dumps(network_log, indent=2))

    ctx.close()
    browser.close()
    return result


def main():
    results = []
    with sync_playwright() as p:
        results.append(run_test(
            p, "google",
            "https://npcwoods.com/uti-care/?gclid=DEPLOY_VERIFY_GOOGLE_5_28",
            expected_source="google",
            expected_pixels=["googleadservices", "google-analytics", "facebook.com/tr"],
        ))
        results.append(run_test(
            p, "facebook",
            "https://npcwoods.com/uti-care/?fbclid=DEPLOY_VERIFY_FACEBOOK_5_28",
            expected_source="facebook",
            expected_pixels=["google-analytics", "facebook.com/tr"],
        ))
        results.append(run_test(
            p, "organic",
            "https://npcwoods.com/uti-treatment/",
            expected_source="organic",
            expected_pixels=["google-analytics", "facebook.com/tr"],
        ))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    all_pass = True
    for r in results:
        status = "PASS" if r["passes"] else "FAIL"
        if not r["passes"]:
            all_pass = False
        print(f"  [{status}] {r['label']:8} → expected={r['expected_source']:8} got={r['detected_source']!r}  sms_clicks={r['sms_click_hits']}  aw={r['aw_conversion_hits']}  meta_lead={r['fb_lead_hits']}")

    (OUT / f"verification-summary-{TS}.json").write_text(json.dumps(results, indent=2, default=str))

    print(f"\nArtifacts saved to: {OUT}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
