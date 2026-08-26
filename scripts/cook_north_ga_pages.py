#!/usr/bin/env python3
"""Cook 2026-08-24 North GA plates on the gold UTI hub chassis. Does not plate live."""
from __future__ import annotations

import html as html_lib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gold_uti_chassis as gold

ROOT = gold.ROOT
HQ = ROOT.parent
BAG = HQ / "content-output" / "grokbot-bags" / "north-ga-blogs-2026-08-24"
DRAFT = "<!-- COOK DRAFT 2026-08-24: kitchen only. Not live. Do not SFTP. Gold UTI chassis. -->\n"
SMS = gold.SMS
LOCKED_911 = gold.LOCKED_911

ARTICLES = [
    {
        "md": "01-woodstock-skip-the-urgent-care-lobby.md",
        "slug": "skip-the-urgent-care-woodstock-ga",
        "title": "7 reasons people in Woodstock skip the urgent-care lobby | $59 text visit",
        "h1": "7 reasons people in Woodstock skip the urgent-care lobby",
        "description": "Woodstock has real walk-ins on Highway 92, Towne Lake, and Main Street. When the issue is treatable by text, skip the chair. $59. Same NP. Pay after care.",
        "kicker": "Woodstock, GA · $59 · Skip the lobby",
        "crumb": "Skip the lobby in Woodstock",
        "cta": "In Woodstock tonight? Text Chris.",
    },
    {
        "md": "02-cobb-county-urgent-care-vs-text-visit.md",
        "slug": "urgent-care-vs-text-visit-cobb-county",
        "title": "Urgent care vs a $59 text visit in Cobb County | NPCWoods",
        "h1": "Urgent care vs a $59 text visit in Cobb County",
        "description": "Marietta and East Cobb walk-ins do real in-person work. A $59 text visit with Chris Woods, NP, is the skip when you do not need a room.",
        "kicker": "Cobb County · $59 · Text visit",
        "crumb": "Cobb County text visit",
        "cta": "East Cobb, Delk, or Sandy Plains? Text first if you do not need a room.",
    },
    {
        "md": "03-canton-ga-5-things-you-can-text.md",
        "slug": "canton-ga-urgent-care-text-visit",
        "title": "5 things Canton GA urgent care can treat that you can also text an NP about",
        "h1": "5 things Canton GA urgent care can treat that you can also text an NP about",
        "description": "UTI, sinus, strep or ear, dental pain, and ED can start by text when the story is straightforward. Canton walk-ins stay for rooms and X-rays. $59.",
        "kicker": "Canton, GA · $59 · Text or lobby",
        "crumb": "Canton text visit",
        "cta": "In Canton? Ask if the lobby is even required.",
    },
    {
        "md": "04-marietta-urgent-care-line-how-to.md",
        "slug": "urgent-care-line-marietta-ga",
        "title": "What to do when every urgent care near Marietta has a line | NPCWoods",
        "h1": "What to do when every urgent care near Marietta has a line",
        "description": "Saturday evening in Marietta: 911 first, then a room if you need one, then a $59 text visit when the issue is treatable by text.",
        "kicker": "Marietta · 911 · Room · Text",
        "crumb": "Marietta urgent-care line",
        "cta": "Marietta line and you do not need a room? Text Chris.",
    },
    {
        "md": "06-cherokee-county-urgent-care-near-me.md",
        "slug": "urgent-care-near-me-cherokee-county",
        "title": "Urgent care near me in Cherokee County — and the text option if you cannot leave",
        "h1": "Urgent care near me in Cherokee County",
        "description": "Named Woodstock and Canton walk-ins, plus a $59 text visit with Chris Woods, NP, when you cannot leave the house.",
        "kicker": "Cherokee County · Near me · $59 text",
        "crumb": "Cherokee County near me",
        "cta": "If the map is a building you cannot drive to, text the NP.",
    },
]


CLOCK_HOURS = re.compile(
    r"\b\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)?\s*(?:-|–|—|to|until)\s*"
    r"\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)\b",
    re.I,
)
CLOCK_SWAPS = (
    (
        "Main Street walk-ins often list 8:00 a.m. to 8:00 p.m. Confirm before you drive.",
        "Main Street walk-ins often list daytime-into-evening hours. Confirm before you drive.",
    ),
    (
        "several publish walk-in hours in the 8 a.m. to 8 p.m. range",
        "several publish daytime-into-evening walk-in hours",
    ),
    (
        "East Cobb walk-ins often list 8 a.m. to 8 p.m. Confirm before you drive",
        "East Cobb walk-ins often list daytime-into-evening hours. Confirm before you drive",
    ),
    (
        "Main Street walk-in (published 8 a.m. to 8 p.m.)",
        "Main Street walk-in (published daytime-into-evening hours)",
    ),
    (
        "Transit Avenue near I-575 and Riverstone Parkway (published 8 a.m. to 8 p.m.)",
        "Transit Avenue near I-575 and Riverstone Parkway (published daytime-into-evening hours)",
    ),
)
CHEROKEE_SWAPS = (
    (
        "This page names real Cherokee County walk-ins so the map feels honest. Then it explains the other option: a $59 text visit with Chris Woods, MSN, APRN, FNP-C, when the issue is treatable by text.",
        "This is not a directory of Cherokee buildings. It is the skip when you cannot leave the house: a $59 text visit with Chris Woods, MSN, APRN, FNP-C, when the issue is treatable by text.",
    ),
    (
        "## What “near me” actually is in this county",
        "## The streets people actually sit on",
    ),
    (
        "**Need an exam, imaging, or a pediatric room:** use a listed Cherokee clinic.",
        "**Need an exam, imaging, or a pediatric room:** use a walk-in on those streets.",
    ),
)


def scrub_article_md(md: str, slug: str) -> str:
    if slug == "urgent-care-near-me-cherokee-county":
        for old, new in CHEROKEE_SWAPS:
            md = md.replace(old, new)
    for old, new in CLOCK_SWAPS:
        md = md.replace(old, new)
    leftover = CLOCK_HOURS.search(md)
    if leftover:
        raise SystemExit(f"published clock hours still in {slug}: {leftover.group(0)!r}")
    return md


def md_inline(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"Text \(480\) 639-4722", f'<a href="{SMS}">Text (480) 639-4722</a>', text)
    return text


def blocks_to_html(blocks: list[str]) -> str:
    out: list[str] = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block == LOCKED_911:
            continue
        if block.startswith("| ") and "\n" in block:
            rows = [r.strip() for r in block.split("\n") if r.strip()]
            cells = []
            for i, row in enumerate(rows):
                if re.match(r"^\|\s*-+", row):
                    continue
                cols = [c.strip() for c in row.strip("|").split("|")]
                tag = "th" if i == 0 else "td"
                cells.append("<tr>" + "".join(f"<{tag}>{md_inline(c)}</{tag}>" for c in cols) + "</tr>")
            out.append('<table class="nga-table">' + "".join(cells) + "</table>")
            continue
        heading = re.match(r"^###\s+(.*)$", block)
        if heading and "\n" not in block:
            out.append(f"<h3>{md_inline(heading.group(1))}</h3>")
            continue
        lines = block.split("\n")
        if all(re.match(r"^[-*]\s+", ln) or re.match(r"^\d+\.\s+", ln) for ln in lines):
            ordered = bool(re.match(r"^\d+\.\s+", lines[0]))
            tag = "ol" if ordered else "ul"
            items = []
            for ln in lines:
                item = re.sub(r"^([-*]|\d+\.)\s+", "", ln)
                items.append(f"<li>{md_inline(item)}</li>")
            out.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        out.append(f"<p>{md_inline(block.replace(chr(10), ' '))}</p>")
    return "\n".join(out)


def md_sections(md: str) -> tuple[str, list[tuple[str, str]]]:
    md = md.replace("\r\n", "\n").strip()
    parts = re.split(r"\n(?=## )", md)
    intro = ""
    sections: list[tuple[str, str]] = []
    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue
        if part.startswith("## "):
            first, _, rest = part.partition("\n")
            title = first[3:].strip()
            html = blocks_to_html(re.split(r"\n\s*\n", rest))
            sections.append((title, html))
        elif i == 0:
            intro = blocks_to_html(re.split(r"\n\s*\n", part))
    return intro, sections


def crumb(spec: dict, url: str) -> str:
    return (
        f'<nav class="crumb" aria-label="Breadcrumb">'
        f'<a href="https://npcwoods.com/">Home</a> &rsaquo; {html_lib.escape(spec["crumb"])}'
        f"</nav>"
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


def cook_articles() -> None:
    for spec in ARTICLES:
        md = scrub_article_md((BAG / spec["md"]).read_text(encoding="utf-8"), spec["slug"])
        if re.search(r"\binsurance\b", md, re.I):
            raise SystemExit(f"insurance slipped into {spec['md']}")
        intro, sections = md_sections(md)
        url = f"https://npcwoods.com/{spec['slug']}/"
        chunks = [
            gold.hero(html_lib.escape(spec["h1"]), html_lib.escape(spec["description"]), spec["kicker"]),
            gold.stats(),
            gold.eeat(),
            gold.gold_reviews(),
        ]
        if intro:
            chunks.append(
                f'<section class="section"><div class="section-inner prose" style="max-width:760px">{intro}</div></section>'
            )
        chunks.append(gold.how_it_works())
        for i, (heading, body) in enumerate(sections):
            klass = "section section-light" if i % 2 == 0 else "section"
            if i == 0:
                klass += " dark-to-light"
            chunks.append(
                f'<section class="{klass}"><div class="section-inner prose" style="max-width:760px">'
                f'<span class="section-kicker">{html_lib.escape(spec["crumb"])}</span>'
                f"<h2 class=\"section-title\">{md_inline(heading)}</h2>{body}</div></section>"
            )
        chunks.extend(
            [
                gold.er_box(),
                gold.states(),
                gold.bottom_cta(html_lib.escape(spec["cta"]), "Text Chris Woods, NP. $59. You only pay if he can treat you."),
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
                        {"@type": "ListItem", "position": 2, "name": spec["crumb"], "item": url},
                    ],
                },
                indent=2,
            )
            + "\n</script>"
        )
        doc = gold.render_page(
            title=spec["title"],
            description=spec["description"],
            canonical=url,
            og_title=spec["h1"],
            crumb_html=crumb(spec, url),
            schema_extra=schema,
            body="\n".join(chunks),
            draft_comment=DRAFT,
        )
        dest = ROOT / "landing-pages" / spec["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(doc, encoding="utf-8")
        print(f"wrote {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes)")


def cook_woodstock_uti() -> None:
    url = "https://npcwoods.com/uti-treatment/woodstock-ga/"
    title = "UTI Treatment in Woodstock, GA | $59 Text Visit"
    h1 = "UTI in Woodstock and you don’t want the waiting room? Text Chris."
    description = (
        "Weekend UTI in Woodstock and the clinic is closed? Text Chris Woods, NP. "
        "$59. Same-day pharmacy when it is safe. You only pay if he can treat you."
    )
    phone = phone_mockup(
        "Saturday in Woodstock. Clinic is closed. It burns when I pee.",
        "Any fever or back pain?",
        "No fever. Just burning and going constantly.",
        "Classic pattern. If text care is a fit, I’ll send it to your Woodstock pharmacy.",
        "✓ Plan ready · $59 · pay after",
    )
    faqs = [
        (
            "The clinic is closed this weekend. Can I get UTI antibiotics by text in Woodstock, GA?",
            "When it is safe, yes. Text Chris Woods, a licensed nurse practitioner, at (480) 639-4722. $59. If antibiotics are appropriate, they can go to a Woodstock-area pharmacy the same day. A prescription is not promised. You only pay if he can treat you.",
        ),
        (
            "What if it is not a UTI, or not safe by text?",
            "Chris will ask follow-up questions. If you need a local walk-in, an ER, or another in-person door, he will say so. You do not pay for that honesty.",
        ),
        (
            "Do I have to be in Woodstock?",
            "You must be physically in Georgia or another licensed state at the time of the visit. This page is for people in Woodstock, Cherokee County, and nearby.",
        ),
        (
            "How is this different from sitting Highway 92?",
            "A Woodstock walk-in is a building with a chair. This is a $59 text visit with the same NP. Use the lobby for X-rays, stitches, kids who need a room, or anything that has to be examined. Use text when the clinic is closed, the weekend line is the problem, and the story is treatable by text.",
        ),
    ]
    faq_html = "".join(
        f'<div class="faq-item"><div class="faq-q">{html_lib.escape(q)}</div>'
        f'<div class="faq-a"><p>{html_lib.escape(a)}</p></div></div>'
        for q, a in faqs
    )
    body = "\n".join(
        [
            gold.hero(h1, description, "$59 Flat · Woodstock, GA · Weekend text", phone),
            gold.stats(),
            gold.eeat(),
            gold.gold_reviews(),
            """<section class="section"><div class="section-inner prose" style="max-width:760px">
<span class="section-kicker">Woodstock, GA · weekend · $59</span>
<h2 class="section-title">A weekend in Woodstock. Clinic closed. $59 text.</h2>
<p>Burning, urgency, going often, pressure — and it is Saturday, Sunday, or the walk-in on Highway 92 already locked the door. You do not have to sit a Cherokee County urgent-care lobby first.</p>
<p>NPCWoods is a <strong>$59 text visit</strong>, not a clinic on Highway 92, Towne Lake Parkway, or Main Street. Chris Woods, MSN, APRN, FNP-C — same nurse practitioner every time — reviews uncomplicated UTI symptoms by text when it is safe. Pay after care. No video. No appointment. No waiting room.</p>
<p>Tonight, the weekend, or you cannot get in. That is the gap this page is for. Walk-ins still matter when you need a room. They are the wrong door for a weekend UTI that is miserable and not an emergency.</p>
</div></section>""",
            gold.how_it_works(),
            """<section class="section section-light dark-to-light"><div class="section-inner" style="max-width:900px">
<span class="section-kicker">Is this right for you?</span>
<h2 class="section-title">Who this is for (and who it isn't)</h2>
<p class="section-body">This page is for adults physically in Georgia, including Woodstock and the rest of Cherokee County, who have classic, uncomplicated UTI-type symptoms and want a clinician review without driving I-575 for a chair — especially when the clinic is closed.</p>
<div class="fit-grid">
  <div class="fit-good"><div class="fit-label">Ask about a text visit if</div>
    <ul class="fit-list">
      <li>It burns when you urinate, you are going often, and this feels like UTIs you have had before</li>
      <li>It is the weekend, after hours, or the Woodstock walk-in is closed or full</li>
      <li>You do not have emergency symptoms, and you can name a Woodstock-area pharmacy for pickup</li>
    </ul>
  </div>
  <div class="fit-bad"><div class="fit-label">Go in instead if</div>
    <ul class="fit-list">
      <li>Fever with back or side pain, pregnancy, or you cannot keep fluids down</li>
      <li>You need a urine culture in a lab today, or you are getting worse fast</li>
      <li>Kids, X-rays, stitches — a Woodstock walk-in on Highway 92, Towne Lake, or Main Street</li>
    </ul>
  </div>
</div>
<p class="section-body" style="margin-top:24px">This is education plus how the visit works. It is not a diagnosis.</p>
</div></section>""",
            gold.er_box(),
            f"""<section id="faq" class="section section-light dark-to-light">
  <div class="section-inner" style="max-width:720px">
    <span class="section-kicker">FAQ</span>
    <h2 class="section-title" style="text-align:center;margin-bottom:36px">Weekend, closed clinic, $59 text</h2>
    <div class="faq-list">{faq_html}</div>
  </div>
</section>""",
            f"""<section class="section"><div class="section-inner prose" style="max-width:760px">
<span class="section-kicker">Pay after · same NP</span>
<h2 class="section-title">$59. You pay after care.</h2>
<p>The visit is $59 cash. Pharmacy medication is separate. We are not quoting Woodstock walk-in cash prices we have not verified.</p>
<p>You text Chris, not a rotating pool and not a video waiting room. Follow-up on the same visit is included.</p>
<p>Full UTI pages already live: <a href="https://npcwoods.com/uti-treatment/">UTI treatment</a>, <a href="https://npcwoods.com/uti-treatment-online/">how online UTI care works</a>, <a href="https://npcwoods.com/learn/uti/">UTI guide</a>. Fee: <a href="https://npcwoods.com/pricing/">pricing</a>. Statewide: <a href="https://npcwoods.com/georgia-telemedicine/">Georgia telemedicine</a>.</p>
<p>Local walk-ins matter for X-rays, stitches, and anything that needs a room. Use them when that is the job. Use this text visit <strong>instead of</strong> the lobby when the issue is treatable by text — including the weekend the clinic is closed.</p>
<p>Chris Woods, MSN, APRN, FNP-C. Licensed in Georgia. He is a nurse practitioner, not a physician.</p>
</div></section>""",
            gold.states(),
            gold.bottom_cta(
                "Clinic closed in Woodstock? Text Chris.",
                "Weekend UTI. $59 text visit. Same-day pharmacy when it is safe. You only pay if he can treat you.",
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
                    {"@type": "ListItem", "position": 3, "name": "UTI Treatment in Woodstock, GA", "item": url},
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
        crumb_html='<nav class="crumb" aria-label="Breadcrumb"><a href="https://npcwoods.com/">Home</a> &rsaquo; <a href="https://npcwoods.com/uti-treatment/">UTI Treatment</a> &rsaquo; Woodstock, GA</nav>',
        schema_extra=schema,
        body=body,
        draft_comment=DRAFT,
    )
    doc = doc.replace(
        '<meta name="description" content="Weekend UTI in Woodstock and the clinic is closed? Text Chris Woods, NP. $59. Same-day pharmacy when it is safe. You only pay if he can treat you.">',
        '<meta name="description" content="Weekend UTI in Woodstock and the clinic is closed? Text Chris Woods, NP. $59. Same-day pharmacy when it is safe. You only pay if he can treat you.">\n'
        '<meta name="keywords" content="weekend UTI Woodstock, clinic closed UTI, UTI treatment Woodstock GA, $59 text visit, urgent care closed Woodstock">',
        1,
    )
    if re.search(r"\binsurance\b", doc, re.I):
        raise SystemExit("insurance in Woodstock plate")
    dest = ROOT / "landing-pages" / "uti-treatment" / "woodstock-ga" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    print(f"wrote {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes)")


BRANDS = re.compile(
    r"\b(Wellstar|Piedmont|Northside|Peachtree|Kennestone|CHOA|Banner|HonorHealth|NextCare|MinuteClinic|AFC)\b"
)


def assert_no_named_brands(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    story = re.sub(r"<table[\s\S]*?</table>", "", html)
    hit = BRANDS.search(story)
    if hit:
        raise SystemExit(f"named clinic brand {hit.group(0)!r} in {path}")


def main() -> None:
    cook_woodstock_uti()
    cook_articles()
    roots = [
        ROOT / "landing-pages" / "uti-treatment" / "woodstock-ga" / "index.html",
        *[ROOT / "landing-pages" / spec["slug"] / "index.html" for spec in ARTICLES],
    ]
    for path in roots:
        assert_no_named_brands(path)
        html = path.read_text(encoding="utf-8")
        hit = CLOCK_HOURS.search(html)
        if hit:
            raise SystemExit(f"published clock hours in {path}: {hit.group(0)!r}")


if __name__ == "__main__":
    main()
