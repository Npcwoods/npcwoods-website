#!/usr/bin/env python3
"""Build the four Phoenix urgent-care plates from locked whiteboard drafts.

Does not publish. Run from npcwoods-website:
  python3 scripts/build-phoenix-urgent-care-pages.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADER = (ROOT / "html" / "shared" / "header-snippet.html").read_text(encoding="utf-8")
FOOTER = (ROOT / "html" / "shared" / "footer-snippet.html").read_text(encoding="utf-8")

SMS = "sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit"
PHONE = "(480) 639-4722"
REVIEWED = "2026-08-24"
REVIEWED_HUMAN = "August 24, 2026"
HEADSHOT = "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp"
LOGO = "https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg"

PLATES = [
    {
        "slug": "skip-the-urgent-care-phoenix-az",
        "title_short": "Skip the urgent care lobby in Phoenix",
        "href": "https://npcwoods.com/skip-the-urgent-care-phoenix-az/",
    },
    {
        "slug": "urgent-care-vs-text-visit-phoenix-az",
        "title_short": "Urgent care vs a $59 text visit in Phoenix",
        "href": "https://npcwoods.com/urgent-care-vs-text-visit-phoenix-az/",
    },
    {
        "slug": "phoenix-az-5-things-you-can-text",
        "title_short": "5 things you can text an NP about in Phoenix",
        "href": "https://npcwoods.com/phoenix-az-5-things-you-can-text/",
    },
    {
        "slug": "skip-phoenix-urgent-care-from-your-pocket",
        "title_short": "Skip the Phoenix line from your pocket",
        "href": "https://npcwoods.com/skip-phoenix-urgent-care-from-your-pocket/",
    },
]


CSS = r"""
#npcSaveWrap { display: none !important; }
body::after { content: none !important; display: none !important; }
:root {
  --white:#FFFFFF; --off-white:#F7F8FA; --warm-white:#FDF8F4;
  --text-primary:#1A1A2E; --text-body:#4A4A5A; --text-muted:#8E8E9A;
  --brand:#2563EB; --brand-light:#EFF6FF; --brand-soft:#DBEAFE; --brand-hover:#1D4ED8;
  --border:#E5E7EB; --success:#16A34A; --success-light:#DCFCE7; --gold:#D4933F;
  --section-pad:80px; --section-pad-mobile:56px; --container-max:1100px;
  --container-narrow:750px; --side-pad:32px; --side-pad-mobile:20px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;font-size:16px}
body{background:var(--white);color:var(--text-body);font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.7;overflow-x:hidden;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:var(--brand);text-decoration:none}
a:hover{color:var(--brand-hover);text-decoration:underline}
:focus-visible{outline:2px solid var(--brand);outline-offset:2px;border-radius:4px}
strong,b{font-weight:600;color:var(--text-primary)}
.skip-link{position:absolute;left:-999px;top:0;background:var(--brand);color:#fff;padding:8px 12px;z-index:10000}
.skip-link:focus{left:12px;top:12px}
.container{max-width:var(--container-max);margin:0 auto;padding:0 var(--side-pad)}
.container-narrow{max-width:var(--container-narrow);margin:0 auto;padding:0 var(--side-pad)}
@media (max-width:768px){.container,.container-narrow{padding:0 var(--side-pad-mobile)}}
h1,h2,h3{font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif;color:var(--text-primary);letter-spacing:-.02em}
h1{font-size:clamp(2.1rem,5.4vw,3.3rem);font-weight:800;line-height:1.08;letter-spacing:-.03em}
h2{font-size:clamp(1.5rem,3.6vw,2.1rem);font-weight:700;line-height:1.2;margin-bottom:1rem}
h3{font-size:1.2rem;font-weight:600;line-height:1.3;margin-bottom:.5rem}
p{font-size:1rem;line-height:1.7;margin-bottom:1rem;color:var(--text-body)}
.breadcrumb{padding:18px 0 0;font-size:.85rem;color:var(--text-muted)}
.breadcrumb a{color:var(--brand)}
.hero{position:relative;padding:72px 0 56px;background:radial-gradient(90% 70% at 12% 18%,rgba(217,119,6,.22),transparent 62%),radial-gradient(85% 70% at 88% 76%,rgba(37,99,235,.24),transparent 60%),linear-gradient(180deg,#091535 0%,#070e24 100%);color:#F2F5F8}
.hero-inner{max-width:820px;margin:0 auto;padding:0 var(--side-pad);text-align:center}
.hero-photo{width:104px;height:104px;border-radius:50%;object-fit:cover;margin:0 auto 18px;border:3px solid rgba(255,255,255,.85);box-shadow:0 8px 24px rgba(0,0,0,.28)}
.hero-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.12);color:#fff;font-weight:600;font-size:.78rem;padding:7px 14px;border-radius:100px;margin-bottom:16px;letter-spacing:.04em;text-transform:uppercase}
.hero-badge .hero-dot{width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 0 3px rgba(34,197,94,.22)}
.hero h1{color:#fff;margin-bottom:16px}
.hero h1 span{color:#FBBF24}
.hero-sub{font-size:1.08rem;color:#C9D4E3;max-width:620px;margin:0 auto 22px;line-height:1.55}
.hero-price{display:inline-block;background:rgba(212,147,63,.18);color:#FBBF24;font-weight:700;font-size:1.05rem;padding:10px 20px;border-radius:100px;margin-bottom:22px}
.hero-cta-row{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-bottom:8px}
.cta-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;background:var(--brand);color:#fff !important;-webkit-text-fill-color:#fff !important;font-weight:600;padding:16px 32px;border-radius:100px;text-decoration:none;box-shadow:0 4px 16px rgba(37,99,235,.35)}
.cta-btn:hover{background:var(--brand-hover);color:#fff !important;text-decoration:none;transform:translateY(-1px)}
.cta-btn-outline{display:inline-flex;align-items:center;justify-content:center;gap:10px;background:transparent;color:#fff !important;font-weight:600;padding:16px 32px;border-radius:100px;border:1px solid rgba(255,255,255,.28);text-decoration:none}
.cta-btn-outline:hover{background:rgba(255,255,255,.08);text-decoration:none}
.safety-strip{background:#111827;color:#FDE68A;text-align:center;padding:12px 20px;font-size:.92rem}
.safety-strip strong{color:#FBBF24}
.article{padding:var(--section-pad) 0}
@media (max-width:768px){.hero{padding:56px 0 40px}.article{padding:var(--section-pad-mobile) 0}}
.article .container-narrow p,.article .container-narrow li{max-width:65ch}
.article h2{margin-top:2.2rem}
.article ol.toc{margin:0 0 28px 18px;color:var(--text-body)}
.article ol.toc li{margin-bottom:6px}
.answer-block{background:var(--brand-light);border:1px solid var(--brand-soft);padding:24px 28px;border-radius:16px;margin:0 auto 28px}
.answer-block p{margin-bottom:0;color:var(--text-primary)}
.hours-list,.plain-list{margin:0 0 18px 18px}
.hours-list li,.plain-list li{margin-bottom:8px}
.comparison-wrap{overflow-x:auto;margin:20px 0 28px}
.comparison-table{width:100%;min-width:560px;border-collapse:collapse;background:#fff;border:1px solid var(--border);border-radius:12px;overflow:hidden}
.comparison-table th{background:var(--brand-light);color:var(--text-primary);padding:14px 16px;font-size:.85rem;text-align:left;border-bottom:1px solid var(--border)}
.comparison-table th:last-child{color:var(--brand)}
.comparison-table td{padding:14px 16px;font-size:.93rem;color:var(--text-body);border-bottom:1px solid var(--border);vertical-align:top}
.comparison-table td:first-child{font-weight:600;color:var(--text-primary)}
.comparison-table td:last-child{color:var(--brand);font-weight:600}
.steps{display:flex;flex-direction:column;gap:22px;margin:18px 0 28px}
.step{display:flex;gap:16px;align-items:flex-start}
.step-num{flex-shrink:0;width:44px;height:44px;background:var(--brand);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800}
.step-content h3{margin-bottom:4px}
.step-content p{margin-bottom:0}
.npc-clinician-byline{margin:8px auto 8px;max-width:720px;padding:14px 18px;border:1px solid #dbe5f5;border-radius:16px;background:linear-gradient(180deg,#f8fbff 0%,#fff 100%)}
.npc-byline-badge{display:inline-flex;margin-bottom:8px;padding:4px 10px;border-radius:999px;background:#e8f1ff;color:#1d4ed8;font-size:.68rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.npc-byline-main{margin:0 0 6px;color:#13233f}
.npc-byline-meta{margin:0;font-size:.82rem;color:#4b5d7a}
.related{padding:56px 0;background:var(--off-white)}
.related-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;max-width:760px;margin:24px auto 0}
@media (max-width:640px){.related-grid{grid-template-columns:1fr}}
.related-card{display:block;background:#fff;border:1px solid var(--border);border-radius:16px;padding:18px 18px 16px;text-decoration:none;color:var(--text-primary)}
.related-card:hover{border-color:var(--brand);text-decoration:none;box-shadow:0 8px 24px rgba(37,99,235,.08)}
.related-card span{display:block;font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--brand);margin-bottom:6px}
.faq-section{padding:var(--section-pad) 0;background:var(--warm-white)}
.section-label{font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--brand);margin-bottom:12px;text-align:center}
.section-title{text-align:center;margin-bottom:18px}
.faq-list{max-width:760px;margin:0 auto}
.faq-item{border-bottom:1px solid var(--border);padding:20px 0}
.faq-question{font-weight:600;color:var(--text-primary);cursor:pointer;display:flex;justify-content:space-between;align-items:center;user-select:none}
.faq-toggle{width:28px;height:28px;border-radius:50%;background:var(--brand-light);color:var(--brand);display:inline-flex;align-items:center;justify-content:center;margin-left:16px}
.faq-item.expanded .faq-toggle{background:var(--brand);color:#fff;transform:rotate(45deg)}
.faq-answer{max-height:0;overflow:hidden;transition:max-height .3s ease,padding .3s ease;color:var(--text-body)}
.faq-item.expanded .faq-answer{max-height:520px;padding-top:14px}
.final-cta{padding:var(--section-pad) 0;background:#091535;color:#F2F5F8;text-align:center}
.final-cta h2{color:#fff}
.final-cta p{color:#C9D4E3;max-width:560px;margin:0 auto 14px}
.final-cta .cta-btn{margin-top:8px}
.mobile-floating-cta{display:none}
@media (max-width:768px){
  body{padding-bottom:92px}
  .hero{padding-bottom:72px}
  .hero-cta-row .cta-btn-outline{display:none}
  .mobile-floating-cta{display:block;position:fixed;left:0;right:0;bottom:0;z-index:9999;padding:12px 16px calc(12px + env(safe-area-inset-bottom));background:rgba(9,21,53,.94);backdrop-filter:blur(10px)}
  .mobile-floating-cta a{display:flex;align-items:center;justify-content:center;gap:8px;background:#1D4ED8;color:#fff !important;-webkit-text-fill-color:#fff !important;font-weight:700;border-radius:100px;padding:14px 20px;text-decoration:none}
}
"""


def related_html(current_slug: str) -> str:
    cards = []
    for plate in PLATES:
        if plate["slug"] == current_slug:
            continue
        cards.append(
            f'<a class="related-card" href="{plate["href"]}"><span>Phoenix</span>{plate["title_short"]}</a>'
        )
    cards.append(
        '<a class="related-card" href="https://npcwoods.com/uti-treatment/phoenix-az/"><span>Already live</span>UTI treatment in Phoenix, AZ</a>'
    )
    return "\n".join(cards)


def faqs_html(faqs: list[dict]) -> str:
    blocks = []
    for faq in faqs:
        blocks.append(
            f"""      <div class="faq-item">
        <div class="faq-question" onclick="toggleFaq(this)" tabindex="0" role="button" aria-expanded="false">
          {faq["q"]}
          <span class="faq-toggle">+</span>
        </div>
        <div class="faq-answer"><p>{faq["a"]}</p></div>
      </div>"""
        )
    return "\n".join(blocks)


def schema_block(page: dict) -> str:
    url = page["canonical"]
    graph = [
        {
            "@context": "https://schema.org",
            "@type": "MedicalWebPage",
            "@id": url + "#webpage",
            "url": url,
            "name": page["title"],
            "headline": page["h1"],
            "description": page["description"],
            "datePublished": REVIEWED,
            "dateModified": REVIEWED,
            "lastReviewed": REVIEWED,
            "inLanguage": "en-US",
            "isPartOf": {"@type": "WebSite", "name": "NPCWoods Telemedicine", "url": "https://npcwoods.com/"},
            "about": {"@id": "https://npcwoods.com/#medical-business"},
            "author": {"@id": "https://npcwoods.com/#chris-woods"},
            "reviewedBy": {"@id": "https://npcwoods.com/#chris-woods"},
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": [".answer-block", "h1"],
            },
            "mainEntity": {"@id": url + "#main"},
        },
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "@id": "https://npcwoods.com/#chris-woods",
            "url": "https://npcwoods.com/about/",
            "name": "Chris Woods",
            "jobTitle": "Nurse Practitioner",
            "image": HEADSHOT,
            "worksFor": {"@id": "https://npcwoods.com/#medical-business"},
            "hasCredential": {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "license",
                "name": "MSN, APRN, FNP-C",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://npcwoods.com/"},
                {"@type": "ListItem", "position": 2, "name": "Arizona", "item": "https://npcwoods.com/arizona-telemedicine/"},
                {"@type": "ListItem", "position": 3, "name": page["crumb"], "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": faq["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": faq["a_text"]},
                }
                for faq in page["faqs"]
            ],
        },
    ]
    if page.get("item_list"):
        graph.append(
            {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "@id": url + "#main",
                "name": page["h1"],
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": name}
                    for i, name in enumerate(page["item_list"])
                ],
            }
        )
    if page.get("howto"):
        steps = []
        for i, step in enumerate(page["howto"], start=1):
            steps.append(
                {
                    "@type": "HowToStep",
                    "position": i,
                    "name": step["name"],
                    "text": step["text"],
                    "url": url + f"#step-{i}",
                }
            )
        graph.append(
            {
                "@context": "https://schema.org",
                "@type": "HowTo",
                "@id": url + "#main",
                "name": page["h1"],
                "description": page["description"],
                "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": "59"},
                "supply": [{"@type": "HowToSupply", "name": "Mobile phone for text messaging"}],
                "step": steps,
            }
        )
    chunks = []
    for block in graph:
        chunks.append(
            '<script type="application/ld+json">\n'
            + json.dumps(block, indent=2, ensure_ascii=False)
            + "\n</script>"
        )
    return "\n".join(chunks)


def render(page: dict) -> str:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{page["title"]}</title>
<meta name="description" content="{page["description"]}">
<meta name="keywords" content="{page["keywords"]}">
<meta name="author" content="Chris Woods, MSN, APRN, FNP-C">
<meta name="theme-color" content="#091535">
<meta name="last-reviewed" content="{REVIEWED}">
<meta name="geo.region" content="US-AZ">
<meta name="geo.placename" content="Phoenix">
<link rel="canonical" href="{page["canonical"]}">
<link rel="cite-as" href="{page["canonical"]}">
<link rel="icon" type="image/jpeg" href="{LOGO}">
<link rel="apple-touch-icon" href="{LOGO}">
<meta property="og:type" content="article">
<meta property="og:url" content="{page["canonical"]}">
<meta property="og:title" content="{page["og_title"]}">
<meta property="og:description" content="{page["description"]}">
<meta property="og:site_name" content="NPCWoods Telemedicine">
<meta property="og:image" content="{HEADSHOT}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page["og_title"]}">
<meta name="twitter:description" content="{page["description"]}">
<meta property="article:published_time" content="{REVIEWED}">
<meta property="article:modified_time" content="{REVIEWED}">
<meta property="article:author" content="Chris Woods">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0&family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0&family=Inter:wght@400;500;600;700;800&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0&family=Inter:wght@400;500;600;700;800&display=swap"></noscript>
{schema_block(page)}
<style>
{CSS}
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{HEADER}
<section class="hero">
  <div class="hero-inner">
    <img class="hero-photo" src="{HEADSHOT}" width="104" height="104" alt="Chris Woods, Nurse Practitioner">
    <div class="hero-badge"><span class="hero-dot"></span> Phoenix, AZ · Text visit</div>
    <h1>{page["h1_html"]}</h1>
    <p class="hero-sub">{page["hero_sub"]}</p>
    <div class="hero-price">$59 cash · pay after care · no subscription</div>
    <div class="hero-cta-row">
      <a class="cta-btn npc-sms-cta" href="{SMS}">Text Chris · {PHONE}</a>
      <a class="cta-btn-outline" href="https://npcwoods.com/how-it-works/">How a text visit works</a>
    </div>
  </div>
</section>
<div class="safety-strip"><strong>Not for emergencies.</strong> Chest pain, trouble breathing, or other emergency symptoms: call 911.</div>
<main id="main">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="https://npcwoods.com/">Home</a> /
      <a href="https://npcwoods.com/arizona-telemedicine/">Arizona</a> /
      {page["crumb"]}
    </nav>
  </div>
  <article class="article">
    <div class="container-narrow">
      <div class="answer-block"><p>{page["answer"]}</p></div>
{page["body"]}
      <section class="npc-clinician-byline" aria-label="Clinician review attribution and freshness">
        <div class="npc-byline-badge" aria-hidden="true">Clinician reviewed</div>
        <p class="npc-byline-main">Clinically reviewed by <a href="https://npcwoods.com/about/" rel="author">Chris Woods, MSN, APRN, FNP-C</a>. Double board-certified Nurse Practitioner. Licensed in Arizona and 10 other states.</p>
        <p class="npc-byline-meta"><strong>Last reviewed: <time datetime="{REVIEWED}">{REVIEWED_HUMAN}</time></strong>. Real clinician. No AI. <a href="https://npcwoods.com/credentials/">Verify credentials</a></p>
      </section>
    </div>
  </article>
  <section class="related">
    <div class="container-narrow" style="text-align:center">
      <div class="section-label">Phoenix plates</div>
      <h2 class="section-title">Keep reading, or text.</h2>
      <div class="related-grid">
        {related_html(page["slug"])}
      </div>
    </div>
  </section>
  <section class="faq-section">
    <div class="container-narrow">
      <div class="section-label">Quick answers</div>
      <h2 class="section-title">FAQ</h2>
      <div class="faq-list">
{faqs_html(page["faqs"])}
      </div>
    </div>
  </section>
  <section class="final-cta">
    <div class="container-narrow">
      <h2>If the story is text-safe, start from Phoenix.</h2>
      <p>Text {PHONE}. Say you are in Phoenix and what started. Same NP every time. $59 after care, only if text treatment is appropriate.</p>
      <a class="cta-btn npc-sms-cta" href="{SMS}">Text Chris · $59</a>
    </div>
  </section>
</main>
{FOOTER}
<div class="mobile-floating-cta">
  <a class="npc-sms-cta" href="{SMS}">
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
    Text Chris · $59
  </a>
</div>
<script>
function toggleFaq(el) {{
  var item = el.parentElement;
  var wasExpanded = item.classList.contains('expanded');
  var allItems = document.querySelectorAll('.faq-item');
  for (var i = 0; i < allItems.length; i++) {{
    allItems[i].classList.remove('expanded');
    var q = allItems[i].querySelector('.faq-question');
    if (q) q.setAttribute('aria-expanded', 'false');
  }}
  if (!wasExpanded) {{
    item.classList.add('expanded');
    el.setAttribute('aria-expanded', 'true');
  }}
}}
document.addEventListener('keydown', function(e) {{
  if ((e.key === 'Enter' || e.key === ' ') && e.target && e.target.classList && e.target.classList.contains('faq-question')) {{
    e.preventDefault();
    toggleFaq(e.target);
  }}
}});
</script>
<script src="/tracking.js"></script>
</body>
</html>
"""
    return html.replace(" — ", " - ").replace("—", " - ")


PAGES = [
    {
        "slug": "skip-the-urgent-care-phoenix-az",
        "canonical": "https://npcwoods.com/skip-the-urgent-care-phoenix-az/",
        "title": "Skip the Urgent Care Lobby in Phoenix | $59 Text Visit",
        "og_title": "Skip the urgent care lobby in Phoenix. Text Chris. $59.",
        "h1": "Skip the urgent care lobby in Phoenix",
        "h1_html": "Skip the urgent care lobby in Phoenix. <span>Text Chris.</span>",
        "crumb": "Skip the lobby",
        "hero_sub": "Banner, HonorHealth, and NextCare doors are real. If the problem is straightforward, you do not always have to sit in that lobby first.",
        "description": "Skip a Phoenix urgent care lobby when the story is text-safe. Same NP, Chris Woods. $59 cash after care. Text (480) 639-4722. Not for emergencies.",
        "keywords": "skip urgent care Phoenix, text NP Phoenix AZ, Phoenix urgent care lobby, $59 text visit Phoenix, NPCWoods Phoenix",
        "answer": "If you are in Phoenix and the problem is straightforward — a UTI pattern you already know, sinus pressure that is not an emergency, a tooth that hurts but you can swallow — you can text Chris Woods, MSN, APRN, FNP-C, at (480) 639-4722. Text only. No video. $59 cash, paid after care. NPCWoods does not have a Phoenix building.",
        "item_list": [
            "The lobbies are real, and they close",
            "I-10 and Loop 101 are not the visit",
            "UTI is the pattern people already know",
            "Sinus and strep are not automatic antibiotics",
            "Dental pain is a bridge, not a fix",
            "Same NP, later — not a rotating video room",
            "When you still go in",
        ],
        "faqs": [
            {
                "q": "Can I skip a Phoenix urgent care lobby by text?",
                "a": "When the story is text-safe, yes. Text Chris at (480) 639-4722. Same NP. $59 after care, only if text treatment is appropriate. If you need a film, stitches, or a child examined, go to an open door.",
                "a_text": "When the story is text-safe, yes. Text Chris Woods, a licensed Arizona nurse practitioner, at (480) 639-4722. $59 after care, only if text treatment is appropriate.",
            },
            {
                "q": "Does NPCWoods have a clinic in Phoenix?",
                "a": "No. There is no NPCWoods storefront in Phoenix. Banner, HonorHealth, NextCare, Dignity in Ahwatukee, and MinuteClinic are the buildings. This is a text visit.",
                "a_text": "No. NPCWoods does not have a Phoenix clinic. Care is by text with Chris Woods, a licensed Arizona nurse practitioner.",
            },
            {
                "q": "When should I still go to Banner, HonorHealth, or NextCare?",
                "a": "Go in for a possible break, a wound that needs closing, a child who looks truly ill, or anything that needs a room. HonorHealth Phoenix doors post 7 a.m. to 7 p.m. Several Banner Phoenix pages post 8 a.m. to 8 p.m. NextCare Thomas posts 8 a.m. to midnight.",
                "a_text": "Go in for films, stitches, a possible break, a child who looks truly ill, or anything that needs a room. Posted hours: HonorHealth 7 a.m. to 7 p.m., several Banner Phoenix pages 8 a.m. to 8 p.m., NextCare Thomas 8 a.m. to midnight.",
            },
            {
                "q": "How much is a Phoenix text visit?",
                "a": "$59 flat. Cash. Pay after care. No membership. Pharmacy cost is separate. You do not pay if text care is not safe.",
                "a_text": "$59 flat cash, paid after care, only if text treatment is appropriate. No membership. Pharmacy cost is separate.",
            },
        ],
        "body": f"""      <ol class="toc">
        <li><a href="#lobbies">The lobbies are real, and they close</a></li>
        <li><a href="#drive">I-10 and Loop 101 are not the visit</a></li>
        <li><a href="#uti">UTI is the pattern people already know</a></li>
        <li><a href="#sinus">Sinus and strep are not automatic antibiotics</a></li>
        <li><a href="#dental">Dental pain is a bridge, not a fix</a></li>
        <li><a href="#same-np">Same NP, not a rotating video room</a></li>
        <li><a href="#go-in">When you still go in</a></li>
      </ol>
      <h2 id="lobbies">1. The lobbies are real, and they close</h2>
      <p>Phoenix has real urgent-care doors. Banner, HonorHealth, and NextCare publish addresses along I-10, Loop 101, Camelback, Bell, and Thomas. Those rooms exist for a reason. This is not a claim that NPCWoods has a building in Phoenix. It does not.</p>
      <ul class="hours-list">
        <li>HonorHealth Urgent Care posts <strong>7 a.m. to 7 p.m. daily</strong> at Thomas (4501 E Thomas Rd), East Bell (17015 N 7th St), Bethany Home, and Saguaro on Tatum.</li>
        <li>Banner Urgent Care pages we could read post <strong>8 a.m. to 8 p.m. daily</strong> at Thunderbird &amp; Tatum, 7th &amp; Camelback, 44th &amp; Camelback, and Bell &amp; 32nd. Downtown Banner at Central &amp; Washington posts <strong>7 a.m. to 7 p.m.</strong></li>
        <li>Dignity Health Urgent Care in Ahwatukee (4545 E Chandler Blvd) posts <strong>8 a.m. to 7 p.m. daily</strong>.</li>
        <li>NextCare lists ten Phoenix doors. Thomas at 1701 E Thomas Rd posts <strong>8 a.m. to midnight daily</strong>.</li>
      </ul>
      <p>If you need a room, those hours matter. If you need a film, stitches, or a child examined, go to a door that is open. If you need a text visit, the lobby clock is not the limit.</p>
      <h2 id="drive">2. I-10 and Loop 101 are not the visit</h2>
      <p>Ahwatukee to downtown on I-10, or Loop 101 around the West Valley, is a drive even when traffic is kind. In August the parking lot is part of the visit. That is honest. It is not a wait-time claim. We did not measure anyone's line.</p>
      <p>HonorHealth's Save a Spot tool holds a place. It is not an appointment. Banner and NextCare also let you check in online. You still go in. You still sit somewhere.</p>
      <p>A <a href="https://npcwoods.com/how-it-works/">text visit</a> starts from the couch, the office, or the car if you are already parked and decide the lobby is the wrong door. You must be physically in Arizona or another licensed state when you text.</p>
      <h2 id="uti">3. UTI is the pattern people already know</h2>
      <p>Burning, urgency, frequency, no fever with flank pain — that is the <a href="https://npcwoods.com/uti-treatment/">UTI visit</a> people also take to Banner and HonorHealth. Phoenix already has a live city plate: <a href="https://npcwoods.com/uti-treatment/phoenix-az/">UTI treatment in Phoenix</a>. Read that if this is the only problem.</p>
      <p>Fever with back or side pain, pregnancy, a child, vomiting so you cannot keep pills down, or a lot of blood in the urine is in-person care. A Banner or hospital door, not a text.</p>
      <h2 id="sinus">4. Sinus and strep are not automatic antibiotics</h2>
      <p>HonorHealth and Banner list sinus and sore throat on their urgent-care pages. So do we. That does not mean every sinus week gets a prescription. Most sinus infections start viral. <a href="https://npcwoods.com/do-i-need-antibiotics-sinus-infection/">Antibiotics are for a pattern</a> — longer than about ten days, or better then worse — not for yellow mucus alone. See <a href="https://npcwoods.com/sinus-infection-treatment/">sinus treatment</a> and <a href="https://npcwoods.com/strep-throat-treatment/">strep</a>.</p>
      <p>If you cannot swallow, you have trouble breathing, or your neck is swelling, that is not a text visit.</p>
      <h2 id="dental">5. Dental pain is a bridge, not a fix</h2>
      <p>NextCare's virtual list includes toothache. In-person urgent care can look at a face. Antibiotics do not repair a tooth. If a <a href="https://npcwoods.com/dental-pain/">dental-pain text visit</a> is safe, it is a bridge to a dentist. Spreading facial swelling, trouble swallowing, or high fever with a tooth is an ER.</p>
      <h2 id="same-np">6. Same NP, later — not a rotating video room</h2>
      <p>Video urgent care exists in Arizona. NextCare posts a scheduled video visit. CVS MinuteClinic posts Virtual Care. Those are different products. NPCWoods is <a href="https://npcwoods.com/arizona-telemedicine/">text with the same nurse practitioner</a> every time. No waiting room on a screen.</p>
      <p>Pay-after and the $59 number are below. They are not why you skip a needed X-ray.</p>
      <h2 id="go-in">7. When you still go in</h2>
      <p>Go in — or call 911 — for chest pain, trouble breathing, stroke signs, a bad belly with rigidity, a possible break, a deep cut, a child who looks truly ill, or anything that needs a room. Phoenix Children's urgent cares are evening and weekend doors in Glendale, Scottsdale, and Mesa if the patient is a child and that is the right place.</p>
      <p>If text care is not safe, you do not pay. Chris will say so.</p>
      <h2>How to start from Phoenix</h2>
      <div class="steps">
        <div class="step"><div class="step-num">1</div><div class="step-content"><h3>Text {PHONE}</h3><p>Say you are in Phoenix and what hurts.</p></div></div>
        <div class="step"><div class="step-num">2</div><div class="step-content"><h3>Answer the follow-up</h3><p>Chris Woods, MSN, APRN, FNP-C, reads the thread. Licensed in Arizona.</p></div></div>
        <div class="step"><div class="step-num">3</div><div class="step-content"><h3>Pharmacy you name</h3><p>If treatment is appropriate, the prescription goes to Fry's, Walgreens, CVS, Costco, wherever you actually pick up.</p></div></div>
      </div>
      <p><a href="https://npcwoods.com/pricing/">$59 flat. Pay after care.</a> No membership. Pharmacy cost is separate.</p>
""",
    },
    {
        "slug": "urgent-care-vs-text-visit-phoenix-az",
        "canonical": "https://npcwoods.com/urgent-care-vs-text-visit-phoenix-az/",
        "title": "Urgent Care vs a $59 Text Visit in Phoenix | NPCWoods",
        "og_title": "Phoenix urgent care is a door. A $59 text visit is not a cheaper room.",
        "h1": "Urgent care versus a $59 text visit in Phoenix",
        "h1_html": "Urgent care vs a $59 text visit in <span>Phoenix</span>",
        "crumb": "Urgent care vs text",
        "hero_sub": "A building with a clock is one visit. A text thread with the same NP is another. This is the split, not a sticker fight.",
        "description": "Phoenix urgent care is a door. A $59 text visit with Chris Woods, NP, is a different visit: no video, pay after care. When the lobby is right, go. When text is safe, text.",
        "keywords": "urgent care vs telehealth Phoenix, $59 text visit Phoenix AZ, Banner vs text visit, HonorHealth vs NPCWoods, NextCare virtual vs text",
        "answer": "Phoenix urgent care is a door with a clock. Banner, HonorHealth, NextCare, Dignity in Ahwatukee, and CVS MinuteClinic all publish hours. A text visit is not a cheaper version of that room. It is a different visit: symptoms that can be reviewed in writing, by the same nurse practitioner, without video. $59 cash after care.",
        "item_list": [
            "What the building is for",
            "What a text visit is for",
            "Hours vs a phone in your pocket",
            "Wait tools are still a lobby",
            "Video telehealth is still an appointment",
            "Pay after, and the same NP",
            "The honest no",
        ],
        "faqs": [
            {
                "q": "What is the difference between Phoenix urgent care and a $59 text visit?",
                "a": "Urgent care is a building for problems that need hands, a test, or a film. A text visit is a written story reviewed by the same NP, Chris Woods. No video. No slot. $59 after care if text treatment is appropriate.",
                "a_text": "Urgent care is a building for problems that need hands, a test, or a film. A text visit is a written story reviewed by Chris Woods, a licensed Arizona nurse practitioner. $59 after care if text treatment is appropriate.",
            },
            {
                "q": "Is a video visit the same as a text visit?",
                "a": "No. NextCare Virtual is book-a-time, camera on. MinuteClinic Virtual Care is a video product. NPCWoods is async text, no camera, no slot. Read the statewide split on telehealth vs urgent care.",
                "a_text": "No. NextCare Virtual and MinuteClinic Virtual Care are scheduled video visits. NPCWoods is async text with the same nurse practitioner and no camera.",
            },
            {
                "q": "When is the Phoenix lobby the right door?",
                "a": "When you need stitches, X-ray, a possible break, a hands-on exam, or a child who needs a room. NPCWoods does not have a Phoenix clinic. NextCare Thomas posts 8 a.m. to midnight if you still need a building after HonorHealth's 7 p.m. close.",
                "a_text": "When you need stitches, X-ray, a possible break, a hands-on exam, or a child who needs a room. NPCWoods has no Phoenix clinic.",
            },
            {
                "q": "Do I pay if text is not safe?",
                "a": "No. If Chris cannot treat you safely by text, he says so and you do not pay.",
                "a_text": "No. If text treatment is not appropriate, there is no charge.",
            },
        ],
        "body": f"""      <p>This page is not a price war with a national app. It is a split: when the lobby is the right place, and when a <a href="https://npcwoods.com/how-it-works/">text visit</a> can be.</p>
      <h2>1. What the building is for</h2>
      <p>Urgent care is built for problems that need hands, a test, or a film the same day. HonorHealth's Phoenix pages list lacerations, possible breaks, and X-ray (call first at Thomas). Banner lists stitches, X-ray when a technician is there, and sports physicals. NextCare Thomas stays open <strong>8 a.m. to midnight</strong>. That late door is useful if you need a room after HonorHealth's <strong>7 p.m.</strong> close or Banner's <strong>8 p.m.</strong> close.</p>
      <p>If you need those things, go. NPCWoods does not have a Phoenix clinic.</p>
      <h2>2. What a text visit is for</h2>
      <p>A text visit is for a story that can be taken in writing: <a href="https://npcwoods.com/uti-treatment/phoenix-az/">UTI</a>, <a href="https://npcwoods.com/sinus-infection-treatment/">sinus</a>, <a href="https://npcwoods.com/strep-throat-treatment/">strep or ear</a>, <a href="https://npcwoods.com/dental-pain/">dental pain as a bridge</a>, <a href="https://npcwoods.com/ed-treatment/">ED</a> when it is appropriate. The full list is on <a href="https://npcwoods.com/conditions/">conditions</a>.</p>
      <p>Chris Woods, MSN, APRN, FNP-C, reads the thread. Licensed in Arizona. You must be in Arizona or another licensed state at the time. No video. No waiting room. No appointment slot.</p>
      <h2>3. Hours vs a phone in your pocket</h2>
      <div class="comparison-wrap">
        <table class="comparison-table">
          <thead>
            <tr><th></th><th>Typical Phoenix urgent care (posted)</th><th>NPCWoods text visit</th></tr>
          </thead>
          <tbody>
            <tr><td>Form</td><td>A building</td><td>A text thread</td></tr>
            <tr><td>Example hours</td><td>HonorHealth 7a-7p daily; Banner 8a-8p on several Phoenix pages; Dignity Ahwatukee 8a-7p; NextCare Thomas 8a-midnight</td><td>Reviewed 7 days a week, by text</td></tr>
            <tr><td>How you pay</td><td>They publish plan lists at the door. Banner Phoenix pages say the counter no longer takes cash (cards and digital wallets).</td><td>$59 cash after care</td></tr>
            <tr><td>Video</td><td>NextCare Virtual is a scheduled video visit; MinuteClinic Virtual Care exists</td><td>No video</td></tr>
            <tr><td>Same clinician</td><td>You see who is on shift</td><td>Same NP every time</td></tr>
          </tbody>
        </table>
      </div>
      <p>We are not posting competitor cash prices. NextCare's <strong>virtual</strong> page posts a self-pay video fee; that is a different visit than walking into Thomas Road.</p>
      <h2>4. Wait tools are still a lobby</h2>
      <p>HonorHealth Save a Spot holds a line. It is not an appointment. Sicker people go first. Banner and NextCare show live wait widgets. Those numbers change. We will not invent a wait for you.</p>
      <p>A text visit has no kiosk. If Chris cannot treat you safely by text, he says so and you do not pay.</p>
      <h2>5. Video telehealth is still an appointment</h2>
      <p>Arizona has video urgent care. NextCare Virtual is book-a-time, camera on. MinuteClinic Virtual Care is a video product. Those visits can be the right call if you want a face on a screen.</p>
      <p>NPCWoods is the other shape: async text, no camera, no slot. Read <a href="https://npcwoods.com/telehealth-vs-urgent-care/">telehealth vs urgent care</a> for the wider split.</p>
      <h2>6. Pay after, and the same NP — below the fold on purpose</h2>
      <p>The visit is <a href="https://npcwoods.com/pricing/">$59 flat</a>. Cash. Not a subscription. You pay after care, and only if text treatment is appropriate. Pharmacy cost is separate.</p>
      <p>The reason to use it is not a sticker fight. It is this: the same nurse practitioner, Chris, every time. A relationship you can text again. No rotating video pool. No app.</p>
      <p>If you want a door that bills a plan, use Banner, HonorHealth, or NextCare, or a video visit they enroll.</p>
      <h2>7. The honest "no"</h2>
      <p>Do not text for a possible fracture, a wound that needs closing, a child under 2, a high fever with a stiff neck, pregnancy plus urinary symptoms you have not had evaluated, or anything that feels like an emergency. <a href="https://npcwoods.com/faq/">FAQ</a> and <a href="https://npcwoods.com/credentials/">credentials</a> are public.</p>
      <p>Text {PHONE}. Say you are in Phoenix. Say what started and when.</p>
""",
    },
    {
        "slug": "phoenix-az-5-things-you-can-text",
        "canonical": "https://npcwoods.com/phoenix-az-5-things-you-can-text/",
        "title": "5 Things You Can Text an NP About in Phoenix | $59",
        "og_title": "Phoenix: 5 things you can text an NP about. $59.",
        "h1": "Phoenix, Arizona: 5 things you can text an NP about",
        "h1_html": "Phoenix, Arizona: <span>5 things</span> you can text an NP about",
        "crumb": "5 things you can text",
        "hero_sub": "People in Phoenix already take these five problems to Banner, HonorHealth, and NextCare. Sometimes that is the right door. Sometimes the story is simple enough to text.",
        "description": "Five Phoenix problems you can text a licensed NP about: UTI, sinus, strep or ear, dental pain, ED. $59 after care. Same NP. Not for emergencies. Text (480) 639-4722.",
        "keywords": "text nurse practitioner Phoenix, UTI text Phoenix AZ, sinus text visit Phoenix, strep ear dental ED telehealth Phoenix",
        "answer": "People in Phoenix already take UTI, sinus, strep or ear, dental pain, and ED to Banner, HonorHealth, and NextCare. Sometimes that door is right. Sometimes the story is simple enough to text Chris Woods, MSN, APRN, FNP-C. $59 cash, pay after care. No Phoenix storefront.",
        "item_list": ["UTI", "Sinus", "Strep or ear", "Dental pain", "ED"],
        "faqs": [
            {
                "q": "What can I text an NP about in Phoenix?",
                "a": "Common text-safe visits: UTI, sinus, strep or ear, dental pain as a bridge to a dentist, and ED when appropriate. The public list is on conditions. Not X-rays, stitches, or a child under 2.",
                "a_text": "Common text-safe visits in Phoenix include UTI, sinus, strep or ear, dental pain as a bridge, and ED when appropriate. Not X-rays, stitches, or a child under 2.",
            },
            {
                "q": "Can I text for a UTI in Phoenix?",
                "a": "When it is safe, yes. Classic bladder symptoms, no fever with flank pain, not pregnant, not a child. Phoenix already has a live city plate: UTI treatment in Phoenix, AZ.",
                "a_text": "When it is safe, yes. Classic bladder symptoms without fever and flank pain. Phoenix already has a live UTI city page at npcwoods.com/uti-treatment/phoenix-az/.",
            },
            {
                "q": "Do sinus infections always need antibiotics?",
                "a": "No. Most sinus infections do not need antibiotics on day two. The pattern that sometimes does: symptoms past about ten days, or better then worse.",
                "a_text": "No. Most sinus infections do not need antibiotics on day two. Antibiotics are for a pattern: about ten days, or better then worse.",
            },
            {
                "q": "Can a text visit fix a tooth?",
                "a": "No. Antibiotics do not repair a tooth. A dental-pain visit is a possible bridge when it is safe. A dentist still has to treat it.",
                "a_text": "No. Antibiotics do not fix the tooth. A dental-pain text visit is a bridge when it is safe. A dentist still has to treat it.",
            },
        ],
        "body": f"""      <ol class="toc">
        <li><a href="#uti">UTI</a></li>
        <li><a href="#sinus">Sinus</a></li>
        <li><a href="#strep">Strep or ear</a></li>
        <li><a href="#dental">Dental pain</a></li>
        <li><a href="#ed">ED</a></li>
      </ol>
      <p>Chris Woods, MSN, APRN, FNP-C, is a nurse practitioner licensed in Arizona. Same person every time. Text only. $59 cash, pay after care, no subscription. No Phoenix storefront.</p>
      <h2 id="uti">1. UTI</h2>
      <p>Classic bladder symptoms: burning, urgency, frequency, pressure low in the belly. No fever with flank pain. Not pregnant. Not a child. You can keep fluids down.</p>
      <p>That is a common <a href="https://npcwoods.com/uti-treatment/">UTI text visit</a>. Phoenix already has a city plate: <a href="https://npcwoods.com/uti-treatment/phoenix-az/">UTI treatment in Phoenix, AZ</a>. The longer explainer is the <a href="https://npcwoods.com/learn/uti/">UTI guide</a>.</p>
      <p>Go in — often an ER — if you have fever <strong>and</strong> pain in the back or side, you are pregnant, this is a child, you cannot keep pills down, or there is a lot of blood in the urine.</p>
      <h2 id="sinus">2. Sinus</h2>
      <p>Dry air, dust, a cold that should have turned the corner and did not. Banner and HonorHealth list sinus on their urgent-care pages. So do we.</p>
      <p>Most sinus infections do not need antibiotics on day two. The pattern that sometimes does: symptoms past about ten days, or better then worse. Read <a href="https://npcwoods.com/sinus-infection-treatment/">sinus treatment</a> and <a href="https://npcwoods.com/do-i-need-antibiotics-sinus-infection/">do I need antibiotics</a>. More background: <a href="https://npcwoods.com/learn/sinus-infection/">learn/sinus</a>.</p>
      <p>Trouble breathing, swelling around the eyes, a severe headache that is new and different, or a stiff neck is not a text visit.</p>
      <h2 id="strep">3. Strep or ear</h2>
      <p>Sore throat with fever, or an ear that hurts after a cold. HonorHealth lists sore throats and patients over six months. <a href="https://npcwoods.com/strep-throat-treatment/">Strep</a> and <a href="https://npcwoods.com/ear-infection-treatment/">ear infection</a> are text visits when the story is straightforward.</p>
      <p>Cannot swallow saliva, drooling, a neck that looks wrong, or a child who is listless: in-person. An ear with spinning, facial weakness, or drainage after a puncture needs a room.</p>
      <p>Strep testing in a lobby is a reason some people still drive. If you want a swab, go to a door. If the history is enough and it is safe, a prescription can go to a Phoenix pharmacy.</p>
      <h2 id="dental">4. Dental pain</h2>
      <p>A tooth that started throbbing after a weekend. NextCare even lists toothache on its virtual-care page. Antibiotics do not fix the tooth. A dentist still has to treat it.</p>
      <p>A <a href="https://npcwoods.com/dental-pain/">dental-pain visit</a> is a possible bridge when it is safe — not a root canal by text. Spreading swelling of the face or neck, trouble swallowing, or high fever with a tooth is an ER.</p>
      <h2 id="ed">5. ED</h2>
      <p>Erectile dysfunction is a visit people also take to urgent care or a video clinic. It can be reviewed by text when it is appropriate. See <a href="https://npcwoods.com/ed-treatment/">ED treatment</a>.</p>
      <p>Chest pain, trouble breathing, or a sudden severe headache with ED symptoms is not this visit. Call 911 for those.</p>
      <p>NPCWoods does not prescribe controlled substances.</p>
      <h2>What these five are not</h2>
      <p>They are not X-rays. They are not stitches. They are not a child under 2. They are not "whatever is wrong." The public list is on <a href="https://npcwoods.com/conditions/">conditions</a>. GLP-1 consults are a separate <a href="https://npcwoods.com/glp1-weight-loss/">$59 fit-and-safety review</a>, not a pen in the mail.</p>
      <h2>How the text works in Phoenix</h2>
      <div class="steps">
        <div class="step"><div class="step-num">1</div><div class="step-content"><h3>Text {PHONE}</h3><p>Say which of the five it is, and that you are in Phoenix.</p></div></div>
        <div class="step"><div class="step-num">2</div><div class="step-content"><h3>Chris asks what he needs</h3><p>Same NP every time. No video. No app.</p></div></div>
        <div class="step"><div class="step-num">3</div><div class="step-content"><h3>Pharmacy you name</h3><p>If treatment is appropriate, the Rx goes there. If it is not safe by text, you do not pay.</p></div></div>
      </div>
      <h2>Weekend and heat, without inventing a line</h2>
      <p>HonorHealth Phoenix urgent cares post 7 a.m. to 7 p.m. daily. Several Banner Phoenix pages post 8 a.m. to 8 p.m. After that, a room means NextCare Thomas (posted 8 a.m. to midnight), an ER, or a text if the story is still text-safe. August heat in a lot is a reason people start the text from the car. It is not a wait-time claim.</p>
      <p>You still need to be in Arizona when you text. A prescription is not promised. <a href="https://npcwoods.com/how-it-works/">How it works</a>. <a href="https://npcwoods.com/faq/">FAQ</a>. <a href="https://npcwoods.com/pricing/">$59</a>. Pay after. Same NP. <a href="https://npcwoods.com/arizona-telemedicine/">Arizona hub</a>.</p>
""",
    },
    {
        "slug": "skip-phoenix-urgent-care-from-your-pocket",
        "canonical": "https://npcwoods.com/skip-phoenix-urgent-care-from-your-pocket/",
        "title": "How to Skip the Phoenix Urgent Care Line From Your Pocket | $59",
        "og_title": "Skip the Phoenix urgent care line from your pocket. $59 text.",
        "h1": "How to skip the Phoenix urgent care line from your pocket",
        "h1_html": "How to skip the Phoenix line <span>from your pocket</span>",
        "crumb": "From your pocket",
        "hero_sub": "Evening or Saturday. You are looking at a parking lot. This is an order of operations — not a promise that a lobby is empty.",
        "description": "Order of operations for Phoenix after hours: 911, a room, or a $59 text visit. HonorHealth 7-7, Banner 8-8, NextCare Thomas to midnight. Text (480) 639-4722.",
        "keywords": "skip Phoenix urgent care line, text NP from car Phoenix, after hours telehealth Phoenix AZ, NextCare Thomas midnight, $59 text visit Phoenix",
        "answer": "You are in Phoenix. It is evening or Saturday. The problem is not vague — UTI, sinus, a tooth, an ear, or something else on the conditions list. Order: 911 if it is an emergency, a room if you need hands or a film, a text if the story is still text-safe. $59 after care. We did not time anyone's wait.",
        "howto": [
            {"name": "Decide if this is 911 or a room", "text": "Call 911 or go to an ER for emergencies. Go to an urgent-care room for films, stitches, a possible break, or a hands-on exam."},
            {"name": "If it is evening, treat heat as part of the plan", "text": "August in a Phoenix lot is not a slogan. Drink water. Do not sit in a closed car with a child. You can still change your mind and text from the driveway."},
            {"name": "Check whether the story is text-safe", "text": "Good candidates include uncomplicated UTI, sinus, strep or ear without red flags, dental pain as a bridge, and ED when appropriate."},
            {"name": "Text from where you are", "text": "Text (480) 639-4722 in your own words. Chris Woods, MSN, APRN, FNP-C, reads it. Same NP. No video."},
            {"name": "Pay after, only if care happened", "text": "The visit is $59 cash. Not a subscription. If text treatment is not appropriate, there is no charge."},
            {"name": "If the pharmacy is closed, plan the pickup", "text": "A Saturday night visit can still be reviewed. The bottle waits until the store opens. NextCare Thomas is the posted late brick door if you still need a building."},
            {"name": "Know when to abandon the thread", "text": "If new fever and back pain show up, if you start vomiting, if swelling spreads, stop texting and go in."},
        ],
        "faqs": [
            {
                "q": "How do I skip the Phoenix urgent care line from my phone?",
                "a": "If it is not 911 and not a room, text (480) 639-4722. Say you are in Phoenix and what started. Chris reads it. $59 after care if text treatment is appropriate.",
                "a_text": "If it is not an emergency and not a room problem, text (480) 639-4722 from where you are. Same NP. $59 after care if text treatment is appropriate.",
            },
            {
                "q": "What if it is Saturday night in Phoenix?",
                "a": "HonorHealth posts 7 a.m. to 7 p.m. Several Banner Phoenix pages post 8 a.m. to 8 p.m. NextCare Thomas posts 8 a.m. to midnight. A text can still be reviewed if the story is text-safe. Pharmacy hours are a separate clock.",
                "a_text": "HonorHealth posts 7 a.m. to 7 p.m. Banner Phoenix pages we read post 8 a.m. to 8 p.m. NextCare Thomas posts 8 a.m. to midnight. A text can still be reviewed if the story is text-safe.",
            },
            {
                "q": "What if the pharmacy is closed?",
                "a": "The visit can still be reviewed. The bottle waits until the store opens. A midnight text does not open a closed pharmacy.",
                "a_text": "A prescription can still be sent. Pickup waits until that pharmacy opens. A midnight text does not open a closed pharmacy.",
            },
            {
                "q": "Do I pay if the text is not safe?",
                "a": "No. When it is not safe, Chris says so. You do not pay.",
                "a_text": "No. If text treatment is not appropriate, there is no charge.",
            },
        ],
        "body": f"""      <p>You are in Phoenix. It is evening or Saturday. The problem is not vague — it is a UTI, sinus, a tooth, an ear, or something else on the <a href="https://npcwoods.com/conditions/">conditions list</a>. You are looking at a parking lot.</p>
      <p>This is an order of operations. It is not a promise that a lobby is empty. We did not time anyone's wait.</p>
      <div class="steps">
        <div class="step" id="step-1"><div class="step-num">1</div><div class="step-content"><h3>Decide if this is 911 or a room</h3>
          <p>Call 911 or go to an ER for chest pain, trouble breathing, stroke signs, severe bleeding, a belly that is rigid, or a child who looks truly sick.</p>
          <p>Go to an urgent-care <strong>room</strong> (not a text) if you need a film, stitches, a wound looked at, a possible break, or a hands-on exam. HonorHealth Phoenix urgent cares post <strong>7 a.m.-7 p.m. daily</strong>. Several Banner Phoenix pages post <strong>8 a.m.-8 p.m. daily</strong>. Dignity Ahwatukee posts <strong>8 a.m.-7 p.m. daily</strong>. NextCare's Thomas Road door posts <strong>8 a.m.-midnight daily</strong> — the late brick option if you still need a building. MinuteClinic hours are shorter and include a lunch close.</p>
          <p>Phoenix Children's urgent cares (Glendale, Scottsdale, Mesa) post weekday evenings <strong>5 p.m.-11 p.m.</strong> and weekends <strong>10 a.m.-7 p.m.</strong>, schedule-ahead. That is for children, not a text practice.</p>
          <p>NPCWoods has no Phoenix door.</p>
        </div></div>
        <div class="step" id="step-2"><div class="step-num">2</div><div class="step-content"><h3>If it is evening, treat heat as part of the plan</h3>
          <p>August in a Phoenix lot is not a slogan. If you are already sitting in a car on Loop 101 or off I-10 because you thought you needed the lobby, you can still change your mind. Drink water. Do not sit in a closed car with a child. If you feel faint, get into air conditioning and rethink 911.</p>
          <p>This is not a wait-time claim. It is why some people text from the driveway.</p>
        </div></div>
        <div class="step" id="step-3"><div class="step-num">3</div><div class="step-content"><h3>Check whether the story is text-safe</h3>
          <p>Good candidates: uncomplicated <a href="https://npcwoods.com/uti-treatment/phoenix-az/">UTI</a>, a <a href="https://npcwoods.com/sinus-infection-treatment/">sinus</a> pattern that might need a closer look, <a href="https://npcwoods.com/ear-infection-treatment/">strep or ear</a> without red flags, <a href="https://npcwoods.com/dental-pain/">dental pain</a> as a bridge to a dentist, <a href="https://npcwoods.com/ed-treatment/">ED</a> when appropriate.</p>
          <p>Bad candidates: fever with flank pain, pregnancy plus urinary symptoms that have not been evaluated in person, vomiting so you cannot take a pill, spreading face or neck swelling, a child under 2, anything that needs a room.</p>
          <p>When it is not safe, <a href="https://npcwoods.com/how-it-works/">how it works</a> is simple: Chris says so. You do not pay.</p>
        </div></div>
        <div class="step" id="step-4"><div class="step-num">4</div><div class="step-content"><h3>Text from where you are</h3>
          <p>Text {PHONE}. Use your own words. "I'm in Phoenix. It burns when I pee. Started this morning. No fever." That is enough to start.</p>
          <p>Chris Woods, MSN, APRN, FNP-C, reads it. Same NP every time. No video. No app. You must be physically in Arizona or another licensed state.</p>
          <p>He will ask a few questions. If a prescription is appropriate, it goes to the pharmacy you name. Fry's, Walgreens, CVS, Costco, the one you actually use. Pharmacy hours are their own clock — a midnight text does not open a closed pharmacy.</p>
        </div></div>
        <div class="step" id="step-5"><div class="step-num">5</div><div class="step-content"><h3>Pay after, only if care happened</h3>
          <p>The visit is <a href="https://npcwoods.com/pricing/">$59 cash</a>. Not a subscription. Pay after care. If text treatment is not appropriate, there is no charge.</p>
          <p>That is the opposite of a membership video clinic. It is also not a fight with a national marketplace on the sticker. The point is the same nurse practitioner and no camera.</p>
        </div></div>
        <div class="step" id="step-6"><div class="step-num">6</div><div class="step-content"><h3>If the pharmacy is closed, plan the pickup</h3>
          <p>A Saturday night sinus visit can still be reviewed. The bottle waits until the store opens. If you cannot wait and you need a room tonight, NextCare Thomas is the posted late door we verified. An ER is the door for emergencies.</p>
        </div></div>
        <div class="step" id="step-7"><div class="step-num">7</div><div class="step-content"><h3>Know when to abandon the thread</h3>
          <p>If new fever and back pain show up, if you start vomiting, if swelling spreads, stop texting and go in. <a href="https://npcwoods.com/faq/">FAQ</a>. <a href="https://npcwoods.com/arizona-telemedicine/">Arizona page</a>. <a href="https://npcwoods.com/credentials/">Credentials</a>.</p>
          <p>Weekend primary-care offices are closed. That is why urgent care exists. Text is only the subset that does not need the room.</p>
        </div></div>
      </div>
""",
    },
]


def main() -> int:
    written = []
    for page in PAGES:
        dest = ROOT / "landing-pages" / page["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        html = render(page)
        dest.write_text(html, encoding="utf-8")
        written.append((page["slug"], dest, dest.stat().st_size))
        print(f"[ok] {page['slug']} -> {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes)")
    banned = ("insurance", " doctor", "physician", " MD", "board-certified")
    # "double board-certified" is allowed; scan leftover bare board-certified after stripping that phrase
    for slug, dest, _ in written:
        text = dest.read_text(encoding="utf-8").lower()
        scrubbed = text.replace("double board-certified", "")
        hits = [w.strip() for w in banned if w in scrubbed]
        if hits:
            raise SystemExit(f"[blocked] {slug} still has banned language: {hits}")
        if "sms:4806394722" not in text:
            raise SystemExit(f"[blocked] {slug} missing sms CTA")
        if "$59" not in dest.read_text(encoding="utf-8"):
            raise SystemExit(f"[blocked] {slug} missing $59")
    print("[ok] compliance scan passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
