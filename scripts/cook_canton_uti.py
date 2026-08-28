#!/usr/bin/env python3
"""Cook Canton UTI city plate on gold chassis. Kitchen only. Does not plate live.

Replaces the listicle sitting at /uti-treatment/canton-ga/ (5 things you can text).
Woodstock stays the weekend/closed-clinic door. Canton is weeknight Riverstone / I-575.
"""
from __future__ import annotations

import html as html_lib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gold_uti_chassis as gold

ROOT = gold.ROOT
DRAFT = "<!-- COOK DRAFT 2026-08-26: Canton UTI city door. Kitchen only. Not live. Gold UTI chassis. -->\n"
BRANDS = re.compile(
    r"\b(Wellstar|Piedmont|Northside|Peachtree|Kennestone|CHOA|Banner|HonorHealth|NextCare|MinuteClinic|AFC)\b"
)


def phone_mockup(user1: str, chris1: str, user2: str, chris2: str, rx: str) -> str:
    return f"""<div class="phone-float">
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
            <div class="imsg-time">Today</div>
            <div class="imsg-bubble user">{user1}</div>
            <div class="imsg-bubble chris">{chris1}</div>
            <div class="imsg-bubble user">{user2}</div>
            <div class="imsg-bubble chris">{chris2}</div>
            <div class="imsg-rx">{rx}</div>
          </div>
        </div>
      </div>
    </div>"""


def cook() -> Path:
    url = "https://npcwoods.com/uti-treatment/canton-ga/"
    title = "UTI Treatment in Canton, GA | $59 Text Visit"
    h1 = "UTI in Canton and you don’t want the Riverstone waiting room? Text Chris."
    description = (
        "Weeknight UTI in Canton and Riverstone is a line? Text Chris Woods, NP. "
        "$59. Same-day pharmacy when it is safe. You only pay if he can treat you."
    )
    phone = phone_mockup(
        "After work in Canton. Riverstone is a line. It burns when I pee.",
        "Any fever or back pain?",
        "No fever. Just burning and I cannot stop going.",
        "Classic pattern. If text care is a fit, I’ll send it to your Canton pharmacy.",
        "✓ Plan ready · $59 · pay after",
    )
    faqs = [
        (
            "Can I get UTI antibiotics by text in Canton, GA?",
            "When it is safe, yes. Text Chris Woods, a licensed nurse practitioner, at (480) 639-4722. $59. If antibiotics are appropriate, they can go to a Canton-area pharmacy the same day. A prescription is not promised. You only pay if he can treat you.",
        ),
        (
            "What if it is not a UTI, or not safe by text?",
            "Chris will ask follow-up questions. If you need a local walk-in, an ER, or another in-person door, he will say so. You do not pay for that honesty.",
        ),
        (
            "Do I have to be in Canton?",
            "You must be physically in Georgia or another licensed state at the time of the visit. This page is for people in Canton, Holly Springs, and the rest of Cherokee County.",
        ),
        (
            "How is this different from sitting Riverstone?",
            "A Canton walk-in is a building with a chair. This is a $59 text visit with the same NP. Use the lobby for X-rays, stitches, kids who need a room, or anything that has to be examined. Use text when Riverstone or I-575 is the problem and the story is treatable by text.",
        ),
        (
            "Is this the same as the Woodstock UTI page?",
            "No. Woodstock is the weekend / clinic-closed door. Canton is the weeknight county-seat door — Riverstone, I-575, Holly Springs. Same $59 text visit. Same NP. Different street.",
        ),
    ]
    faq_html = "".join(
        f'<div class="faq-item"><div class="faq-q">{html_lib.escape(q)}</div>'
        f'<div class="faq-a"><p>{html_lib.escape(a)}</p></div></div>'
        for q, a in faqs
    )
    body = "\n".join(
        [
            gold.hero(h1, description, "$59 Flat · Canton, GA · Riverstone skip", phone),
            gold.stats(),
            gold.eeat(),
            gold.gold_reviews(),
            """<section class="section"><div class="section-inner prose" style="max-width:760px">
<span class="section-kicker">Canton, GA · Riverstone · $59</span>
<h2 class="section-title">A weeknight in Canton. Riverstone is a line. $59 text.</h2>
<p>Burning, urgency, going often, pressure — and you are coming off I-575, stuck near Riverstone Parkway, or already in Holly Springs. A chair at the county seat still means a wait.</p>
<p>NPCWoods is a <strong>$59 text visit</strong>, not a clinic on Riverstone Parkway or downtown Canton. Chris Woods, MSN, APRN, FNP-C — same nurse practitioner every time — reviews uncomplicated UTI symptoms by text when it is safe. Pay after care. No video. No appointment. No waiting room.</p>
<p>After work, after practice, or you cannot leave the house. That is the gap this page is for. Walk-ins still matter when you need a room. They are the wrong door for a weeknight UTI that is miserable and not an emergency.</p>
</div></section>""",
            gold.how_it_works(),
            """<section class="section section-light dark-to-light"><div class="section-inner" style="max-width:900px">
<span class="section-kicker">Is this right for you?</span>
<h2 class="section-title">Who this is for (and who it isn't)</h2>
<p class="section-body">This page is for adults physically in Georgia, including Canton and the rest of Cherokee County, who have classic, uncomplicated UTI-type symptoms and want a clinician review without sitting Riverstone — especially after work on a weeknight.</p>
<div class="fit-grid">
  <div class="fit-good"><div class="fit-label">Ask about a text visit if</div>
    <ul class="fit-list">
      <li>It burns when you urinate, you are going often, and this feels like UTIs you have had before</li>
      <li>You are in Canton, Holly Springs, or off I-575 and you do not want the lobby</li>
      <li>You do not have emergency symptoms, and you can name a Canton-area pharmacy for pickup</li>
    </ul>
  </div>
  <div class="fit-bad"><div class="fit-label">Go in instead if</div>
    <ul class="fit-list">
      <li>Fever with back or side pain, pregnancy, or you cannot keep fluids down</li>
      <li>You need a urine culture in a lab today, or you are getting worse fast</li>
      <li>Kids, X-rays, stitches — a Canton walk-in on Riverstone, downtown, or near I-575</li>
    </ul>
  </div>
</div>
<p class="section-body" style="margin-top:24px">This is education plus how the visit works. It is not a diagnosis.</p>
</div></section>""",
            gold.er_box(),
            f"""<section id="faq" class="section section-light dark-to-light">
  <div class="section-inner" style="max-width:720px">
    <span class="section-kicker">FAQ</span>
    <h2 class="section-title" style="text-align:center;margin-bottom:36px">Riverstone line, $59 text</h2>
    <div class="faq-list">{faq_html}</div>
  </div>
</section>""",
            """<section class="section"><div class="section-inner prose" style="max-width:760px">
<span class="section-kicker">Pay after · same NP</span>
<h2 class="section-title">$59. You pay after care.</h2>
<p>The visit is $59 cash. Pharmacy medication is separate. We are not quoting Canton walk-in cash prices we have not verified.</p>
<p>You text Chris, not a rotating pool and not a video waiting room. Follow-up on the same visit is included.</p>
<p>Full UTI pages already live: <a href="https://npcwoods.com/uti-treatment/">UTI treatment</a>, <a href="https://npcwoods.com/uti-treatment/woodstock-ga/">Woodstock UTI</a>, <a href="https://npcwoods.com/learn/uti/">UTI guide</a>. Fee: <a href="https://npcwoods.com/pricing/">pricing</a>. Statewide: <a href="https://npcwoods.com/georgia-telemedicine/">Georgia telemedicine</a>.</p>
<p>Local walk-ins matter for X-rays, stitches, and anything that needs a room. Use them when that is the job. Use this text visit <strong>instead of</strong> the lobby when the issue is treatable by text — including a weeknight on Riverstone.</p>
<p>Chris Woods, MSN, APRN, FNP-C. Licensed in Georgia under a collaborative agreement with a Georgia-licensed physician. He is a nurse practitioner, not a physician.</p>
</div></section>""",
            gold.states(),
            gold.bottom_cta(
                "Stuck on Riverstone with a UTI? Text Chris.",
                "Weeknight UTI. $59 text visit. Same-day pharmacy when it is safe. You only pay if he can treat you.",
            ),
            gold.clinician_line(),
        ]
    )
    schema = (
        '<script type="application/ld+json">\n'
        + json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://npcwoods.com/"},
                    {"@type": "ListItem", "position": 2, "name": "UTI Treatment", "item": "https://npcwoods.com/uti-treatment/"},
                    {"@type": "ListItem", "position": 3, "name": "UTI Treatment in Canton, GA", "item": url},
                ],
            },
            indent=2,
        )
        + "\n</script>\n<script type=\"application/ld+json\">\n"
        + json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in faqs
                ],
            },
            indent=2,
        )
        + "\n</script>"
    )
    doc = gold.render_page(
        title=title,
        description=description,
        canonical=url,
        og_title=h1,
        crumb_html='<nav class="crumb" aria-label="Breadcrumb"><a href="https://npcwoods.com/">Home</a> &rsaquo; <a href="https://npcwoods.com/uti-treatment/">UTI Treatment</a> &rsaquo; Canton, GA</nav>',
        schema_extra=schema,
        body=body,
        draft_comment=DRAFT,
    )
    if re.search(r"\binsurance\b", doc, re.I):
        raise SystemExit("insurance in Canton plate")
    story = re.sub(r"<table[\s\S]*?</table>", "", doc)
    hit = BRANDS.search(story)
    if hit:
        raise SystemExit(f"named clinic brand {hit.group(0)!r} in Canton plate")
    dest = ROOT / "landing-pages" / "uti-treatment" / "canton-ga" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    print(f"wrote {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes)")
    return dest


if __name__ == "__main__":
    cook()
