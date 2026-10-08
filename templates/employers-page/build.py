#!/usr/bin/env python3
"""Build landing-pages/employers/index.html from template.html.

footer-src.html is the live homepage footer (2026-10-08). flyer.html and og.html
are the sources for assets/npcwoods-break-room-flyer.{pdf,png} and
assets/employers-og.jpg (render with headless Chrome from a server rooted so
/employers/assets and /assets/fonts resolve). Needs: pip install segno.
"""
import html, io, json, re, sys, urllib.parse
from pathlib import Path
import segno

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'landing-pages' / 'employers' / 'index.html'

SMS_BODY = "Hi Chris, I'd like to talk about a pilot for my team."
SMS = "sms:4806394722?body=" + urllib.parse.quote(SMS_BODY)

FAQ = [
    ("What does it cost?",
     "Each text visit is $59, flat. Your team member only pays if Chris can treat them. Want to talk about a pilot for your team? Text Chris at (480) 639-4722."),
    ("Do we have to sign a contract?",
     "No. There's no contract to get started. Share the number, and your team can text when they need care."),
    ("Does my team need to download an app?",
     "No app, no portal, no login. It's a regular text message to (480) 639-4722 from any phone."),
    ("Who is Chris?",
     "Chris Woods, MSN, APRN, FNP-C, is a double board-certified nurse practitioner. He reads and answers every text himself. NPI 1285125468."),
    ("Will I see my employee's health information?",
     "No. Health details stay between your team member and Chris. NPCWoods is HIPAA-compliant."),
    ("Is this a replacement for our health plan?",
     "No. It's a fast, low-cost option for everyday urgent care problems. It doesn't replace a health plan, a primary care clinician, or emergency care."),
    ("Which states do you cover?",
     "13 states, including Florida by telehealth registration: Arizona, Colorado, Georgia, Idaho, Iowa, Montana, Nevada, New Mexico, North Carolina, Oregon, Utah, Washington, and Florida. Your team member has to be physically in one of these states at the time of the visit."),
    ("Does every visit end with a prescription?",
     "No. Chris decides what's safe for each person. If someone needs to be seen in person, he'll tell them."),
    ("What if it's an emergency?",
     "Call 911. Text visits are not for emergencies like chest pain, trouble breathing, or a serious injury."),
]

def faq_html():
    out = []
    for i, (q, a) in enumerate(FAQ):
        op = " open" if i == 0 else ""
        out.append(f'      <details{op}>\n        <summary>{html.escape(q)}</summary>\n        <p>{html.escape(a)}</p>\n      </details>')
    return "\n".join(out)

def faq_jsonld():
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    return json.dumps(data, indent=2, ensure_ascii=False)

def qr_svg():
    q = segno.make(SMS, error='m')
    buf = io.BytesIO()
    q.save(buf, kind='svg', xmldecl=False, svgns=True, nl=False, scale=1, border=1,
           dark='#05060a', light=None, omitsize=True)
    s = buf.getvalue().decode()
    return s.replace('<svg ', '<svg role="img" aria-label="QR code that opens a text to Chris at (480) 639-4722" ', 1)

def footer():
    f = (HERE / 'footer-src.html').read_text()
    # keep page free of booking language; add the employer link in Quick Links
    f = f.replace("No appointment. Just text us", "No waiting room. Just text us")
    f = f.replace('<li><a href="https://npcwoods.com/sitemap/">Site Map</a></li>',
                  '<li><a href="https://npcwoods.com/employers/">For Employers</a></li>\n          <li><a href="https://npcwoods.com/sitemap/">Site Map</a></li>')
    # employer page stays clear of drug-adjacent nav items (ads-safe)
    f = f.replace('          <li><a href="https://npcwoods.com/glp1-weight-loss/">GLP-1 Weight Loss</a></li>\n', '')
    f = f.replace('          <li><a href="https://npcwoods.com/medications/">Medications</a></li>\n', '')
    assert 'glp1-weight-loss' not in f and '/medications/' not in f
    # MedicalBusiness JSON-LD already lives in <head>; drop the duplicate block
    f = re.sub(r'\s*<script type="application/ld\+json">.*?</script>\s*', '\n', f, flags=re.S)
    return "<!-- ===== SITE FOOTER ===== -->\n" + f

t = (HERE / 'template.html').read_text()
t = (t.replace('{{SMS}}', html.escape(SMS, quote=True))
      .replace('{{FAQ_HTML}}', faq_html())
      .replace('{{FAQ_JSONLD}}', faq_jsonld())
      .replace('{{QR_PILOT}}', qr_svg())
      .replace('{{FOOTER}}', footer()))
assert '{{' not in t, re.findall(r'{{\w+}}', t)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(t)
print(OUT, len(t.encode()))
