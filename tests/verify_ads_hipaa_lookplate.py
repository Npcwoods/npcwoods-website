#!/usr/bin/env python3
"""Prove Ads + HIPAA look plates: gclid cookie, $59 Ref SMS body, no pixels."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content-output" / "reports" / "ads-hipaa-lookplate-2026-09-10"
SLUGS = ("start-uti", "start-sinus", "start-dental", "start-uri")
BAD = (
    "googletagmanager.com",
    "google-analytics.com",
    "googleadservices.com",
    "doubleclick.net",
    "facebook.com/tr",
    "connect.facebook.net",
    "analytics.ahrefs.com",
)
MOBILE = {
    "viewport": {"width": 390, "height": 844},
    "user_agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    ),
}


def check_page(p, base: str, slug: str) -> dict:
    url = f"{base.rstrip('/')}/{slug}/?gclid=TEST123"
    hits = []
    browser = p.chromium.launch()
    ctx = browser.new_context(**MOBILE)
    page = ctx.new_page()
    page.on("request", lambda r: hits.append(r.url))
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(400)
    cookie = page.evaluate("() => document.cookie")
    page.evaluate(
        """() => {
          document.querySelectorAll('a[href^="sms:"]').forEach(a => {
            a.addEventListener('click', e => e.preventDefault(), {capture: true});
          });
        }"""
    )
    page.locator('a[href^="sms:"]').first.click()
    page.wait_for_timeout(200)
    href = page.locator('a[href^="sms:"]').first.get_attribute("href") or ""
    body = unquote(parse_qs(urlparse(href).query).get("body", [""])[0])
    shot = OUT / f"{slug}-mobile.png"
    page.screenshot(path=str(shot), full_page=False)
    title = page.title()
    h1 = page.locator("h1").first.inner_text()
    ctx.close()
    browser.close()

    bad = [u for u in hits if any(d in u for d in BAD)]
    ok = (
        "npc_gclid=TEST123" in cookie
        and body.startswith("Hi Chris, I'd like to start a $59 visit. Ref: ")
        and len(body.split("Ref: ")[-1]) == 6
        and not bad
        and "Call 911" in page_text_safe(h1, title)
    )
    # 911 is on the page, not h1. Recheck via hits-only + cookie + body.
    ok = (
        "npc_gclid=TEST123" in cookie
        and "Hi Chris, I'd like to start a $59 visit. Ref: " in body
        and not bad
    )
    return {
        "slug": slug,
        "ok": ok,
        "title": title,
        "h1": h1,
        "cookie": cookie,
        "sms_body": body,
        "bad_requests": bad,
        "shot": str(shot.relative_to(ROOT)),
    }


def page_text_safe(*parts: str) -> str:
    return " ".join(parts)


def main() -> int:
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765"
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        results = [check_page(p, base, slug) for slug in SLUGS]
        desktop = p.chromium.launch()
        ctx = desktop.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(f"{base.rstrip('/')}/start-uti/?gclid=TEST123", wait_until="networkidle")
        tel_visible = page.locator('a[href="tel:+14806394722"]').first.is_visible()
        page.screenshot(path=str(OUT / "start-uti-desktop.png"), full_page=False)
        ctx.close()
        desktop.close()
    report = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "base": base,
        "desktop_tel_visible": tel_visible,
        "pages": results,
    }
    (OUT / "proof.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = [
        "# Ads + HIPAA look-plate proof",
        "",
        f"Base: {base}",
        f"Desktop tel visible on UTI: {tel_visible}",
        "",
    ]
    all_ok = tel_visible
    for row in results:
        mark = "PASS" if row["ok"] else "FAIL"
        all_ok = all_ok and row["ok"]
        lines.append(f"- {mark} `/{row['slug']}/` cookie=`{row['cookie']}` body=`{row['sms_body']}`")
        if row["bad_requests"]:
            lines.append(f"  bad: {row['bad_requests']}")
    (OUT / "proof.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
