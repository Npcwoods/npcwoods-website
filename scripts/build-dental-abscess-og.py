#!/usr/bin/env python3
"""Render 1200x630 social share cards (OG images) for the dental-abscess series.

Kitchen only. Composites Chris's real clinician cutout (unaltered) on the
series hero background with the page title and the topic ghost tooth. Writes
landing-pages/learn/dental-abscess/assets/og/og-<page>.jpg.

Needs: playwright (Chromium or Chrome) and Pillow.
  python3 scripts/build-dental-abscess-og.py [--chrome /path/to/chrome]
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import io
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERIES_DIR = ROOT / "landing-pages" / "learn" / "dental-abscess"
OUT = SERIES_DIR / "assets" / "og"
SITE = "https://npcwoods.com"


def load_build():
    spec = importlib.util.spec_from_file_location("das", ROOT / "scripts" / "build-dental-abscess-series.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def card_html(title: str, kicker: str, ghost: str, cutout_uri: str) -> str:
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;700;800&family=DM+Serif+Display&display=block">
<style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{position:relative;font-family:"DM Sans",Arial,sans-serif;color:#fff;
background:radial-gradient(560px 460px at 78% 60%,rgba(0,113,227,.48),transparent 70%),
radial-gradient(460px 320px at 8% 0%,rgba(41,151,255,.16),transparent 70%),#05060a}}
.hero-ghost{{position:absolute;inset:0;width:100%;height:100%}}
.copy{{position:absolute;left:72px;top:96px;width:640px;z-index:2}}
.pill{{display:inline-flex;align-items:center;gap:10px;font-size:18px;font-weight:800;letter-spacing:.08em;
text-transform:uppercase;border:1.5px solid rgba(255,255,255,.2);background:rgba(255,255,255,.06);padding:10px 18px;border-radius:999px}}
.pill i{{width:10px;height:10px;border-radius:50%;background:#B42318;box-shadow:0 0 0 2px rgba(255,255,255,.85)}}
h1{{font-family:"DM Serif Display",Georgia,serif;font-weight:400;font-size:68px;line-height:1.04;margin:28px 0 22px;letter-spacing:-.01em}}
p{{font-size:24px;color:#c7c7ce;margin:0;font-weight:500}}
img{{position:absolute;right:64px;bottom:0;height:600px;z-index:2;filter:drop-shadow(0 30px 50px rgba(0,0,0,.55))}}
</style></head><body>
{ghost}
<div class="copy"><div class="pill"><i></i>{html.escape(kicker)}</div>
<h1>{html.escape(title)}</h1><p>Plain talk from Chris Woods, NP</p></div>
<img src="{cutout_uri}" alt="">
</body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--cutout", default=None, help="local path to chris-cutout-900.webp")
    args = ap.parse_args()

    from PIL import Image
    from playwright.sync_api import sync_playwright

    build = load_build()
    series = json.loads((SERIES_DIR / "series.json").read_text(encoding="utf-8"))
    content = json.loads((SERIES_DIR / "content.json").read_text(encoding="utf-8"))
    art = json.loads((SERIES_DIR / "art.json").read_text(encoding="utf-8"))

    if args.cutout:
        cutout = Path(args.cutout).read_bytes()
    else:
        req = urllib.request.Request(SITE + art["cutout"]["src900"], headers={"User-Agent": "Mozilla/5.0"})
        cutout = urllib.request.urlopen(req, timeout=30).read()
    import base64
    cutout_uri = "data:image/webp;base64," + base64.b64encode(cutout).decode()

    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        launch = {"executable_path": args.chrome} if args.chrome else {}
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": 1200, "height": 630})
        for stop in series["stops"]:
            key = "hub" if stop["kind"] == "hub" else stop["slug"]
            title = content[key]["h1"]
            kicker = f"Dental abscess series · Stop {stop['episode']}"
            ghost = build.ghost_svg(art["pages"][key]["ghost"])
            page.set_content(card_html(title, kicker, ghost, cutout_uri), wait_until="networkidle")
            page.wait_for_timeout(300)
            png = page.screenshot(type="png")
            img = Image.open(io.BytesIO(png)).convert("RGB")
            out = OUT / f"og-{key}.jpg"
            img.save(out, "JPEG", quality=82, optimize=True, progressive=True)
            print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")
        browser.close()


if __name__ == "__main__":
    main()
