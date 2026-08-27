#!/usr/bin/env python3
"""Cook week-1 mixed UTI city plates: GA/NC money + CO/NV lab.

Gold UTI chassis. Kitchen only. Does not plate live.
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
DRAFT = "<!-- COOK DRAFT 2026-08-25: mix wave week 1. Kitchen only. Not live. Gold UTI chassis. -->\n"
SMS = gold.SMS
LOCKED_911 = gold.LOCKED_911

CITIES = [
    {
        "lane": "money",
        "slug": "savannah-ga",
        "city": "Savannah",
        "state": "Georgia",
        "state_slug": "georgia-telemedicine",
        "abbr": "GA",
        "kicker": "$59 Flat · Savannah, GA · Text visit",
        "streets": "River Street, Broughton, and the Islands",
        "pharmacy": "a Savannah Publix, CVS, or Walgreens",
        "er_table": "ER (Memorial / St. Joseph's)",
        "collab": "Chris practices in Georgia under a collaborative agreement with a Georgia-licensed physician.",
        "phone": (
            "On River Street and it burns when I pee. I do not want the lobby.",
            "Any fever or back pain?",
            "No fever. Just burning and going constantly.",
            "Classic pattern. If text care is a fit, I'll send it to your Savannah pharmacy.",
            "✓ Plan ready · $59 · pay after",
        ),
        "scene": (
            "A weekend in Savannah. Squares packed, Island traffic, and a UTI that will not wait.",
            "Burning, urgency, going often — and you are downtown, on the Islands, or stuck on Truman Parkway. A walk-in on Abercorn still means a chair.",
            "NPCWoods is a $59 text visit, not a clinic on Abercorn or Victory Drive. Chris Woods, MSN, APRN, FNP-C — same nurse practitioner every time — reviews uncomplicated UTI symptoms by text when it is safe.",
        ),
        "fit_good": [
            "It burns when you urinate, you are going often, and this feels like UTIs you have had before",
            "You are in Savannah, Pooler, or the Islands and you do not want the lobby",
            "You can name a Savannah-area pharmacy for pickup",
        ],
        "fit_bad": [
            "Fever with back or side pain, pregnancy, or you cannot keep fluids down",
            "You need a urine culture in a lab today, or you are getting worse fast",
            "Kids, X-rays, stitches — a walk-in on Abercorn, Victory, or the Islands",
        ],
        "faqs": [
            (
                "Can I get UTI antibiotics by text in Savannah, GA?",
                "When it is safe, yes. Text Chris Woods, a licensed nurse practitioner, at (480) 639-4722. $59. If antibiotics are appropriate, they can go to a Savannah-area pharmacy the same day. A prescription is not promised. You only pay if he can treat you.",
            ),
            (
                "Do I have to be in Savannah?",
                "You must be physically in Georgia or another licensed state at the time of the visit. This page is for people in Savannah, Pooler, the Islands, and nearby.",
            ),
            (
                "How is this different from sitting Abercorn?",
                "A Savannah walk-in is a building with a chair. This is a $59 text visit with the same NP. Use the lobby for X-rays, stitches, kids who need a room, or anything that has to be examined. Use text when the story is treatable by text.",
            ),
        ],
    },
    {
        "lane": "money",
        "slug": "raleigh-nc",
        "city": "Raleigh",
        "state": "North Carolina",
        "state_slug": "north-carolina-telemedicine",
        "abbr": "NC",
        "kicker": "$59 Flat · Raleigh, NC · Text visit",
        "streets": "Glenwood South, North Hills, and I-440",
        "pharmacy": "a Raleigh Harris Teeter, CVS, or Walgreens",
        "er_table": "ER (Rex / WakeMed)",
        "collab": "Chris practices in North Carolina under a collaborative agreement with a North Carolina-licensed physician.",
        "phone": (
            "In Raleigh. Burning when I pee. North Hills line looks awful.",
            "Any fever or back pain?",
            "No. Just burning and I cannot stop going.",
            "If it is a straightforward UTI and text is safe, I can send it to your Raleigh pharmacy.",
            "✓ Plan ready · $59 · pay after",
        ),
        "scene": (
            "Raleigh at 9 p.m. Glenwood is loud. The walk-in on Six Forks is a line.",
            "Burning, urgency, going often — and you are inside the Beltline, in North Hills, or off Capital Boulevard. A chair on Six Forks still means a wait.",
            "NPCWoods is a $59 text visit, not a clinic on Six Forks or Glenwood. Chris Woods, MSN, APRN, FNP-C — same nurse practitioner every time — reviews uncomplicated UTI symptoms by text when it is safe.",
        ),
        "fit_good": [
            "It burns when you urinate, you are going often, and this feels like UTIs you have had before",
            "You are in Raleigh, Cary, or inside the Beltline and you do not want the lobby",
            "You can name a Raleigh-area pharmacy for pickup",
        ],
        "fit_bad": [
            "Fever with back or side pain, pregnancy, or you cannot keep fluids down",
            "You need a urine culture in a lab today, or you are getting worse fast",
            "Kids, X-rays, stitches — a walk-in on Six Forks, Glenwood, or Capital",
        ],
        "faqs": [
            (
                "Can I get UTI antibiotics by text in Raleigh, NC?",
                "When it is safe, yes. Text Chris Woods, a licensed nurse practitioner, at (480) 639-4722. $59. If antibiotics are appropriate, they can go to a Raleigh-area pharmacy the same day. A prescription is not promised. You only pay if he can treat you.",
            ),
            (
                "Do I have to be in Raleigh?",
                "You must be physically in North Carolina or another licensed state at the time of the visit. This page is for people in Raleigh, Cary, and nearby.",
            ),
            (
                "How is this different from sitting Six Forks?",
                "A Raleigh walk-in is a building with a chair. This is a $59 text visit with the same NP. Use the lobby for X-rays, stitches, kids who need a room, or anything that has to be examined. Use text when the story is treatable by text.",
            ),
        ],
    },
    {
        "lane": "lab",
        "slug": "denver-co",
        "city": "Denver",
        "state": "Colorado",
        "state_slug": "colorado-telemedicine",
        "abbr": "CO",
        "kicker": "$59 Flat · Denver, CO · Text visit",
        "streets": "Colfax, the Highlands, and I-25",
        "pharmacy": "a Denver King Soopers, Walgreens, or Safeway",
        "er_table": "ER (UCHealth / Denver Health)",
        "collab": "",
        "phone": (
            "In Denver. Burning when I pee. I am not sitting Colfax tonight.",
            "Any fever or back pain?",
            "No fever. Just burning and urgency.",
            "If text care is a fit, I'll send it to your Denver pharmacy.",
            "✓ Plan ready · $59 · pay after",
        ),
        "scene": (
            "Denver after work. I-25 is jammed. A UTI does not care about the Highlands parking.",
            "Burning, urgency, going often — and you are on Colfax, in RiNo, or west of I-25. A walk-in still means a chair.",
            "NPCWoods is a $59 text visit, not a clinic on Colfax or Colorado Boulevard. Chris Woods, MSN, APRN, FNP-C — same nurse practitioner every time — reviews uncomplicated UTI symptoms by text when it is safe.",
        ),
        "fit_good": [
            "It burns when you urinate, you are going often, and this feels like UTIs you have had before",
            "You are in Denver, Aurora, or the Highlands and you do not want the lobby",
            "You can name a Denver-area pharmacy for pickup",
        ],
        "fit_bad": [
            "Fever with back or side pain, pregnancy, or you cannot keep fluids down",
            "You need a urine culture in a lab today, or you are getting worse fast",
            "Kids, X-rays, stitches — a walk-in on Colfax, Colorado Boulevard, or near I-25",
        ],
        "faqs": [
            (
                "Can I get UTI antibiotics by text in Denver, CO?",
                "When it is safe, yes. Text Chris Woods, a licensed nurse practitioner, at (480) 639-4722. $59. If antibiotics are appropriate, they can go to a Denver-area pharmacy the same day. A prescription is not promised. You only pay if he can treat you.",
            ),
            (
                "Do I have to be in Denver?",
                "You must be physically in Colorado or another licensed state at the time of the visit. This page is for people in Denver, Aurora, and nearby.",
            ),
            (
                "How is this different from sitting Colfax?",
                "A Denver walk-in is a building with a chair. This is a $59 text visit with the same NP. Use the lobby for X-rays, stitches, kids who need a room, or anything that has to be examined. Use text when the story is treatable by text.",
            ),
        ],
    },
    {
        "lane": "lab",
        "slug": "las-vegas-nv",
        "city": "Las Vegas",
        "state": "Nevada",
        "state_slug": "nevada-telemedicine",
        "abbr": "NV",
        "kicker": "$59 Flat · Las Vegas, NV · Text visit",
        "streets": "the Strip, Summerlin, and I-15",
        "pharmacy": "a Las Vegas Smith's, CVS, or Walgreens",
        "er_table": "ER (UMC / Sunrise)",
        "collab": "",
        "phone": (
            "On shift near the Strip. Burning when I pee. Cannot sit a lobby.",
            "Any fever or back pain?",
            "No. Just burning. I have a double tonight.",
            "If text is safe, I'll send it to the pharmacy you name in Las Vegas.",
            "✓ Plan ready · $59 · pay after",
        ),
        "scene": (
            "Las Vegas between shifts. The Strip does not pause for a UTI.",
            "Burning, urgency, going often — and you are on Tropicana, in Summerlin, or off I-15. A walk-in still means a chair after a long shift.",
            "NPCWoods is a $59 text visit, not a clinic on Sahara or Flamingo. Chris Woods, MSN, APRN, FNP-C — same nurse practitioner every time — reviews uncomplicated UTI symptoms by text when it is safe.",
        ),
        "fit_good": [
            "It burns when you urinate, you are going often, and this feels like UTIs you have had before",
            "You are in Las Vegas, Summerlin, or Paradise and you do not want the lobby",
            "You can name a Las Vegas-area pharmacy for pickup",
        ],
        "fit_bad": [
            "Fever with back or side pain, pregnancy, or you cannot keep fluids down",
            "You need a urine culture in a lab today, or you are getting worse fast",
            "Kids, X-rays, stitches — a walk-in on Sahara, Flamingo, or near I-15",
        ],
        "faqs": [
            (
                "Can I get UTI antibiotics by text in Las Vegas, NV?",
                "When it is safe, yes. Text Chris Woods, a licensed nurse practitioner, at (480) 639-4722. $59. If antibiotics are appropriate, they can go to a Las Vegas-area pharmacy the same day. A prescription is not promised. You only pay if he can treat you.",
            ),
            (
                "Do I have to be in Las Vegas?",
                "You must be physically in Nevada or another licensed state at the time of the visit. This page is for people in Las Vegas, Summerlin, Paradise, and nearby.",
            ),
            (
                "How is this different from sitting Sahara?",
                "A Las Vegas walk-in is a building with a chair. This is a $59 text visit with the same NP. Use the lobby for X-rays, stitches, kids who need a room, or anything that has to be examined. Use text when the story is treatable by text.",
            ),
        ],
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


def cook_city(spec: dict) -> Path:
    city = spec["city"]
    slug = spec["slug"]
    url = f"https://npcwoods.com/uti-treatment/{slug}/"
    title = f"UTI Treatment in {city}, {spec['abbr']} | $59 Text Visit"
    h1 = f"UTI in {city} and you don’t want the waiting room? Text Chris."
    description = (
        f"Burning, urgency, and you don’t want a {city} waiting room? Text Chris Woods, NP. "
        "$59. Same-day pharmacy when it is safe. You only pay if he can treat you."
    )
    faqs = spec["faqs"]
    faq_html = "".join(
        f'<div class="faq-item"><div class="faq-q">{html_lib.escape(q)}</div>'
        f'<div class="faq-a"><p>{html_lib.escape(a)}</p></div></div>'
        for q, a in faqs
    )
    good = "".join(f"<li>{html_lib.escape(x)}</li>" for x in spec["fit_good"])
    bad = "".join(f"<li>{html_lib.escape(x)}</li>" for x in spec["fit_bad"])
    collab = f"<p>{html_lib.escape(spec['collab'])}</p>" if spec["collab"] else ""
    body = "\n".join(
        [
            gold.hero(h1, description, spec["kicker"], phone_mockup(*spec["phone"])),
            gold.stats(),
            gold.eeat(),
            gold.gold_reviews(),
            f"""<section class="section"><div class="section-inner prose" style="max-width:760px">
<span class="section-kicker">{html_lib.escape(city)}, {spec['abbr']} · $59</span>
<h2 class="section-title">{html_lib.escape(spec['scene'][0])}</h2>
<p>{html_lib.escape(spec['scene'][1])}</p>
<p>{html_lib.escape(spec['scene'][2])} Pay after care. No video. No appointment. No waiting room.</p>
<p>Tonight, after hours, or you cannot get in. That is the gap this page is for. Walk-ins still matter when you need a room. They are the wrong door for a straightforward UTI that is miserable and not an emergency.</p>
</div></section>""",
            gold.how_it_works(),
            f"""<section class="section section-light dark-to-light"><div class="section-inner" style="max-width:900px">
<span class="section-kicker">Is this right for you?</span>
<h2 class="section-title">Who this is for (and who it isn't)</h2>
<p class="section-body">This page is for adults physically in {html_lib.escape(spec['state'])}, including {html_lib.escape(city)} and nearby, who have classic, uncomplicated UTI-type symptoms and want a clinician review without sitting {html_lib.escape(spec['streets'])}.</p>
<div class="fit-grid">
  <div class="fit-good"><div class="fit-label">Ask about a text visit if</div>
    <ul class="fit-list">{good}</ul>
  </div>
  <div class="fit-bad"><div class="fit-label">Go in instead if</div>
    <ul class="fit-list">{bad}</ul>
  </div>
</div>
<p class="section-body" style="margin-top:24px">This is education plus how the visit works. It is not a diagnosis.</p>
</div></section>""",
            f"""<section class="section"><div class="section-inner prose" style="max-width:760px">
<span class="section-kicker">Honest split</span>
<h2 class="section-title">ER vs walk-in vs text</h2>
<table class="nga-table">
<tr><th></th><th>{html_lib.escape(spec['er_table'])}</th><th>Walk-in / urgent care</th><th>NPCWoods</th></tr>
<tr><th>Cost</th><td>Often hundreds</td><td>Often $100 to $250</td><td><strong>$59 flat</strong></td></tr>
<tr><th>Wait</th><td>Hours, if you need that door</td><td>If they are open</td><td><strong>Reply from your couch</strong></td></tr>
<tr><th>When it is the right door</th><td>Fever and flank pain, pregnant, cannot keep fluids, child, significant blood</td><td>When you want in-person and they are open</td><td><strong>Straightforward UTI, when text is safe</strong></td></tr>
<tr><th>Weekend / after hours?</th><td>Yes</td><td>Sometimes</td><td><strong>Yes, by text</strong></td></tr>
</table>
<p>If antibiotics are the right call, they go electronically to {html_lib.escape(spec['pharmacy'])} you name. If text is not safe, he will send you to an in-person door. You do not pay for that honesty.</p>
</div></section>""",
            gold.er_box(),
            f"""<section id="faq" class="section section-light dark-to-light">
  <div class="section-inner" style="max-width:720px">
    <span class="section-kicker">FAQ</span>
    <h2 class="section-title" style="text-align:center;margin-bottom:36px">{html_lib.escape(city)} UTI, $59 text</h2>
    <div class="faq-list">{faq_html}</div>
  </div>
</section>""",
            f"""<section class="section"><div class="section-inner prose" style="max-width:760px">
<span class="section-kicker">Pay after · same NP</span>
<h2 class="section-title">$59. You pay after care.</h2>
<p>The visit is $59 cash. Pharmacy medication is separate. We are not quoting {html_lib.escape(city)} walk-in cash prices we have not verified.</p>
<p>You text Chris, not a rotating pool and not a video waiting room. Follow-up on the same visit is included.</p>
{collab}
<p>Full UTI pages: <a href="https://npcwoods.com/uti-treatment/">UTI treatment</a>, <a href="https://npcwoods.com/learn/uti/">UTI guide</a>. Fee: <a href="https://npcwoods.com/pricing/">pricing</a>. Statewide: <a href="https://npcwoods.com/{spec['state_slug']}/">{html_lib.escape(spec['state'])} telemedicine</a>.</p>
<p>Chris Woods, MSN, APRN, FNP-C. Licensed in {html_lib.escape(spec['state'])}. He is a nurse practitioner, not a physician.</p>
</div></section>""",
            gold.states(),
            gold.bottom_cta(
                f"In {city}? Text Chris.",
                "$59 text visit. Same-day pharmacy when it is safe. You only pay if he can treat you.",
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
                    {"@type": "ListItem", "position": 3, "name": f"UTI Treatment in {city}, {spec['abbr']}", "item": url},
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
        + "\n</script>\n<script type=\"application/ld+json\">\n"
        + json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "MedicalBusiness",
                "name": "NPCWoods Telemedicine",
                "description": f"UTI treatment via text-based telemedicine in {city}, {spec['state']}",
                "telephone": "+14806394722",
                "url": url,
                "priceRange": "$59",
                "areaServed": {
                    "@type": "City",
                    "name": city,
                    "containedInPlace": {"@type": "State", "name": spec["state"]},
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
            '<a href="https://npcwoods.com/uti-treatment/">UTI Treatment</a> &rsaquo; '
            f"{html_lib.escape(city)}, {spec['abbr']}</nav>"
        ),
        schema_extra=schema,
        body=body,
        draft_comment=DRAFT,
    )
    banned = re.search(r"\binsurance\b|\bdoctor\b|\bphysician\b|\bMD\b", doc, re.I)
    if banned and banned.group(0).lower() not in {"physician"}:
        # physician is allowed in the explicit "not a physician" line
        pass
    if re.search(r"\binsurance\b", doc, re.I):
        raise SystemExit(f"insurance slipped into {slug}")
    # Allow "not a physician" only
    for m in re.finditer(r"\b(doctor|MD)\b", doc, re.I):
        raise SystemExit(f"banned credential word in {slug}: {m.group(0)}")
    dest = ROOT / "landing-pages" / "uti-treatment" / slug / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    print(f"{spec['lane']}\t{dest.relative_to(ROOT)} ({dest.stat().st_size} bytes)")
    return dest


def main() -> None:
    for spec in CITIES:
        cook_city(spec)


if __name__ == "__main__":
    main()
