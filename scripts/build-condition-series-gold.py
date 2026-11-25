#!/usr/bin/env python3
"""Build a condition mini-series (hub + stops) and its $59 offer page on the
GOLD look: the live UTI lander (landing-pages/uti-treatment/index.html) and
the UTI Explained series (landing-pages/learn/uti/). Chris 2026-11-24: "do
these match our UTI lander as the gold standard?" -> they do now.

The CSS is read from the gold pages at build time, so there is one look, not
a copy that drifts. Copy comes from the series folder:
  series.json, content.json, art.json, gold.json
Shared header/footer: html/shared/header-snippet.html, footer-snippet.html

  python3 scripts/build-condition-series-gold.py screening-labs
  python3 scripts/build-condition-series-gold.py mastitis

Writes HTML only. Never deploys. Kitchen only.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("ccs", ROOT / "scripts" / "build-condition-series.py")
ccs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ccs)  # helpers only (main() is guarded)

esc, sms_href, load_json = ccs.esc, ccs.sms_href, ccs.load_json
SITE = ccs.SITE
GOLD_LANDER = ROOT / "landing-pages" / "uti-treatment" / "index.html"
GOLD_HUB = ROOT / "landing-pages" / "learn" / "uti" / "index.html"
HEADSHOT = "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp"
CRED = "MSN, APRN, FNP-C, AGACNP-BC"
LICENSE = "14 states, including Florida by telehealth registration (TPAN3355)"
LOCKED_911 = ("Text-based telehealth is not for emergencies. If you have chest pain, trouble "
              "breathing, or other emergency symptoms, call 911.")
CHAT_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true" '
             'focusable="false"><path d="M4 5h16v11H8l-4 4z" stroke-linejoin="round"/></svg>')
HIPAA_OFF = """<!-- Meta Pixel disabled 2026-06-10: no BAA with Meta — health-condition pages must not send PageView there.
     GTM, GA4, and Google Ads stay off this health-condition page (no BAA). -->
<script>
window.fbq = function () {};
window.fbq.queue = [];
window.fbq.loaded = true;
window.fbq.version = '2.0';
window._fbq = window.fbq;
</script>"""


# ---------------------------------------------------------------- gold reads
def _head_styles(path: Path) -> str:
    head = path.read_text(encoding="utf-8").split("</head>", 1)[0]
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", head, re.S)
    if not blocks:
        raise SystemExit(f"gold page {path} has no <style> block")
    return "\n".join(blocks)


def _gold_chunk(start_marker: str, *, end: str = "</section>") -> str:
    text = GOLD_LANDER.read_text(encoding="utf-8")
    i = text.find(start_marker)
    if i < 0:
        raise SystemExit(f"gold lander is missing {start_marker!r}")
    s = text.rfind("<section", 0, i + len(start_marker))
    e = text.find(end, i)
    return text[s:e + len(end)]


RCARD_RE = re.compile(r'<div class="rcard">.*?<span class="rcard-source">[^<]*</span></div></div>', re.S)
# Chris 2026-11-24 (t858u): "Trim it to general reviews please." Drop any card that names a
# condition, symptom, body part, or medicine. Kept cards are copied from the gold lander verbatim.
CONDITION_RE = re.compile(
    r"\b(uti|utis|bladder|urinary|kidney|cough\w*|cold|flu|fever|sinus|strep|throat|ear|infection\w*|rash|"
    r"yeast|tooth|teeth|dental|pink ?eye|stye|allerg\w*|asthma|weight|glp|antibiotic\w*|\w+cillin|"
    r"macrobid|bactrim|keflex|ozempic|wegovy|mounjaro|semaglutide|tirzepatide)\b", re.I)


def gold_reviews() -> str:
    """The gold review carousel, trimmed to general reviews (no condition/medicine talk).
    Each kept card is byte-for-byte from the gold lander; the set is doubled for the loop."""
    m = re.search(r'<!-- REVIEWS -->\s*(<section class="reviews">.*?</section>)', GOLD_LANDER.read_text(encoding="utf-8"), re.S)
    if not m:
        raise SystemExit("gold lander is missing the reviews section")
    section = m.group(1)
    kept: list[str] = []
    quotes: list[str] = []
    for card in RCARD_RE.findall(section):
        q = re.search(r'<p class="rcard-text">(.*?)</p>', card, re.S)
        quote = (q.group(1) if q else re.sub(r"<[^>]+>", " ", card)).strip().strip('"').rstrip('.')
        # skip the loop's repeats, including the gold loop's shortened repeat of a longer review
        if CONDITION_RE.search(quote) or any(quote in old for old in quotes):
            continue
        kept.append(card)
        quotes.append(quote)
    if len(kept) < 3:
        raise SystemExit(f"only {len(kept)} general reviews left in the gold carousel")
    head = section[: section.index('<div class="scroll-track">') + len('<div class="scroll-track">')]
    track = "".join(f"\n      {c}" for c in kept + kept)
    return f"{head}{track}\n    </div>\n  </div>\n</section>"


def gold_atf_style() -> str:
    m = re.search(r"<style>\s*\.npc-atf-answer.*?</style>", GOLD_LANDER.read_text(encoding="utf-8"), re.S)
    if not m:
        raise SystemExit("gold lander is missing the answer-box style")
    return m.group(0)


def gold_states() -> str:
    return _gold_chunk('<h2 class="section-title">Licensed in 14 states')


def gold_cross(short: str, own_path: str) -> str:
    chunk = _gold_chunk("Other conditions we treat")
    chunk = re.sub(r"UTIs aren't the only thing we handle via text\.", f"Not just {esc(short.lower())}. Here is what else we handle by text.", chunk)
    chunk = chunk.replace('<div class="cross-wrap">',
                          '<div class="cross-wrap">\n      <a href="https://npcwoods.com/uti-treatment/" class="cross-link">UTI</a>', 1)
    return chunk.replace(f'href="https://npcwoods.com{own_path}"', 'href="#top"')


# ---------------------------------------------------------------- shared bits
def h1_split(parts: list[str]) -> str:
    a, b = parts
    return f'<span class="gh-grad">{esc(a)}</span> <span class="gh-pop">{esc(b)}</span>'


def byline(series: dict) -> str:
    return (
        '<div class="ex-byline">'
        f'<img src="{HEADSHOT}" width="52" height="52" alt="" loading="lazy" decoding="async">'
        f'<div><strong>By Chris Woods, {CRED}</strong><br>Board-certified nurse practitioner · '
        f'Reviewed <time datetime="{series["reviewed"]}">{esc(series["reviewed_display"])}</time></div></div>'
    )


def crumb(items: list[tuple[str, str | None]]) -> str:
    lis = "".join(
        f'<li><a href="{href}">{esc(name)}</a></li>' if href else f'<li aria-current="page">{esc(name)}</li>'
        for name, href in items
    )
    return f'<nav class="ex-crumb" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'


def tldr(items: list[str]) -> str:
    return ('<div class="ex-tldr"><h2>The short <em>version</em></h2><ul>'
            + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul></div>")


def ghost(series: dict, variant: str) -> str:
    ccs.GHOST_ACCENT = series["accent"]["hex"]
    return ccs.ghost_svg(variant, series["ghost_base"]).replace('class="hero-ghost"', 'class="gh-ghost"', 1)


def gh_header(series: dict, gold: dict, art: dict, page_art: dict, *, pill: str, h1: list[str], sub: str,
              cta: str, ghost_href: str, ghost_label: str) -> str:
    cut = art["cutout"]
    s1, s2 = page_art["stickers"]
    return f"""<header class="gh" aria-labelledby="gh-title">
{ghost(series, page_art["ghost"])}
    <div class="gh-wrap">
      <div class="gh-copy">
        <span class="gh-pill"><i aria-hidden="true"></i>{esc(pill)}</span>
        <h1 id="gh-title">{h1_split(h1)}</h1>
        <p class="gh-sub">{esc(sub)}</p>
        <div class="gh-ctas">
          <a class="gh-btn" href="{cta}">{CHAT_ICON}Text Chris · $59 visit</a>
          <a class="gh-ghostbtn" href="{ghost_href}">{esc(ghost_label)}</a>
        </div>
        <p class="gh-fine">{esc(gold["offer"]["fine"])}</p>
      </div>
      <div class="gh-photo">
        <img src="{esc(cut["src600"])}" srcset="{esc(cut["src600"])} 600w, {esc(cut["src900"])} 900w" sizes="(max-width: 640px) 272px, (max-width: 900px) 315px, 415px" width="{cut["width"]}" height="{cut["height"]}" alt="{esc(cut["alt"])}" fetchpriority="high" decoding="async">
        <span class="gh-sticker gh-s1">{esc(s1)}</span>
        <span class="gh-sticker gh-s2">{esc(s2)}</span>
      </div>
    </div>
  </header>"""


def fig_html(art: dict, fig: dict) -> str:
    src = f"{art['asset_base']}{fig['src']}?v={art['version']}"
    return (f'<figure class="ex-fig ex-card-fig"><img src="{esc(src)}" width="{fig["width"]}" height="{fig["height"]}" '
            f'alt="{esc(fig["alt"])}" loading="lazy" decoding="async"><figcaption>{esc(fig["caption"])}</figcaption></figure>')


def ex_sections(sections: list[dict], figures: list[dict], art: dict, *, light: tuple[str, str]) -> str:
    """Map content blocks onto the gold ex-sec bands. light = (class_a, class_b)
    for the alternating plain bands (ex-cream/ex-white on stops, hub-story on the hub)."""
    out, n, alt = [], 0, 0
    pre = [f for f in figures if f.get("after_section", 0) < 0]
    for idx, block in enumerate(sections):
        figs = [f for f in figures if f.get("after_section", 0) == idx] + (pre if idx == 0 else [])
        kind = block.get("type")
        sid = f"s{idx + 1}"
        if kind == "callout" and block.get("kind") == "safety":
            copy = (f'<span class="ex-kick">Red flag · call 911</span><h2 id="{sid}-h">{esc(block["title"])}</h2>'
                    f'<div class="ex-vs ex-vs-one"><div class="er"><h3>Go now. Do not text first.</h3><p>{esc(block["body"])}</p></div></div>')
            klass = "ex-sec ex-night"
        elif kind == "callout":
            copy = f'<span class="ex-kick">Heads up</span><h2 id="{sid}-h">{esc(block["title"])}</h2><p>{esc(block["body"])}</p>'
            klass = "ex-sec ex-orange"
        else:
            n += 1
            inner = ""
            if kind == "prose":
                inner = "".join(f"<p>{esc(p)}</p>" for p in block.get("body", []))
            elif kind == "list":
                checks = re.search(r"helps|good fit|feeding easier|most adults", block.get("heading", ""), re.I)
                inner = f'<ol class="ex-steps{" checks" if checks else ""}">' + "".join(f"<li>{esc(x)}</li>" for x in block.get("items", [])) + "</ol>"
            copy = f'<span class="ex-kick">Part {n}</span><h2 id="{sid}-h">{esc(block.get("heading", ""))}</h2>{inner}'
            klass = light[alt % 2]
            alt += 1
        if figs:
            body = (f'<div class="ex-split"><div class="ex-copy">{copy}</div>'
                    + "".join(fig_html(art, f) for f in figs) + "</div>")
        else:
            body = f'<div class="ex-copy">{copy}</div>'
        out.append(f'<section class="{klass}" id="{sid}" aria-labelledby="{sid}-h"><div class="ex-in">{body}</div></section>')
    return "\n".join(out)


def recap_from_bubbles(bubbles: list[dict]) -> str:
    if not bubbles:
        return ""
    msgs = "".join(
        (f'<li class="ex-bub you"><span class="who">You text</span><p>{esc(b["text"])}</p></li>' if b.get("who") == "You" else
         f'<li class="ex-bub me"><span class="who">I answer</span><p>{esc(b["text"])}</p></li>')
        for b in bubbles
    )
    return (f'<section class="ex-recap ex-texts" aria-labelledby="recap-title"><div class="ex-in"><span class="ex-kick">In my texts</span>'
            f'<h2 id="recap-title">The kind of text I get.</h2>'
            f'<div class="ex-thread"><div class="ex-thread-top">Text visit with Chris</div><ol class="ex-thread-msgs">{msgs}</ol></div></div></section>')


def faq_details(faqs: list[dict], klass: str, narrow: bool = True) -> str:
    items = "".join(f"<details><summary>{esc(f['q'])}</summary><p>{esc(f['a'])}</p></details>" for f in faqs)
    inner = "ex-in ex-narrow" if narrow else "ex-in"
    return (f'<section class="{klass}" aria-labelledby="faq-title"><div class="{inner}"><span class="ex-kick">Quick questions</span>'
            f'<h2 id="faq-title">You asked. I answered.</h2>{items}</div></section>')


def sources(srcs: list[dict], klass: str, title: str) -> str:
    lis = "".join(f'<li id="src-{i}">{esc(s["label"])} <a href="{esc(s["url"])}" rel="noopener">{esc(s["url"].split("//", 1)[-1].split("/", 1)[0])}</a></li>'
                  for i, s in enumerate(srcs, 1))
    return f'<section class="{klass}" aria-labelledby="src-title"><div class="ex-in"><h2 id="src-title">{esc(title)}</h2><ol>{lis}</ol></div></section>'


def ex_map(series: dict, here: str) -> str:
    lis = []
    for st in series["stops"]:
        if st["path"] == here:
            lis.append(f'<li class="here" aria-current="step"><span class="dot" aria-hidden="true"></span><span class="t">{esc(st["nav_label"])}</span><span class="vh"> (you are here)</span></li>')
        else:
            lis.append(f'<li class="live"><span class="dot" aria-hidden="true"></span><a href="{SITE}{st["path"]}">{esc(st["nav_label"])}</a></li>')
    return (f'<nav class="ex-map" aria-label="{esc(series["name"])} road map"><div class="ex-in">'
            f'<a class="ex-map-hub" href="{SITE}{series["hub"]["path"]}">← Series hub</a>'
            f'<div class="ex-map-scroll" tabindex="0" aria-label="Series stops, scroll sideways"><ol>{"".join(lis)}</ol></div></div></nav>')


def ex_pn(series: dict, gold: dict, index: int) -> str:
    stops = series["stops"]
    def card(st, klass, small):
        d = gold["stops"][st["slug"]]["desc"]
        return f'<a class="{klass}" href="{SITE}{st["path"]}"><small>{small}</small><strong>{esc(st["title"])}</strong><span class="d">{esc(d)}</span></a>'
    prev = card(stops[index - 1], "prev", "← Last stop") if index > 0 else ""
    nxt = card(stops[index + 1], "next", "Next stop →") if index < len(stops) - 1 else (
        f'<a class="next" href="{SITE}{series["one_pager"]["path"]}"><small>Ready? →</small><strong>{esc(series["one_pager"]["title"])}</strong>'
        f'<span class="d">How the $59 text visit works.</span></a>')
    return (f'<nav class="ex-pn" aria-label="Series: previous and next"><div class="ex-in"><div class="ex-pn-grid">{prev}{nxt}</div>'
            f'<a class="hub" href="{SITE}{series["hub"]["path"]}">See the whole road map on the series hub →</a></div></nav>')


def cta_block(klass: str, title: list[str], p: str, cta: str, white_btn: bool = False) -> str:
    style = ' style="background:#fff;color:#0071e3!important"' if white_btn else ""
    return (f'<section class="{klass}" aria-labelledby="cta-title"><div class="ex-in">'
            f'<h2 id="cta-title">{esc(title[0])}<span>{esc(title[1])}</span></h2><p class="ex-big">{esc(p)}</p>'
            f'<a class="gh-btn" href="{cta}"{style}>{CHAT_ICON}Text Chris · $59 visit</a>'
            f'<p class="fine">Educational info, not medical advice. A text visit is not a promise of a prescription. {LOCKED_911} Licensed in {LICENSE}.</p></div></section>')


SERIES_EXTRA_CSS = """
/* condition-series additions on the gold UTI Explained look */
.ex-fig img{display:block;width:100%;height:auto;border-radius:18px;background:#fff}
.ex-vs.ex-vs-one{grid-template-columns:1fr;max-width:640px}
.ex-vs .er p{margin:8px 0 0;color:#fff}
.ex-src li a{word-break:break-word}
.hub-faq summary{padding:12px 0;min-height:44px;box-sizing:border-box}
/* hub sections reuse the explainer bands, so the hub needs the same color tokens */
.hub-main{--ink:#1d1d1f;--body:#3a3a42;--muted:#5f5f68;--blue:#0071e3;--bright:#2997ff;--green:#148a53;--orange:#f5a524;--cream:#F6F3EE;--night:#05060a;--line:rgba(0,0,0,.09)}
/* road map cards: fit the content, no status badges */
.stop-card,a.stop-card{min-height:0}
.stop-card h3:first-child{margin-top:0}
/* by the numbers: matches the UTI lander stats band */
.ex-stats{background:#05060a;color:#c7c7ce;padding:64px 0}
.ex-stats .ex-kick{color:#f5c36a}
.ex-stats h2,.ex-texts h2{color:#fff;font-weight:900;font-size:clamp(32px,4.4vw,52px);line-height:1.05;letter-spacing:-.045em;margin:10px 0 24px}
.ex-stat-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.ex-stat{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:10px;padding:24px 20px;border-radius:20px;background:#10121a;border:1px solid rgba(255,255,255,.1)}
.ex-stat-n{font-size:clamp(36px,5vw,52px);font-weight:900;letter-spacing:-.05em;line-height:1;background:linear-gradient(120deg,#fff,#2997ff);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:#fff}
.ex-stat-l{font-size:16px;line-height:1.4;color:#c7c7ce;max-width:28ch}
/* in my texts: a real text thread, no dead space */
.ex-texts{padding:64px 0}
.ex-thread{max-width:560px;background:#111318;border:1px solid rgba(255,255,255,.1);border-radius:28px;padding:0 0 18px;overflow:hidden}
.ex-thread-top{padding:12px 16px;font-size:13px;font-weight:700;color:#e5e5ea;text-align:center;border-bottom:1px solid rgba(255,255,255,.08);background:rgba(24,24,28,.96)}
.ex-thread-msgs{list-style:none;margin:0;padding:16px 14px 0;display:flex;flex-direction:column;gap:12px}
.ex-bub{max-width:84%;display:flex;flex-direction:column;gap:4px}
.ex-bub .who{font-size:12px;font-weight:700;letter-spacing:.02em;color:#8e8e93;padding:0 6px}
.ex-bub p{margin:0;padding:10px 14px;border-radius:20px;font-size:17px;line-height:1.45}
.ex-bub.you{align-self:flex-end;align-items:flex-end}
.ex-bub.you p{background:#0a84ff;color:#fff;border-bottom-right-radius:6px}
.ex-bub.me{align-self:flex-start}
.ex-bub.me p{background:#2c2c2e;color:#f2f2f7;border-bottom-left-radius:6px}
/* figures: phone-first SVGs, full content width on phones */
.ex-split .ex-fig{width:100%;max-width:460px;justify-self:center}
@media(max-width:640px){
.ex-stats,.ex-texts{padding:52px 0}
.ex-stat-row{grid-template-columns:1fr;gap:12px}
.ex-stat{padding:20px 18px;gap:8px}
.ex-stat-n{font-size:40px}
.ex-thread{border-radius:24px}
.ex-bub{max-width:88%}
.ex-split .ex-fig{max-width:none}
.ex-card-fig{padding:0;background:transparent;box-shadow:none;border-radius:0}
.ex-fig figcaption{padding:0 4px}
}
"""


def head(*, title: str, desc: str, canonical: str, og_img: str, og_alt: str, schemas: list[str], css: str,
         theme: str, og_type: str = "article", fonts: str = "") -> str:
    blocks = "\n".join(f'<script type="application/ld+json">\n{b}\n</script>' for b in schemas)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HIPAA_OFF}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="{theme}">
<link rel="canonical" href="{esc(canonical)}">
<link rel="cite-as" href="{esc(canonical)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="NPCWoods Telemedicine">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_img)}">
<meta property="og:image:secure_url" content="{esc(og_img)}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(og_img)}">
<meta name="twitter:image:alt" content="{esc(og_alt)}">
<link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
{fonts}
{blocks}
<style>
{css}
</style>
</head>"""


# ---------------------------------------------------------------- series pages
def build_series_page(series, content, gold, art, header, footer, stop, index) -> str:
    is_hub = stop["kind"] == "hub"
    key = "hub" if is_hub else stop["slug"]
    page, page_art, g = content[key], art["pages"][key], gold["stops"][stop["slug"]]
    cta = sms_href(series["sms"]["number"], series["sms"]["prefill"])
    canonical = f"{SITE}{stop['path']}"
    crumbs = [("Home", f"{SITE}/"), ("Learn", f"{SITE}/learn/"), (series["name"], f"{SITE}{series['hub']['path']}")]
    if not is_hub:
        crumbs.append((stop["nav_label"], canonical))
    vis_crumbs = [(n, u) for n, u in crumbs[:-1]] + [(crumbs[-1][0], None)]
    pill = f'{gold["pill"]} · ' + ("Plain talk from your NP" if is_hub else stop["nav_label"])
    hdr = gh_header(series, gold, art, page_art, pill=pill, h1=g["h1"], sub=g["sub"], cta=cta,
                    ghost_href="#series-roadmap" if is_hub else "#start",
                    ghost_label="See the road map ↓" if is_hub else "Start reading ↓")
    intro = (f'<div class="ex-in">{crumb(vis_crumbs)}{byline(series)}'
             f'<p class="ex-lede">{esc(page["lede"])}</p>{tldr(g["tldr"])}</div>')
    figures = page_art.get("figures", [])
    if is_hub:
        stats = page.get("stats", [])
        stat_html = ""
        if stats:
            chips = "".join(f'<div class="ex-stat"><div class="ex-stat-n">{esc(s["num"])}</div><div class="ex-stat-l">{esc(s["label"])}</div></div>' for s in stats)
            stat_html = (f'<section class="ex-stats" aria-labelledby="num-title"><div class="ex-in"><span class="ex-kick">By the numbers</span>'
                         f'<h2 id="num-title">Three numbers to know.</h2><div class="ex-stat-row">{chips}</div></div></section>')
        cards = []
        for i, st in enumerate(series["stops"]):
            here = st["path"] == stop["path"]
            cur = ' aria-current="page"' if here else ""
            tag = '<span class="tag">You are here</span>' if here else ""
            cards.append(f'<li class="stop{" here" if here else ""}"><span class="stop-node" aria-hidden="true"></span>'
                         f'<a class="stop-card" href="{SITE}{st["path"]}"{cur}>{tag}'
                         f'<h3>{esc(st["title"])}</h3><p>{esc(gold["stops"][st["slug"]]["desc"])}</p></a></li>')
        op_t, op_p = gold["offer"]["hub_onepager"]
        main = "\n".join([
            '<main class="hub-main" id="main">',
            f'<section class="hub-intro" id="start">{intro}</section>',
            ex_sections(page.get("sections", []), figures, art, light=("ex-sec ex-cream", "ex-sec ex-white")),
            stat_html,
            recap_from_bubbles(page.get("bubbles", [])),
            f'<section class="roadmap" id="series-roadmap" aria-labelledby="roadmap-title"><div class="ex-in">'
            f'<h2 class="section-title" id="roadmap-title">Your {esc(gold["short"].lower())} road map</h2>'
            f'<p class="road-intro">Follow the dotted path. You\'re standing on the first one.</p>'
            f'<ol class="stop-list">{"".join(cards)}</ol></div></section>',
            f'<section class="hub-onepager" aria-labelledby="offer-title"><div class="ex-in"><span class="ex-kick">Need care, not just reading?</span>'
            f'<h2 id="offer-title" style="font-size:clamp(28px,4vw,40px);font-weight:900;letter-spacing:-.04em;margin:0 0 16px;color:#1d1d1f">Ready for a visit?</h2>'
            f'<a class="card" href="{SITE}{series["one_pager"]["path"]}"><strong>{esc(op_t)}</strong><span>{esc(op_p)}</span></a></div></section>',
            faq_details(page.get("faqs", []), "hub-faq", narrow=False),
            sources(page.get("sources", []), "hub-src", "Core sources for this series"),
            cta_block("hub-cta", gold["offer"]["hub_cta"], gold["offer"]["hub_cta_p"], cta, white_btn=True),
            f'<div class="hub-disc"><div class="ex-in"><p>{esc(gold["offer"]["disc"])}</p></div></div>',
            "</main>",
        ])
    else:
        main = "\n".join([
            '<main class="ex" id="main">',
            ex_map(series, stop["path"]),
            f'<section class="ex-intro" id="start">{intro}</section>',
            ex_sections(page.get("sections", []), figures, art, light=("ex-sec ex-cream", "ex-sec ex-white")),
            recap_from_bubbles(page.get("bubbles", [])),
            faq_details(page.get("faqs", []), "ex-faq"),
            sources(page.get("sources", []), "ex-src", "Sources"),
            ex_pn(series, gold, index),
            cta_block("ex-cta", gold["offer"]["stop_cta"], gold["offer"]["stop_cta_p"], cta),
            f'<div class="ex-disc"><div class="ex-in"><p>{esc(gold["offer"]["disc"])}</p></div></div>',
            "</main>",
        ])
    css = _head_styles(GOLD_HUB) + "\n" + SERIES_EXTRA_CSS
    og = ccs.og_url(art, key)
    schemas = [
        ccs.medical_schema(page["h1"], canonical, page["meta_description"], series["reviewed"], image=ccs.og_image_obj(art, key, page["h1"])),
        ccs.faq_schema(page["faqs"]),
        ccs.breadcrumb_schema(crumbs),
        ccs.person_schema(),
    ]
    h = head(title=page["meta_title"], desc=page["meta_description"], canonical=canonical, og_img=og,
             og_alt=f'{page["h1"]}: {series["og_alt_suffix"]}', schemas=schemas, css=css, theme="#05060a",
             fonts='<link rel="preload" href="/assets/fonts/inter-latin-var.woff2" as="font" type="font/woff2" crossorigin>')
    return f"""{h}
<body>
<a class="skip-link" href="#main">Skip to content</a>
{header}
{hdr}
{main}
{footer}
</body>
</html>
"""


# ---------------------------------------------------------------- offer page
OFFER_EXTRA_CSS = """
/* condition-offer additions on the gold UTI lander look */
.symptom-icon.txt{width:auto;min-width:34px;padding:0 7px;font-size:11px;font-weight:800;letter-spacing:.02em;color:var(--blue-bright)}
.drug-card .brand{display:none}
"""


def sms_cta(cta: str, style: str = "") -> str:
    st = f' style="{style}"' if style else ""
    return f"""<a href="{cta}" class="btn-primary npc-sms-cta"{st}>Text Us Now: (480) 639-4722</a>
        <div class="npc-qr-cta" role="group" aria-label="Scan to text NPCWoods">
          <div class="npc-qr-code" data-sms="{cta}" aria-hidden="true"></div>
          <div class="npc-qr-meta">
            <span class="npc-qr-label">Scan to Text Us</span>
            <a class="npc-qr-phone" href="tel:+14806394722">(480) 639-4722</a>
            <span class="npc-qr-sub">$59 flat fee &middot; text to start</span>
          </div>
        </div>"""


TAIL_JS = """<script>
// FAQ accordion
document.querySelectorAll('.faq-q').forEach(q => {
  q.addEventListener('click', () => {
    const item = q.parentElement;
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});
</script>
<!-- QR codes for desktop sms: CTAs -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js" defer></script>
<script>
(function () {
  function buildQRs() {
    if (typeof QRCode === 'undefined') { return setTimeout(buildQRs, 120); }
    document.querySelectorAll('.npc-qr-code').forEach(function (el) {
      if (el.dataset.rendered) { return; }
      var sms = el.getAttribute('data-sms');
      if (!sms) { return; }
      new QRCode(el, { text: sms, width: 118, height: 118, colorDark: '#0a0a0a', colorLight: '#ffffff', correctLevel: QRCode.CorrectLevel.M });
      el.dataset.rendered = '1';
    });
  }
  if (document.readyState !== 'loading') { buildQRs(); }
  else { document.addEventListener('DOMContentLoaded', buildQRs); }
})();
</script>"""


def howto_schema(name: str, steps: list[list[str]]) -> str:
    return json.dumps({
        "@context": "https://schema.org", "@type": "HowTo", "name": name,
        "description": "Three texts with Chris Woods, NP. $59 flat.",
        "step": [{"@type": "HowToStep", "position": i, "name": s[0], "text": re.sub(r"<[^>]+>", "", s[1])}
                 for i, s in enumerate(steps, 1)],
    }, indent=2, ensure_ascii=False)


def build_offer(series, content, gold, art, header, footer) -> str:
    page, o = content["one_pager"], gold["offer"]
    cta = sms_href(series["sms"]["number"], o["sms_body"])
    canonical = f"{SITE}{series['one_pager']['path']}"
    fill = lambda s: s.replace("{sms}", cta)
    chat = "\n".join(f'            <div class="imsg-bubble {w}">{esc(t)}</div>' for w, t in o["chat"])
    stats = "".join(f'<div class="stat"><div class="stat-n">{esc(n)}</div><div class="stat-l">{esc(l)}</div></div>' for n, l in o["stats"])
    vs_rows = "\n".join(
        f'      <div class="vs-cell vs-feature">{f}</div>\n      <div class="vs-cell vs-us"><span class="vs-check">✓</span>{u}</div>\n      <div class="vs-cell vs-them">{t}</div>'
        for f, u, t in o["vs"])
    bento = []
    for i, (t, p) in enumerate(o["how"], 1):
        av = f'\n        <img src="{HEADSHOT}" class="chris-avatar" alt="Chris Woods NP">' if i == 2 else ""
        bento.append(f'      <div class="bento-card">\n        <div class="step-num">{i}</div>{av}\n        <h3>{esc(t)}</h3>\n        <p>{fill(p)}</p>\n      </div>')
    w = o["what"]
    sym = "\n".join(f'      <div class="symptom-card"><div class="symptom-icon txt">{esc(b)}</div><div><strong>{esc(t)}</strong><span>{esc(s)}</span></div></div>'
                    for b, t, s in w["cards"])
    tb = o["table"]
    def cell(c):
        if isinstance(c, list):
            return f'<td class="{c[0]}">{esc(c[1])}</td>'
        return f"<td>{esc(c)}</td>"
    rows = "\n".join("          <tr>" + "".join(cell(c) for c in r) + "</tr>" for r in tb["rows"])
    cv = o["covers"]
    covers = "\n".join(f'      <div class="drug-card">\n        <div class="drug-badge {b}">{esc(k)}</div>\n        <h3>{esc(t)}</h3>\n        <p>{esc(p)}</p>\n      </div>'
                       for b, k, t, p in cv["cards"])
    er = "\n".join(f"        <li>{esc(x)}</li>" for x in o["er"])
    fits = page["fits"]
    fy = "\n".join(f"          <li>{esc(x)}</li>" for x in fits["yes"])
    fn = "\n".join(f"          <li>{esc(x)}</li>" for x in fits["no"])
    ex = o["extra"]
    faqs = "\n".join(f'      <div class="faq-item"><div class="faq-q">{esc(f["q"])}</div><div class="faq-a"><p>{esc(f["a"])}</p></div></div>' for f in page["faqs"])
    explained = "\n".join(
        f'      <a href="{SITE}{st["path"]}" class="explained-card"><strong>{esc(st["title"])}</strong><span>{esc(gold["stops"][st["slug"]]["desc"])}</span></a>'
        for st in series["stops"])
    body = f"""<main id="main">
<section class="hero" id="top">
  <div class="hero-inner hero-split">
    <div class="hero-text">
      <div class="hero-kicker">
        <span class="hero-dot"></span>
        {o["kicker"]}
      </div>
      <h1>{esc(o["h1"])}</h1>
      <p class="hero-sub">{esc(o["sub"])}</p>
      <div class="hero-actions">
        {sms_cta(cta)}
        <a href="#how-it-works" class="btn-ghost">See how it works</a>
      </div>
      <div class="hero-trust">
        <span>🔒 HIPAA-Compliant</span>
        <span>⭐ 5.0 · 80+ Five-Star Google Reviews</span>
        <span>{o["trust3"]}</span>
      </div>
    </div>
    <div class="phone-float" aria-hidden="true">
      <div class="phone-frame">
        <div class="phone-notch"></div>
        <div class="phone-screen">
          <div class="imsg-header">
            <img src="{HEADSHOT}" class="imsg-avatar" alt="">
            <div>
              <div class="imsg-name">Chris @ NPCWoods</div>
              <div class="imsg-status">● Available now</div>
            </div>
          </div>
          <div class="imsg-body">
            <div class="imsg-time">Example text · Today 2:14 PM</div>
{chat}
            <div class="imsg-rx">{esc(o["chat_status"])}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
{gold_atf_style()}
<div class="npc-atf-answer" data-npc-aeo="atf-answer">
  <p>{fill(o["atf"])}</p>
</div>

<!-- STATS BAND -->
<div class="stats-band">
  <div class="stats-inner">
    {stats}
  </div>
</div>

<div class="eeat-byline" style="background:var(--panel-2);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:0 24px 24px;max-width:var(--max);margin-left:auto;margin-right:auto;font-size:13px;line-height:1.5;color:var(--body);">
  <p style="margin:0 0 8px 0;color:#fff;font-weight:600;">Written and clinically reviewed by <strong>Chris Woods, {CRED}</strong>, double board-certified Nurse Practitioner and founder of NPCWoods.</p>
  <p style="margin:0 0 4px 0;">{esc(o["eeat_note"])} <a href="https://npcwoods.com/about/" style="color:var(--blue-bright);text-decoration:underline;">About Chris</a> · <a href="https://npcwoods.com/credentials/" style="color:var(--blue-bright);text-decoration:underline;">Full credentials, NPI &amp; state licenses</a></p>
  <p style="margin:0;font-size:12px;color:var(--muted);">Last reviewed: <time datetime="{series["reviewed"]}">{esc(series["reviewed_display"])}</time></p>
</div>

<!-- NPC WOODS vs BIG TELEHEALTH -->
<section class="vs-section" id="npc-vs-telehealth" aria-label="NPC Woods compared to big telehealth services">
  <div class="vs-inner">
    <div class="vs-head">
      <span class="section-kicker">The honest comparison</span>
      <h2>NPC Woods vs. Big Telehealth</h2>
      <p>{esc(o["vs_sub"])}</p>
    </div>
    <div class="vs-grid">
      <div class="vs-cell vs-corner"></div>
      <div class="vs-cell vs-us-head">NPC Woods</div>
      <div class="vs-cell vs-them-head">Big Telehealth</div>
{vs_rows}
    </div>
  </div>
</section>

<!-- REVIEWS -->
{gold_reviews()}

<!-- HOW IT WORKS -->
<section id="how-it-works" class="section section-light dark-to-light">
  <div class="section-inner">
    <span class="section-kicker">How it works</span>
    <h2 class="section-title">Three texts. That's it.</h2>
    <p class="section-body">{esc(o["how_sub"])}</p>
    <div class="bento">
{chr(10).join(bento)}
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:20px;text-align:center">{esc(o["how_note"])}</p>
  </div>
</section>

<!-- WHAT IT IS -->
<section id="what-is" class="section section-white">
  <div class="section-inner" style="max-width:820px">
    <span class="section-kicker">{esc(w["kicker"])}</span>
    <h2 class="section-title">{esc(w["h2"])}</h2>
    <p class="section-body">{esc(w["body"])}</p>
    <h3 style="font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);margin-bottom:14px">{esc(w["cards_h"])}</h3>
    <div class="symptom-grid">
{sym}
    </div>
  </div>
</section>

<!-- COMPARE -->
<section id="compare" class="section section-light">
  <div class="section-inner" style="max-width:900px">
    <span class="section-kicker">{esc(tb["kicker"])}</span>
    <h2 class="section-title">{esc(tb["h2"])}</h2>
    <p class="section-body">{esc(tb["sub"])}</p>
    <div class="table-wrap">
      <table class="compare-table">
        <thead><tr>{"".join(f"<th>{esc(x)}</th>" for x in tb["head"])}</tr></thead>
        <tbody>
{rows}
        </tbody>
      </table>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:16px;text-align:center">{esc(tb["note"])}</p>
  </div>
</section>

<!-- WHAT THE $59 COVERS -->
<section id="pricing" class="section">
  <div class="section-inner" style="max-width:1000px">
    <span class="section-kicker">{esc(cv["kicker"])}</span>
    <h2 class="section-title">{esc(cv["h2"])}</h2>
    <p class="section-body">{esc(cv["sub"])}</p>
    <div class="drug-grid">
{covers}
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:20px;text-align:center">{esc(cv["note"])}</p>
  </div>
</section>

<!-- ER WARNING -->
<section id="er-warning" class="section section-light dark-to-light">
  <div class="section-inner" style="max-width:740px;text-align:center">
    <span class="section-kicker">Safety first</span>
    <h2 class="section-title">{esc(o["er_h2"])}</h2>
    <p class="section-body" style="max-width:100%">{esc(o["er_intro"])}</p>
    <div class="er-box" style="text-align:left">
      <h3>⚠ Call 911 or go now if any of these apply:</h3>
      <ul>
{er}
      </ul>
    </div>
    <p style="font-size:14px;color:var(--muted);margin-top:20px">{esc(LOCKED_911)} {esc(o["er_after"])}</p>
  </div>
</section>

<!-- WHO IT'S FOR -->
<section id="who-its-for" class="section section-white">
  <div class="section-inner" style="max-width:900px">
    <span class="section-kicker">Is this right for you?</span>
    <h2 class="section-title">Who this is for (and who it isn't)</h2>
    <p class="section-body">{esc(o["fit_sub"])}</p>
    <div class="fit-grid">
      <div class="fit-good">
        <div class="fit-label">Good fit ✓</div>
        <ul class="fit-list">
{fy}
        </ul>
      </div>
      <div class="fit-bad">
        <div class="fit-label">Needs in-person care ✗</div>
        <ul class="fit-list">
{fn}
        </ul>
      </div>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:16px;text-align:center">{esc(o["fit_note"])}</p>
  </div>
</section>

<section class="section alt-bg">
  <div class="section-inner" style="max-width:820px">
    <span class="section-kicker">{esc(ex["kicker"])}</span>
    <h2 class="section-title">{esc(ex["h2"])}</h2>
    {"".join(f'<p style="font-size:16px;color:var(--body);line-height:1.7;margin-bottom:16px">{esc(p)}</p>' for p in ex["p"])}
    <p style="font-size:14px;color:var(--muted);line-height:1.7">{esc(ex["small"])}</p>
  </div>
</section>

<!-- FAQ -->
<section id="faq" class="section section-light dark-to-light">
  <div class="section-inner" style="max-width:720px">
    <span class="section-kicker">FAQ</span>
    <h2 class="section-title" style="text-align:center;margin-bottom:36px">Common questions</h2>
    <div class="faq-list">
{faqs}
    </div>
  </div>
</section>

{gold_states()}

<section class="section section-white" id="explained" aria-labelledby="explained-title">
  <div class="section-inner">
    <span class="section-kicker">Learn first</span>
    <h2 class="section-title" id="explained-title">{esc(o["explained_h2"])}</h2>
    <p class="section-body">{esc(o["explained_body"])}</p>
    <div class="explained-grid">
{explained}
    </div>
  </div>
</section>

<!-- CROSS LINKS -->
{gold_cross(gold["short"], series["one_pager"]["path"])}

<!-- BOTTOM CTA -->
<section class="bottom-cta">
  <div class="bottom-cta-inner">
    <h2>{esc(o["bottom_h2"])}</h2>
    <p>{esc(o["bottom_p"])}</p>
    {sms_cta(cta, "font-size:16px;padding:16px 32px")}
    <div class="bottom-trust-line">
      <span>🔒 HIPAA-Compliant &amp; Secure</span>
      <span>💳 HSA/FSA accepted</span>
      <span>{o["bottom_trust3"]}</span>
    </div>
  </div>
</section>
<div class="clinician-line" style="font-size:12px;line-height:1.6;">
  Clinically reviewed by <strong>Chris Woods, {CRED}</strong>, double board-certified Nurse Practitioner.<br>
  Licensed in 14 states, including Florida by telehealth registration (AZ, CO, CT, GA, ID, IA, MT, NV, NM, NC, OR, UT, WA, plus FL TPAN3355). &bull; <a href="https://npcwoods.com/about/" style="color:var(--blue-bright);">About Chris</a> &bull; <a href="https://npcwoods.com/credentials/" style="color:var(--blue-bright);">Credentials</a> &bull; Last reviewed: <time datetime="{series["reviewed"]}">{esc(series["reviewed_display"])}</time>
</div>
</main>"""
    css = _head_styles(GOLD_LANDER) + "\n" + OFFER_EXTRA_CSS
    crumbs = [("Home", f"{SITE}/"), (series["one_pager"]["title"], canonical)]
    og = ccs.og_url(art, "offer")
    schemas = [
        ccs.medical_schema(page["h1"], canonical, page["meta_description"], series["reviewed"], image=ccs.og_image_obj(art, "offer", page["h1"])),
        howto_schema(f'How a {gold["short"].lower()} text visit works', o["how"]),
        ccs.faq_schema(page["faqs"]),
        ccs.breadcrumb_schema(crumbs),
        ccs.person_schema(),
    ]
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
             '<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">')
    h = head(title=page["meta_title"], desc=page["meta_description"], canonical=canonical, og_img=og,
             og_alt=f'{o["h1"]} {series["og_alt_suffix"]}', schemas=schemas, css=css, theme="#05060a", fonts=fonts)
    return f"""{h}
<body>
<a class="skip-link" href="#main">Skip to content</a>
{header}
{body}
{footer}
{TAIL_JS}
</body>
</html>
"""


def main() -> None:
    series_id = sys.argv[1] if len(sys.argv) > 1 else "screening-labs"
    sdir = ROOT / "landing-pages" / "learn" / series_id
    series = load_json(sdir / "series.json")
    content = load_json(sdir / "content.json")
    gold = load_json(sdir / "gold.json")
    art = load_json(sdir / "art.json")
    header = (ROOT / "html" / "shared" / "header-snippet.html").read_text(encoding="utf-8")
    footer = (ROOT / "html" / "shared" / "footer-snippet.html").read_text(encoding="utf-8")
    ccs.check_footer(footer)
    for index, stop in enumerate(series["stops"]):
        out = sdir / stop["slug"] / "index.html" if stop["slug"] else sdir / "index.html"
        ccs.write(out, build_series_page(series, content, gold, art, header, footer, stop, index))
    offer_dir = ROOT / "landing-pages" / series["one_pager"]["path"].strip("/")
    ccs.write(offer_dir / "index.html", build_offer(series, content, gold, art, header, footer))


if __name__ == "__main__":
    main()
