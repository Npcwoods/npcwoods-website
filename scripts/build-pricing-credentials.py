#!/usr/bin/env python3
"""
Build /pricing/ and /credentials/ pages by assembling shared header + footer
with page-specific head + body content. Idempotent — rerun any time.

Reads from:
  html/shared/header-snippet.html
  html/shared/footer-snippet.html

Writes to:
  landing-pages/pricing/index.html
  landing-pages/credentials/index.html

Conventions matched from landing-pages/how-it-works/index.html:
- GTM-59QSWZRC + gtag G-EFFRQMG8TC + AW-610222919
- DM Sans + DM Serif Display + Inter fonts
- Brand blue #2563EB, gold #F59E0B, shadow-soft pattern
- Schema: MedicalBusiness + BreadcrumbList + FAQPage + Person
- Banned words enforced: no "doctor", no "insurance", no "Text a Doctor"
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADER = (ROOT / "html/shared/header-snippet.html").read_text()
FOOTER = (ROOT / "html/shared/footer-snippet.html").read_text()

BANNED = [
    (r"\bdoctor\b", "doctor (Chris is a Licensed NP)"),
    (r"\binsurance\b", "insurance (use 'cash rate', 'flat fee')"),
    (r"Text a Doctor", "'Text a Doctor' (banned phrase)"),
    (r"\bboard-certified\b(?<!double board-certified)", "bare 'board-certified' — use 'double board-certified' or 'Licensed NP'"),
]


def validate(html: str, label: str):
    """Check visible copy for banned words. Strips URL attributes (href/src/content=url)
    since pre-existing links like /affordable-telemedicine-arizona-no-insurance/ and
    doctor.webmd.com are legitimate and not customer-facing copy."""
    # Strip attribute values that are URLs
    stripped = re.sub(r'(?:href|src|action|content|cite-as|canonical)\s*=\s*"[^"]*"', '', html, flags=re.IGNORECASE)
    stripped = re.sub(r"(?:href|src|action|content|cite-as|canonical)\s*=\s*'[^']*'", '', stripped, flags=re.IGNORECASE)
    # Strip URL string values inside JSON-LD (e.g. "https://doctor.webmd.com/..." in sameAs arrays)
    stripped = re.sub(r'"https?://[^"\s]+"', '""', stripped)
    errors = []
    for pat, reason in BANNED:
        if pat == r"\bboard-certified\b(?<!double board-certified)":
            for m in re.finditer(r"board-certified", stripped, re.IGNORECASE):
                start = max(0, m.start() - 7)
                lead = stripped[start:m.start()].lower()
                if "double " not in lead:
                    errors.append(f"  {label}: bare 'board-certified' at char {m.start()}")
            continue
        for m in re.finditer(pat, stripped, re.IGNORECASE):
            ctx_start = max(0, m.start() - 40)
            ctx_end = min(len(stripped), m.end() + 40)
            errors.append(f"  {label}: banned '{m.group()}' at char {m.start()} — {reason} | context: ...{stripped[ctx_start:ctx_end]!r}...")
    return errors


# ============================================================================
# SHARED <head> BOILERPLATE (GTM, gtag, fonts, preconnect)
# ============================================================================

HEAD_TRACKING = """<!-- NPCWoods Tracking: GTM -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-59QSWZRC');</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EFFRQMG8TC"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-EFFRQMG8TC');
gtag('config', 'AW-610222919');
</script>"""

HEAD_FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&amp;family=DM+Serif+Display:ital@0;1&amp;family=Inter:wght@400;500;600;700;800&amp;display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&amp;family=DM+Serif+Display:ital@0;1&amp;family=Inter:wght@400;500;600;700;800&amp;display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&amp;family=DM+Serif+Display:ital@0;1&amp;family=Inter:wght@400;500;600;700;800&amp;display=swap"></noscript>
<link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="apple-touch-icon" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">"""

# Crawler directives — give Google and LLMs maximum extractability
CRAWLER_META = """<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="bingbot" content="index, follow">
<meta name="author" content="Chris Woods, MSN, APRN, FNP-C">
<meta name="publisher" content="NPCWoods Telemedicine">
<meta name="geo.region" content="US">
<meta name="format-detection" content="telephone=yes">
<meta http-equiv="content-language" content="en-US">
<link rel="author" href="https://npcwoods.com/about/">
<link rel="publisher" href="https://npcwoods.com/">
<link rel="alternate" type="application/llms.txt" href="https://npcwoods.com/llms.txt">
<link rel="alternate" type="application/llms-full.txt" href="https://npcwoods.com/llms-full.txt">"""

# Shared base CSS tokens + utility classes pulled from how-it-works/index.html
BASE_CSS = """<style>
:root {
  --white: #FFFFFF;
  --off-white: #F7F8FA;
  --paper: #FBFCFE;
  --text-primary: #1A1A2E;
  --text-body: #4A4A5A;
  --text-muted: #8E8E9A;
  --brand: #2563EB;
  --brand-hover: #1D4ED8;
  --brand-light: #EFF6FF;
  --brand-soft: #DBEAFE;
  --brand-deep: #1A4FD4;
  --gold: #F59E0B;
  --gold-soft: #FEF3C7;
  --success: #16A34A;
  --success-light: #DCFCE7;
  --danger: #DC2626;
  --danger-light: #FEE2E2;
  --border: #E5E7EB;
  --shadow: 0 16px 50px rgba(26, 26, 46, 0.10);
  --shadow-soft: 0 8px 28px rgba(37, 99, 235, 0.10);
  --container-max: 1180px;
  --content-max: 1040px;
  --section-pad: 96px;
  --side-pad: 24px;
}
* ,*::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body { background: var(--white); color: var(--text-body); font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.65; overflow-x: hidden; -webkit-font-smoothing: antialiased; }
img { display: block; max-width: 100%; height: auto; }
a { color: inherit; text-decoration: none; }
:focus-visible { outline: 2px solid var(--brand); outline-offset: 2px; border-radius: 6px; }
.container { max-width: var(--container-max); margin: 0 auto; padding: 0 var(--side-pad); }
.section-shell { max-width: var(--content-max); margin: 0 auto; }
.section-label { font-family: 'DM Sans', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--brand); margin-bottom: 14px; }
.section-heading { font-family: 'DM Serif Display', serif; font-size: clamp(2rem, 4vw, 3.25rem); line-height: 1.08; color: var(--text-primary); margin-bottom: 18px; letter-spacing: -0.02em; }
.section-sub { font-size: 1.05rem; color: var(--text-body); max-width: 720px; }

/* Hero */
.hero { position: relative; overflow: hidden; background: linear-gradient(160deg, #1a4fd4 0%, #2563EB 25%, #3b82f6 50%, #60a5fa 75%, #93c5fd 100%); padding: clamp(72px, 12vw, 140px) 0 clamp(96px, 14vw, 180px); }
.hero::before { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.18), transparent 55%); pointer-events: none; }
.hero-inner { position: relative; z-index: 1; max-width: var(--content-max); margin: 0 auto; padding: 0 var(--side-pad); text-align: center; }
.hero-badge { display: inline-flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.26); color: #FFFFFF; font-family: 'DM Sans', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; border-radius: 999px; padding: 9px 18px; margin-bottom: 26px; backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
.hero-badge-dot { width: 7px; height: 7px; border-radius: 50%; background: #4ADE80; box-shadow: 0 0 0 4px rgba(74,222,128,0.18); }
.hero h1 { font-family: 'DM Serif Display', serif; font-size: clamp(2.6rem, 6vw, 4.8rem); line-height: 1.02; color: #FFFFFF; letter-spacing: -0.03em; margin-bottom: 22px; text-shadow: 0 2px 24px rgba(0,0,0,0.12); }
.hero-sub { font-size: clamp(1.05rem, 1.5vw, 1.2rem); color: rgba(255,255,255,0.92); max-width: 680px; margin: 0 auto 32px; }
.hero-sub strong { color: #FFFFFF; }
.btn-row { display: inline-flex; gap: 14px; flex-wrap: wrap; justify-content: center; }
.btn-primary, .btn-secondary, .btn-dark { display: inline-flex; align-items: center; justify-content: center; gap: 10px; min-height: 56px; padding: 16px 30px; border-radius: 16px; font-family: 'DM Sans', sans-serif; font-size: 0.98rem; font-weight: 700; transition: transform 0.2s, box-shadow 0.2s, background 0.2s, border-color 0.2s; border: none; cursor: pointer; }
.btn-primary { background: #FFFFFF; color: var(--brand); box-shadow: 0 12px 28px rgba(15, 23, 42, 0.16); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 18px 34px rgba(15, 23, 42, 0.22); }
.btn-secondary { background: rgba(255,255,255,0.14); color: #FFFFFF; border: 1px solid rgba(255,255,255,0.28); backdrop-filter: blur(8px); }
.btn-secondary:hover { transform: translateY(-2px); background: rgba(255,255,255,0.22); }
.btn-dark { background: var(--brand); color: #FFFFFF; box-shadow: 0 14px 30px rgba(37, 99, 235, 0.25); }
.btn-dark:hover { background: var(--brand-hover); transform: translateY(-2px); }

/* Content sections */
.section { padding: clamp(64px, 8vw, var(--section-pad)) 0; }
.section.alt { background: var(--off-white); }
.section-head { text-align: center; margin-bottom: 56px; }
.section-head .section-sub { margin: 0 auto; }

/* Cards */
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }
.card { background: #FFFFFF; border: 1px solid var(--border); border-radius: 20px; padding: 28px; box-shadow: var(--shadow-soft); transition: transform 0.2s, box-shadow 0.2s; }
.card:hover { transform: translateY(-4px); box-shadow: var(--shadow); }
.card h3 { font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: var(--text-primary); margin-bottom: 10px; line-height: 1.15; }
.card p { color: var(--text-body); font-size: 0.98rem; }
.card-icon { width: 48px; height: 48px; border-radius: 12px; background: var(--brand-light); color: var(--brand); display: flex; align-items: center; justify-content: center; margin-bottom: 18px; }
.card-icon svg { width: 24px; height: 24px; }

/* Price spotlight */
.price-hero { display: flex; flex-direction: column; align-items: center; gap: 10px; margin-bottom: 24px; }
.price-huge { font-family: 'DM Serif Display', serif; font-size: clamp(4.5rem, 14vw, 9rem); line-height: 0.95; color: #FFFFFF; letter-spacing: -0.04em; text-shadow: 0 4px 40px rgba(0,0,0,0.15); }
.price-meta { display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.3); backdrop-filter: blur(8px); color: #FFFFFF; font-family: 'DM Sans', sans-serif; font-size: 0.85rem; font-weight: 600; padding: 6px 14px; border-radius: 100px; }

/* Comparison table */
.compare { max-width: 980px; margin: 0 auto; background: #FFFFFF; border-radius: 24px; border: 1px solid var(--border); overflow: hidden; box-shadow: var(--shadow); }
.compare-row { display: grid; grid-template-columns: 1.2fr 0.8fr 1fr; gap: 16px; padding: 22px 28px; align-items: center; border-bottom: 1px solid var(--border); }
.compare-row:last-child { border-bottom: none; }
.compare-row.header { background: var(--off-white); font-family: 'DM Sans', sans-serif; font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); font-weight: 700; }
.compare-row.highlight { background: linear-gradient(135deg, rgba(37,99,235,0.06), rgba(37,99,235,0.02)); }
.compare-who { font-family: 'DM Sans', sans-serif; font-weight: 700; color: var(--text-primary); font-size: 1.05rem; }
.compare-who .tag { display: inline-block; margin-left: 8px; padding: 2px 8px; background: var(--brand); color: #FFFFFF; border-radius: 100px; font-size: 0.65rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
.compare-price { font-family: 'DM Serif Display', serif; font-size: 1.5rem; color: var(--text-primary); }
.compare-price.brand { color: var(--brand); }
.compare-note { font-size: 0.9rem; color: var(--text-body); }
@media (max-width: 720px) {
  .compare-row { grid-template-columns: 1fr; gap: 6px; padding: 18px 22px; }
  .compare-row.header { display: none; }
  .compare-price { font-size: 1.7rem; }
}

/* List items with checkmarks */
.check-list { list-style: none; padding: 0; margin: 0; display: grid; gap: 14px; }
.check-list li { display: flex; gap: 14px; align-items: flex-start; font-size: 1.02rem; color: var(--text-body); line-height: 1.55; }
.check-list li::before { content: ''; display: inline-block; flex-shrink: 0; margin-top: 3px; width: 22px; height: 22px; border-radius: 50%; background: var(--success-light) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2316A34A' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'/%3E%3C/svg%3E") center/13px no-repeat; }
.ex-list { list-style: none; padding: 0; margin: 0; display: grid; gap: 14px; }
.ex-list li { display: flex; gap: 14px; align-items: flex-start; font-size: 1.02rem; color: var(--text-body); line-height: 1.55; }
.ex-list li::before { content: ''; display: inline-block; flex-shrink: 0; margin-top: 3px; width: 22px; height: 22px; border-radius: 50%; background: var(--danger-light) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23DC2626' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='6' x2='6' y2='18'/%3E%3Cline x1='6' y1='6' x2='18' y2='18'/%3E%3C/svg%3E") center/13px no-repeat; }

/* Credential blocks */
.cred-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; }
.cred-card { background: #FFFFFF; border: 1px solid var(--border); border-radius: 18px; padding: 22px; }
.cred-label { font-family: 'DM Sans', sans-serif; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px; }
.cred-value { font-family: 'DM Serif Display', serif; font-size: 1.35rem; color: var(--text-primary); line-height: 1.2; margin-bottom: 6px; }
.cred-link { font-size: 0.87rem; color: var(--brand); font-weight: 600; display: inline-flex; align-items: center; gap: 6px; }
.cred-link:hover { color: var(--brand-hover); text-decoration: underline; }
.cred-link::after { content: '↗'; font-size: 0.85em; }

/* License table */
.license-table { width: 100%; max-width: 980px; margin: 0 auto; background: #FFFFFF; border-radius: 20px; border: 1px solid var(--border); overflow: hidden; box-shadow: var(--shadow-soft); }
.license-row { display: grid; grid-template-columns: 1.1fr 1fr 120px; gap: 16px; padding: 18px 24px; align-items: center; border-bottom: 1px solid var(--border); }
.license-row:last-child { border-bottom: none; }
.license-row.header { background: var(--off-white); font-family: 'DM Sans', sans-serif; font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); font-weight: 700; }
.license-state { font-family: 'DM Sans', sans-serif; font-weight: 700; color: var(--text-primary); font-size: 1rem; display: flex; align-items: center; gap: 10px; }
.license-state::before { content: ''; width: 8px; height: 8px; border-radius: 50%; background: var(--success); box-shadow: 0 0 0 3px var(--success-light); flex-shrink: 0; }
.license-board { font-size: 0.92rem; color: var(--text-body); }
.license-verify { font-size: 0.83rem; color: var(--brand); font-weight: 700; text-align: right; white-space: nowrap; }
.license-verify:hover { text-decoration: underline; }
@media (max-width: 720px) {
  .license-row { grid-template-columns: 1fr; gap: 4px; padding: 14px 20px; }
  .license-row.header { display: none; }
  .license-verify { text-align: left; }
}

/* FAQ */
.faq-list { max-width: 820px; margin: 0 auto; display: grid; gap: 12px; }
.faq-item { background: #FFFFFF; border: 1px solid var(--border); border-radius: 14px; padding: 0; overflow: hidden; transition: border-color 0.2s; }
.faq-item[open] { border-color: var(--brand-soft); box-shadow: var(--shadow-soft); }
.faq-item summary { list-style: none; padding: 20px 24px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 16px; font-family: 'DM Sans', sans-serif; font-weight: 700; color: var(--text-primary); font-size: 1.04rem; }
.faq-item summary::-webkit-details-marker { display: none; }
.faq-item summary::after { content: '+'; font-family: 'DM Sans', sans-serif; font-size: 1.6rem; color: var(--brand); font-weight: 300; transition: transform 0.2s; }
.faq-item[open] summary::after { transform: rotate(45deg); }
.faq-answer { padding: 0 24px 22px; color: var(--text-body); font-size: 1rem; line-height: 1.65; }
.faq-answer p + p { margin-top: 10px; }

/* CTA section */
.cta-band { background: linear-gradient(135deg, #1a4fd4 0%, #2563EB 50%, #3b82f6 100%); color: #FFFFFF; text-align: center; padding: clamp(64px, 9vw, 104px) var(--side-pad); }
.cta-band h2 { font-family: 'DM Serif Display', serif; font-size: clamp(2rem, 4vw, 3rem); line-height: 1.1; margin-bottom: 16px; }
.cta-band p { font-size: 1.08rem; opacity: 0.92; max-width: 620px; margin: 0 auto 28px; }
.cta-phone { font-family: 'DM Sans', sans-serif; font-size: 0.9rem; color: rgba(255,255,255,0.78); margin-top: 16px; }
.cta-phone a { color: #FFFFFF; font-weight: 700; }
</style>"""


# ============================================================================
# PRICING PAGE
# ============================================================================

PRICING_HEAD = """<title>Pricing &mdash; $59 Flat Fee, Same-Day Care | NPCWoods</title>
<meta name="description" content="$59 flat fee for every NPCWoods text visit &mdash; no paperwork, no hidden fees, no surprise bills. Prescriptions sent to your pharmacy when appropriate. Licensed NP.">
<meta name="theme-color" content="#2563EB">
<meta name="keywords" content="telemedicine pricing, $59 telehealth, flat fee telemedicine, cash pay telehealth, affordable online care, no hidden fees telehealth">
<link rel="canonical" href="https://npcwoods.com/pricing/">
<link rel="cite-as" href="https://npcwoods.com/pricing/">

<meta property="og:type" content="website">
<meta property="og:url" content="https://npcwoods.com/pricing/">
<meta property="og:title" content="Pricing &mdash; $59 Flat Fee, Same-Day Care | NPCWoods">
<meta property="og:description" content="One price. One promise. $59 for a text-based visit with a licensed nurse practitioner. No paperwork, no hassle.">
<meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp">
<meta name="twitter:card" content="summary_large_image">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "MedicalBusiness",
      "@id": "https://npcwoods.com/#medical-business",
      "name": "NPCWoods Telemedicine",
      "alternateName": "NPCWoods",
      "url": "https://npcwoods.com/",
      "description": "Flat-fee text-based telehealth visits for $59 with a Licensed Nurse Practitioner. No paperwork, same-day response, prescriptions routed to your pharmacy when medically appropriate.",
      "telephone": "+14806394722",
      "priceRange": "$59",
      "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
      "logo": "https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg",
      "medicalSpecialty": "FamilyPractice",
      "employee": { "@id": "https://npcwoods.com/#chris-woods" },
      "areaServed": [
        { "@type": "State", "name": "Arizona" },
        { "@type": "State", "name": "Colorado" },
        { "@type": "State", "name": "Georgia" },
        { "@type": "State", "name": "Idaho" },
        { "@type": "State", "name": "Iowa" },
        { "@type": "State", "name": "Montana" },
        { "@type": "State", "name": "Nevada" },
        { "@type": "State", "name": "New Mexico" },
        { "@type": "State", "name": "North Carolina" },
        { "@type": "State", "name": "Oregon" },
        { "@type": "State", "name": "Utah" }
      ],
      "sameAs": [
        "https://www.legitscript.com/",
        "https://npiregistry.cms.hhs.gov/provider-view/1285125468"
      ]
    },
    {
      "@type": "Service",
      "@id": "https://npcwoods.com/pricing/#service",
      "name": "NPCWoods Async Telehealth Visit",
      "serviceType": "Asynchronous Telemedicine",
      "category": "Telehealth",
      "description": "A text-based telehealth visit with Chris Woods, MSN, APRN, FNP-C. Includes full clinical review, treatment plan, and prescription routed to your pharmacy when medically appropriate. Follow-up questions for the same visit are included.",
      "provider": { "@id": "https://npcwoods.com/#medical-business" },
      "areaServed": [
        { "@type": "State", "name": "Arizona" },
        { "@type": "State", "name": "Nevada" },
        { "@type": "State", "name": "New Mexico" },
        { "@type": "State", "name": "Utah" },
        { "@type": "State", "name": "Iowa" },
        { "@type": "State", "name": "Montana" },
        { "@type": "State", "name": "Colorado" },
        { "@type": "State", "name": "Idaho" },
        { "@type": "State", "name": "Oregon" },
        { "@type": "State", "name": "Georgia" },
        { "@type": "State", "name": "North Carolina" }
      ],
      "offers": {
        "@type": "Offer",
        "@id": "https://npcwoods.com/pricing/#offer-59",
        "name": "$59 Flat-Fee Async Telehealth Visit",
        "price": "59.00",
        "priceCurrency": "USD",
        "priceValidUntil": "2027-12-31",
        "availability": "https://schema.org/InStock",
        "eligibleRegion": { "@type": "Country", "name": "United States" },
        "description": "$59 flat fee, no paperwork, no hidden costs, no subscription. Cash-pay only.",
        "url": "https://npcwoods.com/pricing/",
        "priceSpecification": {
          "@type": "UnitPriceSpecification",
          "price": "59.00",
          "priceCurrency": "USD",
          "unitCode": "C62",
          "unitText": "per visit"
        }
      }
    },
    {
      "@type": "Product",
      "@id": "https://npcwoods.com/pricing/#product",
      "name": "$59 Async Telehealth Visit",
      "description": "Text-based visit with a Licensed Nurse Practitioner — $59 flat, no paperwork, same-day response, prescription sent to your pharmacy when appropriate.",
      "brand": { "@type": "Brand", "name": "NPCWoods Telemedicine" },
      "category": "Medical Service",
      "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
      "offers": { "@id": "https://npcwoods.com/pricing/#offer-59" }
    },
    {
      "@type": "WebPage",
      "@id": "https://npcwoods.com/pricing/",
      "url": "https://npcwoods.com/pricing/",
      "name": "Pricing — $59 Flat Fee, Same-Day Care | NPCWoods",
      "isPartOf": { "@type": "WebSite", "@id": "https://npcwoods.com/#website", "url": "https://npcwoods.com/", "name": "NPCWoods Telemedicine" },
      "about": { "@id": "https://npcwoods.com/pricing/#service" },
      "author": { "@id": "https://npcwoods.com/#chris-woods" },
      "publisher": { "@id": "https://npcwoods.com/#medical-business" },
      "datePublished": "2026-04-23",
      "dateModified": "2026-04-23",
      "inLanguage": "en-US",
      "primaryImageOfPage": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp"
    }
  ]
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://npcwoods.com/" },
    { "@type": "ListItem", "position": 2, "name": "Pricing", "item": "https://npcwoods.com/pricing/" }
  ]
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "@id": "https://npcwoods.com/pricing/#faq",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".faq-item summary", ".faq-answer p"]
  },
  "author": { "@id": "https://npcwoods.com/#chris-woods" },
  "publisher": { "@id": "https://npcwoods.com/#medical-business" },
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What does $59 include?",
      "acceptedAnswer": { "@type": "Answer", "text": "A full text-based visit with Chris Woods, a Licensed Nurse Practitioner. That means a real back-and-forth conversation about what's going on, a clinical review, a recommended plan, and a prescription sent to your pharmacy when it's medically appropriate. Follow-up questions for the same visit are included." }
    },
    {
      "@type": "Question",
      "name": "Are there hidden fees or surprise bills?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. $59 is the whole cost of the visit. There's no membership, no subscription, no facility fee, no separate prescription cost from us. You'll pay your pharmacy for the medication itself like any other prescription." }
    },
    {
      "@type": "Question",
      "name": "Do you accept payment plans or copays?",
      "acceptedAnswer": { "@type": "Answer", "text": "It's a flat $59 paid at the start of the visit by card. We don't bill any third parties, so there's nothing to file and nothing coming back in the mail six weeks later." }
    },
    {
      "@type": "Question",
      "name": "What if I don't need a prescription?",
      "acceptedAnswer": { "@type": "Answer", "text": "The $59 covers the visit itself, not the prescription. If the clinical picture doesn't call for medication, you'll still get a clear plan, guidance on when to escalate, and the same follow-up window. You paid for the evaluation, not a guaranteed script." }
    },
    {
      "@type": "Question",
      "name": "Can I get a refund if I'm not the right fit?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. If after reviewing what you send, Chris decides this is something better handled in person (or that you need urgent in-person care), we'll refund the visit and tell you what to do next. You won't pay for a visit we can't responsibly complete." }
    },
    {
      "@type": "Question",
      "name": "Is this cheaper than urgent care?",
      "acceptedAnswer": { "@type": "Answer", "text": "For straightforward infections, a retail urgent care cash rate usually runs $150-$250 for the visit alone, plus lab fees, plus whatever the pharmacy charges. Emergency rooms are far more than that. $59 is the full visit cost here — a fraction of what a walk-in clinic charges for the same kind of evaluation." }
    }
  ]
}
</script>"""

PRICING_BODY = """<!-- HERO -->
<section class="hero">
  <div class="hero-inner">
    <div class="hero-badge"><span class="hero-badge-dot"></span> One Price &middot; One Promise</div>
    <div class="price-hero">
      <div class="price-huge">$59</div>
      <div class="price-meta">Flat fee &middot; Same-day response &middot; No paperwork</div>
    </div>
    <h1>$59. One price. One promise.</h1>
    <p class="hero-sub">A full text-based visit with a <strong>Licensed Nurse Practitioner</strong>. No membership. No subscription. No surprise bills. If medication makes sense, it's sent to your pharmacy &mdash; that's it.</p>
    <div class="btn-row">
      <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" class="btn-primary">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
        Text Chris &mdash; Start My $59 Visit
      </a>
      <a href="https://npcwoods.com/credentials/" class="btn-secondary">See credentials &amp; licenses</a>
    </div>
    <p style="margin-top:24px;font-family:'DM Sans',sans-serif;font-size:0.78rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:rgba(255,255,255,0.78);">
      NPI 1285125468 &nbsp;&middot;&nbsp; LegitScript certified &nbsp;&middot;&nbsp; Licensed in 11 states
    </p>
  </div>
</section>

<!-- WHAT'S INCLUDED -->
<section class="section">
  <div class="container">
    <div class="section-head">
      <div class="section-label">What $59 gets you</div>
      <h2 class="section-heading">The whole visit. Not a teaser.</h2>
      <p class="section-sub">Every visit runs the same way &mdash; no upsells, no "premium tier." When you pay $59, this is what you're getting.</p>
    </div>
    <div class="section-shell">
      <ul class="check-list">
        <li><strong>A real clinical conversation.</strong> Text back and forth with Chris Woods, a Licensed Nurse Practitioner &mdash; not a chatbot, not a form, not a triage script.</li>
        <li><strong>Same-day response</strong> during clinic hours, and usually within minutes for acute infections like UTI, sinus, or strep.</li>
        <li><strong>A clear treatment plan</strong> in writing &mdash; what you have, what to do, what would change the plan, when to escalate.</li>
        <li><strong>Prescription to your pharmacy</strong> when it's medically appropriate. Sent electronically to whatever pharmacy you use.</li>
        <li><strong>Follow-up questions on the same visit</strong> are included. If symptoms change or the plan needs tweaking, text back &mdash; no new charge.</li>
        <li><strong>No paperwork, no copays to chase, no third-party billing.</strong> One flat charge to the card at the start and we're done.</li>
      </ul>
    </div>
  </div>
</section>

<!-- COMPARISON -->
<section class="section alt">
  <div class="container">
    <div class="section-head">
      <div class="section-label">The math on this</div>
      <h2 class="section-heading">$59 vs. what the same visit costs elsewhere</h2>
      <p class="section-sub">Cash rates for a single acute visit. Numbers below are typical ranges for sinus, UTI, strep-style visits in the Southwest &mdash; your exact local cash rate may vary.</p>
    </div>
    <div class="compare" role="table" aria-label="Cash price comparison">
      <div class="compare-row header" role="row">
        <div role="columnheader">Where you go</div>
        <div role="columnheader">Visit cost</div>
        <div role="columnheader">What that covers</div>
      </div>
      <div class="compare-row highlight" role="row">
        <div class="compare-who" role="cell">NPCWoods <span class="tag">You are here</span></div>
        <div class="compare-price brand" role="cell">$59</div>
        <div class="compare-note" role="cell">Full text-based visit, licensed NP, prescription routed if appropriate, follow-up included.</div>
      </div>
      <div class="compare-row" role="row">
        <div class="compare-who" role="cell">Retail urgent care (cash)</div>
        <div class="compare-price" role="cell">$150&ndash;$250</div>
        <div class="compare-note" role="cell">Visit only. Labs, imaging, and prescriptions usually billed separately on top.</div>
      </div>
      <div class="compare-row" role="row">
        <div class="compare-who" role="cell">Emergency room (cash)</div>
        <div class="compare-price" role="cell">$2,000+</div>
        <div class="compare-note" role="cell">Facility fee, provider fee, and any testing stacked on one bill. Appropriate for real emergencies &mdash; overkill for a UTI.</div>
      </div>
      <div class="compare-row" role="row">
        <div class="compare-who" role="cell">Subscription telehealth</div>
        <div class="compare-price" role="cell">$30&ndash;$50/mo</div>
        <div class="compare-note" role="cell">Recurring charge whether you use it or not. Most visits still add a per-visit copay.</div>
      </div>
    </div>
  </div>
</section>

<!-- WHAT'S NOT INCLUDED -->
<section class="section">
  <div class="container">
    <div class="section-head">
      <div class="section-label">Honest limits</div>
      <h2 class="section-heading">When $59 isn't the right answer</h2>
      <p class="section-sub">Telehealth has real limits. If your situation falls into one of these buckets, the right move is usually in-person care &mdash; and we'll tell you that up front.</p>
    </div>
    <div class="section-shell">
      <ul class="ex-list">
        <li><strong>Controlled substances.</strong> We don't prescribe opioids, benzodiazepines, ADHD stimulants, testosterone, or anything Schedule II&ndash;IV. That's a modality limit, not a price limit.</li>
        <li><strong>Conditions requiring a hands-on exam</strong> &mdash; chest pain, abdominal pain that won't localize, neurological symptoms, injuries needing imaging.</li>
        <li><strong>Chronic disease management</strong> &mdash; hypertension, diabetes, thyroid, ongoing mental health &mdash; is better done with a PCP who can run labs and see you longitudinally.</li>
        <li><strong>Pediatrics under age 2</strong>, or any presentation where a physical exam or vitals are clearly needed to rule out something serious.</li>
        <li><strong>Anything that feels like an emergency.</strong> If you're unsure whether it's an emergency, that usually means it's time to call 911 or head to the ER.</li>
      </ul>
    </div>
  </div>
</section>

<!-- STATES SERVED -->
<section class="section alt">
  <div class="container">
    <div class="section-head">
      <div class="section-label">Where this works</div>
      <h2 class="section-heading">Licensed in 11 states</h2>
      <p class="section-sub">You need to be physically located in one of these states at the time of the visit. Chris is a double board-certified Nurse Practitioner, licensed in:</p>
    </div>
    <div class="section-shell">
      <div class="card-grid" style="max-width:920px;margin:0 auto;">
        <div class="card"><a href="https://npcwoods.com/arizona-telemedicine/"><strong>Arizona</strong> &mdash; Phoenix, Scottsdale, Mesa, Tucson, Flagstaff</a></div>
        <div class="card"><a href="https://npcwoods.com/nevada-telemedicine/"><strong>Nevada</strong> &mdash; Las Vegas, Reno, Henderson</a></div>
        <div class="card"><a href="https://npcwoods.com/new-mexico-telemedicine/"><strong>New Mexico</strong> &mdash; Albuquerque, Santa Fe, Las Cruces</a></div>
        <div class="card"><a href="https://npcwoods.com/utah-telemedicine/"><strong>Utah</strong> &mdash; Salt Lake City, Provo, St. George</a></div>
        <div class="card"><a href="https://npcwoods.com/iowa-telemedicine/"><strong>Iowa</strong> &mdash; Des Moines, Cedar Rapids, Iowa City</a></div>
        <div class="card"><a href="https://npcwoods.com/montana-telemedicine/"><strong>Montana</strong> &mdash; Billings, Missoula, Bozeman</a></div>
        <div class="card"><a href="https://npcwoods.com/colorado-telemedicine/"><strong>Colorado</strong> &mdash; Denver, Colorado Springs, Boulder</a></div>
        <div class="card"><a href="https://npcwoods.com/idaho-telemedicine/"><strong>Idaho</strong> &mdash; Boise, Coeur d'Alene, Idaho Falls</a></div>
        <div class="card"><a href="https://npcwoods.com/oregon-telemedicine/"><strong>Oregon</strong> &mdash; Portland, Eugene, Bend</a></div>
        <div class="card"><a href="https://npcwoods.com/georgia-telemedicine/"><strong>Georgia</strong> &mdash; Atlanta, Athens, Savannah</a></div>
        <div class="card"><a href="https://npcwoods.com/north-carolina-telemedicine/"><strong>North Carolina</strong> &mdash; Charlotte, Raleigh, Asheville</a></div>
      </div>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="section">
  <div class="container">
    <div class="section-head">
      <div class="section-label">Questions &amp; answers</div>
      <h2 class="section-heading">People ask us this a lot</h2>
    </div>
    <div class="faq-list">
      <details class="faq-item"><summary>What does $59 include?</summary><div class="faq-answer"><p>A full text-based visit with Chris Woods, a Licensed Nurse Practitioner. That means a real back-and-forth conversation about what's going on, a clinical review, a recommended plan, and a prescription sent to your pharmacy when it's medically appropriate. Follow-up questions for the same visit are included.</p></div></details>
      <details class="faq-item"><summary>Are there hidden fees or surprise bills?</summary><div class="faq-answer"><p>No. $59 is the whole cost of the visit. There's no membership, no subscription, no facility fee, no separate prescription cost from us. You'll pay your pharmacy for the medication itself like any other prescription.</p></div></details>
      <details class="faq-item"><summary>What if I don't need a prescription?</summary><div class="faq-answer"><p>The $59 covers the visit itself, not the prescription. If the clinical picture doesn't call for medication, you'll still get a clear plan, guidance on when to escalate, and the same follow-up window. You paid for the evaluation, not a guaranteed script.</p></div></details>
      <details class="faq-item"><summary>Can I get a refund if I'm not the right fit?</summary><div class="faq-answer"><p>Yes. If after reviewing what you send, Chris decides this is something better handled in person (or that you need urgent in-person care), we refund the visit and tell you what to do next. You won't pay for a visit we can't responsibly complete.</p></div></details>
      <details class="faq-item"><summary>Is this cheaper than urgent care?</summary><div class="faq-answer"><p>For a routine acute visit (UTI, sinus, strep, yeast, pink eye), a retail urgent care cash rate is usually $150-$250 for the visit alone, plus lab fees, plus whatever the pharmacy charges. Emergency rooms are far more than that. $59 is the full visit cost here &mdash; a fraction of what a walk-in clinic charges for the same kind of evaluation.</p></div></details>
      <details class="faq-item"><summary>Why not a monthly membership?</summary><div class="faq-answer"><p>Because most people who need a telehealth visit need it once a quarter, not once a week. A $59 flat fee paid when you actually need care is cheaper than $30-$50/mo running in the background and still adding a copay per visit. Simple beats sticky.</p></div></details>
      <details class="faq-item"><summary>Can I use an HSA or FSA card?</summary><div class="faq-answer"><p>Yes &mdash; HSA and FSA cards are accepted the same as any other card. Telehealth visits with a licensed clinician are qualified medical expenses. Save your receipt if your administrator asks.</p></div></details>
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="cta-band">
  <h2>$59 and a text away.</h2>
  <p>Text Chris now. Describe what's going on. Get a real plan today.</p>
  <div class="btn-row">
    <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" class="btn-primary">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
      Text Chris &mdash; Start My $59 Visit
    </a>
  </div>
  <p class="cta-phone">Or call <a href="tel:4806394722">(480) 639-4722</a> &middot; 7 days a week</p>
</section>"""


# ============================================================================
# CREDENTIALS PAGE
# ============================================================================

CREDENTIALS_HEAD = """<title>Credentials &mdash; Chris Woods, MSN, APRN, FNP-C | NPCWoods</title>
<meta name="description" content="Chris Woods, MSN, APRN, FNP-C &mdash; Licensed Nurse Practitioner in 11 states. NPI, state license verification links, LegitScript-certified. Verify every credential yourself.">
<meta name="theme-color" content="#2563EB">
<meta name="keywords" content="chris woods nurse practitioner, NPCWoods credentials, verify nurse practitioner, NPI 1285125468, FNP-C credentials, licensed nurse practitioner 11 states">
<link rel="canonical" href="https://npcwoods.com/credentials/">
<link rel="cite-as" href="https://npcwoods.com/credentials/">

<meta property="og:type" content="profile">
<meta property="og:url" content="https://npcwoods.com/credentials/">
<meta property="og:title" content="Credentials &mdash; Chris Woods, MSN, APRN, FNP-C | NPCWoods">
<meta property="og:description" content="Every license, every board, every verification link. A real clinician with real credentials &mdash; verify them yourself.">
<meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp">
<meta name="twitter:card" content="summary_large_image">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://npcwoods.com/#chris-woods",
      "url": "https://npcwoods.com/credentials/",
      "name": "Chris Woods",
      "alternateName": "Christopher Woods",
      "honorificSuffix": "MSN, APRN, FNP-C",
      "jobTitle": "Nurse Practitioner",
      "description": "Chris Woods, MSN, APRN, FNP-C is a double board-certified Licensed Nurse Practitioner practicing asynchronous telemedicine through NPCWoods. Licensed in 11 U.S. states.",
      "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
      "worksFor": { "@id": "https://npcwoods.com/#medical-business" },
      "makesOffer": {
        "@type": "Offer",
        "name": "$59 Async Telehealth Visit",
        "price": "59.00",
        "priceCurrency": "USD",
        "url": "https://npcwoods.com/pricing/"
      },
      "identifier": [
        { "@type": "PropertyValue", "propertyID": "NPI", "value": "1285125468", "url": "https://npiregistry.cms.hhs.gov/provider-view/1285125468" }
      ],
      "hasCredential": [
        { "@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "Master of Science in Nursing (MSN)" },
        { "@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "Family Nurse Practitioner - Certified (FNP-C)", "recognizedBy": { "@type": "Organization", "name": "American Association of Nurse Practitioners Certification Board", "url": "https://www.aanpcert.org/" } },
        { "@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": "Advanced Practice Registered Nurse (APRN)" }
      ],
      "knowsAbout": ["Family Practice", "Primary Care", "Urgent Care", "Telemedicine", "Asynchronous Telemedicine", "Text-Based Telehealth", "UTI Treatment", "Sinus Infection", "Strep Throat", "Pink Eye", "Yeast Infection"],
      "memberOf": [
        { "@type": "Organization", "name": "American Association of Nurse Practitioners", "url": "https://www.aanp.org/" }
      ],
      "sameAs": [
        "https://npiregistry.cms.hhs.gov/provider-view/1285125468",
        "https://www.healthgrades.com/providers/christopher-woods-xynt5wl",
        "https://doctor.webmd.com/doctor/christopher-woods-7b55e933-62ef-4d7b-975c-9cfc40eb3ad8-overview"
      ]
    },
    {
      "@type": "MedicalBusiness",
      "@id": "https://npcwoods.com/#medical-business",
      "name": "NPCWoods Telemedicine",
      "url": "https://npcwoods.com/",
      "logo": "https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg",
      "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
      "telephone": "+14806394722",
      "priceRange": "$59",
      "employee": { "@id": "https://npcwoods.com/#chris-woods" },
      "medicalSpecialty": "FamilyPractice"
    },
    {
      "@type": "WebPage",
      "@id": "https://npcwoods.com/credentials/",
      "url": "https://npcwoods.com/credentials/",
      "name": "Credentials — Chris Woods, MSN, APRN, FNP-C | NPCWoods",
      "isPartOf": { "@type": "WebSite", "@id": "https://npcwoods.com/#website", "url": "https://npcwoods.com/", "name": "NPCWoods Telemedicine" },
      "about": { "@id": "https://npcwoods.com/#chris-woods" },
      "author": { "@id": "https://npcwoods.com/#chris-woods" },
      "publisher": { "@id": "https://npcwoods.com/#medical-business" },
      "datePublished": "2026-04-23",
      "dateModified": "2026-04-23",
      "inLanguage": "en-US",
      "primaryImageOfPage": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
      "speakable": {
        "@type": "SpeakableSpecification",
        "cssSelector": [".cred-card", ".hero-sub"]
      }
    }
  ]
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://npcwoods.com/" },
    { "@type": "ListItem", "position": 2, "name": "Credentials", "item": "https://npcwoods.com/credentials/" }
  ]
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "@id": "https://npcwoods.com/credentials/#faq",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".faq-item summary", ".faq-answer p"]
  },
  "author": { "@id": "https://npcwoods.com/#chris-woods" },
  "publisher": { "@id": "https://npcwoods.com/#medical-business" },
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Who is Chris Woods and what are his credentials?",
      "acceptedAnswer": { "@type": "Answer", "text": "Chris Woods is a Licensed Nurse Practitioner with an MSN (Master of Science in Nursing), APRN designation, and FNP-C certification (Family Nurse Practitioner - Certified). He is double board-certified and licensed to practice in 11 states. His NPI number is 1285125468 and is verifiable in the CMS NPI Registry." }
    },
    {
      "@type": "Question",
      "name": "What does FNP-C mean?",
      "acceptedAnswer": { "@type": "Answer", "text": "FNP-C stands for Family Nurse Practitioner - Certified, a board certification granted by the American Association of Nurse Practitioners Certification Board (AANPCB). It certifies advanced clinical competence across the family lifespan &mdash; pediatrics, adults, and geriatrics. It's separate from the state license that authorizes practice." }
    },
    {
      "@type": "Question",
      "name": "How do I verify Chris's license in my state?",
      "acceptedAnswer": { "@type": "Answer", "text": "Every state nursing board runs a free public license lookup. This page links directly to the verification tool for each state Chris is licensed in. Search by name: 'Christopher Woods' or 'Chris Woods' will return the active license record. You can also verify his federal NPI number (1285125468) at npiregistry.cms.hhs.gov." }
    },
    {
      "@type": "Question",
      "name": "Is NPCWoods Telemedicine LegitScript-certified?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. LegitScript verifies that the practice meets the standards required to advertise on Google, Meta, and other major platforms. The LegitScript seal is displayed on every page of the site and can be verified directly at legitscript.com." }
    },
    {
      "@type": "Question",
      "name": "Can I see Chris's profile on WebMD or Healthgrades?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes &mdash; Chris has public provider profiles on WebMD and Healthgrades. Both list his practice details and years of experience. Links are included in the third-party verifications section below." }
    }
  ]
}
</script>"""

CREDENTIALS_BODY = """<!-- HERO -->
<section class="hero">
  <div class="hero-inner">
    <div class="hero-badge"><span class="hero-badge-dot"></span> Verify everything yourself</div>
    <h1>Real credentials.<br>Verified proof.</h1>
    <p class="hero-sub">Chris Woods, <strong>MSN, APRN, FNP-C</strong> &mdash; a double board-certified Licensed Nurse Practitioner. Below: every license, every board link, every number you need to confirm what you're paying for before you text.</p>
    <div class="btn-row">
      <a href="#npi" class="btn-primary">See the NPI &amp; licenses</a>
      <a href="https://npcwoods.com/pricing/" class="btn-secondary">See $59 pricing</a>
    </div>
    <p style="margin-top:24px;font-family:'DM Sans',sans-serif;font-size:0.78rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:rgba(255,255,255,0.78);">
      NPI 1285125468 &nbsp;&middot;&nbsp; LegitScript certified &nbsp;&middot;&nbsp; 11 active state licenses
    </p>
  </div>
</section>

<!-- CORE CREDENTIALS -->
<section class="section" id="npi">
  <div class="container">
    <div class="section-head">
      <div class="section-label">Core credentials</div>
      <h2 class="section-heading">The short version</h2>
      <p class="section-sub">These are the identifiers and certifications that make NPCWoods a real clinical practice, not a referral hub or a marketing front.</p>
    </div>
    <div class="section-shell">
      <div class="cred-grid">
        <div class="cred-card">
          <div class="cred-label">Federal NPI number</div>
          <div class="cred-value">1285125468</div>
          <a class="cred-link" href="https://npiregistry.cms.hhs.gov/provider-view/1285125468" target="_blank" rel="noopener">Verify at CMS NPI Registry</a>
        </div>
        <div class="cred-card">
          <div class="cred-label">Graduate degree</div>
          <div class="cred-value">MSN</div>
          <p style="font-size:0.9rem;color:var(--text-body);">Master of Science in Nursing &mdash; the graduate degree required to practice as an advanced practice nurse.</p>
        </div>
        <div class="cred-card">
          <div class="cred-label">Advanced practice designation</div>
          <div class="cred-value">APRN</div>
          <p style="font-size:0.9rem;color:var(--text-body);">Advanced Practice Registered Nurse &mdash; the legal designation under which nurse practitioners prescribe and diagnose.</p>
        </div>
        <div class="cred-card">
          <div class="cred-label">Board certification</div>
          <div class="cred-value">FNP-C</div>
          <a class="cred-link" href="https://www.aanpcert.org/" target="_blank" rel="noopener">American Academy of Nurse Practitioners</a>
        </div>
        <div class="cred-card">
          <div class="cred-label">Practice certification</div>
          <div class="cred-value">Double board-certified</div>
          <p style="font-size:0.9rem;color:var(--text-body);">Certified across two distinct clinical specialties &mdash; a separate exam and continuing education track for each.</p>
        </div>
        <div class="cred-card">
          <div class="cred-label">Platform certification</div>
          <div class="cred-value">LegitScript</div>
          <a class="cred-link" href="https://www.legitscript.com/" target="_blank" rel="noopener">Verify LegitScript approval</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- LICENSES -->
<section class="section alt">
  <div class="container">
    <div class="section-head">
      <div class="section-label">Active state licenses</div>
      <h2 class="section-heading">Licensed in 11 states</h2>
      <p class="section-sub">Each state board link below is a direct line to that state's public license verification tool. Search "Christopher Woods" or "Chris Woods" to pull up the active record.</p>
    </div>
    <div class="license-table" role="table" aria-label="State licenses and verification links">
      <div class="license-row header" role="row">
        <div role="columnheader">State</div>
        <div role="columnheader">Licensing board</div>
        <div role="columnheader" style="text-align:right;">Verify</div>
      </div>
      <div class="license-row" role="row">
        <div class="license-state">Arizona</div>
        <div class="license-board">Arizona State Board of Nursing</div>
        <a class="license-verify" href="https://www.azbn.gov/licensure/verifications" target="_blank" rel="noopener">Verify &rarr;</a>
      </div>
      <div class="license-row" role="row">
        <div class="license-state">Colorado</div>
        <div class="license-board">Colorado Board of Nursing (DORA)</div>
        <a class="license-verify" href="https://www.colorado.gov/dora/licensing/Lookup/LicenseLookup.aspx" target="_blank" rel="noopener">Verify &rarr;</a>
      </div>
      <div class="license-row" role="row">
        <div class="license-state">Georgia</div>
        <div class="license-board">Georgia Board of Nursing</div>
        <a class="license-verify" href="https://verify.sos.ga.gov/verification/" target="_blank" rel="noopener">Verify &rarr;</a>
      </div>
      <div class="license-row" role="row">
        <div class="license-state">Idaho</div>
        <div class="license-board">Idaho Board of Nursing</div>
        <a class="license-verify" href="https://dopl.idaho.gov/online-services-license-search/" target="_blank" rel="noopener">Verify &rarr;</a>
      </div>
      <div class="license-row" role="row">
        <div class="license-state">Iowa</div>
        <div class="license-board">Iowa Board of Nursing</div>
        <a class="license-verify" href="https://ibonlineservices.iowa.gov/PublicPortal/Iowa/IBON/licenseVerification/licenseVerification.jsp" target="_blank" rel="noopener">Verify &rarr;</a>
      </div>
      <div class="license-row" role="row">
        <div class="license-state">Montana</div>
        <div class="license-board">Montana Board of Nursing</div>
        <a class="license-verify" href="https://ebiz.mt.gov/POL/Default.aspx" target="_blank" rel="noopener">Verify &rarr;</a>
      </div>
      <div class="license-row" role="row">
        <div class="license-state">Nevada</div>
        <div class="license-board">Nevada State Board of Nursing</div>
        <a class="license-verify" href="https://nsbn.state.nv.us/verifications/" target="_blank" rel="noopener">Verify &rarr;</a>
      </div>
      <div class="license-row" role="row">
        <div class="license-state">New Mexico</div>
        <div class="license-board">New Mexico Board of Nursing</div>
        <a class="license-verify" href="https://nmbon.sks.com/Verification" target="_blank" rel="noopener">Verify &rarr;</a>
      </div>
      <div class="license-row" role="row">
        <div class="license-state">North Carolina</div>
        <div class="license-board">North Carolina Board of Nursing</div>
        <a class="license-verify" href="https://portal.ncbon.com/verification/search.aspx" target="_blank" rel="noopener">Verify &rarr;</a>
      </div>
      <div class="license-row" role="row">
        <div class="license-state">Oregon</div>
        <div class="license-board">Oregon State Board of Nursing</div>
        <a class="license-verify" href="https://osbn.oregon.gov/OSBNVerification/Default.aspx" target="_blank" rel="noopener">Verify &rarr;</a>
      </div>
      <div class="license-row" role="row">
        <div class="license-state">Utah</div>
        <div class="license-board">Utah Division of Professional Licensing</div>
        <a class="license-verify" href="https://secure.utah.gov/llv/search/index.html" target="_blank" rel="noopener">Verify &rarr;</a>
      </div>
    </div>
  </div>
</section>

<!-- THIRD-PARTY VERIFICATIONS -->
<section class="section">
  <div class="container">
    <div class="section-head">
      <div class="section-label">Third-party records</div>
      <h2 class="section-heading">Not just our word for it</h2>
      <p class="section-sub">Public profiles and seals maintained by organizations we don't control.</p>
    </div>
    <div class="section-shell">
      <div class="card-grid">
        <div class="card">
          <div class="card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
          <h3>LegitScript</h3>
          <p>Independent certifier of legitimate healthcare operations online. Required to run ads on Google, Meta, and Microsoft health verticals.</p>
          <p style="margin-top:14px;"><a class="cred-link" href="https://www.legitscript.com/" target="_blank" rel="noopener">Verify at legitscript.com</a></p>
        </div>
        <div class="card">
          <div class="card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
          <h3>Healthgrades</h3>
          <p>Public provider directory with profile, practice details, and patient-facing listings.</p>
          <p style="margin-top:14px;"><a class="cred-link" href="https://www.healthgrades.com/providers/christopher-woods-xynt5wl" target="_blank" rel="noopener">View Healthgrades profile</a></p>
        </div>
        <div class="card">
          <div class="card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg></div>
          <h3>WebMD Provider Directory</h3>
          <p>Profile with telemedicine service details and years of clinical experience.</p>
          <p style="margin-top:14px;"><a class="cred-link" href="https://doctor.webmd.com/doctor/christopher-woods-7b55e933-62ef-4d7b-975c-9cfc40eb3ad8-overview" target="_blank" rel="noopener">View WebMD profile</a></p>
        </div>
        <div class="card">
          <div class="card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 100 20 10 10 0 000-20z"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg></div>
          <h3>CMS NPI Registry (federal)</h3>
          <p>The federal source of truth for any licensed clinician in the U.S. Searchable by NPI, name, or location.</p>
          <p style="margin-top:14px;"><a class="cred-link" href="https://npiregistry.cms.hhs.gov/provider-view/1285125468" target="_blank" rel="noopener">Look up NPI 1285125468</a></p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ASYNC MODALITY NOTE -->
<section class="section alt">
  <div class="container">
    <div class="section-head">
      <div class="section-label">About the async modality</div>
      <h2 class="section-heading">Why text-based works (and where it doesn't)</h2>
    </div>
    <div class="section-shell" style="max-width:820px;">
      <p style="font-size:1.05rem;color:var(--text-body);margin-bottom:16px;">Asynchronous telemedicine &mdash; text-based, not real-time video &mdash; is explicitly recognized by state nursing boards where Chris practices, provided the clinician gathers enough clinical information to establish an appropriate plan. That's the part that matters: it's not a static questionnaire, it's a real back-and-forth conversation.</p>
      <p style="font-size:1.05rem;color:var(--text-body);margin-bottom:16px;">Every visit goes through a licensed NP personally &mdash; no AI, no chatbot, no algorithmic triage. The text-based modality exists so you don't have to take time off work to sit in a waiting room for a UTI; it does not exist to remove the clinician from the loop.</p>
      <p style="font-size:1.05rem;color:var(--text-body);">State-board rules vary. A condition or prescription that's fine in one state may not be fine in another. If something on your visit requires an in-person exam &mdash; or falls outside what async care can responsibly handle &mdash; Chris will tell you and refund the visit.</p>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="section">
  <div class="container">
    <div class="section-head">
      <div class="section-label">Verify &amp; validate</div>
      <h2 class="section-heading">How to check anything on this page</h2>
    </div>
    <div class="faq-list">
      <details class="faq-item"><summary>What does FNP-C mean?</summary><div class="faq-answer"><p>FNP-C stands for <strong>Family Nurse Practitioner - Certified</strong>, a board certification granted by the American Association of Nurse Practitioners Certification Board (AANPCB). It certifies advanced clinical competence across the family lifespan &mdash; pediatrics, adults, and geriatrics. It's separate from the state license that authorizes practice.</p></div></details>
      <details class="faq-item"><summary>How do I verify Chris's license in my state?</summary><div class="faq-answer"><p>Every state nursing board runs a free public license lookup. The table above links directly to the verification tool for each state Chris is licensed in. Search by name: "Christopher Woods" or "Chris Woods" will return the active license record.</p><p>If you want the fastest path, the federal NPI Registry at npiregistry.cms.hhs.gov lists NPI 1285125468 with all active state licenses in one view.</p></div></details>
      <details class="faq-item"><summary>What's the difference between MSN, APRN, and FNP-C?</summary><div class="faq-answer"><p><strong>MSN</strong> is the graduate degree &mdash; Master of Science in Nursing &mdash; required to become a nurse practitioner. <strong>APRN</strong> (Advanced Practice Registered Nurse) is the legal designation under which NPs diagnose, prescribe, and practice. <strong>FNP-C</strong> is the board certification proving clinical competence as a Family Nurse Practitioner. Together they describe the academic, legal, and clinical pillars of one practicing clinician.</p></div></details>
      <details class="faq-item"><summary>Is NPCWoods Telemedicine LegitScript-certified?</summary><div class="faq-answer"><p>Yes. LegitScript verifies that the practice meets the standards required to advertise on Google, Meta, Microsoft, and other major platforms &mdash; they audit licensing, regulatory compliance, and patient safety before granting certification. The LegitScript seal is displayed in the footer of every page on the site.</p></div></details>
      <details class="faq-item"><summary>Can a Nurse Practitioner prescribe medication?</summary><div class="faq-answer"><p>Yes. In every state Chris is licensed in, Nurse Practitioners have independent or collaborative prescriptive authority for non-controlled medications (antibiotics, antifungals, antivirals, most common prescription drugs). NPCWoods does not prescribe controlled substances &mdash; that's a separate decision we made, not a licensing limit.</p></div></details>
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="cta-band">
  <h2>Now that you've checked.</h2>
  <p>Same clinician. Real credentials. $59 flat. Text to start.</p>
  <div class="btn-row">
    <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" class="btn-primary">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
      Text Chris &mdash; Start My $59 Visit
    </a>
  </div>
  <p class="cta-phone">Or call <a href="tel:4806394722">(480) 639-4722</a> &middot; 7 days a week</p>
</section>"""


# ============================================================================
# ASSEMBLE + WRITE
# ============================================================================

def assemble(head_block: str, body_block: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{CRAWLER_META}
{HEAD_TRACKING}
{head_block}
{HEAD_FONTS}
{BASE_CSS}
</head>
<body>
{HEADER}
{body_block}
{FOOTER}
</body>
</html>
"""


def main():
    pages = [
        ("pricing", PRICING_HEAD, PRICING_BODY),
        ("credentials", CREDENTIALS_HEAD, CREDENTIALS_BODY),
    ]
    all_errors = []
    for slug, head, body in pages:
        html = assemble(head, body)
        errors = validate(html, slug)
        if errors:
            all_errors.extend(errors)
            continue
        out = ROOT / "landing-pages" / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        print(f"[ok] wrote {out} ({len(html):,} bytes)")

    if all_errors:
        print("\n[BANNED WORDS FOUND — pages NOT written]")
        for e in all_errors:
            print(e)
        raise SystemExit(1)

    print("\n[done] Both pages generated. Review locally, then run scripts/deploy-pricing-credentials.py to ship.")


if __name__ == "__main__":
    main()
