#!/usr/bin/env python3
"""Build the dental-abscess SEO mini-series and PMax offer one-pager.

Reads:
  landing-pages/learn/dental-abscess/series.json
  landing-pages/learn/dental-abscess/content.json
  landing-pages/learn/dental-abscess/_shared/series.css
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


def medical_schema(name: str, url: str, description: str, reviewed: str) -> str:
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "MedicalWebPage",
            "name": name,
            "url": url,
            "description": description,
            "lastReviewed": reviewed,
            "author": {"@id": "https://npcwoods.com/#chris-woods"},
            "reviewedBy": {"@id": "https://npcwoods.com/#chris-woods"},
            "publisher": {"@id": "https://npcwoods.com/#medical-business"},
        },
        indent=2,
        ensure_ascii=False,
    )


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


def sections_html(sections: list[dict]) -> str:
    out: list[str] = []
    for block in sections:
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
<meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp">
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


def build_explainer(series: dict, content: dict, css: str, header: str, footer: str, stop: dict, index: int) -> str:
    key = "hub" if stop["kind"] == "hub" else stop["slug"]
    page = content[key]
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
        '<article class="series-wrap">',
        '<header class="hero">',
        f'<div class="hero-kicker"><span class="dot"></span> Dental abscess series · Stop {stop["episode"]}</div>',
        f"<h1>{esc(page['h1'])}</h1>",
        f'<p class="lede">{esc(page["lede"])}</p>',
        "</header>",
        chris_card(series) if stop["kind"] == "hub" else "",
        bubbles_html(page.get("bubbles", [])),
        stats_html(page.get("stats", [])),
        sections_html(page.get("sections", [])),
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
            medical_schema(page["h1"], canonical, page["meta_description"], series["reviewed"]),
            faq_schema(page["faqs"]),
            breadcrumb_schema(crumbs),
            person_schema(),
        ],
        body="\n".join(part for part in body_parts if part),
        body_class="series-page series-hub" if stop["kind"] == "hub" else "series-page series-stop",
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


def main() -> None:
    series = load_json(SERIES_DIR / "series.json")
    content = load_json(SERIES_DIR / "content.json")
    css = (SERIES_DIR / "_shared" / "series.css").read_text(encoding="utf-8")
    header = (ROOT / "html" / "shared" / "header-snippet.html").read_text(encoding="utf-8")
    footer = (ROOT / "html" / "shared" / "footer-snippet.html").read_text(encoding="utf-8")

    for index, stop in enumerate(series["stops"]):
        html_text = build_explainer(series, content, css, header, footer, stop, index)
        if stop["slug"]:
            out = SERIES_DIR / stop["slug"] / "index.html"
        else:
            out = SERIES_DIR / "index.html"
        write(out, html_text)

    write(OFFER_DIR / "index.html", build_offer(series, content, css, header, footer))


if __name__ == "__main__":
    main()
