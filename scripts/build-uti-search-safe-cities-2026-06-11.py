#!/usr/bin/env python3
"""Generate search-safe UTI city landing pages in the Apple-style design.

v2 (2026-06-11, Chris's feedback): the first cut used the plain Mesa
search-safe template and Chris wants the Apple-style design instead
(commit 5da80d2, /uti-treatment/surprise-az/). This script splices the
Apple design's CSS and drug-free sections straight from the Surprise
page so the look stays in sync, and hand-builds the sections that
contained drug names — RESTRICTED_DRUG_TERMS is why search-safe pages
exist, so no drug/antibiotic/prescription vocabulary anywhere.

Pages are written to landing-pages/uti-treatment/{slug}/search-safe/index.html.
This script does NOT deploy anything.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN_SRC = ROOT / "landing-pages/uti-treatment/surprise-az/index.html"

CITIES = [
    ("mesa-az", "Mesa", "Arizona", "AZ"),
    ("scottsdale-az", "Scottsdale", "Arizona", "AZ"),
    ("surprise-az", "Surprise", "Arizona", "AZ"),
    ("chandler-az", "Chandler", "Arizona", "AZ"),
    ("gilbert-az", "Gilbert", "Arizona", "AZ"),
    ("tempe-az", "Tempe", "Arizona", "AZ"),
    ("glendale-az", "Glendale", "Arizona", "AZ"),
    ("albuquerque-nm", "Albuquerque", "New Mexico", "NM"),
]

STATE_PAGE = {"Arizona": "arizona-telemedicine", "New Mexico": "new-mexico-telemedicine"}

REQUIRED = [
    "GTM-59QSWZRC",
    "gtag/js?id=G-EFFRQMG8TC",
    "AW-610222919",
    "tracking.js",
    'content="noindex,follow"',
    "Most patients hear back the same day, usually within a few hours.",
]
FORBIDDEN = [
    "connect.facebook.net",
    "facebook.com/tr",
    "fbevents.js",
    "nitrofurantoin",
    "trimethoprim",
    "macrobid",
    "bactrim",
    "cephalexin",
    "phenazopyridine",
    "nystatin",
    "antibiotic",
    "prescription",
    "insurance",
]

STAR = '<svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>'

# Reviews that never mention pharmacy scripts — search-safe quote pool
QUOTES = [
    ("Fast, easy, no waiting, very professional. I recommend him to everyone.", "D.C.D."),
    ("Messaged Chris he responded in a timely manner. Very professional. Easy to talk to about our concerns. It was nice to be able to stay at home and get quality care.", "T.P."),
    ("I had a great experience with NPCWoods Telemed Clinic! Chris was incredibly efficient and genuinely helpful. He made the whole process quick and stress-free.", "H.P.W."),
    ("Literally cannot recommend enough! My daughter had the worst cough ever and it was so bad on a Saturday night after midnight, I text Chris, he replied immediately.", "A.A."),
]


def chunk(src: str, start: str, end: str) -> str:
    i = src.index(start)
    j = src.index(end)
    return src[i:j]


def build_reviews() -> str:
    cards = ""
    for text, author in QUOTES:
        cards += (
            f'<div class="rcard"><div class="stars-row" style="margin-bottom:10px">{STAR * 5}</div>'
            f'<p class="rcard-text">"{text}"</p>'
            f'<div class="rcard-foot"><span class="rcard-author">{author}</span>'
            f'<span class="rcard-source">Facebook</span></div></div>\n'
        )
    return f"""<!-- REVIEWS -->
<section class="reviews">
  <div class="reviews-head">
    <div class="stars-row">{STAR * 5}</div>
    <h2>50+ Five-Star Reviews</h2>
    <p>Real patients. Real reviews. From Facebook &amp; Google.</p>
  </div>
  <div class="scroll-mask">
    <div class="scroll-track">
{cards}      <!-- Duplicate for infinite scroll -->
{cards}    </div>
  </div>
</section>
"""


def build_template() -> str:
    src = DESIGN_SRC.read_text()

    css = chunk(src, "<style>", "</style>") + "</style>"

    what_is = chunk(src, "<!-- WHAT IS A UTI -->", "<!-- UTI VS OTHER -->")
    differential = chunk(src, "<!-- UTI VS OTHER -->", "<!-- ANTIBIOTICS -->")

    er = chunk(src, "<!-- ER WARNING -->", "<!-- WHO IT'S FOR -->")
    er = er.replace("may need IV antibiotics", "may need IV treatment at the hospital")
    er = er.replace(
        "can't take oral antibiotics if you're vomiting",
        "can't keep oral medicine down",
    )
    er = er.replace("nurse practitioner in Arizona", "nurse practitioner in {{STATE}}")

    fit = chunk(src, "<!-- WHO IT'S FOR -->", "<!-- FAQ -->")
    fit = fit.replace("Located in Arizona", "Located in {{STATE}}")

    states = chunk(src, "<!-- STATES -->", "<!-- CROSS LINKS -->")

    cross = chunk(src, "<!-- CROSS LINKS -->", "<!-- BOTTOM CTA -->")
    cross = cross.replace(
        'href="https://npcwoods.com/arizona-telemedicine/" class="cross-link">Arizona Telemedicine',
        'href="https://npcwoods.com/{{STATE_PAGE}}/" class="cross-link">{{STATE}} Telemedicine',
    )

    footer = chunk(src, "<!-- FOOTER -->", "<script>\n// FAQ accordion")
    footer = footer.replace(
        'href="https://npcwoods.com/uti-treatment/surprise-az/">UTI — Surprise, AZ',
        'href="https://npcwoods.com/uti-treatment/{{SLUG}}/search-safe/">UTI — {{CITY}}, {{ST}}',
    )

    sms = "sms:4806394722?body=Hi%2C%20I%20think%20I%20have%20a%20UTI%20in%20{{CITY}}%20{{ST}}"

    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<!-- Meta Pixel disabled: no BAA with Meta — health-condition pages must not send PageView there.
     Predefining a no-op fbq means the GTM-injected pixel never loads on this page. -->
<script>
window.fbq = function () {{}};
window.fbq.queue = [];
window.fbq.loaded = true;
window.fbq.version = '2.0';
window._fbq = window.fbq;
</script>
<!-- NPCWoods Tracking: GTM -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-59QSWZRC');</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EFFRQMG8TC"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', 'G-EFFRQMG8TC');
gtag('config', 'AW-610222919');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>UTI Visit in {{{{CITY}}}}, {{{{ST}}}} | Text a Licensed NP | NPCWoods</title>
<meta name="description" content="UTI symptoms in {{{{CITY}}}}? Text Chris Woods, a licensed {{{{STATE}}}} nurse practitioner. $59 text-based visit, clear triage, and same-day review when available.">
<meta name="robots" content="noindex,follow">
<meta name="theme-color" content="#05060a">
<link rel="canonical" href="https://npcwoods.com/uti-treatment/{{{{SLUG}}}}/search-safe/">
<meta property="og:type" content="website">
<meta property="og:url" content="https://npcwoods.com/uti-treatment/{{{{SLUG}}}}/search-safe/">
<meta property="og:title" content="UTI Visit in {{{{CITY}}}}, {{{{ST}}}} | NPCWoods">
<meta property="og:description" content="Text a licensed {{{{STATE}}}} nurse practitioner for a $59 UTI visit from home.">
<meta property="og:site_name" content="NPCWoods Telemedicine">
<meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp">
<link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="apple-touch-icon" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"MedicalBusiness","name":"NPCWoods Telemedicine","description":"Text-based UTI symptom review with a licensed nurse practitioner in {{{{CITY}}}}, {{{{STATE}}}}.","telephone":"+14806394722","url":"https://npcwoods.com/uti-treatment/{{{{SLUG}}}}/search-safe/","priceRange":"$59","areaServed":{{"@type":"City","name":"{{{{CITY}}}}","containedInPlace":{{"@type":"State","name":"{{{{STATE}}}}"}}}},"medicalSpecialty":"FamilyPractice","aggregateRating":{{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"58","bestRating":"5","worstRating":"1"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Can NPCWoods review UTI symptoms by text in {{{{CITY}}}}?","acceptedAnswer":{{"@type":"Answer","text":"Yes. Adults in {{{{STATE}}}} can text NPCWoods for a $59 UTI symptom review with Chris Woods, a licensed nurse practitioner. Chris asks follow-up questions and explains the next step based on your answers."}}}},{{"@type":"Question","name":"How fast will I hear back?","acceptedAnswer":{{"@type":"Answer","text":"Most patients hear back the same day, usually within a few hours. Messages are reviewed 7 days a week."}}}},{{"@type":"Question","name":"How much does it cost?","acceptedAnswer":{{"@type":"Answer","text":"$59 flat. No hidden fees, no surprise bills, no paperwork. Meds, when appropriate, typically $4–$20 with GoodRx."}}}},{{"@type":"Question","name":"When should I go in person instead?","acceptedAnswer":{{"@type":"Answer","text":"Go in person for fever, back or side pain, pregnancy, severe vomiting, significant blood in urine, or symptoms in a young child. Those signs may need hands-on evaluation."}}}}]}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
{css}
<style>
/* Softened light sections (Chris 2026-06-11): ease the black-hero -> bright-white jump.
   Light areas become a calm muted gray instead of glare-white. */
.section-light {{ background: #e2e4e9; }}
.section-white {{ background: #e9eaef; }}
.local-scene {{ background: #e2e4e9; }}
.local-scene h2 {{ color: #1b1b21; }}
.local-scene p {{ color: #3a3a40; }}
.section-light,
.section-white {{
  --panel: #eef0f4;
  --panel-2: #e6e8ee;
  --panel-3: #dcdee5;
  --ink: #1b1b21;
  --body: #3a3a40;
  --muted: #63636a;
  --line: rgba(0,0,0,0.08);
  color: #1b1b21;
}}
/* Gentle fade into each light block instead of a hard edge */
.section-light.dark-to-light,
.section-white.dark-to-light {{
  background-image: linear-gradient(to bottom, #c9ccd4 0%, #e2e4e9 140px);
}}
.section-white.dark-to-light {{
  background-image: linear-gradient(to bottom, #cfd2da 0%, #e9eaef 140px);
}}
</style>
</head>
"""

    body = f"""<body>

<!-- GTM noscript -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-59QSWZRC"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

<!-- NAV -->
<nav class="nav">
  <div class="nav-logo">
    <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" alt="NPCWoods">
    NPCWoods
  </div>
  <a href="{sms}" class="nav-cta">Text Now · $59</a>
</nav>

<!-- SAFETY STRIP -->
<div class="safety-strip">
  <span>⚠ Go to the ER instead if: fever + back/side pain · vomiting · pregnant · child under 2 ·</span>
  <a href="#er-warning">→ Full safety guide</a>
</div>

<!-- HERO -->
<section class="hero">
  <div class="hero-inner hero-split">
    <div class="hero-text">
      <div class="hero-kicker">
        <span class="hero-dot"></span>
        📍 {{{{CITY}}}}, {{{{ST}}}} &nbsp;·&nbsp; $59 Flat &nbsp;·&nbsp; No Waiting Room &nbsp;·&nbsp; Same Day
      </div>
      <h1>UTI in {{{{CITY}}}}, {{{{ST}}}}? Care without leaving home.</h1>
      <p class="hero-sub">Text a double board-certified Nurse Practitioner licensed in {{{{STATE}}}}. Chris reads your message personally, asks the right questions, and handles the next step the same day.</p>
      <div class="hero-actions">
        <a href="{sms}" class="btn-primary">Start My $59 Visit — Text (480) 639-4722</a>
        <a href="#how-it-works" class="btn-ghost">See how it works</a>
      </div>
      <div class="hero-trust">
        <span>📍 Serving {{{{CITY}}}}, {{{{ST}}}}</span>
        <span>🏥 {{{{STATE}}}}-licensed NP</span>
        <span>⭐ 50+ five-star reviews</span>
        <span>💊 Meds typically $4–$20 with GoodRx</span>
      </div>
    </div>
    <div class="phone-float">
      <div class="phone-frame">
        <div class="phone-notch"></div>
        <div class="phone-screen">
          <div class="imsg-header">
            <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" class="imsg-avatar" alt="Chris">
            <div>
              <div class="imsg-name">Chris @ NPCWoods</div>
              <div class="imsg-status">● Available now</div>
            </div>
          </div>
          <div class="imsg-body">
            <div class="imsg-time">Today 2:14 PM</div>
            <div class="imsg-bubble user">Hi, it burns when I pee and I have to go every 5 min 😩</div>
            <div class="imsg-bubble chris">Hey! Sounds like a classic UTI. Quick question — any fever or back pain?</div>
            <div class="imsg-bubble user">No fever, no back pain at all</div>
            <div class="imsg-bubble chris">Perfect. Starting your $59 visit now — I'll handle everything from here 💬</div>
            <div class="imsg-rx">✓ Taken care of — same day</div>
            <div class="imsg-time" style="margin-top:4px">2:19 PM</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- STATS BAND -->
<div class="stats-band">
  <div class="stats-inner">
    <div class="stat"><div class="stat-n">$59</div><div class="stat-l">Flat fee, no surprises</div></div>
    <div class="stat"><div class="stat-n">{{{{ST}}}}</div><div class="stat-l">{{{{STATE}}}}-licensed NP</div></div>
    <div class="stat"><div class="stat-n">Same day</div><div class="stat-l">Response for most patients</div></div>
  </div>
</div>

{build_reviews()}
<!-- LOCAL BAND -->
<section class="local-scene">
  <div class="local-scene-inner">
    <span style="display:inline-block;background:rgba(0,113,227,.1);border:1px solid rgba(0,113,227,.22);border-radius:999px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#0071e3;margin-bottom:16px;">📍 Serving {{{{CITY}}}}, {{{{ST}}}}</span>
    <h2>Care that fits {{{{CITY}}}} life</h2>
    <p>No drive across town and no waiting room. Your visit starts the moment you text, from home, work, or anywhere in {{{{CITY}}}} — and if your symptoms need hands-on care, Chris tells you straight up.</p>
  </div>
</section>

<!-- HOW IT WORKS -->
<section id="how-it-works" class="section section-light dark-to-light">
  <div class="section-inner">
    <span class="section-kicker">How it works</span>
    <h2 class="section-title">Three texts. That's it.</h2>
    <p class="section-body">Faster than ordering food. No app, no portal, no video call — just text.</p>
    <div class="bento">
      <div class="bento-card">
        <div class="step-num">1</div>
        <h3>Text Us</h3>
        <p>Text <a href="sms:4806394722">(480) 639-4722</a> and say something like "hey, it burns when I pee." No app, no portal, no account. That's literally all you need to start.</p>
      </div>
      <div class="bento-card">
        <div class="step-num">2</div>
        <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" class="chris-avatar" alt="Chris Woods NP">
        <h3>Chris Reviews</h3>
        <p>Chris Woods, your double board-certified Nurse Practitioner, reads your message personally. He'll ask a couple quick follow-up questions — think texting a friend who happens to know medicine.</p>
      </div>
      <div class="bento-card">
        <div class="step-num">3</div>
        <h3>Clear Next Step</h3>
        <p>If text-based care fits your situation, Chris handles everything electronically the same day and tells you exactly what to do. If it needs hands-on care, he'll say so straight up.</p>
      </div>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:20px;text-align:center">Care follows national clinical guidelines for uncomplicated UTI.</p>
  </div>
</section>

{what_is}
{differential}
{er}
{fit}
<!-- FAQ -->
<section id="faq" class="section section-light dark-to-light">
  <div class="section-inner" style="max-width:720px">
    <span class="section-kicker">FAQ</span>
    <h2 class="section-title" style="text-align:center;margin-bottom:36px">{{{{CITY}}}}, {{{{ST}}}} — common questions</h2>
    <div class="faq-list">
      <div class="faq-item"><div class="faq-q">Can NPCWoods review UTI symptoms by text in {{{{CITY}}}}?</div><div class="faq-a"><p><strong>Yes.</strong> Adults in {{{{STATE}}}} can text (480) 639-4722 for a $59 UTI symptom review with Chris Woods, a licensed nurse practitioner. He asks follow-up questions and explains the next step based on your answers.</p></div></div>
      <div class="faq-item"><div class="faq-q">How fast will I hear back?</div><div class="faq-a"><p>Most patients hear back the same day, usually within a few hours. <strong>Messages are reviewed 7 days a week.</strong> If symptoms feel urgent, don't wait — use urgent care or the ER.</p></div></div>
      <div class="faq-item"><div class="faq-q">How much does it cost?</div><div class="faq-a"><p><strong>$59 flat.</strong> No hidden fees. No surprise bills. No paperwork. Meds, when appropriate, typically run $4–$20 with GoodRx.</p></div></div>
      <div class="faq-item"><div class="faq-q">Do I need an app or a video call?</div><div class="faq-a"><p>No. The whole visit happens by text — <strong>no app, no portal, no camera.</strong></p></div></div>
      <div class="faq-item"><div class="faq-q">What if it's not a UTI?</div><div class="faq-a"><p>Chris will ask enough questions to figure out what's going on. If it needs in-person care or testing, he'll tell you straight up — <strong>no charge for the honesty.</strong></p></div></div>
      <div class="faq-item"><div class="faq-q">When should I go in person instead?</div><div class="faq-a"><p>Fever, back or side pain, pregnancy, severe vomiting, significant blood in urine, or symptoms in a young child. <strong>Those signs may need hands-on evaluation.</strong></p></div></div>
      <div class="faq-item"><div class="faq-q">What if I don't feel better in 48 hours?</div><div class="faq-a"><p>Text Chris back and he'll figure out the next step with you. <strong>The follow-up is part of your $59.</strong></p></div></div>
    </div>
  </div>
</section>

{states}
{cross}
<!-- BOTTOM CTA -->
<section class="bottom-cta">
  <div class="bottom-cta-inner">
    <h2>Ready to feel better, {{{{CITY}}}}?</h2>
    <p>Text us what's going on. $59 flat, no waiting room, no paperwork. Reviewed the same day for most patients.</p>
    <a href="{sms}" class="btn-primary" style="font-size:16px;padding:16px 32px">Text (480) 639-4722 — Start My $59 Visit</a>
    <div class="bottom-trust-line">
      <span>🔒 HIPAA-Compliant &amp; Secure</span>
      <span>💳 HSA/FSA accepted</span>
      <span>🏥 Licensed in {{{{STATE}}}}</span>
    </div>
  </div>
</section>

<!-- CLINICIAN LINE -->
<div class="clinician-line">
  Reviewed by Chris Woods, MSN, APRN, FNP-C — Licensed Nurse Practitioner<br>
  Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT &bull; Serving {{{{CITY}}}}, {{{{ST}}}} &bull; Last updated: <time datetime="2026-06-11">June 11, 2026</time>
</div>

{footer}<script>
// FAQ accordion
document.querySelectorAll('.faq-q').forEach(q => {{
  q.addEventListener('click', () => {{
    const item = q.parentElement;
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  }});
}});
</script>
<!-- NPCWoods Tracking: tracking.js -->
<script src="/tracking.js?v=20260528-no-phi"></script>
</body>
</html>
"""
    return head + body


def render(template: str, slug: str, city: str, state: str, abbr: str) -> str:
    return (
        template.replace("{{SLUG}}", slug)
        .replace("{{CITY}}", city)
        .replace("{{STATE_PAGE}}", STATE_PAGE[state])
        .replace("{{STATE}}", state)
        .replace("{{ST}}", abbr)
    )


def check_page(slug: str, city: str, html: str) -> list[str]:
    problems = []
    lower = html.lower()
    for marker in REQUIRED:
        if marker not in html:
            problems.append(f"missing required marker: {marker}")
    for bad in FORBIDDEN:
        if bad.lower() in lower:
            problems.append(f"contains forbidden marker: {bad}")
    if "{{" in html:
        problems.append("unrendered placeholder")
    if city != "Surprise" and "Surprise" in html:
        problems.append("leftover 'Surprise' reference")
    if slug.endswith("-nm") and (" Arizona" in html or ", AZ " in html):
        problems.append("leftover Arizona reference on NM page")
    if f"/uti-treatment/{slug}/search-safe/" not in html:
        problems.append("canonical URL not updated")
    return problems


def main() -> int:
    template = build_template()
    failures = 0
    for slug, city, state, abbr in CITIES:
        html = render(template, slug, city, state, abbr)
        problems = check_page(slug, city, html)
        if problems:
            failures += 1
            for p in problems:
                print(f"[FAIL] {slug}: {p}")
            continue
        dest = ROOT / "landing-pages" / "uti-treatment" / slug / "search-safe" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html)
        print(f"[ok] {dest.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
