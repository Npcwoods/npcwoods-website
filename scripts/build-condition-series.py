#!/usr/bin/env python3
"""HELPER MODULE (retired builder). Use scripts/build-condition-series-gold.py.

Build a condition SEO mini-series (hub + stops) and its $59 offer one-pager.

Generic copy of build-dental-abscess-series.py (2026-11-24). Everything
series-specific lives in the series folder (series.json, content.json,
art.json, _shared/*.css). Usage:

  python3 scripts/build-condition-series.py screening-labs
  python3 scripts/build-condition-series.py mastitis


Reads (per series folder landing-pages/learn/<id>/):
  series.json, content.json, art.json, _shared/series.css, _shared/art.css
  html/shared/header-snippet.html
  html/shared/footer-snippet.html

Writes HTML under landing-pages/learn/<id>/ and the one_pager path.
Never deploy. Kitchen only.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SERIES_ID = sys.argv[1] if len(sys.argv) > 1 and __name__ == "__main__" else "screening-labs"
SERIES_DIR = ROOT / "landing-pages" / "learn" / SERIES_ID
OFFER_DIR = None  # set in main() from series.json one_pager.path
SITE = "https://npcwoods.com"
# The pre-WA/FL footer licensing line. If the shared footer snippet ever regresses
# to it, refuse to build rather than re-plate an 11-state footer onto the series.
STALE_FOOTER_LICENSE_LINE = "Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT<br>"
CURRENT_FOOTER_LICENSE_LINE = (
    "Licensed in 14 states, including Florida by telehealth registration "
    "(AZ, CO, CT, GA, ID, IA, MT, NV, NM, NC, OR, UT, WA, plus FL TPAN3355).<br>"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sms_href(number: str, prefill: str) -> str:
    return f"sms:{number}?body={quote(prefill)}"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def inline_links(text: str) -> str:
    return esc(text)


def person_schema() -> str:
    return """{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://npcwoods.com/#chris-woods",
  "url": "https://npcwoods.com/about/",
  "name": "Chris Woods",
  "jobTitle": "Nurse Practitioner",
  "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
  "worksFor": { "@id": "https://npcwoods.com/#medical-business" },
  "hasCredential": {
    "@type": "EducationalOccupationalCredential",
    "credentialCategory": "license",
    "name": "MSN, APRN, FNP-C, AGACNP-BC"
  }
}"""


def faq_schema(faqs: list[dict]) -> str:
    entities = []
    for item in faqs:
        entities.append(
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
            }
        )
    return json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities},
        indent=2,
        ensure_ascii=False,
    )


def breadcrumb_schema(crumbs: list[tuple[str, str]]) -> str:
    elements = []
    for i, (name, url) in enumerate(crumbs, start=1):
        elements.append(
            {"@type": "ListItem", "position": i, "name": name, "item": url}
        )
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": elements,
        },
        indent=2,
        ensure_ascii=False,
    )


def medical_schema(name: str, url: str, description: str, reviewed: str, image: dict | None = None) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "MedicalWebPage",
        "name": name,
        "url": url,
        "description": description,
        "lastReviewed": reviewed,
        "author": {"@id": "https://npcwoods.com/#chris-woods"},
        "reviewedBy": {"@id": "https://npcwoods.com/#chris-woods"},
        "publisher": {"@id": "https://npcwoods.com/#medical-business"},
    }
    if image:
        data["image"] = image
    return json.dumps(data, indent=2, ensure_ascii=False)


def bubbles_html(bubbles: list[dict]) -> str:
    parts = ['<div class="thread" aria-label="Sample texts">']
    for bubble in bubbles:
        who = esc(bubble.get("who", ""))
        style = bubble.get("style", "blue")
        klass = "bubble-blue" if style == "blue" else "bubble-black"
        parts.append(f'<div class="bubble-label">{who}</div>')
        parts.append(f'<div class="bubble {klass}">{esc(bubble["text"])}</div>')
    parts.append("</div>")
    return "\n".join(parts)


def figure_html(art: dict, fig: dict) -> str:
    src = f"{art['asset_base']}{fig['src']}?v={art['version']}"
    return (
        '<figure class="art-fig">'
        f'<img src="{esc(src)}" width="{fig["width"]}" height="{fig["height"]}" '
        f'alt="{esc(fig["alt"])}" loading="lazy" decoding="async">'
        f'<figcaption>{esc(fig["caption"])}</figcaption>'
        "</figure>"
    )


def sections_html(sections: list[dict], figures: list[dict] | None = None, art: dict | None = None) -> str:
    out: list[str] = []
    figures = figures or []
    for fig in figures:
        if fig.get("after_section", 0) < 0:
            out.append(figure_html(art, fig))
    for idx, block in enumerate(sections):
        kind = block.get("type")
        if kind == "prose":
            out.append('<div class="prose">')
            if block.get("heading"):
                out.append(f"<h2>{esc(block['heading'])}</h2>")
            for para in block.get("body", []):
                out.append(f"<p>{esc(para)}</p>")
            out.append("</div>")
        elif kind == "list":
            out.append('<div class="prose">')
            if block.get("heading"):
                out.append(f"<h2>{esc(block['heading'])}</h2>")
            out.append("<ul>")
            for item in block.get("items", []):
                out.append(f"<li>{esc(item)}</li>")
            out.append("</ul></div>")
        elif kind == "callout":
            klass = "safety" if block.get("kind") == "safety" else "ink-block"
            out.append(f'<aside class="{klass}">')
            if block.get("kind") == "safety":
                out.append("<b>Red flag</b>")
            out.append(f"<h2>{esc(block.get('title', ''))}</h2>")
            out.append(f"<p>{esc(block.get('body', ''))}</p>")
            out.append("</aside>")
        for fig in figures:
            if fig.get("after_section", 0) == idx:
                out.append(figure_html(art, fig))
    return "\n".join(out)


def stats_html(stats: list[dict]) -> str:
    if not stats:
        return ""
    cards = []
    for item in stats:
        cards.append(
            f'<div class="stat"><div class="stat-num">{esc(item["num"])}</div>'
            f'<div class="stat-label">{esc(item["label"])}</div></div>'
        )
    return '<div class="stats">' + "".join(cards) + "</div>"


def faqs_html(faqs: list[dict]) -> str:
    parts = ['<section class="faq" id="faq"><h2>Questions I get</h2>']
    for item in faqs:
        parts.append("<details>")
        parts.append(f"<summary>{esc(item['q'])}</summary>")
        parts.append(f"<p>{esc(item['a'])}</p>")
        parts.append("</details>")
    parts.append("</section>")
    return "\n".join(parts)


def sources_html(sources: list[dict]) -> str:
    if not sources:
        return ""
    parts = ['<section class="sources" id="sources"><h2>Sources</h2><ol>']
    for src in sources:
        label = esc(src["label"])
        url = esc(src["url"])
        parts.append(f'<li><a href="{url}" rel="noopener">{label}</a></li>')
    parts.append("</ol></section>")
    return "\n".join(parts)


def roadmap_html(series: dict, here_path: str, dotted: bool = True) -> str:
    items = []
    for stop in series["stops"]:
        current = stop["path"] == here_path
        klass = "roadmap-item"
        if current:
            klass += " is-here"
        if stop.get("kind") == "hub":
            klass += " is-hub"
        here_badge = ' <span class="you-are-here">You are here</span>' if current else ""
        items.append(
            f'<li class="{klass}">'
            f'<span class="roadmap-dot" aria-hidden="true"></span>'
            f'<a href="{SITE}{stop["path"]}">'
            f'<div class="roadmap-ep">Stop {stop["episode"]}</div>'
            f'<div class="roadmap-title">{esc(stop["nav_label"])}{here_badge}</div>'
            f"</a></li>"
        )
    lead = (
        "The dotted line is the whole story. Start at the big picture. Keep walking."
        if dotted
        else "The rest of the series, in order."
    )
    return (
        '<nav class="roadmap" aria-label="Series roadmap">'
        "<h2>The series</h2>"
        f'<p class="roadmap-lead">{lead}</p>'
        f'<ol class="roadmap-list">{"".join(items)}</ol></nav>'
    )


def prev_next_html(series: dict, index: int) -> str:
    stops = series["stops"]
    parts = ['<nav class="prev-next" aria-label="Series next and previous">']
    if index > 0:
        prev = stops[index - 1]
        parts.append(
            f'<a href="{SITE}{prev["path"]}"><div class="label">Previous</div>'
            f'<div class="title">{esc(prev["title"])}</div></a>'
        )
    else:
        parts.append("<div></div>")
    if index < len(stops) - 1:
        nxt = stops[index + 1]
        parts.append(
            f'<a href="{SITE}{nxt["path"]}"><div class="label">Next</div>'
            f'<div class="title">{esc(nxt["title"])}</div></a>'
        )
    parts.append("</nav>")
    return "".join(parts)


def eeat_html(series: dict) -> str:
    reviewed = series["reviewed"]
    display = series["reviewed_display"]
    license_line = series["license_line"]
    return f"""<section class="npc-clinician-byline" aria-label="Clinician review attribution and freshness">
  <div class="npc-byline-inner">
    <div class="npc-byline-badge" aria-hidden="true">Clinician reviewed</div>
    <p class="npc-byline-main">
      Clinically reviewed by
      <a href="https://npcwoods.com/about/" rel="author">Chris Woods, MSN, APRN, FNP-C, AGACNP-BC</a>
      — Double board-certified Nurse Practitioner. {esc(license_line)}.
    </p>
    <p class="npc-byline-meta">
      <strong>Last reviewed: <time datetime="{reviewed}">{esc(display)}</time></strong>.
      This page reflects Chris's real clinical experience treating patients via NPCWoods Telemedicine.
      <span class="npc-byline-real">Real clinician. No AI.</span>
      <a href="https://npcwoods.com/credentials/" class="npc-byline-verify">Verify credentials</a>
    </p>
  </div>
</section>"""


def sticky_html(cta: str, label: str) -> str:
    return (
        f'<div class="series-sticky" role="navigation" aria-label="Episode bar">'
        f'<span class="series-sticky-ep">{esc(label)}</span>'
        f'<a class="series-sticky-cta" href="{cta}">Text Chris</a></div>'
    )



GHOST_BLUE = "#7cc4ff"
GHOST_BLUE2 = "#2997ff"
GHOST_ACCENT = "#B42318"  # replaced in main() with the series accent

def _gs(color: str, opacity: float, width: float, dash: str = "") -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'fill="none" stroke="{color}" stroke-opacity="{opacity}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"{d}'
    )


# Base ghost shapes (drawn in a ~200 x 340 box, like the dental tooth).
# Decorative only: no text, no numbers.
BASE_SHAPES = {
    "vial": (
        "M70 40 V268 A30 30 0 0 0 130 268 V40",
        "M56 8 H144 Q150 8 150 14 V34 Q150 40 144 40 H56 Q50 40 50 34 V14 Q50 8 56 8 Z "
        "M70 160 Q85 150 100 160 Q115 170 130 160 "
        "M116 80 H130 M116 110 H130 M116 140 H130 M116 200 H130 M116 230 H130",
    ),
    "drop": (
        "M100 0 C100 0 14 118 14 206 A86 86 0 0 0 186 206 C186 118 100 0 100 0 Z",
        "M54 214 A46 46 0 0 0 100 258 M100 60 C100 60 52 130 52 190",
    ),
}


def _motif(name: str) -> str:
    A, B, B2 = GHOST_ACCENT, GHOST_BLUE, GHOST_BLUE2
    m = {
        "hub": f'<path d="M-140 136 Q-60 112 20 128 M180 128 Q260 112 340 136" {_gs(B, .3, 4)}/>'
               f'<circle cx="100" cy="206" r="30" {_gs(A, .42, 4)}/>',
        "rings": "".join(
            f'<path d="M{100 - r} 40 A{r} {r} 0 0 1 {100 + r} 40" {_gs(A, o, 4)}/>'
            for r, o in ((60, .45), (80, .3), (100, .18))
        ),
        "cells": "".join(
            f'<circle cx="{x}" cy="{y}" r="{r}" {_gs(c, .42, 4)}/>'
            for x, y, r, c in ((270, 40, 22, A), (330, 90, 18, B), (280, 140, 26, B2), (350, 180, 14, A), (240, 210, 16, B))
        ),
        "bars": "".join(
            f'<path d="M{x} 220 V{220 - h}" {_gs(c, .45, 10)}/>'
            for x, h, c in ((250, 60, B), (285, 110, B2), (320, 80, B), (355, 150, A))
        ) + f'<path d="M230 222 H380" {_gs(B, .3, 3)}/>',
        "wave": f'<path d="M220 120 C250 60 280 180 310 120 C340 60 370 180 400 120" {_gs(A, .45, 4)}/>'
                f'<path d="M220 170 C250 110 280 230 310 170 C340 110 370 230 400 170" {_gs(B, .3, 4, "2 12")}/>',
        "butterfly": f'<path d="M300 60 C250 20 200 60 220 120 C235 165 280 170 300 140 C320 170 365 165 380 120 '
                     f'C400 60 350 20 300 60 Z" {_gs(A, .42, 4)}/>'
                     f'<path d="M300 60 V150" {_gs(B, .35, 4, "2 10")}/>',
        "warning": f'<path d="M300 10 L392 176 L208 176 Z" {_gs(A, .42, 5)}/>'
                   f'<path d="M300 64 V124" {_gs(A, .42, 6)}/>'
                   f'<circle cx="300" cy="150" r="5" fill="{A}" fill-opacity=".42"/>',
        "path": f'<path d="M240 30 C320 70 210 150 290 200 C350 236 270 300 320 350" {_gs(B, .4, 4, "2 12")}/>'
                + "".join(
                    f'<circle cx="{x}" cy="{y}" r="12" {_gs(c, .5, 4)}/>'
                    for x, y, c in ((240, 30, A), (262, 118, B), (290, 200, B), (320, 350, B))
                ),
        "chat": f'<path d="M250 20 H370 Q400 20 400 50 V90 Q400 120 370 120 H290 L262 144 L268 120 H250 '
                f'Q220 120 220 90 V50 Q220 20 250 20 Z" {_gs(B2, .34, 4)}/>'
                f'<path d="M255 70 H365" {_gs(B, .35, 4, "2 12")}/>',
        "loop": f'<path d="M100 -20 A220 220 0 1 1 -110 230" {_gs(A, .4, 4, "2 12")}/>'
                f'<path d="M-130 212 L-110 232 L-88 214" {_gs(A, .5, 4)}/>',
        "checkx": f'<path d="M250 40 L298 88 M298 40 L250 88" {_gs(A, .42, 5)}/>'
                  f'<path d="M248 176 L270 198 L310 150" {_gs(B, .4, 5)}/>',
        "grid": "".join(
            f'<rect x="{230 + c * 36}" y="{30 + r * 36}" width="26" height="26" rx="6" '
            f'{_gs(A if (r, c) in ((1, 2), (3, 0)) else B, .4 if (r, c) in ((1, 2), (3, 0)) else .26, 3)}/>'
            for r in range(4) for c in range(4)
        ),
        "split": f'<path d="M300 20 V120 M300 120 L230 200 M300 120 L370 200" {_gs(B, .4, 4, "2 12")}/>'
                 f'<circle cx="230" cy="214" r="14" {_gs(B, .5, 4)}/><circle cx="370" cy="214" r="14" {_gs(A, .5, 4)}/>',
        "range": f'<path d="M220 120 H400" {_gs(B, .3, 10)}/>'
                 f'<path d="M270 120 H350" {_gs(B2, .45, 10)}/>'
                 f'<circle cx="370" cy="120" r="12" {_gs(A, .55, 4)}/>',
    }
    return m.get(name, "")


def ghost_svg(variant: str, base: str = "vial") -> str:
    """Topic ghost graphic behind the hero headline: a big series outline plus
    one stop motif. Decorative, no text, no numbers."""
    outline, inner = BASE_SHAPES[base]
    grid = "".join(
        f'<line x1="0" y1="{y}" x2="1440" y2="{y}" stroke="rgba(255,255,255,.05)" stroke-dasharray="2 10"/>'
        for y in range(90, 720, 90)
    ) + "".join(
        f'<line x1="{x}" y1="0" x2="{x}" y2="720" stroke="rgba(255,255,255,.05)" stroke-dasharray="2 10"/>'
        for x in range(120, 1440, 120)
    )
    return (
        '<svg class="hero-ghost" focusable="false" viewBox="0 0 1440 720" '
        'preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
        f"{grid}"
        '<g class="ghost-shape" transform="translate(500 118) scale(1.4)">'
        f'<path d="{outline}" {_gs(GHOST_BLUE, .26, 5)}/>'
        f'<path d="{inner}" {_gs(GHOST_BLUE2, .24, 3, "3 9")}/>'
        f"{_motif(variant)}"
        "</g></svg>"
    )


def hero_html(page: dict, stop: dict, art: dict, page_art: dict, series: dict) -> str:
    cut = art["cutout"]
    s1, s2 = page_art["stickers"]
    return "\n".join([
        '<header class="hero hero-art">',
        ghost_svg(page_art["ghost"], series["ghost_base"]),
        '<div class="hero-inner">',
        '<div class="hero-copy">',
        f'<div class="hero-kicker"><span class="dot"></span> {esc(series["kicker"])} · Stop {stop["episode"]}</div>',
        f"<h1>{esc(page['h1'])}</h1>",
        f'<p class="lede">{esc(page["lede"])}</p>',
        "</div>",
        '<div class="hero-photo">',
        f'<img class="hero-cutout" src="{esc(cut["src600"])}" '
        f'srcset="{esc(cut["src600"])} 600w, {esc(cut["src900"])} 900w" '
        f'sizes="(max-width: 640px) 258px, (max-width: 900px) 301px, 372px" '
        f'width="{cut["width"]}" height="{cut["height"]}" alt="{esc(cut["alt"])}" '
        'fetchpriority="high" decoding="async">',
        f'<span class="hero-bubble hb-black">{esc(s1)}</span>',
        f'<span class="hero-bubble hb-blue">{esc(s2)}</span>',
        "</div>",
        "</div>",
        "</header>",
    ])


def og_url(art: dict, key: str) -> str:
    return f"{SITE}{art['asset_base']}og/og-{key}.jpg?v={art['version']}"


def og_image_obj(art: dict, key: str, title: str) -> dict:
    return {
        "@type": "ImageObject",
        "url": og_url(art, key).split("?", 1)[0],
        "width": 1200,
        "height": 630,
        "caption": title,
    }


def page_shell(
    *,
    title: str,
    description: str,
    canonical: str,
    css: str,
    header: str,
    footer: str,
    schema_blocks: list[str],
    body: str,
    extra_head: str = "",
    body_class: str = "series-page",
    og_image: str = "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
    og_extra: str = "",
) -> str:
    schemas = "\n".join(
        f'<script type="application/ld+json">\n{block}\n</script>' for block in schema_blocks
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<!-- Meta Pixel disabled 2026-06-10: no BAA with Meta — health-condition pages must not send PageView there.
     GTM, GA4, and Google Ads stay off this health-condition page (no BAA). -->
<script>
window.fbq = function () {{}};
window.fbq.queue = [];
window.fbq.loaded = true;
window.fbq.version = '2.0';
window._fbq = window.fbq;
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<link rel="cite-as" href="{esc(canonical)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_image)}">{og_extra}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800&amp;family=DM+Serif+Display:ital@0;1&amp;display=swap">
{extra_head}
{schemas}
<style>
{css}
.npc-clinician-byline {{
  margin: 28px 0;
  padding: 14px 18px;
  border: 1px solid #dbe5f5;
  border-radius: 16px;
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
  font-size: 0.92rem;
  color: #25364f;
}}
.npc-clinician-byline .npc-byline-badge {{
  display: inline-flex; margin-bottom: 8px; padding: 4px 10px; border-radius: 999px;
  background: #e8f1ff; color: #1d4ed8; font-size: 0.68rem; font-weight: 700;
  letter-spacing: 0.05em; text-transform: uppercase;
}}
.npc-clinician-byline a {{ color: #1d4ed8; font-weight: 600; }}
</style>
</head>
<body class="{body_class}">
<a class="skip-link" href="#main">Skip to content</a>
{header}
{body}
{footer}
</body>
</html>
"""


def chris_card(series: dict) -> str:
    return f"""<aside class="chris-card">
  <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" width="88" height="88" alt="Chris Woods, Nurse Practitioner">
  <div>
    <strong>Chris Woods, MSN, APRN, FNP-C, AGACNP-BC</strong>
    <span>I read the texts myself. {esc(series["license_line"])}. Real photo. Real person.</span>
  </div>
</aside>"""


def cta_band(series: dict, href: str, heading: str, body: str) -> str:
    return f"""<section class="cta-band">
  <h2>{esc(heading)}</h2>
  <p>{esc(body)}</p>
  <a class="btn" href="{href}">Text {esc(series["sms"]["display"])}</a>
</section>"""


def build_explainer(series: dict, content: dict, css: str, header: str, footer: str, stop: dict, index: int, art: dict) -> str:
    key = "hub" if stop["kind"] == "hub" else stop["slug"]
    page = content[key]
    page_art = art["pages"][key]
    cta = sms_href(series["sms"]["number"], series["sms"]["prefill"])
    canonical = f"{SITE}{stop['path']}"
    crumbs = [
        ("Home", f"{SITE}/"),
        ("Learn", f"{SITE}/learn/"),
        (series["name"], f"{SITE}{series['hub']['path']}"),
    ]
    if stop["kind"] != "hub":
        crumbs.append((stop["title"], canonical))

    total = len(series["stops"])
    sticky_label = f"Stop {stop['episode']} of {total} · {stop['nav_label']}"
    body_parts = [
        sticky_html(cta, sticky_label),
        '<main id="main">',
        hero_html(page, stop, art, page_art, series),
        '<article class="series-wrap">',
        chris_card(series) if stop["kind"] == "hub" else "",
        bubbles_html(page.get("bubbles", [])),
        stats_html(page.get("stats", [])),
        sections_html(page.get("sections", []), page_art.get("figures", []), art),
        roadmap_html(series, stop["path"], dotted=True),
        eeat_html(series),
        faqs_html(page.get("faqs", [])),
        sources_html(page.get("sources", [])),
        prev_next_html(series, index),
        cta_band(
            series,
            cta,
            series["cta_band"]["heading"],
            series["cta_band"]["body"],
        ),
        f'<p class="prose"><a href="{SITE}{series["one_pager"]["path"]}">$59 text visit one-pager</a></p>',
        "</article></main>",
    ]

    return page_shell(
        title=page["meta_title"],
        description=page["meta_description"],
        canonical=canonical,
        css=css,
        header=header,
        footer=footer,
        schema_blocks=[
            medical_schema(
                page["h1"], canonical, page["meta_description"], series["reviewed"],
                image=og_image_obj(art, key, page["h1"]),
            ),
            faq_schema(page["faqs"]),
            breadcrumb_schema(crumbs),
            person_schema(),
        ],
        body="\n".join(part for part in body_parts if part),
        body_class="series-page series-hub" if stop["kind"] == "hub" else "series-page series-stop",
        og_image=og_url(art, key),
        og_extra=(
            '\n<meta property="og:image:width" content="1200">'
            '\n<meta property="og:image:height" content="630">'
            f'\n<meta property="og:image:alt" content="{esc(page["h1"])}: {esc(series["og_alt_suffix"])}">'
            f'\n<meta name="twitter:image" content="{esc(og_url(art, key))}">'
        ),
    )


def build_offer(series: dict, content: dict, css: str, header: str, footer: str, art: dict) -> str:
    page = content["one_pager"]
    cta = sms_href(series["sms"]["number"], series["sms"]["prefill"])
    canonical = f"{SITE}{series['one_pager']['path']}"
    cards = []
    for card in page["plain_cards"]:
        cards.append(
            f'<a class="plain-card" href="{SITE}{card["href"]}">'
            f'<span>Explained plainly · {esc(card["kicker"])}</span>'
            f'<strong>{esc(card["title"])}</strong>'
            f'<p>{esc(card["text"])}</p></a>'
        )
    body = f"""
{sticky_html(cta, page["sticky"])}
<main id="main">
<article class="series-wrap">
  <header class="hero offer-hero">
    <div class="hero-kicker"><span class="dot"></span> $59 text visit</div>
    <h1>{esc(page["h1"])}</h1>
    <p class="lede">{esc(page["lede"])}</p>
    <div class="offer-price">$59 flat · no charge if text care is not safe</div>
  </header>
  {chris_card(series)}
  {bubbles_html(page["bubbles"])}
  <div class="accent-block">
    <h2>{esc(page["accent_block"]["h2"])}</h2>
    <p>{esc(page["accent_block"]["p"])}</p>
  </div>
  {sections_html(page.get("sections", []))}
  <div class="split">
    <div class="yes">
      <h3>{esc(page["fits"]["yes_h"])}</h3>
      <ul>
        {"".join(f"<li>{esc(x)}</li>" for x in page["fits"]["yes"])}
      </ul>
    </div>
    <div class="no">
      <h3>{esc(page["fits"]["no_h"])}</h3>
      <ul>
        {"".join(f"<li>{esc(x)}</li>" for x in page["fits"]["no"])}
      </ul>
    </div>
  </div>
  <section class="prose">
    <h2>Explained plainly</h2>
    <p>If you want the long story before you text, walk the series. Start at the hub. The cards below skip to the useful stops.</p>
  </section>
  <div class="plain-cards">{''.join(cards)}</div>
  {eeat_html(series)}
  {faqs_html(page["faqs"])}
  {cta_band(series, cta, "Text Chris", page["cta_body"])}
  <p class="prose"><a href="{SITE}{series['hub']['path']}">Read the full {esc(series["name"])} series</a></p>
</article>
</main>
"""
    crumbs = [
        ("Home", f"{SITE}/"),
        (series["one_pager"]["title"], canonical),
    ]
    return page_shell(
        title=page["meta_title"],
        description=page["meta_description"],
        canonical=canonical,
        css=css,
        header=header,
        footer=footer,
        schema_blocks=[
            medical_schema(page["h1"], canonical, page["meta_description"], series["reviewed"], image=og_image_obj(art, "offer", page["h1"])),
            faq_schema(page["faqs"]),
            breadcrumb_schema(crumbs),
            person_schema(),
        ],
        body=body,
        extra_head=f'<meta name="theme-color" content="{series["accent"]["hex"]}">',
        og_image=og_url(art, "offer"),
        og_extra=(
            '\n<meta property="og:image:width" content="1200">'
            '\n<meta property="og:image:height" content="630">'
            f'\n<meta property="og:image:alt" content="{esc(page["h1"])}: {esc(series["og_alt_suffix"])}">'
            f'\n<meta name="twitter:image" content="{esc(og_url(art, "offer"))}">'
        ),
        body_class="series-page series-offer",
    )


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


def check_footer(footer: str) -> None:
    """The series embeds html/shared/footer-snippet.html verbatim. Guard the
    licensing line so a stale snippet can't bring the 11-state footer back."""
    if STALE_FOOTER_LICENSE_LINE in footer or CURRENT_FOOTER_LICENSE_LINE not in footer:
        raise SystemExit(
            "html/shared/footer-snippet.html does not carry the current 14-state "
            "licensing line; fix the shared footer before rebuilding the series."
        )


def main() -> None:
    raise SystemExit(
        "Retired 2026-11-24: the condition series now builds on the gold UTI look. "
        "Run scripts/build-condition-series-gold.py <series-id>. This file stays as a helper module."
    )


def _legacy_main() -> None:
    global OFFER_DIR, GHOST_ACCENT
    series = load_json(SERIES_DIR / "series.json")
    OFFER_DIR = ROOT / "landing-pages" / series["one_pager"]["path"].strip("/")
    GHOST_ACCENT = series["accent"]["hex"]
    content = load_json(SERIES_DIR / "content.json")
    css = (SERIES_DIR / "_shared" / "series.css").read_text(encoding="utf-8")
    art_css = (SERIES_DIR / "_shared" / "art.css").read_text(encoding="utf-8")
    art = load_json(SERIES_DIR / "art.json")
    header = (ROOT / "html" / "shared" / "header-snippet.html").read_text(encoding="utf-8")
    footer = (ROOT / "html" / "shared" / "footer-snippet.html").read_text(encoding="utf-8")
    check_footer(footer)

    for index, stop in enumerate(series["stops"]):
        html_text = build_explainer(series, content, css + "\n" + art_css, header, footer, stop, index, art)
        if stop["slug"]:
            out = SERIES_DIR / stop["slug"] / "index.html"
        else:
            out = SERIES_DIR / "index.html"
        write(out, html_text)

    write(OFFER_DIR / "index.html", build_offer(series, content, css, header, footer, art))


if __name__ == "__main__":
    main()
