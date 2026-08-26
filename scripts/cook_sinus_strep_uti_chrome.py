#!/usr/bin/env python3
"""Wrap Aug 21 sinus + strep drafts in live UTI chrome.

Chris signed A/A on 2026-08-25: CDC sinus list, honest no-swab strep.
Do not re-inject kitchen-draft flags.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gold_uti_chassis import (  # noqa: E402
    FOOTER,
    GOLD,
    HEADER,
    HIPAA_OFF,
    PROSE_CSS,
    TAIL_JS,
    gold_css,
    gold_reviews,
)

ROOT = Path(__file__).resolve().parents[1]
SINUS_OUT = ROOT / "landing-pages" / "sinus-infection-treatment" / "index.html"
STREP_OUT = ROOT / "landing-pages" / "strep-throat-treatment" / "index.html"

AHREFS = (
    '<script src="https://analytics.ahrefs.com/analytics.js" '
    'data-key="1qFceGSHKP6yg4JlSdNJ4Q" async></script>'
)

STATES = [
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

SINUS_SMS = (
    "sms:4806394722?body=Hi%20Chris%2C%20I%27m%20on%20day%205-7%20or%20worse%20"
    "with%20sinus%20symptoms.%20Can%20you%20review%20my%20pattern%3F"
)
STREP_SMS = "sms:4806394722?body=Hi%2C%20I%20think%20I%20have%20strep%20throat"

EXTRA_CSS = ""


def dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=True, indent=None, separators=(",", ":"))


def faq_html(faqs: list[tuple[str, str]]) -> str:
    items = [
        (
            f'<div class="faq-item"><div class="faq-q">{q}</div>'
            f'<div class="faq-a"><p>{a}</p></div></div>'
        )
        for q, a in faqs
    ]
    return "\n      ".join(items)


def faq_jsonld(faqs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": re.sub(r"<[^>]+>", "", a).replace("&amp;", "&"),
                },
            }
            for q, a in faqs
        ],
    }


def person_graph() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": "https://npcwoods.com/credentials/#chris",
        "name": "Chris Woods",
        "honorificSuffix": "MSN, APRN, FNP-C, AGACNP-BC",
        "jobTitle": "Nurse Practitioner",
        "description": (
            "Double board-certified Family and Adult-Gerontology Acute Care "
            "Nurse Practitioner. Not a chatbot. Not an AI clinician. Not a physician."
        ),
        "url": "https://npcwoods.com/credentials/",
        "hasOccupation": {
            "@type": "Occupation",
            "name": "Nurse Practitioner",
            "occupationalCategory": "29-1171.00",
        },
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "NPI",
            "value": "1285125468",
        },
        "sameAs": [
            "https://npcwoods.com/about/",
            "https://npcwoods.com/credentials/",
            "https://npiregistry.cms.hhs.gov/provider-view/1285125468",
            "https://www.healthgrades.com/providers/christopher-woods-xynt5wl",
        ],
    }


def org_graph(page_url: str, service_name: str, service_desc: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": ["MedicalBusiness", "MedicalOrganization", "Organization"],
        "@id": "https://npcwoods.com/#org",
        "name": "NPCWoods Telemedicine",
        "url": page_url,
        "telephone": "+14806394722",
        "priceRange": "$59",
        "paymentAccepted": "Cash, HSA, FSA",
        "foundingDate": "2025",
        "founder": {"@id": "https://npcwoods.com/credentials/#chris"},
        "employee": {"@id": "https://npcwoods.com/credentials/#chris"},
        "areaServed": [{"@type": "State", "name": name} for _, name in STATES],
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "NPI",
            "value": "1285125468",
        },
        "availableService": {
            "@type": "Service",
            "name": service_name,
            "description": service_desc,
            "offers": {
                "@type": "Offer",
                "price": "59",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": page_url,
                "category": "Telehealth visit",
            },
        },
        "sameAs": [
            "https://npcwoods.com/credentials/",
            "https://npcwoods.com/about/",
            "https://npiregistry.cms.hhs.gov/provider-view/1285125468",
            "https://www.legitscript.com/websites/?checker_keywords=npcwoods.com",
            "https://www.healthgrades.com/providers/christopher-woods-xynt5wl",
        ],
    }


def sms_block(sms: str, label: str = "Text Us Now: (480) 639-4722") -> str:
    return f"""<a href="{sms}" class="btn-primary npc-sms-cta">{label}</a>
        <div class="npc-qr-cta" role="group" aria-label="Scan to text NPCWoods">
          <div class="npc-qr-code" data-sms="{sms}" aria-hidden="true"></div>
          <div class="npc-qr-meta">
            <span class="npc-qr-label">Scan to Text Us</span>
            <a class="npc-qr-phone" href="{sms}">(480) 639-4722</a>
            <span class="npc-qr-sub">$59 flat fee &middot; text to start</span>
          </div>
        </div>"""


def states_pills() -> str:
    return "\n      ".join(
        f'<a href="https://npcwoods.com/{slug}/" class="state-pill">{name}</a>'
        for slug, name in STATES
    )


def head(
    *,
    title: str,
    description: str,
    canonical: str,
    og_title: str,
    keywords: str,
    schemas: list[dict],
) -> str:
    schema_tags = "\n".join(
        f'<script type="application/ld+json">\n{dumps(s)}\n</script>' for s in schemas
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HIPAA_OFF}
<meta charset="UTF-8">
{AHREFS}
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{canonical}">
<link rel="cite-as" href="{canonical}">
<link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="apple-touch-icon" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="NPCWoods Telemedicine">
<meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/03/chris-woods-headshot.png">
<meta property="og:image:alt" content="Chris Woods, MSN, APRN, FNP-C — double board-certified Nurse Practitioner at NPCWoods Telemedicine">
<meta property="article:modified_time" content="2026-08-25T00:00:00-07:00">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://npcwoods.com/wp-content/uploads/2026/03/chris-woods-headshot.png">
{schema_tags}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
{gold_css()}
{PROSE_CSS}
{EXTRA_CSS}
</style>
</head>
"""


SINUS_FAQS = [
    (
        "Can I get sinus infection treatment online?",
        "Yes — for the straightforward adult pattern. Text (480) 639-4722. Chris Woods reads it himself. If the timeline fits bacterial sinusitis, he can send an antibiotic same day. If it still looks viral, you get the honest support plan instead of a leftover Z-pack.",
    ),
    (
        "Do I automatically need antibiotics for a sinus infection?",
        "No. Most start as viral colds. Chris looks at day-count, direction (better, worse, or rebound), fever, and how sick you actually are. Antibiotics enter when symptoms last about 10 days with no improvement, get better then worse, or are severe early with fever and face pain. That is CDC / IDSA stewardship, not a vibe.",
    ),
    (
        "Is green or yellow mucus proof it's bacterial?",
        "No. Viral colds make colored mucus too. Drainage color alone does not decide treatment. The timeline does.",
    ),
    (
        "How do I get sinus antibiotics online without a video visit?",
        "Text the pattern. Include what day you're on, pressure, fever, whether it rebounded, allergies, pregnancy, and what you've already tried. No app, no portal, no camera.",
    ),
    (
        "What sinus antibiotic will I get?",
        "When appropriate, typically amoxicillin-clavulanate or amoxicillin, with doxycycline as a common penicillin-allergy alternative. You do not order a specific drug off a menu.",
    ),
    (
        "How much does a sinus visit cost?",
        "$59 flat. Meds separate, often $4–$20 with GoodRx. No recurring fee. No surprise facility fee. If I can't treat you by text, you are not charged.",
    ),
    (
        "How fast will I hear back?",
        "Most people get a plan within a few hours. Chris reviews same-day, including weekends. A lot of sinus texts start after hours.",
    ),
    (
        "What if I'm only on day 2 or 3?",
        'You can still text. I\'ll tell you how to support it. You are not charged if the honest answer is "not yet."',
    ),
    (
        "What if it doesn't get better on the antibiotic?",
        "Text back. Follow-up for the same visit is free. We may switch the prescription or send you in.",
    ),
    (
        "Can kids get sinus treatment by text?",
        "Older kids with a straightforward pattern, sometimes. Under 2, in person. Any child with eye swelling, trouble breathing, or who looks seriously ill — ER. A parent or guardian has to run the visit.",
    ),
    (
        "I'm in Atlanta / Charlotte. Can you treat me?",
        "If you are physically in Georgia, North Carolina, or another licensed state at the time of the visit, yes.",
    ),
    (
        "Is this a chatbot?",
        "No. Every message is read by Chris Woods, MSN, APRN, FNP-C &amp; AGACNP-BC. NPI 1285125468.",
    ),
]


STREP_FAQS = [
    (
        "Can strep throat be treated online without a swab?",
        "Yes, a licensed Nurse Practitioner can treat a classic strep pattern by text using modified Centor / McIsaac criteria. There is no swab over text. If your story is mixed, I will send you in for a test rather than guess.",
    ),
    (
        "How do I get strep antibiotics online?",
        "Text (480) 639-4722. Describe onset, fever, cough or no cough, glands, tonsils, age, and sick contacts. A photo helps. If criteria support strep, the Rx goes to your pharmacy same day. Visit is $59. Meds extra.",
    ),
    (
        "What if it's not strep, just a viral sore throat?",
        "Most sore throats are viral. You get a pain-and-fluids plan, not an antibiotic. You are not charged if I can't treat you by text.",
    ),
    (
        "What antibiotic will I get for strep?",
        "First-line is penicillin or amoxicillin. Allergy alternatives depend on the actual reaction (rash vs anaphylaxis). Typical generic cost is $4–$15 with GoodRx.",
    ),
    (
        "How much does the visit cost?",
        "$59 flat. Pay after you're treated. No recurring fee. No facility fee. Meds separate.",
    ),
    (
        "How fast will I hear back?",
        "Most people get a plan within a few hours, same day including weekends.",
    ),
    (
        "How long until I can go back to work or school?",
        "Once you've been on the antibiotic 12–24 hours <strong>and</strong> the fever is gone.",
    ),
    (
        "Can kids get strep treatment by text?",
        "Often, if they're over 3 and the pattern is classic. A parent or guardian texts. Under 3 with fever and significant throat pain — in person. Any kid drooling, struggling to breathe, or looking seriously ill — ER.",
    ),
    (
        "Can I get a strep test from you?",
        "Not by text. If I need a swab to be safe, I'll tell you where that belongs. I will not invent a negative test.",
    ),
    (
        "Is this a chatbot?",
        "No. Chris Woods, MSN, APRN, FNP-C &amp; AGACNP-BC. NPI 1285125468.",
    ),
    (
        "I'm in Charlotte or Atlanta. Can you treat my strep?",
        "If you are physically in North Carolina, Georgia, or another licensed state at the time of the visit — yes.",
    ),
]


def sinus_schemas() -> list[dict]:
    url = "https://npcwoods.com/sinus-infection-treatment/"
    return [
        org_graph(
            url,
            "Sinus Infection Treatment",
            "Async text-based telemedicine consultation for sinus infections with antibiotics when the pattern fits.",
        ),
        person_graph(),
        {
            "@context": "https://schema.org",
            "@type": "MedicalCondition",
            "@id": f"{url}#condition",
            "name": "Acute rhinosinusitis",
            "alternateName": ["Sinus infection", "Acute bacterial rhinosinusitis", "Sinusitis"],
            "code": {
                "@type": "MedicalCode",
                "codingSystem": "ICD-10",
                "code": "J01.90",
                "name": "Acute sinusitis, unspecified",
            },
            "signOrSymptom": [
                {"@type": "MedicalSymptom", "name": "Facial pressure or pain, often worse bending forward"},
                {"@type": "MedicalSymptom", "name": "Nasal congestion"},
                {"@type": "MedicalSymptom", "name": "Thick nasal drainage"},
                {"@type": "MedicalSymptom", "name": "Post-nasal drip"},
                {"@type": "MedicalSymptom", "name": "Tooth or upper-jaw pressure"},
                {"@type": "MedicalSymptom", "name": "Fever or heavier-than-usual fatigue"},
            ],
            "possibleTreatment": [
                {"@type": "MedicalTherapy", "name": "Amoxicillin-clavulanate (Augmentin)"},
                {"@type": "MedicalTherapy", "name": "Amoxicillin (Amoxil)"},
                {"@type": "MedicalTherapy", "name": "Doxycycline"},
                {"@type": "MedicalTherapy", "name": "Intranasal steroid plus saline"},
                {"@type": "MedicalTherapy", "name": "Antihistamine plan when the story is allergic"},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": "How to get sinus treatment by text",
            "description": "Three-text process with a Licensed Nurse Practitioner. Plan, and a pharmacy Rx when the pattern fits.",
            "totalTime": "PT4H",
            "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": "59"},
            "step": [
                {"@type": "HowToStep", "position": 1, "name": "Text us", "text": "Text (480) 639-4722 with the day you're on, pressure, fever, and whether it got better then worse."},
                {"@type": "HowToStep", "position": 2, "name": "Chris reviews", "text": "Chris Woods, a Licensed Nurse Practitioner, reads your text and sorts watch-and-support, treat, or be seen in person."},
                {"@type": "HowToStep", "position": 3, "name": "Plan sent", "text": "Saline and symptom support if it's still viral. An antibiotic to your pharmacy if the pattern fits. A straight redirect if this needs eyes, imaging, or an ER."},
            ],
        },
        faq_jsonld(SINUS_FAQS),
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://npcwoods.com/"},
                {"@type": "ListItem", "position": 2, "name": "Conditions", "item": "https://npcwoods.com/conditions/"},
                {"@type": "ListItem", "position": 3, "name": "Sinus Infection Treatment", "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "MedicalWebPage",
            "url": url,
            "name": "Sinus Infection Treatment Online | $59 | NPCWoods",
            "headline": "Day 5-7 and still getting worse? Sinus treatment by text.",
            "about": {"@id": f"{url}#condition"},
            "author": {"@id": "https://npcwoods.com/credentials/#chris"},
            "reviewedBy": {"@id": "https://npcwoods.com/credentials/#chris"},
            "publisher": {"@id": "https://npcwoods.com/#org"},
            "datePublished": "2025-01-01",
            "dateModified": "2026-08-25",
            "lastReviewed": "2026-08-25",
            "mainEntityOfPage": True,
            "isPartOf": {"@type": "WebSite", "name": "NPCWoods", "@id": "https://npcwoods.com/#website"},
        },
    ]


def strep_schemas() -> list[dict]:
    url = "https://npcwoods.com/strep-throat-treatment/"
    return [
        org_graph(
            url,
            "Strep Throat Treatment",
            "Async text-based telemedicine consultation for streptococcal pharyngitis with antibiotics when modified Centor criteria support treatment.",
        ),
        person_graph(),
        {
            "@context": "https://schema.org",
            "@type": "MedicalCondition",
            "@id": f"{url}#condition",
            "name": "Streptococcal pharyngitis",
            "alternateName": ["Strep throat", "Sore throat", "Group A strep pharyngitis"],
            "code": {
                "@type": "MedicalCode",
                "codingSystem": "ICD-10",
                "code": "J02.0",
                "name": "Streptococcal pharyngitis",
            },
            "signOrSymptom": [
                {"@type": "MedicalSymptom", "name": "Sudden severe sore throat"},
                {"@type": "MedicalSymptom", "name": "Fever"},
                {"@type": "MedicalSymptom", "name": "Painful swallowing"},
                {"@type": "MedicalSymptom", "name": "Tender anterior neck glands"},
                {"@type": "MedicalSymptom", "name": "Tonsillar exudate (white patches)"},
                {"@type": "MedicalSymptom", "name": "Little or no cough"},
            ],
            "possibleTreatment": [
                {"@type": "MedicalTherapy", "name": "Amoxicillin"},
                {"@type": "MedicalTherapy", "name": "Penicillin VK"},
                {"@type": "MedicalTherapy", "name": "Cephalexin (Keflex)"},
                {"@type": "MedicalTherapy", "name": "Clindamycin or a macrolide when true penicillin allergy"},
                {"@type": "MedicalTherapy", "name": "Ibuprofen or acetaminophen plus fluids"},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": "How to get strep treatment by text",
            "description": "Three-text process with a Licensed Nurse Practitioner. Antibiotic when strep criteria fit.",
            "totalTime": "PT4H",
            "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": "59"},
            "step": [
                {"@type": "HowToStep", "position": 1, "name": "Text us", "text": "Text (480) 639-4722 with sudden sore throat, fever, cough or no cough, and a tonsil photo if you have one."},
                {"@type": "HowToStep", "position": 2, "name": "Chris reviews", "text": "Chris Woods, a Licensed Nurse Practitioner, scores modified Centor: fever, no cough, tender glands, white patches, age."},
                {"@type": "HowToStep", "position": 3, "name": "Plan sent", "text": "If criteria support strep, the antibiotic goes to your pharmacy. If it looks viral, you get a pain-control plan. If it looks like an abscess or airway problem, you get the ER speech."},
            ],
        },
        faq_jsonld(STREP_FAQS),
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://npcwoods.com/"},
                {"@type": "ListItem", "position": 2, "name": "Conditions", "item": "https://npcwoods.com/conditions/"},
                {"@type": "ListItem", "position": 3, "name": "Strep Throat Treatment", "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "MedicalWebPage",
            "url": url,
            "name": "Strep Throat Treatment Online | $59 | NPCWoods",
            "headline": "Sore throat that won't quit? Strep treatment by text.",
            "about": {"@id": f"{url}#condition"},
            "author": {"@id": "https://npcwoods.com/credentials/#chris"},
            "reviewedBy": {"@id": "https://npcwoods.com/credentials/#chris"},
            "publisher": {"@id": "https://npcwoods.com/#org"},
            "datePublished": "2025-01-01",
            "dateModified": "2026-08-25",
            "lastReviewed": "2026-08-25",
            "mainEntityOfPage": True,
            "isPartOf": {"@type": "WebSite", "name": "NPCWoods", "@id": "https://npcwoods.com/#website"},
        },
    ]


def sinus_body() -> str:
    return f"""<body>
{HEADER}

<!-- HERO -->
<section class="hero">
  <div class="hero-inner hero-split">
    <div class="hero-text">
      <div class="hero-kicker">
        <span class="hero-dot"></span>
        $59 Flat &nbsp;·&nbsp; No Waiting Room &nbsp;·&nbsp; Same Day
      </div>
      <h1>Day 5–7 and still getting worse? Sinus treatment by text.</h1>
      <p class="hero-sub">Text a double board-certified Nurse Practitioner. A real plan — saline, symptom support, or antibiotics when the pattern actually fits. No video call. No waiting room. No paperwork.</p>
      <div class="hero-actions">
        {sms_block(SINUS_SMS)}
        <a href="#how-it-works" class="btn-ghost">See how it works</a>
      </div>
      <div class="hero-trust">
        <span>🔒 HIPAA-Compliant</span>
        <span>⭐ 50+ Five-Star Reviews</span>
        <span>💊 Generics typically $4–$20 with GoodRx</span>
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
            <div class="imsg-time">Today 7:42 PM</div>
            <div class="imsg-bubble user">Hey, I'm on day 6 of a sinus thing. Face hurts when I bend over and the drainage is thicker.</div>
            <div class="imsg-bubble chris">Got you. Any fever? And did it ease up mid-week, then come back harder?</div>
            <div class="imsg-bubble user">Low-grade last night. It did ease up, then the pressure came back. No vision changes, no stiff neck.</div>
            <div class="imsg-bubble chris">That's a useful pattern. Sending amoxicillin-clavulanate — take it with food. If one eye starts swelling, that's an ER thing, not a text-back.</div>
            <div class="imsg-rx">✓ Prescription sent to your Walgreens</div>
            <div class="imsg-time" style="margin-top:4px">7:51 PM</div>
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
    <div class="stat"><div class="stat-n">11</div><div class="stat-l">Licensed states</div></div>
    <div class="stat"><div class="stat-n">Same day</div><div class="stat-l">Plan, and Rx when it fits</div></div>
  </div>
</div>

<div class="eeat-byline" style="background:var(--panel-2);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:0 24px 24px;max-width:var(--max);margin-left:auto;margin-right:auto;font-size:13px;line-height:1.5;color:var(--body);">
  <p style="margin:0 0 8px 0;color:#fff;font-weight:600;">Written and clinically reviewed by <strong>Chris Woods, MSN, APRN, FNP-C</strong>, double board-certified Nurse Practitioner and founder of NPCWoods. Real NP. Not a chatbot. Not an AI clinician. Chris reads every text himself.</p>
  <p style="margin:0 0 4px 0;"><a href="https://npcwoods.com/about/" style="color:var(--blue-bright);text-decoration:underline;">About Chris</a> · <a href="https://npcwoods.com/credentials/" style="color:var(--blue-bright);text-decoration:underline;">Full credentials, NPI and state licenses</a> · <a href="https://npcwoods.com/how-it-works/" style="color:var(--blue-bright);text-decoration:underline;">How a visit works</a> · <a href="https://npcwoods.com/faq/" style="color:var(--blue-bright);text-decoration:underline;">FAQ</a></p>
  <p style="margin:0;font-size:12px;color:var(--muted);">Last reviewed: <time datetime="2026-08-25">August 25, 2026</time> — Sinus decisions follow CDC adult outpatient antibiotic guidance and IDSA acute bacterial rhinosinusitis principles. Most sinus infections start viral. Antibiotics are not automatic.</p>
</div>

<!-- NPC WOODS vs URGENT CARE -->
<section class="vs-section" id="npc-vs-urgent-care" aria-label="NPC Woods compared to typical urgent care">
  <div class="vs-inner">
    <div class="vs-head">
      <span class="section-kicker">The honest comparison</span>
      <h2>NPC Woods vs. typical urgent care</h2>
      <p>Same-day plan when it fits. None of the waiting-room games.</p>
    </div>
    <div class="vs-grid">
      <div class="vs-cell vs-corner"></div>
      <div class="vs-cell vs-us-head">NPC Woods</div>
      <div class="vs-cell vs-them-head">Typical urgent care</div>

      <div class="vs-cell vs-feature">Price</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>$59 flat fee</div>
      <div class="vs-cell vs-them">Often $150+ before meds</div>

      <div class="vs-cell vs-feature">How you start</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>One text from the couch</div>
      <div class="vs-cell vs-them">Drive, park, sign in, wait</div>

      <div class="vs-cell vs-feature">Video call</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>Never required</div>
      <div class="vs-cell vs-them">Often required online</div>

      <div class="vs-cell vs-feature">Paperwork</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>No portal, no account</div>
      <div class="vs-cell vs-them">Forms and a clipboard</div>

      <div class="vs-cell vs-feature">Who reviews</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>Chris, a real NP</div>
      <div class="vs-cell vs-them">Whoever is on shift</div>

      <div class="vs-cell vs-feature">If this isn't safe by text</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>No charge</div>
      <div class="vs-cell vs-them">You still sat there</div>
    </div>
  </div>
</section>

{gold_reviews()}

<!-- HOW IT WORKS -->
<section id="how-it-works" class="section section-light dark-to-light">
  <div class="section-inner">
    <span class="section-kicker">How it works</span>
    <h2 class="section-title">Three texts. That's it.</h2>
    <p class="section-body">No app, no portal, no video call — just text. You only pay if he can treat you.</p>
    <div class="bento">
      <div class="bento-card">
        <div class="step-num">1</div>
        <h3>Text Us</h3>
        <p>Text <a href="{SINUS_SMS}">(480) 639-4722</a> and say something like "day 6, face pressure, getting worse." Include the day you're on, whether you got better then worse, fever, and what you've already tried.</p>
      </div>
      <div class="bento-card">
        <div class="step-num">2</div>
        <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" class="chris-avatar" alt="Chris Woods NP">
        <h3>Chris Reviews</h3>
        <p>Chris Woods, your double board-certified Nurse Practitioner, reads it personally and sorts the lane: watch and support, treat, or be seen in person. Think texting a friend who happens to know medicine.</p>
      </div>
      <div class="bento-card">
        <div class="step-num">3</div>
        <h3>Plan Sent</h3>
        <p>Saline and symptom support if it's still viral. An antibiotic to your pharmacy if the pattern fits. A straight redirect if this needs eyes, imaging, or an ER. Follow-ups for the same visit are free.</p>
      </div>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:20px;text-align:center">I am not trying to prescribe antibiotics for every stuffy nose. I am trying to help you know when the pattern deserves a closer look.</p>
  </div>
</section>

<!-- WHAT IS A SINUS INFECTION -->
<section id="what-is-sinus" class="section section-white">
  <div class="section-inner" style="max-width:820px">
    <span class="section-kicker">Clinical overview</span>
    <h2 class="section-title">What a sinus infection is, in plain language</h2>
    <p class="section-body">Your sinuses are air-filled pockets behind the cheeks, forehead, and eyes. When the lining swells, mucus gets trapped, pressure builds. Most of what people call a sinus infection starts as a <strong>viral cold</strong>. Colored mucus is not a reason by itself to start antibiotics. The useful question is not "is my snot green?" It's "what day am I on, and which way is this going?"</p>
    <h3 style="font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);margin:8px 0 14px">Three lanes</h3>
    <div class="table-wrap">
      <table class="compare-table">
        <thead>
          <tr><th>Lane</th><th>What it usually is</th><th>What we do</th></tr>
        </thead>
        <tbody>
          <tr><td>Day 1–4, slowly messy</td><td>Viral or allergy</td><td>Watch and support. Saline, fluids, rest, humidity.</td></tr>
          <tr><td>Day 5–7 and not turning the corner</td><td>Pay-attention window</td><td class="treat-us">Text Chris. Especially with facial pressure, fever, thick drainage, or a story that doesn't feel like usual allergies.</td></tr>
          <tr><td>10+ days with no improvement, or better then worse</td><td>More likely bacterial</td><td class="treat-us">Text visit is often a fit. Antibiotic when the pattern and your history support it.</td></tr>
          <tr><td>Eye, vision, neck, confusion, breathing</td><td>Complication territory</td><td class="treat-er">Not a text visit. In-person / ER.</td></tr>
        </tbody>
      </table>
    </div>
    <h3 style="font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);margin:28px 0 14px">Classic symptoms</h3>
    <div class="symptom-grid">
      <div class="symptom-card"><div class="symptom-icon">🛋</div><div><strong>Facial pressure</strong><span>Cheeks, forehead, between the eyes; worse bending forward</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">😷</div><div><strong>Blocked nose</strong><span>One side or both</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">💧</div><div><strong>Thick drainage</strong><span>Yellow/green happens with viral colds too; color is a clue, not a verdict</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">🧠</div><div><strong>Post-nasal drip</strong><span>Throat clearing, cough, something running down the back</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">🦷</div><div><strong>Tooth / upper-jaw pressure</strong><span>Maxillary sinuses sit right there</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">🌡</div><div><strong>Fever or heavier fatigue</strong><span>Heavier than a usual stuffy day</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">🔄</div><div><strong>Rebound</strong><span>Better, then worse. The most useful detail you can text</span></div></div>
    </div>
  </div>
</section>

<!-- DIFFERENTIAL -->
<section id="sinus-vs-other" class="section section-light">
  <div class="section-inner" style="max-width:900px">
    <span class="section-kicker">Differential</span>
    <h2 class="section-title">Sinus vs. cold vs. allergy vs. strep</h2>
    <p class="section-body">Face pressure is not always a sinus infection. Here's how the lanes usually split.</p>
    <div class="table-wrap">
      <table class="compare-table">
        <thead>
          <tr><th>Condition</th><th>Hallmark</th><th>What it needs</th></tr>
        </thead>
        <tbody>
          <tr><td>Viral sinus / cold</td><td>Day 1–10, slowly improving, cough + sore throat + congestion</td><td>Supportive care. We can still coach this by text.</td></tr>
          <tr><td>Bacterial sinusitis</td><td>10+ days no better, or double-worsening, or severe early fever + face pain + pus</td><td class="treat-us">Often treatable by text</td></tr>
          <tr><td>Allergies</td><td>Itchy eyes, sneezing, clear drainage, repeats every pollen season, no fever</td><td class="treat-us">We treat this by text</td></tr>
          <tr><td>Migraine</td><td>Throbbing head, light/sound sensitivity, nausea — face pressure without the drainage story</td><td class="treat-maybe">Sometimes — text us to sort it</td></tr>
          <tr><td>Dental / tooth</td><td>One-sided upper tooth pain, biting pain, gum swelling</td><td>Bridge care possible; a dentist still has to fix the source. See <a href="https://npcwoods.com/dental-pain/">dental pain</a>.</td></tr>
          <tr><td>Strep throat</td><td>Sudden sore throat, fever, tender neck glands, white patches, little or no cough</td><td class="treat-us">Often treatable by text — <a href="https://npcwoods.com/strep-throat-treatment/">strep page</a></td></tr>
          <tr><td>UTI</td><td>Burning, urgency, frequency</td><td class="treat-us"><a href="https://npcwoods.com/uti-treatment/">UTI treatment page</a></td></tr>
        </tbody>
      </table>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:16px;text-align:center">References: <a href="https://www.cdc.gov/sinus-infection/about/index.html" target="_blank" rel="noopener" style="color:var(--blue-bright)">CDC sinus basics</a> · <a href="https://www.cdc.gov/antibiotic-use/hcp/clinical-care/adult-outpatient.html" target="_blank" rel="noopener" style="color:var(--blue-bright)">CDC adult outpatient antibiotics</a> · <a href="https://academic.oup.com/cid/article/54/8/1041/364141" target="_blank" rel="noopener" style="color:var(--blue-bright)">IDSA ABRS guideline</a></p>
  </div>
</section>

<!-- ANTIBIOTICS -->
<section id="antibiotics" class="section">
  <div class="section-inner" style="max-width:1000px">
    <span class="section-kicker">What we prescribe</span>
    <h2 class="section-title">When an antibiotic actually fits</h2>
    <p class="section-body">Not automatic. Pattern first. If the story is still viral, the honest plan is saline, fluids, rest, and time. If the pattern fits bacterial sinusitis, first-line choices follow IDSA / CDC adult guidance. We send the Rx electronically. You pick the pharmacy.</p>
    <div class="drug-grid">
      <a href="https://npcwoods.com/medications/augmentin/" class="drug-card">
        <div class="drug-badge badge-blue">First-line antibiotic</div>
        <h3>Amoxicillin-clavulanate</h3>
        <div class="brand">Brand: Augmentin</div>
        <p>Take with food. Covers the usual sinus bacteria, including some plain amoxicillin misses. Workhorse when the pattern is bacterial.</p>
      </a>
      <a href="https://npcwoods.com/medications/amoxicillin/" class="drug-card">
        <div class="drug-badge badge-blue">First-line alternative</div>
        <h3>Amoxicillin</h3>
        <div class="brand">Brand: Amoxil</div>
        <p>Selected otherwise-healthy adults when resistance risk is low. Chris decides from history and recent antibiotics.</p>
      </a>
      <a href="https://npcwoods.com/medications/doxycycline/" class="drug-card">
        <div class="drug-badge badge-orange">Penicillin-allergy alternative</div>
        <h3>Doxycycline</h3>
        <div class="brand">Brand: Vibramycin, Doryx</div>
        <p>Full glass of water, stay upright 30 minutes, sun-sensitive. Not for pregnancy.</p>
      </a>
      <div class="drug-card">
        <div class="drug-badge badge-purple">Symptom support, not an antibiotic</div>
        <h3>Intranasal steroid + saline</h3>
        <div class="brand">Fluticasone (Flonase) plus a rinse or spray</div>
        <p>Distilled or boiled-then-cooled water only for rinses.</p>
      </div>
      <div class="drug-card">
        <div class="drug-badge badge-green">If allergies are the real driver</div>
        <h3>Antihistamine plan</h3>
        <div class="brand">Non-drowsy option</div>
        <p>When the story is itchy eyes + sneezing + clear drainage, not a 10-day bacterial picture.</p>
      </div>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:20px;text-align:center">Most generics typically run $4–$20 with <strong style="color:var(--body)">GoodRx</strong>. The $59 is the visit. Meds are separate. Deeper guide: <a href="https://npcwoods.com/learn/sinus-infection/" style="color:var(--blue-bright)">learn/sinus-infection</a>.</p>
  </div>
</section>

<!-- ER WARNING -->
<section id="er-warning" class="section section-light dark-to-light">
  <div class="section-inner" style="max-width:740px;text-align:center">
    <span class="section-kicker">Safety first</span>
    <h2 class="section-title">When to go to the ER instead</h2>
    <p class="section-body" style="max-width:100%">I'm a nurse practitioner, not a salesman. If something more serious is going on, I want you in an ER, not texting me.</p>
    <div class="er-box" style="text-align:left">
      <h3>⚠ Head to the ER (or emergency-capable urgent care) if any of these apply:</h3>
      <ul>
        <li>Swelling or redness around <strong>one eye</strong>, or the eyelid starting to puff shut</li>
        <li>Vision changes, double vision, or new eye pain</li>
        <li>Severe headache with a <strong>stiff neck</strong></li>
        <li>Confusion, trouble staying awake</li>
        <li>Chest pain or trouble breathing</li>
        <li>High fever that feels severe, or a fever that came back hard after you were improving</li>
        <li>You can't keep fluids down</li>
        <li>You're pregnant or think you might be — text anyway and I'll tell you honestly if this needs in-person obstetric-aware care</li>
      </ul>
    </div>
    <p style="font-size:14px;color:var(--muted);margin-top:20px">For the classic stuff — day 5–7 pressure, thick drainage, a rebound after a few better days, no eye or neck drama — that's bread-and-butter telehealth.</p>
  </div>
</section>

<!-- WHO IT'S FOR -->
<section id="who-its-for" class="section section-white">
  <div class="section-inner" style="max-width:900px">
    <span class="section-kicker">Is this right for you?</span>
    <h2 class="section-title">Who this is for (and who it isn't)</h2>
    <div class="fit-grid">
      <div class="fit-good">
        <div class="fit-label">Good fit ✓</div>
        <ul class="fit-list">
          <li>Adult in one of our 11 licensed states</li>
          <li>Day 5–7 and not improving, 10+ days stuck, or better-then-worse</li>
          <li>Facial pressure, congestion, drainage — the usual miserable picture</li>
          <li>No eye swelling, no vision change, no stiff neck, no trouble breathing</li>
        </ul>
      </div>
      <div class="fit-bad">
        <div class="fit-label">Needs in-person care ✗</div>
        <ul class="fit-list">
          <li>Any red flag in the ER list</li>
          <li>Immunocompromised, on chemo, or poorly controlled diabetes with a severe face infection</li>
          <li>Known chronic sinus disease / recent sinus surgery / recurrent infections that need imaging or culture</li>
          <li>Children under 2</li>
          <li>Pregnant or possibly pregnant (text anyway — no charge for the honesty if I have to send you in)</li>
        </ul>
      </div>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:16px;text-align:center">Not sure where you fall? Text us anyway — we'll point you to the right care, no charge for the honesty.</p>
  </div>
</section>

<!-- RECURRENT / CHRONIC -->
<section class="section alt-bg">
  <div class="section-inner" style="max-width:820px">
    <span class="section-kicker">Recurrent infections</span>
    <h2 class="section-title">Getting sinus infections over and over?</h2>
    <p style="font-size:16px;color:var(--body);line-height:1.7;margin-bottom:16px">Acute bacterial sinusitis is a short, nasty chapter. Chronic sinusitis is a different book — symptoms lingering past 12 weeks, polyps, or a CT already in the chart.</p>
    <p style="font-size:15px;color:var(--body);line-height:1.7;margin-bottom:16px">A text visit can still handle <strong style="color:#fff">this flare</strong> when the pattern is straightforward. What we cannot do by text is the longer workup: nasal endoscopy, imaging, allergy testing, or an ENT plan.</p>
    <p style="font-size:14px;color:var(--muted);line-height:1.7">If that's where you are, I'll be straight with you and you are not charged for the honesty.</p>
  </div>
</section>

<!-- FAQ -->
<section id="faq" class="section section-light dark-to-light">
  <div class="section-inner" style="max-width:720px">
    <span class="section-kicker">FAQ</span>
    <h2 class="section-title" style="text-align:center;margin-bottom:36px">Common questions</h2>
    <div class="faq-list">
      {faq_html(SINUS_FAQS)}
    </div>
  </div>
</section>

<!-- STATES -->
<section class="section section-white">
  <div class="section-inner" style="text-align:center">
    <span class="section-kicker">Coverage</span>
    <h2 class="section-title">Licensed in 11 states</h2>
    <p style="font-size:15px;color:var(--body);max-width:560px;margin:0 auto 8px">Arizona · Colorado · Georgia · Idaho · Iowa · Montana · Nevada · New Mexico · North Carolina · Oregon · Utah. You must be physically in a licensed state at the time of the visit.</p>
    <div class="states-pills">
      {states_pills()}
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:16px">Verify on <a href="https://npcwoods.com/credentials/" style="color:var(--blue-bright)">credentials</a>. Georgia: <a href="https://npcwoods.com/georgia-telemedicine/" style="color:var(--blue-bright)">georgia-telemedicine</a>. North Carolina: <a href="https://npcwoods.com/north-carolina-telemedicine/" style="color:var(--blue-bright)">north-carolina-telemedicine</a>.</p>
  </div>
</section>

<!-- SUPPORTING GUIDES: existing URLs only. Do not invent child slugs. -->
<section class="section section-light">
  <div class="section-inner">
    <span class="section-kicker">Sinus guides already live</span>
    <h2 class="section-title">Not sure if this is bacterial?</h2>
    <p class="section-body">These existing pages answer the questions people usually search before they text. No new slugs in this pass.</p>
    <div class="guides-grid">
      <a href="https://npcwoods.com/learn/sinus-infection/" class="guide-card"><strong>Sinus infection learn page</strong><span>Symptoms, when antibiotics actually help, and red flags.</span></a>
      <a href="https://npcwoods.com/do-i-need-antibiotics-sinus-infection/" class="guide-card"><strong>Do I need antibiotics?</strong><span>Day count, double-worsening, and why color is not a verdict.</span></a>
      <a href="https://npcwoods.com/how-it-works/" class="guide-card"><strong>How a text visit works</strong><span>Three texts, $59, pay after you're treated.</span></a>
      <a href="https://npcwoods.com/faq/" class="guide-card"><strong>Practice FAQ</strong><span>Price, states, and what text care can and cannot do.</span></a>
    </div>
  </div>
</section>

<!-- CROSS LINKS -->
<section class="section section-white">
  <div class="section-inner" style="text-align:center">
    <span class="section-kicker">Also available</span>
    <h2 class="section-title" style="margin-bottom:8px">Other conditions we treat</h2>
    <p style="font-size:14px;color:var(--muted);margin-bottom:24px">Sinus isn't the only thing we handle via text.</p>
    <div class="cross-wrap">
      <a href="https://npcwoods.com/uti-treatment/" class="cross-link">UTI Treatment</a>
      <a href="https://npcwoods.com/strep-throat-treatment/" class="cross-link">Strep / Sore Throat</a>
      <a href="https://npcwoods.com/ear-infection-treatment/" class="cross-link">Ear Infection</a>
      <a href="https://npcwoods.com/dental-pain/" class="cross-link">Dental Pain</a>
      <a href="https://npcwoods.com/conditions/" class="cross-link">All Conditions</a>
      <a href="https://npcwoods.com/how-it-works/" class="cross-link">How It Works</a>
      <a href="https://npcwoods.com/credentials/" class="cross-link">Credentials</a>
      <a href="https://npcwoods.com/faq/" class="cross-link">FAQ</a>
    </div>
  </div>
</section>

<!-- BOTTOM CTA -->
<section class="bottom-cta">
  <div class="bottom-cta-inner">
    <h2>Ready to get this handled?</h2>
    <p>Text what day you're on. $59 flat. A real nurse practitioner — not a chatbot.</p>
    {sms_block(SINUS_SMS)}
    <div class="bottom-trust-line">
      <span>🔒 HIPAA-Compliant &amp; Secure</span>
      <span>💳 HSA/FSA accepted</span>
      <span>💊 Sent same-day to your local pharmacy when it fits</span>
    </div>
  </div>
</section>

<div class="clinician-line" style="font-size:12px;line-height:1.6;">
  Clinically reviewed by <strong>Chris Woods, MSN, APRN, FNP-C</strong>, double board-certified Nurse Practitioner.<br>
  Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT &bull; <a href="https://npcwoods.com/about/" style="color:var(--blue-bright);">About Chris</a> &bull; <a href="https://npcwoods.com/credentials/" style="color:var(--blue-bright);">Credentials</a> &bull; Last reviewed: <time datetime="2026-08-25">August 25, 2026</time>
</div>

{FOOTER}
{TAIL_JS}
<script src="/tracking.js"></script>
</body>
</html>
"""


def strep_body() -> str:
    return f"""<body>
{HEADER}

<!-- HERO -->
<section class="hero">
  <div class="hero-inner hero-split">
    <div class="hero-text">
      <div class="hero-kicker">
        <span class="hero-dot"></span>
        $59 Flat &nbsp;·&nbsp; No Waiting Room &nbsp;·&nbsp; Same Day
      </div>
      <h1>Sore throat that won't quit? Strep treatment by text.</h1>
      <p class="hero-sub">Text a double board-certified Nurse Practitioner. If the pattern looks like strep, your antibiotic goes to the pharmacy same day. If it's a viral sore throat, you'll hear that too — I'm not here to sell you a leftover Z-pack. No video call. No waiting room. No paperwork.</p>
      <div class="hero-actions">
        {sms_block(STREP_SMS)}
        <a href="#how-it-works" class="btn-ghost">See how it works</a>
      </div>
      <div class="hero-trust">
        <span>🔒 HIPAA-Compliant</span>
        <span>⭐ 50+ Five-Star Reviews</span>
        <span>💊 Strep antibiotics typically $4–$15 with GoodRx</span>
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
            <div class="imsg-time">Today 11:03 AM</div>
            <div class="imsg-bubble user">My throat is killing me. Came on last night. Fever 101. Kids at school have strep.</div>
            <div class="imsg-bubble chris">Sorry you're miserable. Any cough or runny nose? Can you see white patches, and are the glands under your jaw tender?</div>
            <div class="imsg-bubble user">No cough. Glands are sore. Partner said my tonsils look white.</div>
            <div class="imsg-bubble chris">Classic strep picture. Sending amoxicillin to your CVS. Stay home until you've been on it 12–24 hours and the fever's gone. If you start drooling or can't swallow spit, that's an ER, not a text-back.</div>
            <div class="imsg-rx">✓ Prescription sent to your CVS</div>
            <div class="imsg-time" style="margin-top:4px">11:11 AM</div>
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
    <div class="stat"><div class="stat-n">11</div><div class="stat-l">Licensed states</div></div>
    <div class="stat"><div class="stat-n">Same day</div><div class="stat-l">Rx when criteria fit</div></div>
  </div>
</div>

<div class="eeat-byline" style="background:var(--panel-2);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:0 24px 24px;max-width:var(--max);margin-left:auto;margin-right:auto;font-size:13px;line-height:1.5;color:var(--body);">
  <p style="margin:0 0 8px 0;color:#fff;font-weight:600;">Written and clinically reviewed by <strong>Chris Woods, MSN, APRN, FNP-C</strong>, double board-certified Nurse Practitioner and founder of NPCWoods. Real NP. Not a chatbot. Not an AI clinician.</p>
  <p style="margin:0 0 4px 0;"><a href="https://npcwoods.com/about/" style="color:var(--blue-bright);text-decoration:underline;">About</a> · <a href="https://npcwoods.com/credentials/" style="color:var(--blue-bright);text-decoration:underline;">Credentials, NPI, 11-state licenses</a> · <a href="https://npcwoods.com/how-it-works/" style="color:var(--blue-bright);text-decoration:underline;">How it works</a> · <a href="https://npcwoods.com/faq/" style="color:var(--blue-bright);text-decoration:underline;">FAQ</a></p>
  <p style="margin:0;font-size:12px;color:var(--muted);">Last reviewed: <time datetime="2026-08-25">August 25, 2026</time> — Assessments use modified Centor / McIsaac plus individual judgment. Prescriptions only when criteria and scope support. There is no throat swab over text — if the story is muddy, I send you in rather than guess.</p>
</div>

<!-- NPC WOODS vs URGENT CARE -->
<section class="vs-section" id="npc-vs-urgent-care" aria-label="NPC Woods compared to typical urgent care">
  <div class="vs-inner">
    <div class="vs-head">
      <span class="section-kicker">The honest comparison</span>
      <h2>NPC Woods vs. typical urgent care</h2>
      <p>Classic strep pattern by text. Honest redirect when a swab is safer.</p>
    </div>
    <div class="vs-grid">
      <div class="vs-cell vs-corner"></div>
      <div class="vs-cell vs-us-head">NPC Woods</div>
      <div class="vs-cell vs-them-head">Typical urgent care</div>

      <div class="vs-cell vs-feature">Price</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>$59 flat</div>
      <div class="vs-cell vs-them">Often $150+ before the test and the meds</div>

      <div class="vs-cell vs-feature">How you start</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>One text</div>
      <div class="vs-cell vs-them">Drive, park, wait, retell it</div>

      <div class="vs-cell vs-feature">Swab</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>Clinical criteria first. If I need a swab, I'll say so.</div>
      <div class="vs-cell vs-them">Rapid strep if they have the kit</div>

      <div class="vs-cell vs-feature">Video</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>Never required</div>
      <div class="vs-cell vs-them">Often required online</div>

      <div class="vs-cell vs-feature">If this isn't strep — or isn't safe by text</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>Honest plan, no charge if I can't treat</div>
      <div class="vs-cell vs-them">You still spent the evening there</div>
    </div>
  </div>
</section>

{gold_reviews()}

<!-- HOW IT WORKS -->
<section id="how-it-works" class="section section-light dark-to-light">
  <div class="section-inner">
    <span class="section-kicker">How it works</span>
    <h2 class="section-title">Three texts. That's it.</h2>
    <p class="section-body">No app, no portal, no video call — just text. You only pay if he can treat you.</p>
    <div class="bento">
      <div class="bento-card">
        <div class="step-num">1</div>
        <h3>Text Us</h3>
        <p>Say something like "throat is killing me, fever started yesterday, I think it's strep." A photo of the tonsils helps. No account. Text <a href="{STREP_SMS}">(480) 639-4722</a>.</p>
      </div>
      <div class="bento-card">
        <div class="step-num">2</div>
        <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" class="chris-avatar" alt="Chris Woods NP">
        <h3>Chris Reviews</h3>
        <p>Onset, fever, cough or no cough, tender neck glands, white patches, age, sick contacts. That's modified Centor, not a vibe.</p>
      </div>
      <div class="bento-card">
        <div class="step-num">3</div>
        <h3>Plan Sent</h3>
        <p>If criteria support strep, the antibiotic goes to your pharmacy. If it looks viral, you get pain control and the honest "this is a cold in your throat" plan. If it looks like an abscess or airway problem, you get the ER speech, not a prescription.</p>
      </div>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:20px;text-align:center">Treatment follows IDSA / CDC / AAP principles. Penicillin and amoxicillin remain first-line.</p>
  </div>
</section>

<!-- WHAT STREP IS -->
<section id="what-is-strep" class="section section-white">
  <div class="section-inner" style="max-width:820px">
    <span class="section-kicker">Clinical overview</span>
    <h2 class="section-title">What strep is, in plain language</h2>
    <p class="section-body">Strep throat is group A Streptococcus. It likes a sudden, miserable onset: fever, painful swallowing, tender glands, white patches — and often <strong>no cough</strong>.</p>
    <p class="section-body">Most sore throats are <strong>not</strong> strep. They are viral. Viral sore throats come with a cold: cough, runny nose, hoarse voice, slower onset. Antibiotics do nothing for those.</p>
    <p class="section-body">There is no rapid swab over a text thread. That's a real limitation and I'm not going to dress it up. If the score and the story are classic, treating by text is how this practice actually works. If the story is mixed, I will tell you to get a swab — and you are not charged for that honesty.</p>
    <h3 style="font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);margin:8px 0 14px">Modified Centor — what I'm actually scoring</h3>
    <div class="table-wrap">
      <table class="compare-table">
        <thead>
          <tr><th>Feature</th><th>Points the way of strep</th></tr>
        </thead>
        <tbody>
          <tr><td>Fever</td><td>Yes</td></tr>
          <tr><td>No cough</td><td>Yes</td></tr>
          <tr><td>Tender anterior neck glands</td><td>Yes</td></tr>
          <tr><td>Tonsillar exudate (white patches)</td><td>Yes</td></tr>
          <tr><td>Age 3–14</td><td>More likely</td></tr>
          <tr><td>Age 45+</td><td>Less likely</td></tr>
        </tbody>
      </table>
    </div>
    <p style="font-size:14px;color:var(--body);margin:16px 0 24px">High score + classic story → treatment by text can be appropriate. Low score + a cold sitting on your throat → no antibiotic. Middle gray zone → I may send you in for a swab instead of guessing.</p>
    <h3 style="font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);margin-bottom:14px">Classic symptoms</h3>
    <div class="symptom-grid">
      <div class="symptom-card"><div class="symptom-icon">⚡</div><div><strong>Sudden onset</strong><span>Hours, not a slow scratchy week</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">🌡</div><div><strong>Fever</strong><span>Often 100.4 or higher</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">😷</div><div><strong>Painful swallowing</strong><span>It hurts to drink, not just to talk</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">🧠</div><div><strong>Tender glands</strong><span>Along the front of the neck</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">🦠</div><div><strong>White patches</strong><span>Or pus on the tonsils</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">🙅</div><div><strong>Little or no cough</strong><span>Little or no runny nose either</span></div></div>
      <div class="symptom-card"><div class="symptom-icon">👥</div><div><strong>Sick contact</strong><span>School, work, or home helps — not required</span></div></div>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:16px;text-align:center">References: <a href="https://www.idsociety.org/practice-guideline/group-a-streptococcal-pharyngitis/" target="_blank" rel="noopener" style="color:var(--blue-bright)">IDSA GAS pharyngitis</a> · <a href="https://www.cdc.gov/group-a-strep/about/strep-throat.html" target="_blank" rel="noopener" style="color:var(--blue-bright)">CDC strep throat</a> · <a href="https://www.aafp.org/pubs/afp/issues/2009/0301/p383.html" target="_blank" rel="noopener" style="color:var(--blue-bright)">AAFP strep pharyngitis</a></p>
  </div>
</section>

<!-- DIFFERENTIAL -->
<section id="strep-vs-other" class="section section-light">
  <div class="section-inner" style="max-width:900px">
    <span class="section-kicker">Differential</span>
    <h2 class="section-title">Strep vs. viral vs. mono vs. abscess</h2>
    <p class="section-body">A sore throat is not automatically strep. The story tells us which door to use.</p>
    <div class="table-wrap">
      <table class="compare-table">
        <thead>
          <tr><th>Condition</th><th>Hallmark</th><th>What it needs</th></tr>
        </thead>
        <tbody>
          <tr><td>Strep throat</td><td>Sudden, fever, no cough, tender glands, white patches</td><td class="treat-us">Often treatable by text</td></tr>
          <tr><td>Viral pharyngitis</td><td>Cough, runny nose, hoarse, slower onset</td><td>Symptom care. We can still coach this.</td></tr>
          <tr><td>Post-nasal drip / sinus</td><td>Face pressure, drainage, throat irritation without the sudden strep picture</td><td>See <a href="https://npcwoods.com/sinus-infection-treatment/">sinus treatment</a></td></tr>
          <tr><td>Mono (EBV)</td><td>Teen/young adult, long fatigue, huge glands, spleen risk</td><td>Usually in-person. Don't start amoxicillin if mono is the better story.</td></tr>
          <tr><td>Peritonsillar abscess</td><td>One-sided bulge, hot-potato voice, can't open the mouth, drooling</td><td class="treat-er">ER / ENT. Not text.</td></tr>
          <tr><td>Airway / epiglottitis</td><td>Drooling, tripoding, trouble breathing</td><td class="treat-er">ER now.</td></tr>
          <tr><td>UTI</td><td>Burning, urgency, frequency</td><td class="treat-us"><a href="https://npcwoods.com/uti-treatment/">UTI treatment page</a></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<!-- ANTIBIOTICS -->
<section id="antibiotics" class="section">
  <div class="section-inner" style="max-width:1000px">
    <span class="section-kicker">What we prescribe</span>
    <h2 class="section-title">When it is actually strep</h2>
    <p class="section-body">First-line remains penicillin and amoxicillin. Allergy alternatives depend on the actual reaction. We send the Rx electronically. You pick the pharmacy.</p>
    <div class="drug-grid">
      <a href="https://npcwoods.com/medications/amoxicillin/" class="drug-card">
        <div class="drug-badge badge-blue">First-line</div>
        <h3>Amoxicillin</h3>
        <div class="brand">Brand: Amoxil</div>
        <p>First-line for most people who can take penicillin. Cheap, well tolerated. Finish the course even when you feel human on day two.</p>
      </a>
      <a href="https://npcwoods.com/medications/penicillin/" class="drug-card">
        <div class="drug-badge badge-blue">First-line</div>
        <h3>Penicillin VK</h3>
        <div class="brand">Still the IDSA first-line</div>
        <p>Narrow, targeted, old-school in the good way.</p>
      </a>
      <a href="https://npcwoods.com/medications/cephalexin/" class="drug-card">
        <div class="drug-badge badge-orange">Non-anaphylactic penicillin allergy</div>
        <h3>Cephalexin</h3>
        <div class="brand">Brand: Keflex</div>
        <p>Often usable when the reaction was a rash, not anaphylaxis. Chris decides from the actual allergy story.</p>
      </a>
      <a href="https://npcwoods.com/medications/clindamycin/" class="drug-card">
        <div class="drug-badge badge-orange">True penicillin allergy</div>
        <h3>Clindamycin or a macrolide</h3>
        <div class="brand">Selected from your history</div>
        <p>Macrolide resistance is real, which is why this is not a default.</p>
      </a>
      <div class="drug-card">
        <div class="drug-badge badge-purple">Symptom relief, not an antibiotic</div>
        <h3>Ibuprofen or acetaminophen + fluids</h3>
        <div class="brand">Pain and fever control</div>
        <p>The thing that makes swallowing possible while the antibiotic (or the virus) does its work.</p>
      </div>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:20px;text-align:center">Most generic strep antibiotics typically run $4–$15 with <strong style="color:var(--body)">GoodRx</strong>. The $59 is the visit. Meds are separate.</p>
  </div>
</section>

<!-- ER WARNING -->
<section id="er-warning" class="section section-light dark-to-light">
  <div class="section-inner" style="max-width:740px;text-align:center">
    <span class="section-kicker">Safety first</span>
    <h2 class="section-title">When to go to the ER instead</h2>
    <p class="section-body" style="max-width:100%">I'm a nurse practitioner, not a salesman.</p>
    <div class="er-box" style="text-align:left">
      <h3>⚠ Head to the ER if any of these apply:</h3>
      <ul>
        <li>Trouble breathing, drooling because you can't swallow, or a muffled hot-potato voice</li>
        <li>Severe <strong>one-sided</strong> throat swelling, or you cannot open your mouth fully (trismus)</li>
        <li>Stiff neck with a high fever</li>
        <li>A sandpaper rash with high fever that has you looking toxic, not just pink</li>
        <li>You can't keep fluids down</li>
        <li>Chest pain or a neck that is rapidly swelling</li>
        <li>A child under 3 with high fever and significant throat pain</li>
        <li>You're pregnant or think you might be — text anyway; I'll tell you if this still fits text care</li>
      </ul>
    </div>
    <p style="font-size:14px;color:var(--muted);margin-top:20px">For the classic strep picture — sudden severe sore throat, fever, tender glands, white patches, no cough — that's bread-and-butter telehealth.</p>
  </div>
</section>

<!-- WHO IT'S FOR -->
<section id="who-its-for" class="section section-white">
  <div class="section-inner" style="max-width:900px">
    <span class="section-kicker">Is this right for you?</span>
    <h2 class="section-title">Who this is for (and who it isn't)</h2>
    <div class="fit-grid">
      <div class="fit-good">
        <div class="fit-label">Good fit ✓</div>
        <ul class="fit-list">
          <li>Adult or older child in a licensed state</li>
          <li>Sudden sore throat with fever, tender glands, white patches, little or no cough</li>
          <li>Can swallow fluids</li>
          <li>Not drooling</li>
        </ul>
      </div>
      <div class="fit-bad">
        <div class="fit-label">Needs in-person care ✗</div>
        <ul class="fit-list">
          <li>Any ER red flag</li>
          <li>Child under 3 with fever and throat pain</li>
          <li>Toxic / can't swallow spit / muffled voice</li>
          <li>Recurrent strep that already has an ENT plan</li>
          <li>Immunocompromised with a severe throat infection</li>
          <li>Pregnancy when the story is not straightforward</li>
        </ul>
      </div>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:16px;text-align:center">Not sure? Text us anyway. No charge for the honesty if I send you in.</p>
  </div>
</section>

<!-- RETURN TO WORK / RECURRENT -->
<section class="section alt-bg">
  <div class="section-inner" style="max-width:820px">
    <span class="section-kicker">Return to work and school</span>
    <h2 class="section-title">Going back to work, school, or the shared fridge</h2>
    <p style="font-size:16px;color:var(--body);line-height:1.7;margin-bottom:16px">Stay home until you've been on the antibiotic <strong style="color:#fff">12–24 hours and the fever is gone</strong>. That is a public-health thing, not me being fussy.</p>
    <p style="font-size:15px;color:var(--body);line-height:1.7;margin-bottom:16px">A text visit treats <strong style="color:#fff">this</strong> strep picture. Recurrent strep that already has an ENT plan, tonsil-talk, or a workplace that requires a documented swab — I will tell you that belongs in person, and you are not charged for the honesty.</p>
    <p style="font-size:14px;color:var(--muted);line-height:1.7">Why treat strep at all when most sore throats are viral? Because when it <em>is</em> strep, antibiotics shorten how long you're contagious and how miserable you are. I will not pretend a viral sore throat needs the same prescription.</p>
  </div>
</section>

<!-- FAQ -->
<section id="faq" class="section section-light dark-to-light">
  <div class="section-inner" style="max-width:720px">
    <span class="section-kicker">FAQ</span>
    <h2 class="section-title" style="text-align:center;margin-bottom:36px">Common questions</h2>
    <div class="faq-list">
      {faq_html(STREP_FAQS)}
    </div>
  </div>
</section>

<!-- STATES -->
<section class="section section-white">
  <div class="section-inner" style="text-align:center">
    <span class="section-kicker">Coverage</span>
    <h2 class="section-title">Licensed in 11 states</h2>
    <p style="font-size:15px;color:var(--body);max-width:560px;margin:0 auto 8px">AZ · CO · GA · ID · IA · MT · NV · NM · NC · OR · UT. You must be physically in a licensed state at the time of the visit.</p>
    <div class="states-pills">
      {states_pills()}
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:16px"><a href="https://npcwoods.com/credentials/" style="color:var(--blue-bright)">Credentials</a> · <a href="https://npcwoods.com/georgia-telemedicine/" style="color:var(--blue-bright)">Georgia</a> · <a href="https://npcwoods.com/north-carolina-telemedicine/" style="color:var(--blue-bright)">North Carolina</a> · <a href="https://npcwoods.com/uti-treatment/" style="color:var(--blue-bright)">UTI</a> · <a href="https://npcwoods.com/sinus-infection-treatment/" style="color:var(--blue-bright)">Sinus</a></p>
  </div>
</section>

<!-- SUPPORTING GUIDES: existing URLs only. Do not invent child slugs. -->
<section class="section section-light">
  <div class="section-inner">
    <span class="section-kicker">Strep guides already live</span>
    <h2 class="section-title">Want the longer version?</h2>
    <p class="section-body">Existing pages only. No empty child URLs in this pass.</p>
    <div class="guides-grid">
      <a href="https://npcwoods.com/learn/strep-throat/" class="guide-card"><strong>Strep throat learn page</strong><span>What Centor actually is, and when antibiotics fit.</span></a>
      <a href="https://npcwoods.com/how-it-works/" class="guide-card"><strong>How a text visit works</strong><span>Three texts, $59, pay after you're treated.</span></a>
      <a href="https://npcwoods.com/ear-infection-treatment/" class="guide-card"><strong>Ear infection treatment</strong><span>Keep the ear URL. Do not mix it with this strep plate.</span></a>
      <a href="https://npcwoods.com/faq/" class="guide-card"><strong>Practice FAQ</strong><span>Price, states, and what text care can and cannot do.</span></a>
    </div>
  </div>
</section>

<!-- CROSS LINKS -->
<section class="section section-white">
  <div class="section-inner" style="text-align:center">
    <span class="section-kicker">Also available</span>
    <h2 class="section-title" style="margin-bottom:8px">Other conditions we treat</h2>
    <p style="font-size:14px;color:var(--muted);margin-bottom:24px">Strep isn't the only thing we handle via text.</p>
    <div class="cross-wrap">
      <a href="https://npcwoods.com/uti-treatment/" class="cross-link">UTI Treatment</a>
      <a href="https://npcwoods.com/sinus-infection-treatment/" class="cross-link">Sinus Infection</a>
      <a href="https://npcwoods.com/ear-infection-treatment/" class="cross-link">Ear Infection</a>
      <a href="https://npcwoods.com/conditions/" class="cross-link">All Conditions</a>
      <a href="https://npcwoods.com/how-it-works/" class="cross-link">How It Works</a>
      <a href="https://npcwoods.com/credentials/" class="cross-link">Credentials</a>
      <a href="https://npcwoods.com/faq/" class="cross-link">FAQ</a>
    </div>
  </div>
</section>

<!-- BOTTOM CTA -->
<section class="bottom-cta">
  <div class="bottom-cta-inner">
    <h2>Ready to get this handled?</h2>
    <p>Text sudden vs slow, fever vs no fever, cough vs no cough. Those three details save us a round. $59 flat. A real nurse practitioner.</p>
    {sms_block(STREP_SMS)}
    <div class="bottom-trust-line">
      <span>🔒 HIPAA-Compliant &amp; Secure</span>
      <span>💳 HSA/FSA accepted</span>
      <span>💊 Sent same-day to your local pharmacy when criteria fit</span>
    </div>
  </div>
</section>

<div class="clinician-line" style="font-size:12px;line-height:1.6;">
  Clinically reviewed by <strong>Chris Woods, MSN, APRN, FNP-C</strong>, double board-certified Nurse Practitioner.<br>
  Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT &bull; <a href="https://npcwoods.com/about/" style="color:var(--blue-bright);">About Chris</a> &bull; <a href="https://npcwoods.com/credentials/" style="color:var(--blue-bright);">Credentials</a> &bull; Last reviewed: <time datetime="2026-08-25">August 25, 2026</time>
</div>

{FOOTER}
{TAIL_JS}
<script src="/tracking.js"></script>
</body>
</html>
"""


def write_page(path: Path, html: str) -> None:
    path.write_text(html, encoding="utf-8")
    print(f"wrote {path} ({len(html)} bytes, {html.count(chr(10))+1} lines)")


def assert_no_physician(html: str, label: str) -> None:
    if re.search(r"@type\"\s*:\s*\"Physician\"", html) or '"@type":"Physician"' in html:
        raise SystemExit(f"{label}: Person schema used Physician")
    if re.search(r'"@type":\s*"Physician"', html):
        raise SystemExit(f"{label}: Person schema used Physician")


def main() -> None:
    if not GOLD.exists():
        raise SystemExit(f"missing gold UTI chrome: {GOLD}")

    sinus_html = (
        head(
            title="Sinus Infection Treatment Online | $59 | NPCWoods",
            description="Facial pressure that won't quit? Text a real NP. $59 flat. Same-day pharmacy when antibiotics actually fit — not for every stuffy nose. No video. 11 states.",
            canonical="https://npcwoods.com/sinus-infection-treatment/",
            og_title="Sinus Infection Treatment Online | $59 | NPCWoods",
            keywords="sinus infection treatment online, sinus antibiotics online, sinus telemedicine, facial pressure telehealth, $59 sinus visit",
            schemas=sinus_schemas(),
        )
        + sinus_body()
    )
    strep_html = (
        head(
            title="Strep Throat Treatment Online | $59 | NPCWoods",
            description="Sore throat that won't quit? Text a real NP. $59 flat. Same-day antibiotics when strep criteria fit — not for every scratchy throat. No video. 11 states.",
            canonical="https://npcwoods.com/strep-throat-treatment/",
            og_title="Strep Throat Treatment Online | $59 | NPCWoods",
            keywords="strep throat treatment online, strep antibiotics online, sore throat telemedicine, strep telehealth, $59 strep visit",
            schemas=strep_schemas(),
        )
        + strep_body()
    )

    for label, html in (("sinus", sinus_html), ("strep", strep_html)):
        assert_no_physician(html, label)
        if "insurance" in html.lower():
            raise SystemExit(f"{label}: insurance leaked")
        if re.search(r"\bdoctors?\b", html, re.I) and "NPI Registry" not in html:
            # still check doctor word
            hits = re.findall(r".{0,40}\bdoctors?\b.{0,40}", html, re.I)
            raise SystemExit(f"{label}: doctor language: {hits[:3]}")
        if re.search(r"\bdoctors?\b", html, re.I):
            hits = re.findall(r".{0,40}\bdoctors?\b.{0,40}", html, re.I)
            raise SystemExit(f"{label}: doctor language: {hits[:3]}")
        if "connect.facebook.net" in html or "fbq('init'" in html or 'fbq("init"' in html:
            raise SystemExit(f"{label}: live Meta pixel leaked")
        if "GTM-59QSWZRC" in html or "G-EFFRQMG8TC" in html or "AW-610222919" in html:
            raise SystemExit(f"{label}: health-page ad tags leaked")

    write_page(SINUS_OUT, sinus_html)
    write_page(STREP_OUT, strep_html)


if __name__ == "__main__":
    main()
