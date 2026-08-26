#!/usr/bin/env python3
"""Gold-standard plate chassis.

Every new NPCWoods landing plate copies the look of
`landing-pages/uti-treatment/index.html` (dark hero, stats, bento, bottom CTA).
Cook scripts import this. Do not invent a second look.

Copy rule: do not name hospitals or clinic brands in story copy. Streets and
towns are fine. Named competitors belong only in a head-to-head compare table
or list.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "landing-pages" / "uti-treatment" / "index.html"
HEADER = (ROOT / "html" / "shared" / "header-snippet.html").read_text(encoding="utf-8")
FOOTER = (ROOT / "html" / "shared" / "footer-snippet.html").read_text(encoding="utf-8")

SMS = "sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit"
LOCKED_911 = (
    "Text-based telehealth is not for emergencies. "
    "If you have chest pain, trouble breathing, or other emergency symptoms, call 911."
)
HIPAA_OFF = """<!-- Meta Pixel disabled 2026-06-10: no BAA with Meta — health-condition pages must not send PageView there.
     The stub below also blocks the GTM-injected pixel: Meta's base code starts with `if(f.fbq)return;`,
     so predefining a no-op fbq means fbevents.js never loads on this page.
     GTM, GA4, and Google Ads stay off this health-condition page (no BAA). -->
<script>
window.fbq = function () {};
window.fbq.queue = [];
window.fbq.loaded = true;
window.fbq.version = '2.0';
window._fbq = window.fbq;
</script>
"""
PROSE_CSS = """
#npcSaveWrap { display: none !important; }
body::after { content: none !important; display: none !important; }
.prose p, .prose li { font-size: 16px; color: var(--body); line-height: 1.7; }
.prose p { margin: 0 0 16px; }
.prose ul, .prose ol { margin: 0 0 16px; padding-left: 1.2em; }
.prose a { color: var(--blue-bright); }
.prose strong { color: #fff; }
.prose h2 { font-size: clamp(24px, 3vw, 36px); font-weight: 800; letter-spacing: -0.04em; color: #fff; margin: 0 0 14px; }
.prose h3 { font-size: 18px; font-weight: 700; color: #fff; margin: 20px 0 10px; }
.section-light .prose h2, .section-white .prose h2,
.section-light .prose h3, .section-white .prose h3,
.section-light .prose strong, .section-white .prose strong { color: #111114; }
.section-light .prose p, .section-white .prose p,
.section-light .prose li, .section-white .prose li { color: #3d3d3f; }
.nga-table { width: 100%; border-collapse: collapse; margin: 0 0 24px; font-size: 14px; }
.nga-table th, .nga-table td { border: 1px solid var(--line); padding: 12px 14px; text-align: left; vertical-align: top; }
.nga-table th { background: var(--panel-3); font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }
.crumb { max-width: var(--max); margin: 16px auto 0; padding: 0 24px; font-size: 13px; color: var(--muted); }
.crumb a { color: var(--blue-bright); }

/* Phoenix-style site header on dark gold plates — light bar, always on top of the hero */
.npc-nav{
  position:sticky;top:0;z-index:10000;
  background:#ffffff !important;
  border-bottom:1px solid #e5e7eb;
}
.npc-nav-inner{height:64px}
.npc-nav-logo-name,
.npc-nav-links > li > a:not(.npc-nav-cta){
  color:#1A1A2E !important;
  -webkit-text-fill-color:#1A1A2E !important;
}
.npc-nav-logo-tag{
  color:#2563EB !important;
  -webkit-text-fill-color:#2563EB !important;
}
.npc-nav-links > li > a.npc-nav-cta,
.npc-nav-cta,
.npc-nav-cta-mobile{
  color:#FFFFFF !important;
  -webkit-text-fill-color:#FFFFFF !important;
}
.npc-nav-cta svg,
.npc-nav-cta-mobile svg{
  stroke:#FFFFFF !important;
  color:#FFFFFF !important;
}
.npc-nav-toggle span{background:#1A1A2E !important}
.hero{padding-top:28px}
"""
TAIL_JS = """
<script>
document.querySelectorAll('.faq-q').forEach(q => {
  q.addEventListener('click', () => {
    const item = q.parentElement;
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js" defer></script>
<script>
(function () {
  function buildQRs() {
    if (typeof QRCode === 'undefined') { return setTimeout(buildQRs, 120); }
    document.querySelectorAll('.npc-qr-code').forEach(function (el) {
      if (el.dataset.rendered) { return; }
      var sms = el.getAttribute('data-sms');
      if (!sms) { return; }
      new QRCode(el, {
        text: sms, width: 118, height: 118,
        colorDark: '#0a0a0a', colorLight: '#ffffff',
        correctLevel: QRCode.CorrectLevel.M
      });
      el.dataset.rendered = '1';
    });
  }
  if (document.readyState !== 'loading') { buildQRs(); }
  else { document.addEventListener('DOMContentLoaded', buildQRs); }
})();
</script>
"""


def gold_html() -> str:
    return GOLD.read_text(encoding="utf-8")


def gold_css() -> str:
    match = re.search(r"<style>(.*?)</style>", gold_html(), re.S)
    if not match:
        raise SystemExit("gold UTI hub is missing a <style> block")
    return match.group(1)


def gold_reviews() -> str:
    match = re.search(r"<!-- REVIEWS -->\s*(<section class=\"reviews\">.*?</section>)", gold_html(), re.S)
    if not match:
        raise SystemExit("gold UTI hub is missing the reviews section")
    return match.group(1)


def sms_cta(label: str = "Text Us Now: (480) 639-4722") -> str:
    return (
        f'<a href="{SMS}" class="btn-primary npc-sms-cta">{label}</a>\n'
        f'<div class="npc-qr-cta" role="group" aria-label="Scan to text NPCWoods">\n'
        f'  <div class="npc-qr-code" data-sms="{SMS}" aria-hidden="true"></div>\n'
        f'  <div class="npc-qr-meta">\n'
        f'    <span class="npc-qr-label">Scan to Text Us</span>\n'
        f'    <a class="npc-qr-phone" href="{SMS}">(480) 639-4722</a>\n'
        f'    <span class="npc-qr-sub">$59 flat fee · text to start</span>\n'
        f'  </div>\n'
        f'</div>'
    )


def hero(h1: str, sub: str, kicker: str, phone_html: str = "") -> str:
    inner_class = "hero-inner hero-split" if phone_html else "hero-inner"
    phone = f"\n    {phone_html}" if phone_html else ""
    text_wrap_open = '<div class="hero-text">' if phone_html else ""
    text_wrap_close = "</div>" if phone_html else ""
    return f"""<section class="hero">
  <div class="{inner_class}">
    {text_wrap_open}
      <div class="hero-kicker"><span class="hero-dot"></span> {kicker}</div>
      <h1>{h1}</h1>
      <p class="hero-sub">{sub}</p>
      <div class="hero-actions">
        {sms_cta()}
        <a href="#how-it-works" class="btn-ghost">See how it works</a>
      </div>
      <div class="hero-trust">
        <span>HIPAA-Compliant</span>
        <span>Same NP every time</span>
        <span>$59 · pay after care</span>
      </div>
    {text_wrap_close}{phone}
  </div>
</section>"""


def stats() -> str:
    return """<div class="stats-band">
  <div class="stats-inner">
    <div class="stat"><div class="stat-n">$59</div><div class="stat-l">Flat fee, pay after care</div></div>
    <div class="stat"><div class="stat-n">11</div><div class="stat-l">Licensed states</div></div>
    <div class="stat"><div class="stat-n">Same NP</div><div class="stat-l">Chris Woods, FNP-C</div></div>
  </div>
</div>"""


def eeat() -> str:
    return """<div class="eeat-byline" style="background:var(--panel-2);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:24px auto;max-width:var(--max);font-size:13px;line-height:1.5;color:var(--body);">
  <p style="margin:0 0 8px 0;color:#fff;font-weight:600;">Written and clinically reviewed by <strong>Chris Woods, MSN, APRN, FNP-C</strong>, double board-certified Nurse Practitioner and founder of NPCWoods.</p>
  <p style="margin:0 0 4px 0;"><a href="https://npcwoods.com/about/" style="color:var(--blue-bright);text-decoration:underline;">About Chris</a> · <a href="https://npcwoods.com/credentials/" style="color:var(--blue-bright);text-decoration:underline;">Full credentials, NPI &amp; state licenses</a></p>
  <p style="margin:0;font-size:12px;color:var(--muted);">Last reviewed: <time datetime="2026-08-24">August 24, 2026</time></p>
</div>"""


def how_it_works() -> str:
    return f"""<section id="how-it-works" class="section section-light dark-to-light">
  <div class="section-inner">
    <span class="section-kicker">How it works</span>
    <h2 class="section-title">Three texts. That's it.</h2>
    <p class="section-body">No app, no portal, no video call — just text. You only pay if he can treat you.</p>
    <div class="bento">
      <div class="bento-card">
        <div class="step-num">1</div>
        <h3>Text Chris</h3>
        <p>Text <a href="{SMS}">(480) 639-4722</a> in your own words. No app. No appointment.</p>
      </div>
      <div class="bento-card">
        <div class="step-num">2</div>
        <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" class="chris-avatar" alt="Chris Woods NP">
        <h3>Chris reviews it</h3>
        <p>Chris Woods, MSN, APRN, FNP-C, reads it himself. Same nurse practitioner every time. He asks what he needs.</p>
      </div>
      <div class="bento-card">
        <div class="step-num">3</div>
        <h3>Plan, then pharmacy</h3>
        <p>If treatment is appropriate, a prescription can go to the pharmacy you name. If text is not safe, he tells you to go in. No charge for that honesty.</p>
      </div>
    </div>
  </div>
</section>"""


def er_box() -> str:
    return f"""<section id="er-warning" class="section">
  <div class="section-inner" style="max-width:740px;text-align:center">
    <span class="section-kicker">Safety first</span>
    <h2 class="section-title">When this is not the door</h2>
    <div class="er-box">
      <h3>Call 911 instead</h3>
      <p style="color:var(--body);font-size:15px;line-height:1.65">{LOCKED_911}</p>
    </div>
  </div>
</section>"""


def states() -> str:
    pills = [
        ("arizona-telemedicine", "Arizona"),
        ("colorado-telemedicine", "Colorado"),
        ("georgia-telemedicine", "Georgia"),
        ("idaho-telemedicine", "Idaho"),
        ("iowa-telemedicine", "Iowa"),
        ("montana-telemedicine", "Montana"),
        ("nevada-telemedicine", "Nevada"),
        ("new-mexico-telemedicine", "New Mexico"),
        ("north-carolina-telemedicine", "North Carolina"),
        ("oregon-telemedicine", "Oregon"),
        ("utah-telemedicine", "Utah"),
    ]
    links = "\n      ".join(
        f'<a href="https://npcwoods.com/{slug}/" class="state-pill">{name}</a>'
        for slug, name in pills
    )
    return f"""<section class="section section-white">
  <div class="section-inner" style="text-align:center">
    <span class="section-kicker">Coverage</span>
    <h2 class="section-title">Licensed in 11 states</h2>
    <p class="section-body" style="margin-left:auto;margin-right:auto">You must be physically in a licensed state at the time of the visit.</p>
    <div class="states-pills">
      {links}
    </div>
  </div>
</section>"""


def bottom_cta(title: str, sub: str) -> str:
    return f"""<section class="bottom-cta">
  <div class="bottom-cta-inner">
    <h2>{title}</h2>
    <p>{sub}</p>
    {sms_cta()}
    <div class="bottom-trust-line">
      <span>HIPAA-compliant</span>
      <span>Pay after care</span>
      <span>Same NP every time</span>
    </div>
  </div>
</section>"""


def clinician_line() -> str:
    return """<div class="clinician-line">
  Clinically reviewed by <strong>Chris Woods, MSN, APRN, FNP-C</strong>, double board-certified Nurse Practitioner.<br>
  Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT · <a href="https://npcwoods.com/about/" style="color:var(--blue-bright);">About Chris</a> · <a href="https://npcwoods.com/credentials/" style="color:var(--blue-bright);">Credentials</a> · Last reviewed: <time datetime="2026-08-24">August 24, 2026</time>
</div>"""


def render_page(
    *,
    title: str,
    description: str,
    canonical: str,
    og_title: str,
    crumb_html: str,
    schema_extra: str,
    body: str,
    draft_comment: str = "",
) -> str:
    schema_page = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "url": canonical,
            "name": title,
            "description": description,
            "about": {"@type": "MedicalBusiness", "@id": "https://npcwoods.com/#medical-business"},
            "reviewedBy": {"@type": "Person", "name": "Chris Woods", "jobTitle": "Nurse Practitioner"},
        },
        indent=2,
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HIPAA_OFF}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#05060a">
<link rel="canonical" href="{canonical}">
<link rel="cite-as" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp">
<link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<script type="application/ld+json">
{schema_page}
</script>
{schema_extra}
<style>
{gold_css()}
{PROSE_CSS}
</style>
{draft_comment}
</head>
<body>
{HEADER}
{crumb_html}
{body}
{FOOTER}
{TAIL_JS}
</body>
</html>
"""
