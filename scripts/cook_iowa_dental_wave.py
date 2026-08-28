#!/usr/bin/env python3
"""Cook Iowa dental-abscess city plates on the gold UTI chassis.

Clinical lock: antibiotics are a bridge. A dentist still has to treat the tooth.
Kitchen only. Does not plate live.

Week roster (4/day, mid-size first):
  Day 1: ames-ia, iowa-city-ia, dubuque-ia, waterloo-ia
  Day 2: cedar-falls-ia, mason-city-ia, burlington-ia, ottumwa-ia
  Day 3: fort-dodge-ia, muscatine-ia, marshalltown-ia, clinton-ia
  Day 4: ankeny-ia, marion-ia, bettendorf-ia, cedar-rapids-ia
  Day 5: davenport-ia, sioux-city-ia, council-bluffs-ia, des-moines-ia
  Day 6: west-des-moines-ia, coralville-ia, urbandale-ia, johnston-ia
  Day 7: newton-ia, pella-ia, indianola-ia, grinnell-ia
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
DRAFT = "<!-- COOK DRAFT 2026-08-28: Iowa dental wave. Kitchen only. Not live. Gold chassis. Bridge antibiotics. -->\n"
DAY1 = ["ames-ia", "iowa-city-ia", "dubuque-ia", "waterloo-ia"]
SMS = gold.SMS

CITIES = [
    {
        "slug": "ames-ia",
        "city": "Ames",
        "nearby": "Ames, Nevada, or Boone",
        "streets": "Main Street, Lincoln Way, and campus",
        "pharmacy": "an Ames Hy-Vee, CVS, or Walgreens",
        "er_table": "ER (Mary Greeley)",
        "phone": (
            "In Ames. Tooth is pounding. Dentist is closed.",
            "Any swelling of the face or trouble swallowing?",
            "No. Just the tooth. Throbbing. I cannot get a dentist until next week.",
            "If a bridge antibiotic is safe, I can send it to your Ames pharmacy. You still need a dentist for the tooth.",
            "✓ Bridge plan · $59 · pay after",
        ),
        "scene": (
            "Ames on a weeknight. Campus is quiet. The tooth is not.",
            "Throbbing, swelling at the gum, and the dentist on Main Street is closed. A walk-in on Lincoln Way still means a chair — and they still cannot drill the tooth.",
            "NPCWoods is a $59 text visit. Chris Woods, MSN, APRN, FNP-C, reviews dental abscess symptoms by text when it is safe. If antibiotics are appropriate, they can go to your pharmacy. That is a bridge. A dentist still has to treat the tooth.",
        ),
        "walk_in": "Lincoln Way, Main Street, or near campus",
    },
    {
        "slug": "iowa-city-ia",
        "city": "Iowa City",
        "nearby": "Iowa City, Coralville, or North Liberty",
        "streets": "downtown, Gilbert Street, and Iowa Avenue",
        "pharmacy": "an Iowa City Hy-Vee, CVS, or Walgreens",
        "er_table": "ER (UIHC)",
        "phone": (
            "Iowa City. Abscess. I cannot get a dentist until Monday.",
            "Face swelling, fever, or trouble swallowing?",
            "Gum is puffy. Tooth hurts. No trouble breathing.",
            "If text is safe, I can send a bridge antibiotic to your Iowa City pharmacy. You still need a dentist for the tooth.",
            "✓ Bridge plan · $59 · pay after",
        ),
        "scene": (
            "Iowa City after hours. Downtown is still up. The dentist is not.",
            "Throbbing tooth, gum swelling, and you are on Gilbert, Iowa Avenue, or campus. A walk-in still cannot pull the tooth.",
            "NPCWoods is a $59 text visit. Chris Woods, MSN, APRN, FNP-C, reviews dental abscess symptoms by text when it is safe. If antibiotics are appropriate, they can go to your pharmacy. That is a bridge. A dentist still has to treat the tooth.",
        ),
        "walk_in": "Gilbert, Iowa Avenue, or downtown",
    },
    {
        "slug": "dubuque-ia",
        "city": "Dubuque",
        "nearby": "Dubuque, Asbury, or East Dubuque",
        "streets": "Main Street, Central, and the bluff",
        "pharmacy": "a Dubuque Hy-Vee, CVS, or Walgreens",
        "er_table": "ER (MercyOne / Finley)",
        "phone": (
            "In Dubuque. Tooth abscess. Dentist cannot see me for days.",
            "Any spreading face swelling or trouble swallowing?",
            "No. Just the tooth and the gum.",
            "If a bridge antibiotic is safe, I will send it to your Dubuque pharmacy. A dentist still has to treat the tooth.",
            "✓ Bridge plan · $59 · pay after",
        ),
        "scene": (
            "Dubuque on the bluff. Main Street is closed for the night. The abscess is not.",
            "Throbbing, gum swelling, and you are downtown, on Central, or off US-20. A walk-in is a chair. It is not a dental drill.",
            "NPCWoods is a $59 text visit. Chris Woods, MSN, APRN, FNP-C, reviews dental abscess symptoms by text when it is safe. If antibiotics are appropriate, they can go to your pharmacy. That is a bridge. A dentist still has to treat the tooth.",
        ),
        "walk_in": "Main Street, Central, or US-20",
    },
    {
        "slug": "waterloo-ia",
        "city": "Waterloo",
        "nearby": "Waterloo, Cedar Falls, or Evansdale",
        "streets": "downtown, San Marnan, and University",
        "pharmacy": "a Waterloo Hy-Vee, CVS, or Walgreens",
        "er_table": "ER (UnityPoint / MercyOne)",
        "phone": (
            "Waterloo. Tooth is killing me. Cannot get a dentist today.",
            "Fever, face swelling, or trouble swallowing?",
            "No fever. Just throbbing and a swollen gum.",
            "If text is safe, I can send a bridge antibiotic to your Waterloo pharmacy. You still need a dentist for the tooth.",
            "✓ Bridge plan · $59 · pay after",
        ),
        "scene": (
            "Waterloo after a shift. San Marnan is a line. The tooth will not wait.",
            "Throbbing, gum swelling, and you are downtown, on University, or off US-20. A walk-in can look. It cannot finish the tooth.",
            "NPCWoods is a $59 text visit. Chris Woods, MSN, APRN, FNP-C, reviews dental abscess symptoms by text when it is safe. If antibiotics are appropriate, they can go to your pharmacy. That is a bridge. A dentist still has to treat the tooth.",
        ),
        "walk_in": "San Marnan, University, or downtown",
    },
]


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
            <div class="imsg-bubble user">{html_lib.escape(user1)}</div>
            <div class="imsg-bubble chris">{html_lib.escape(chris1)}</div>
            <div class="imsg-bubble user">{html_lib.escape(user2)}</div>
            <div class="imsg-bubble chris">{html_lib.escape(chris2)}</div>
            <div class="imsg-rx">{html_lib.escape(rx)}</div>
          </div>
        </div>
      </div>
    </div>"""


def dental_how_it_works() -> str:
    return f"""<section id="how-it-works" class="section section-light dark-to-light">
  <div class="section-inner">
    <span class="section-kicker">How it works</span>
    <h2 class="section-title">Three texts. Bridge only.</h2>
    <p class="section-body">No app, no portal, no video. Antibiotics, when appropriate, are a bridge. A dentist still has to treat the tooth. You only pay if he can treat you.</p>
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
        <p>Chris Woods, MSN, APRN, FNP-C, reads it himself. Same nurse practitioner every time. He screens for spreading infection.</p>
      </div>
      <div class="bento-card">
        <div class="step-num">3</div>
        <h3>Bridge, then dentist</h3>
        <p>If a bridge antibiotic is safe, it can go to the pharmacy you name. It does not fix the tooth. You still need a dentist.</p>
      </div>
    </div>
  </div>
</section>"""


def cook_city(spec: dict) -> Path:
    city = spec["city"]
    slug = spec["slug"]
    url = f"https://npcwoods.com/dental-pain/{slug}/"
    title = f"Dental Abscess in {city}, IA | $59 Text Bridge"
    h1 = f"Dental abscess in {city} and the dentist is closed? Text Chris."
    description = (
        f"Tooth infection or dental abscess in {city} and you cannot get to a dentist? "
        "Text Chris Woods, NP. $59. Same-day pharmacy when it is safe. Antibiotics are a bridge. "
        "You still need a dentist for the tooth."
    )
    faqs = [
        (
            f"Can I get antibiotics for a dental abscess by text in {city}, IA?",
            f"When it is safe, sometimes. Text Chris Woods, a licensed nurse practitioner, at (480) 639-4722. $59. If antibiotics are appropriate, they can go to {spec['pharmacy']} the same day. A prescription is not promised. Antibiotics are a bridge. You still need a dentist for the tooth.",
        ),
        (
            "Do antibiotics cure the tooth?",
            "No. Antibiotics do not repair a decayed or infected tooth. NPCWoods can only bridge the gap so you can get to a dentist for the real work: root canal, extraction, or whatever the tooth needs.",
        ),
        (
            f"Do I have to be in {city}?",
            f"You must be physically in Iowa or another licensed state at the time of the visit. This page is for people in {spec['nearby']}.",
        ),
        (
            "When is this the wrong door?",
            "Go to the ER for spreading facial swelling, trouble breathing or swallowing, high fever, or an infection that looks like it is moving into the neck or eye. Text is not for that.",
        ),
    ]
    faq_html = "".join(
        f'<div class="faq-item"><div class="faq-q">{html_lib.escape(q)}</div>'
        f'<div class="faq-a"><p>{html_lib.escape(a)}</p></div></div>'
        for q, a in faqs
    )
    body = "\n".join(
        [
            gold.hero(h1, description, f"$59 Flat · {city}, IA · Bridge only", phone_mockup(*spec["phone"])),
            gold.stats(),
            gold.eeat(),
            gold.gold_reviews(),
            f"""<section class="section"><div class="section-inner prose" style="max-width:760px">
<span class="section-kicker">{html_lib.escape(city)}, IA · dental abscess · $59</span>
<h2 class="section-title">{html_lib.escape(spec['scene'][0])}</h2>
<p>{html_lib.escape(spec['scene'][1])}</p>
<p>{html_lib.escape(spec['scene'][2])} Pay after care. No video. No appointment.</p>
<p><strong>This is not dental care.</strong> It is a clinical bridge when a dentist cannot see you tonight. The tooth still needs a dentist.</p>
</div></section>""",
            dental_how_it_works(),
            f"""<section class="section section-light dark-to-light"><div class="section-inner" style="max-width:900px">
<span class="section-kicker">Is this right for you?</span>
<h2 class="section-title">Who this is for (and who it isn't)</h2>
<p class="section-body">This page is for adults physically in Iowa, including {html_lib.escape(spec['nearby'])}, who have a tooth infection or dental abscess and cannot get to a dentist right now.</p>
<div class="fit-grid">
  <div class="fit-good"><div class="fit-label">Ask about a text visit if</div>
    <ul class="fit-list">
      <li>The tooth is throbbing, the gum is swollen, and this feels like an abscess</li>
      <li>The dentist is closed, full, or days out, and you are in {html_lib.escape(city)}</li>
      <li>You can name {html_lib.escape(spec['pharmacy'])} for pickup</li>
    </ul>
  </div>
  <div class="fit-bad"><div class="fit-label">Go in instead if</div>
    <ul class="fit-list">
      <li>Spreading facial swelling, trouble breathing or swallowing, high fever</li>
      <li>The infection looks like it is moving into the neck or around the eye</li>
      <li>You need a room, imaging, or kids — a walk-in on {html_lib.escape(spec['walk_in'])}</li>
    </ul>
  </div>
</div>
<p class="section-body" style="margin-top:24px">This is education plus how the visit works. It is not a diagnosis. Antibiotics do not replace a dentist.</p>
</div></section>""",
            f"""<section class="section"><div class="section-inner prose" style="max-width:760px">
<span class="section-kicker">Honest split</span>
<h2 class="section-title">ER vs walk-in vs text bridge</h2>
<table class="nga-table">
<tr><th></th><th>{html_lib.escape(spec['er_table'])}</th><th>Walk-in</th><th>NPCWoods</th></tr>
<tr><th>Cost</th><td>Often hundreds</td><td>Often $100 to $250</td><td><strong>$59 flat</strong></td></tr>
<tr><th>What they can do</th><td>Airway, spreading infection, imaging</td><td>Look, maybe pain meds, rarely the tooth</td><td><strong>Bridge antibiotic when text is safe</strong></td></tr>
<tr><th>Fixes the tooth?</th><td>No</td><td>No</td><td><strong>No. Dentist still required</strong></td></tr>
<tr><th>When it is the right door</th><td>Spreading swelling, fever, cannot swallow</td><td>When you want in-person and they are open</td><td><strong>Dentist closed, abscess pattern, text is safe</strong></td></tr>
</table>
<p>If a bridge antibiotic is the right call, it goes electronically to {html_lib.escape(spec['pharmacy'])} you name. If text is not safe, he will send you to an in-person door. You do not pay for that honesty.</p>
</div></section>""",
            gold.er_box(),
            f"""<section id="faq" class="section section-light dark-to-light">
  <div class="section-inner" style="max-width:720px">
    <span class="section-kicker">FAQ</span>
    <h2 class="section-title" style="text-align:center;margin-bottom:36px">{html_lib.escape(city)} dental abscess, $59 bridge</h2>
    <div class="faq-list">{faq_html}</div>
  </div>
</section>""",
            f"""<section class="section"><div class="section-inner prose" style="max-width:760px">
<span class="section-kicker">Pay after · same NP</span>
<h2 class="section-title">$59. Bridge only. Dentist still required.</h2>
<p>The visit is $59 cash. Pharmacy medication is separate. We are not quoting {html_lib.escape(city)} walk-in cash prices we have not verified.</p>
<p>You text Chris, not a rotating pool. Follow-up on the same visit is included. A dentist still has to treat the tooth.</p>
<p>Hub: <a href="https://npcwoods.com/dental-pain/">dental pain</a>. Fee: <a href="https://npcwoods.com/pricing/">pricing</a>. Statewide: <a href="https://npcwoods.com/iowa-telemedicine/">Iowa telemedicine</a>.</p>
<p>Chris Woods, MSN, APRN, FNP-C. Licensed in Iowa. He is a nurse practitioner.</p>
</div></section>""",
            gold.states(),
            gold.bottom_cta(
                f"Dentist closed in {city}? Text Chris.",
                "Dental abscess. $59 text visit. Bridge antibiotic when it is safe. You still need a dentist for the tooth.",
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
                    {"@type": "ListItem", "position": 2, "name": "Dental Pain", "item": "https://npcwoods.com/dental-pain/"},
                    {"@type": "ListItem", "position": 3, "name": f"Dental Abscess in {city}, IA", "item": url},
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
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in faqs
                ],
            },
            indent=2,
        )
        + "\n</script>\n<script type=\"application/ld+json\">\n"
        + json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "MedicalBusiness",
                "name": "NPCWoods Telemedicine",
                "description": f"Dental abscess bridge care via text-based telemedicine in {city}, Iowa",
                "telephone": "+14806394722",
                "url": url,
                "priceRange": "$59",
                "areaServed": {
                    "@type": "City",
                    "name": city,
                    "containedInPlace": {"@type": "State", "name": "Iowa"},
                },
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
        crumb_html=(
            '<nav class="crumb" aria-label="Breadcrumb">'
            '<a href="https://npcwoods.com/">Home</a> &rsaquo; '
            '<a href="https://npcwoods.com/dental-pain/">Dental Pain</a> &rsaquo; '
            f"{html_lib.escape(city)}, IA</nav>"
        ),
        schema_extra=schema,
        body=body,
        draft_comment=DRAFT,
    )
    if re.search(r"\binsurance\b", doc, re.I):
        raise SystemExit(f"insurance slipped into {slug}")
    for m in re.finditer(r"\b(doctor|MD)\b", doc, re.I):
        raise SystemExit(f"banned credential word in {slug}: {m.group(0)}")
    dest = ROOT / "landing-pages" / "dental-pain" / slug / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    print(f"wrote {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes)")
    return dest


def main() -> None:
    wanted = set(sys.argv[1:] or DAY1)
    cooked = [spec for spec in CITIES if spec["slug"] in wanted]
    if not cooked:
        raise SystemExit(f"no matching cities for {sorted(wanted)}")
    for spec in cooked:
        cook_city(spec)


if __name__ == "__main__":
    main()
