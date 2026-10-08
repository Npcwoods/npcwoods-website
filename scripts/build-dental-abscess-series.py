#!/usr/bin/env python3
"""Build the dental-abscess SEO mini-series and PMax offer one-pager.

Reads:
  landing-pages/learn/dental-abscess/series.json
  landing-pages/learn/dental-abscess/content.json
  landing-pages/learn/dental-abscess/_shared/series.css
  landing-pages/learn/dental-abscess/_shared/art.css   (explainer pages only)
  landing-pages/learn/dental-abscess/art.json          (hero art + body figures)
  html/shared/header-snippet.html
  html/shared/footer-snippet.html

Writes HTML under landing-pages/learn/dental-abscess/ and
landing-pages/dental-abscess-treatment/. Never deploy. Kitchen only.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SERIES_DIR = ROOT / "landing-pages" / "learn" / "dental-abscess"
OFFER_DIR = ROOT / "landing-pages" / "dental-abscess-treatment"
SITE = "https://npcwoods.com"
# The pre-WA/FL footer licensing line. If the shared footer snippet ever regresses
# to it, refuse to build rather than re-plate an 11-state footer onto the series.
STALE_FOOTER_LICENSE_LINE = "Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT<br>"
CURRENT_FOOTER_LICENSE_LINE = (
    "Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT, WA, plus Florida by "
    "telehealth registration (TPAN3355). 13 states served.<br>"
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
    "name": "MSN, APRN, FNP-C"
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
      <a href="https://npcwoods.com/about/" rel="author">Chris Woods, MSN, APRN, FNP-C</a>
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



TOOTH_PATH = (
    "M20 60 C20 25 40 8 60 14 C75 18 85 28 100 22 C115 16 125 10 140 14 "
    "C165 20 180 35 180 60 C180 95 172 120 165 140 C160 190 158 250 150 320 "
    "C148 338 129 338 127 322 C122 270 115 222 100 202 C85 222 78 270 73 322 "
    "C71 338 52 338 50 320 C42 250 40 190 35 140 C28 120 20 95 20 60 Z"
)
PULP_PATH = (
    "M70 100 C69 84 76 76 86 84 C93 90 107 90 114 84 C124 76 131 84 130 100 "
    "C130 126 128 150 126 166 L74 166 C72 150 70 126 70 100 Z "
    "M74 166 C70 205 66 262 61.5 326 M126 166 C130 205 134 262 138.5 326"
)
GHOST_BLUE = "#7cc4ff"
GHOST_BLUE2 = "#2997ff"
GHOST_RED = "#B42318"


def _gs(color: str, opacity: float, width: float, dash: str = "") -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'fill="none" stroke="{color}" stroke-opacity="{opacity}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"{d}'
    )


GHOST_EXTRAS = {
    "hub": (
        f'<path d="M-140 136 Q-60 112 20 128 M180 128 Q260 112 340 136" {_gs(GHOST_BLUE, .3, 4)}/>'
        f'<circle cx="61.5" cy="344" r="26" {_gs(GHOST_RED, .42, 4)}/>'
    ),
    "how-it-starts": (
        f'<path d="M118 16 L112 40 L120 58 L110 80 L116 98" {_gs(GHOST_RED, .42, 4)}/>'
        + "".join(
            f'<circle cx="{x}" cy="{y}" r="4.5" fill="{GHOST_BLUE2}" fill-opacity=".45"/>'
            for x, y in ((84, 30), (88, 52), (83, 72), (80, 120), (72, 170), (68, 230), (64, 290))
        )
    ),
    "what-it-feels-like": "".join(
        f'<path d="M{100 - r} 40 A{r} {r} 0 0 1 {100 + r} 40" {_gs(GHOST_RED, o, 4)}/>'
        for r, o in ((60, .45), (80, .3), (100, .18))
    ),
    "tooth-vs-gum": (
        f'<path d="M-140 136 Q-60 112 20 128 M180 128 Q260 112 340 136" {_gs(GHOST_BLUE, .3, 4)}/>'
        f'<circle cx="61.5" cy="344" r="24" {_gs(GHOST_RED, .42, 4)}/>'
        f'<ellipse cx="190" cy="178" rx="18" ry="30" {_gs(GHOST_BLUE, .36, 4)}/>'
    ),
    "lookalikes": (
        f'<circle cx="290" cy="70" r="22" {_gs(GHOST_RED, .5, 4)}/>'
        f'<ellipse cx="350" cy="80" rx="20" ry="34" {_gs(GHOST_BLUE, .34, 4)}/>'
        f'<path d="M300 92 C300 140 300 170 280 190 L200 196" {_gs(GHOST_BLUE, .35, 4)}/>'
        f'<path d="M-120 -10 C-120 -60 -30 -66 -10 -30 C10 -66 100 -60 100 -10" {_gs(GHOST_BLUE2, .3, 4)}/>'
    ),
    "red-flags": (
        f'<path d="M300 10 L392 176 L208 176 Z" {_gs(GHOST_RED, .42, 5)}/>'
        f'<path d="M300 64 V124" {_gs(GHOST_RED, .42, 6)}/>'
        f'<circle cx="300" cy="150" r="5" fill="{GHOST_RED}" fill-opacity=".42"/>'
    ),
    "what-care-looks-like": (
        f'<path d="M240 30 C320 70 210 150 290 200 C350 236 270 300 320 350" {_gs(GHOST_BLUE, .4, 4, "2 12")}/>'
        + "".join(
            f'<circle cx="{x}" cy="{y}" r="12" {_gs(c, .5, 4)}/>'
            for x, y, c in ((240, 30, GHOST_RED), (262, 118, GHOST_BLUE), (290, 200, GHOST_BLUE), (320, 350, GHOST_BLUE))
        )
    ),
    "dentist-vs-text": (
        f'<path d="M250 20 H370 Q400 20 400 50 V90 Q400 120 370 120 H290 L262 144 L268 120 H250 '
        f'Q220 120 220 90 V50 Q220 20 250 20 Z" {_gs(GHOST_BLUE2, .34, 4)}/>'
        f'<path d="M255 70 H365" {_gs(GHOST_BLUE, .35, 4, "2 12")}/>'
    ),
    "why-it-comes-back": (
        f'<path d="M100 -20 A220 220 0 1 1 -110 230" {_gs(GHOST_RED, .4, 4, "2 12")}/>'
        f'<path d="M-130 212 L-110 232 L-88 214" {_gs(GHOST_RED, .5, 4)}/>'
    ),
    "myths": (
        f'<path d="M250 40 L298 88 M298 40 L250 88" {_gs(GHOST_RED, .42, 5)}/>'
        f'<path d="M248 176 L270 198 L310 150" {_gs(GHOST_BLUE, .4, 5)}/>'
    ),
}


def ghost_svg(variant: str) -> str:
    """Topic ghost graphic behind the hero headline: a big tooth outline plus
    one stop motif. Decorative, no text, no numbers."""
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
        '<g class="ghost-tooth" transform="translate(500 118) scale(1.4)">'
        f'<path d="{TOOTH_PATH}" {_gs(GHOST_BLUE, .26, 5)}/>'
        f'<path d="{PULP_PATH}" {_gs(GHOST_BLUE2, .24, 3, "3 9")}/>'
        f"{GHOST_EXTRAS.get(variant, '')}"
        "</g></svg>"
    )


def hero_html(page: dict, stop: dict, art: dict, page_art: dict) -> str:
    cut = art["cutout"]
    s1, s2 = page_art["stickers"]
    return "\n".join([
        '<header class="hero hero-art">',
        ghost_svg(page_art["ghost"]),
        '<div class="hero-inner">',
        '<div class="hero-copy">',
        f'<div class="hero-kicker"><span class="dot"></span> Dental abscess series · Stop {stop["episode"]}</div>',
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
    <strong>Chris Woods, MSN, APRN, FNP-C</strong>
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
        ("Dental Abscess Explained", f"{SITE}/learn/dental-abscess/"),
    ]
    if stop["kind"] != "hub":
        crumbs.append((stop["title"], canonical))

    total = len(series["stops"])
    sticky_label = f"Stop {stop['episode']} of {total} · {stop['nav_label']}"
    body_parts = [
        sticky_html(cta, sticky_label),
        '<main id="main">',
        hero_html(page, stop, art, page_art),
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
            "If you fit a text visit, start here",
            "Soft ask: text me the tooth, the swelling, and whether you can swallow. I will tell you if this is me, a dentist, or the ER. A consult does not guarantee a prescription.",
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
            f'\n<meta property="og:image:alt" content="{esc(page["h1"])}: Chris Woods, NP, with a tooth diagram">'
            f'\n<meta name="twitter:image" content="{esc(og_url(art, key))}">'
        ),
    )


def build_offer(series: dict, content: dict, css: str, header: str, footer: str) -> str:
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
{sticky_html(cta, "Visit · $59 text · Dental abscess")}
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
    <h2>I will not promise a script</h2>
    <p>A consult does not guarantee a prescription. Many abscesses need a dentist to open the tooth or drain the pocket. Some need the ER. If a helper medicine fits, I may send it to your pharmacy as a bridge. The dentist still fixes the house.</p>
  </div>
  <div class="split">
    <div class="yes">
      <h3>Who often fits a text</h3>
      <ul>
        <li>Adult, swallowing and breathing fine</li>
        <li>Swelling over one tooth or gum spot</li>
        <li>Physically in a state I can treat</li>
        <li>You know the dentist is still required</li>
      </ul>
    </div>
    <div class="no">
      <h3>Who needs another door</h3>
      <ul>
        <li>Trouble breathing or swallowing spit</li>
        <li>Floor of the mouth rising, eye closing</li>
        <li>A tooth that needs to be opened or pulled today</li>
        <li>A child under 2</li>
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
  {cta_band(series, cta, "Text Chris", "Soft ask. Tell me what the tooth is doing. I will tell you if I am the right door.")}
  <p class="prose"><a href="{SITE}/learn/dental-abscess/">Read the full Dental Abscess Explained series</a></p>
</article>
</main>
"""
    crumbs = [
        ("Home", f"{SITE}/"),
        ("Dental abscess treatment", canonical),
    ]
    return page_shell(
        title=page["meta_title"],
        description=page["meta_description"],
        canonical=canonical,
        css=css,
        header=header,
        footer=footer,
        schema_blocks=[
            medical_schema(page["h1"], canonical, page["meta_description"], series["reviewed"]),
            faq_schema(page["faqs"]),
            breadcrumb_schema(crumbs),
            person_schema(),
        ],
        body=body,
        extra_head='<meta name="theme-color" content="#B42318">',
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
            "html/shared/footer-snippet.html does not carry the current 13-state "
            "licensing line; fix the shared footer before rebuilding the series."
        )


def main() -> None:
    series = load_json(SERIES_DIR / "series.json")
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

    write(OFFER_DIR / "index.html", build_offer(series, content, css, header, footer))


if __name__ == "__main__":
    main()
