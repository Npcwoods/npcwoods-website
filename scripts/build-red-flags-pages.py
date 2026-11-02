#!/usr/bin/env python3
"""Build the condition red-flags pages (kitchen only).

  /learn/sinus-infection/red-flags/
  /learn/ear-infection/red-flags/
  /learn/skin-infection/red-flags/

Layout, CSS, shared header/footer and byline are copied from the live-approved
/learn/dental-abscess/red-flags/ stop page (the template). Copy lives in
landing-pages/learn/_red-flags/content.json. Do not hand-edit the generated
index.html files.

  python3 scripts/build-red-flags-pages.py          # HTML only
  python3 scripts/build-red-flags-pages.py --og     # also render 1200x630 share cards
                                                     # (needs playwright + Pillow; uses Chris's
                                                     #  real cutout, unaltered)
"""
from __future__ import annotations

import argparse
import base64
import html
import io
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
LP = ROOT / "landing-pages"
TEMPLATE = LP / "learn" / "dental-abscess" / "red-flags" / "index.html"
CONTENT = LP / "learn" / "_red-flags" / "content.json"
SHARE_DIR = ROOT / "assets" / "img" / "share"
SITE = "https://npcwoods.com"
SMS = "4806394722"
OG_VER = "20261102"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def abs_url(p: str) -> str:
    return SITE + p


def sms_href(prefill: str) -> str:
    return f"sms:{SMS}?body=" + quote(prefill, safe="")


def og_name(key: str) -> str:
    return f"{key}-red-flags-1200x630.jpg"


def ghost_svg() -> str:
    grid = "".join(
        f'<line x1="0" y1="{y}" x2="1440" y2="{y}" stroke="rgba(255,255,255,.05)" stroke-dasharray="2 10"/>'
        for y in range(90, 720, 90)
    ) + "".join(
        f'<line x1="{x}" y1="0" x2="{x}" y2="720" stroke="rgba(255,255,255,.05)" stroke-dasharray="2 10"/>'
        for x in range(120, 1440, 120)
    )
    return ('<svg class="hero-ghost" focusable="false" viewBox="0 0 1440 720" '
            'preserveAspectRatio="xMidYMid slice" aria-hidden="true">' + grid + "</svg>")


def figure_svg(title: str, rows: list[str]) -> str:
    """Red warning card, same look as the dental red-flags-er.svg (640x720)."""
    parts = [
        # aria-label instead of an SVG <title>: page parsers (and the pre-flight script) would
        # otherwise glue the SVG title onto the page <title>.
        '<svg class="rf-card" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 720" role="img" '
        f'aria-label="{esc(title)}" font-family="\'DM Sans\',\'Helvetica Neue\',Helvetica,Arial,sans-serif">',
        '<defs><linearGradient id="rfrd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C8321F"/>'
        '<stop offset="1" stop-color="#8F1C12"/></linearGradient></defs>',
        '<rect x="8" y="8" width="624" height="704" rx="26" fill="#FFFFFF" stroke="#B42318" stroke-width="3"/>',
        '<path d="M8 34 Q8 8 34 8 H606 Q632 8 632 34 V104 H8 Z" fill="url(#rfrd)"/>',
        '<g transform="translate(34 26)"><path d="M28 0 L56 50 L0 50 Z" fill="#fff"/>'
        '<rect x="25" y="15" width="6" height="20" rx="3" fill="#B42318"/><circle cx="28" cy="42" r="3.5" fill="#B42318"/></g>',
        '<text x="108" y="54" font-size="28" font-weight="800" fill="#FFFFFF">Go to the ER or call 911</text>',
        '<text x="108" y="84" font-size="18" font-weight="600" fill="#FFE4E0">Do not text first. Go.</text>',
    ]
    y0, h, gap = 128, 82, 14
    for i, row in enumerate(rows):
        y = y0 + i * (h + gap)
        parts.append(f'<rect x="28" y="{y}" width="584" height="{h}" rx="18" fill="#FFF1F0" '
                     'stroke="rgba(180,35,24,.25)" stroke-width="1.5"/>')
        parts.append(f'<circle cx="74" cy="{y + h / 2:.0f}" r="22" fill="#B42318"/>')
        parts.append(f'<text x="74" y="{y + h / 2 + 8:.0f}" font-size="22" font-weight="800" fill="#FFFFFF" '
                     f'text-anchor="middle">{i + 1}</text>')
        parts.append(f'<text x="114" y="{y + h / 2 + 8:.0f}" font-size="27" font-weight="700" fill="#1A1A2E">{esc(row)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def jsonld(page: dict, reviewed: str, key: str) -> str:
    url = abs_url(page["path"])
    img = f"{SITE}/assets/img/share/{og_name(key)}"
    blocks = [
        {
            "@context": "https://schema.org",
            "@type": "MedicalWebPage",
            "name": page["h1"],
            "url": url,
            "description": page["description"],
            "lastReviewed": reviewed,
            "author": {"@id": "https://npcwoods.com/#chris-woods"},
            "reviewedBy": {"@id": "https://npcwoods.com/#chris-woods"},
            "publisher": {"@id": "https://npcwoods.com/#medical-business"},
            "image": {"@type": "ImageObject", "url": img, "width": 1200, "height": 630, "caption": page["h1"]},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in page["faq"]
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://npcwoods.com/"},
                {"@type": "ListItem", "position": 2, "name": "Learn", "item": "https://npcwoods.com/learn/"},
                {"@type": "ListItem", "position": 3, "name": page["guide"]["name"], "item": abs_url(page["guide"]["path"])},
                {"@type": "ListItem", "position": 4, "name": page["crumb"], "item": url},
            ],
        },
    ]
    return "\n".join(
        '<script type="application/ld+json">\n' + json.dumps(b, indent=2, ensure_ascii=False) + "\n</script>"
        for b in blocks
    )


def build_head(tpl_head: str, page: dict, key: str, reviewed: str) -> str:
    url = abs_url(page["path"])
    img = f"{SITE}/assets/img/share/{og_name(key)}?v={OG_VER}"
    meta = "\n".join([
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"<title>{esc(page['title'])}</title>",
        f'<meta name="description" content="{esc(page["description"])}">',
        f'<link rel="canonical" href="{url}">',
        f'<link rel="cite-as" href="{url}">',
        '<meta property="og:type" content="article">',
        f'<meta property="og:title" content="{esc(page["title"])}">',
        f'<meta property="og:description" content="{esc(page["description"])}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{img}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{esc(page["og_alt"])}">',
        f'<meta name="twitter:image" content="{img}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(page["title"])}">',
        f'<meta name="twitter:description" content="{esc(page["description"])}">',
    ])
    # keep template prelude (no-op fbq stub comment block) + icon/fonts + person JSON-LD + CSS
    pre = tpl_head[: tpl_head.index('<meta charset="UTF-8">')]
    icon_start = tpl_head.index('<link rel="icon"')
    ld_start = tpl_head.index('<script type="application/ld+json">')
    fonts = tpl_head[icon_start:ld_start].rstrip() + "\n"
    person_i = tpl_head.index('"@type": "Person"')
    person_start = tpl_head.rindex('<script type="application/ld+json">', 0, person_i)
    rest = tpl_head[person_start:]  # Person JSON-LD + <style>...</style> + </head>
    extra_css = ("<style>.rf-card{width:100%;height:auto;display:block;border-radius:18px;"
                 "box-shadow:0 0 0 1px var(--line)}</style>\n")
    rest = rest.replace("</head>", extra_css + "</head>")
    return pre + meta + "\n" + fonts + "\n" + jsonld(page, reviewed, key) + "\n" + rest


def ul(items: list[str]) -> str:
    return "<ul>\n" + "\n".join(f"<li>{esc(i)}</li>" for i in items) + "\n</ul>"


def main_html(page: dict, key: str, tpl: str, reviewed: str, reviewed_display: str) -> str:
    sms = sms_href(page["sms_prefill"])
    hero_img = re.search(r'<img class="hero-cutout"[^>]*>', tpl).group(0)
    b1, b2 = page["bubbles"]
    out = [
        f'<div class="series-sticky" role="navigation" aria-label="Page bar"><span class="series-sticky-ep">{esc(page["sticky"])}</span>'
        f'<a class="series-sticky-cta" href="{esc(sms)}">Text Chris</a></div>',
        "",
        '<main id="main">',
        '<header class="hero hero-art">',
        ghost_svg(),
        '<div class="hero-inner">',
        '<div class="hero-copy">',
        f'<div class="hero-kicker"><span class="dot"></span> {esc(page["kicker"])}</div>',
        f"<h1>{esc(page['h1'])}</h1>",
        f'<p class="lede">{esc(page["lede"])}</p>',
        "</div>",
        '<div class="hero-photo">',
        hero_img,
        f'<span class="hero-bubble hb-black">{esc(b1)}</span>',
        f'<span class="hero-bubble hb-blue">{esc(b2)}</span>',
        "</div>",
        "</div>",
        "</header>",
        '<article class="series-wrap">',
        '<div class="thread" aria-label="Sample texts">',
        '<div class="bubble-label">You</div>',
        f'<div class="bubble bubble-blue">{esc(page["thread"][0])}</div>',
        '<div class="bubble-label">Chris</div>',
        f'<div class="bubble bubble-black">{esc(page["thread"][1])}</div>',
        "</div>",
        '<aside class="safety">',
        "<b>Red flag</b>",
        "<h2>Go to the ER or call 911 now</h2>",
        f"<p>{esc(page['er_text'])}</p>",
        "</aside>",
        f'<figure class="art-fig" aria-label="{esc(page["fig_alt"])}">{figure_svg(page["fig_title"], page["fig_rows"])}'
        f"<figcaption>{esc(page['fig_caption'])}</figcaption></figure>",
    ]
    for s in page["sections"]:
        out.append('<div class="prose">')
        out.append(f"<h2>{esc(s['h2'])}</h2>")
        for p in s.get("p", []):
            out.append(f"<p>{esc(p)}</p>")
        if s.get("ul"):
            out.append(ul(s["ul"]))
        for p in s.get("p_after", []):
            out.append(f"<p>{esc(p)}</p>")
        out.append("</div>")
    # related reading, reusing the series roadmap styling
    items = []
    for i, (path, title, ep) in enumerate(page["related"]):
        cls = "roadmap-item is-hub" if i == 0 else "roadmap-item"
        items.append(f'<li class="{cls}"><span class="roadmap-dot" aria-hidden="true"></span>'
                     f'<a href="{abs_url(path)}"><div class="roadmap-ep">{esc(ep)}</div>'
                     f'<div class="roadmap-title">{esc(title)}</div></a></li>')
    out.append('<nav class="roadmap" aria-label="Keep reading"><h2>Keep reading</h2>'
               '<p class="roadmap-lead">Calmer pages for when you are stable.</p>'
               f'<ol class="roadmap-list">{"".join(items)}</ol></nav>')
    # byline (copied from template, date swapped)
    by = re.search(r'<section class="npc-clinician-byline".*?</section>', tpl, re.S).group(0)
    by = re.sub(r'<time datetime="[^"]+">[^<]+</time>', f'<time datetime="{reviewed}">{reviewed_display}</time>', by)
    out.append(by)
    out.append('<section class="faq" id="faq"><h2>Questions I get</h2>')
    for q, a in page["faq"]:
        out.append(f"<details>\n<summary>{esc(q)}</summary>\n<p>{esc(a)}</p>\n</details>")
    out.append("</section>")
    out.append('<section class="sources" id="sources"><h2>Sources</h2><ol>')
    for u, t in page["sources"]:
        out.append(f'<li><a href="{esc(u)}" rel="noopener">{esc(t)}</a></li>')
    out.append("</ol></section>")
    (pp, pt), (np_, nt) = page["prev"], page["next"]
    out.append('<nav class="prev-next" aria-label="Previous and next">'
               f'<a href="{abs_url(pp)}"><div class="label">Back</div><div class="title">{esc(pt)}</div></a>'
               f'<a href="{abs_url(np_)}"><div class="label">Next</div><div class="title">{esc(nt)}</div></a></nav>')
    out.append('<section class="cta-band">')
    out.append("  <h2>If you fit a text visit, start here</h2>")
    out.append(f"  <p>{esc(page['cta_p'])}</p>")
    out.append(f'  <a class="btn" href="{esc(sms)}">Text (480) 639-4722</a>')
    out.append("</section>")
    out.append("</article></main>")
    return "\n".join(out)


def build_page(key: str, page: dict, content: dict, tpl: str) -> str:
    head_end = tpl.index("</head>") + len("</head>")
    head = build_head(tpl[:head_end], page, key, content["reviewed"])
    body_open = tpl.index("<body")
    sticky = tpl.index('<div class="series-sticky"')
    header = tpl[body_open:sticky]
    footer_start = tpl.index("<!-- ===== NPCWOODS SITE FOOTER")
    footer = tpl[footer_start:]
    main = main_html(page, key, tpl, content["reviewed"], content["reviewed_display"])
    return tpl[:0] + head + "\n" + "\n" + header + main + "\n" + footer


def card_html(title: str, kicker: str, cutout_uri: str) -> str:
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;700;800&family=DM+Serif+Display&display=block">
<style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{position:relative;font-family:"DM Sans",Arial,sans-serif;color:#fff;
background:radial-gradient(560px 460px at 78% 60%,rgba(0,113,227,.48),transparent 70%),
radial-gradient(460px 320px at 8% 0%,rgba(41,151,255,.16),transparent 70%),#05060a}}
.hero-ghost{{position:absolute;inset:0;width:100%;height:100%}}
.copy{{position:absolute;left:72px;top:84px;width:640px;z-index:2}}
.pill{{display:inline-flex;align-items:center;gap:10px;font-size:18px;font-weight:800;letter-spacing:.08em;
text-transform:uppercase;border:1.5px solid rgba(255,255,255,.2);background:rgba(255,255,255,.06);padding:10px 18px;border-radius:999px}}
.pill i{{width:10px;height:10px;border-radius:50%;background:#B42318;box-shadow:0 0 0 2px rgba(255,255,255,.85)}}
h1{{font-family:"DM Serif Display",Georgia,serif;font-weight:400;font-size:64px;line-height:1.05;margin:26px 0 22px;letter-spacing:-.01em}}
p{{font-size:24px;color:#c7c7ce;margin:0;font-weight:500}}
.price{{display:inline-block;margin-top:22px;font-size:26px;font-weight:800;color:#fff;background:#007AFF;padding:10px 20px;border-radius:999px}}
img{{position:absolute;right:64px;bottom:0;height:600px;z-index:2;filter:drop-shadow(0 30px 50px rgba(0,0,0,.55))}}
</style></head><body>
{ghost_svg()}
<div class="copy"><div class="pill"><i></i>{esc(kicker)}</div>
<h1>{esc(title)}</h1><p>Plain talk from Chris Woods, NP</p><div class="price">$59 text visits</div></div>
<img src="{cutout_uri}" alt="">
</body></html>"""


def render_og(content: dict, cutout: Path, chrome: str | None = None) -> None:
    from PIL import Image
    from playwright.sync_api import sync_playwright

    uri = "data:image/webp;base64," + base64.b64encode(cutout.read_bytes()).decode()
    SHARE_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(**({"executable_path": chrome} if chrome else {}))
        pg = browser.new_page(viewport={"width": 1200, "height": 630})
        for key, page in content["pages"].items():
            pg.set_content(card_html(page["h1"], page["card_kicker"], uri), wait_until="networkidle")
            pg.wait_for_timeout(400)
            img = Image.open(io.BytesIO(pg.screenshot(type="png"))).convert("RGB")
            out = SHARE_DIR / og_name(key)
            img.save(out, "JPEG", quality=82, optimize=True, progressive=True)
            print(f"wrote {out.relative_to(ROOT)} {img.size} {out.stat().st_size} bytes")
        browser.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--og", action="store_true", help="also render share cards")
    ap.add_argument("--cutout", default=str(ROOT / "assets" / "img" / "people" / "chris-cutout-900.webp"))
    ap.add_argument("--chrome", default=None, help="path to a Chrome/Chromium binary")
    args = ap.parse_args()
    content = json.loads(CONTENT.read_text(encoding="utf-8"))
    tpl = TEMPLATE.read_text(encoding="utf-8")
    for key, page in content["pages"].items():
        out = LP / page["path"].strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_page(key, page, content, tpl), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")
    if args.og:
        render_og(content, Path(args.cutout), args.chrome)


if __name__ == "__main__":
    main()
