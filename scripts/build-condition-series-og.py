#!/usr/bin/env python3
"""Render 1200x630 share cards for a condition series (hub, stops, offer page).

Generic copy of build-dental-abscess-og.py (2026-11-24). Chris's real cutout,
unaltered, on the series hero background, plus the page title, the topic
ghost graphic, and a $59 text-visit badge. Kitchen only.

  python3 scripts/build-condition-series-og.py <series-id> --cutout assets/img/people/chris-cutout-900.webp [--chrome /path]
"""
from __future__ import annotations

import argparse, base64, html, importlib.util, io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_build(series_id: str):
    spec = importlib.util.spec_from_file_location("ccs", ROOT / "scripts" / "build-condition-series.py")
    mod = importlib.util.module_from_spec(spec)
    sys.argv = [sys.argv[0], series_id]
    spec.loader.exec_module(mod)
    return mod


def card_html(title: str, kicker: str, ghost: str, cutout_uri: str, accent: str) -> str:
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;700;800&family=DM+Serif+Display&display=block">
<style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{position:relative;font-family:"DM Sans",Arial,sans-serif;color:#fff;
background:radial-gradient(560px 460px at 78% 60%,rgba(0,113,227,.48),transparent 70%),
radial-gradient(460px 320px at 8% 0%,rgba(41,151,255,.16),transparent 70%),#05060a}}
.hero-ghost{{position:absolute;inset:0;width:100%;height:100%}}
.copy{{position:absolute;left:72px;top:84px;width:660px;z-index:2}}
.pill{{display:inline-flex;align-items:center;gap:10px;font-size:18px;font-weight:800;letter-spacing:.08em;
text-transform:uppercase;border:1.5px solid rgba(255,255,255,.2);background:rgba(255,255,255,.06);padding:10px 18px;border-radius:999px}}
.pill i{{width:10px;height:10px;border-radius:50%;background:{accent};box-shadow:0 0 0 2px rgba(255,255,255,.85)}}
h1{{font-family:"DM Serif Display",Georgia,serif;font-weight:400;font-size:64px;line-height:1.04;margin:26px 0 20px;letter-spacing:-.01em}}
p{{font-size:24px;color:#c7c7ce;margin:0;font-weight:500}}
.badge{{position:absolute;left:72px;bottom:56px;z-index:3;display:flex;align-items:center;gap:14px}}
.badge b{{font-family:"DM Serif Display",Georgia,serif;font-weight:400;font-size:44px;background:#fff;color:#05060a;padding:4px 18px;border-radius:14px}}
.badge span{{font-size:22px;font-weight:800;background:#007AFF;border:1.5px solid #fff;padding:12px 18px;border-radius:20px 20px 20px 6px}}
img{{position:absolute;right:56px;bottom:0;height:600px;z-index:2;filter:drop-shadow(0 30px 50px rgba(0,0,0,.55))}}
</style></head><body>
{ghost}
<div class="copy"><div class="pill"><i></i>{html.escape(kicker)}</div>
<h1>{html.escape(title)}</h1><p>Plain talk from Chris Woods, NP</p></div>
<div class="badge"><b>$59</b><span>Text visit · (480) 639-4722</span></div>
<img src="{cutout_uri}" alt="">
</body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("series_id")
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--cutout", required=True, help="local path to chris-cutout-900.webp")
    args = ap.parse_args()
    from PIL import Image
    from playwright.sync_api import sync_playwright

    build = load_build(args.series_id)
    sdir = ROOT / "landing-pages" / "learn" / args.series_id
    series = json.loads((sdir / "series.json").read_text(encoding="utf-8"))
    content = json.loads((sdir / "content.json").read_text(encoding="utf-8"))
    art = json.loads((sdir / "art.json").read_text(encoding="utf-8"))
    build.GHOST_ACCENT = series["accent"]["hex"]
    cutout_uri = "data:image/webp;base64," + base64.b64encode(Path(args.cutout).read_bytes()).decode()
    out_dir = sdir / "assets" / "og"
    out_dir.mkdir(parents=True, exist_ok=True)
    jobs = []
    for stop in series["stops"]:
        key = "hub" if stop["kind"] == "hub" else stop["slug"]
        jobs.append((key, content[key]["h1"], f"{series['kicker']} · Stop {stop['episode']}", art["pages"][key]["ghost"]))
    jobs.append(("offer", content["one_pager"]["h1"], "$59 text visit", "chat"))
    with sync_playwright() as p:
        launch = {"executable_path": args.chrome} if args.chrome else {}
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": 1200, "height": 630})
        for key, title, kicker, ghost in jobs:
            page.set_content(card_html(title, kicker, build.ghost_svg(ghost, series["ghost_base"]), cutout_uri, series["accent"]["hex"]), wait_until="networkidle")
            page.wait_for_timeout(300)
            img = Image.open(io.BytesIO(page.screenshot(type="png"))).convert("RGB")
            out = out_dir / f"og-{key}.jpg"
            img.save(out, "JPEG", quality=82, optimize=True, progressive=True)
            print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")
        browser.close()


if __name__ == "__main__":
    main()
