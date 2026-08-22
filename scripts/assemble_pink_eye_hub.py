#!/usr/bin/env python3
"""Assemble UTI-chrome pink-eye hub. Run from npcwoods-website root."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UTI = ROOT / "landing-pages/uti-treatment/index.html"
BODY = ROOT / "scripts/_pink_eye_rebuild_body.html"
OUT = ROOT / "landing-pages/pink-eye-treatment/index.html"

EXTRA_CSS = """
#npcSaveWrap{display:none!important}
body::after{content:none!important;display:none!important}
.faq-item.open .faq-a{max-height:920px}
.npc-sms-cta{color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important}
"""

HEAD = r'''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Meta Pixel disabled 2026-06-10: no BAA with Meta — health-condition pages must not send PageView there.
     The stub below also blocks the GTM-injected pixel: Meta's base code starts with `if(f.fbq)return;`,
     so predefining a no-op fbq means fbevents.js never loads on this page.
     GTM, GA4, and Google Ads stay off this health-condition page (no BAA). -->
<meta charset="UTF-8">
<!-- NPCWoods Tracking: Ahrefs Analytics -->
<script src="https://analytics.ahrefs.com/analytics.js" data-key="1qFceGSHKP6yg4JlSdNJ4Q" async></script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pink Eye Treatment Online | $59 Visit | NPCWoods</title>
<meta name="description" content="Pink eye by text with a Licensed Nurse Practitioner. Viral vs bacterial vs allergy. Antibiotic drops only if the pattern fits. $59 flat. Licensed in 11 states.">
<meta name="keywords" content="pink eye treatment online, conjunctivitis telemedicine, viral vs bacterial pink eye, Polytrim online, erythromycin eye ointment, pink eye by text">
<link rel="canonical" href="https://npcwoods.com/pink-eye-treatment/">
<link rel="cite-as" href="https://npcwoods.com/pink-eye-treatment/">
<link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="apple-touch-icon" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<meta property="og:title" content="Pink Eye Treatment Online — $59 | NPCWoods Telemedicine">
<meta property="og:description" content="Text a Licensed Nurse Practitioner for pink eye. Antibiotic drops are not automatic. $59 flat. Licensed in 11 states.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://npcwoods.com/pink-eye-treatment/">
<meta property="og:site_name" content="NPCWoods Telemedicine">
<meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/03/chris-woods-headshot.png">
<meta property="og:image:alt" content="Chris Woods, MSN, APRN, FNP-C — double board-certified Nurse Practitioner at NPCWoods Telemedicine">
<meta property="article:modified_time" content="2026-08-21T00:00:00-04:00">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Pink Eye Treatment Online — $59 | NPCWoods">
<meta name="twitter:description" content="Text a Licensed Nurse Practitioner. Viral vs bacterial vs allergy. $59 flat.">
<meta name="twitter:image" content="https://npcwoods.com/wp-content/uploads/2026/03/chris-woods-headshot.png">
<script>
window.fbq = window.fbq || function(){};
window._fbq = window._fbq || window.fbq;
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"MedicalBusiness","@id":"https://npcwoods.com/#medical-business","name":"NPCWoods Telemedicine","description":"Online pink eye (conjunctivitis) care via text-based telemedicine. $59 flat fee. Licensed in 11 states.","telephone":"+14806394722","url":"https://npcwoods.com/pink-eye-treatment/","priceRange":"$59","areaServed":[{"@type":"State","name":"Arizona"},{"@type":"State","name":"Colorado"},{"@type":"State","name":"Georgia"},{"@type":"State","name":"Idaho"},{"@type":"State","name":"Iowa"},{"@type":"State","name":"Montana"},{"@type":"State","name":"Nevada"},{"@type":"State","name":"New Mexico"},{"@type":"State","name":"North Carolina"},{"@type":"State","name":"Oregon"},{"@type":"State","name":"Utah"}],"medicalSpecialty":"https://schema.org/FamilyPractice","availableService":{"@type":"Service","name":"Pink Eye Treatment","description":"Async text-based telemedicine consultation for conjunctivitis with drops only when the bacterial pattern fits","offers":{"@type":"Offer","price":"59","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://npcwoods.com/pink-eye-treatment/","category":"Telehealth visit"}},"sameAs":["https://share.google/XlmNvRT4vihOJ8KBH"]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"MedicalCondition","@id":"https://npcwoods.com/pink-eye-treatment/#condition","name":"Conjunctivitis","alternateName":["Pink eye","Viral conjunctivitis","Bacterial conjunctivitis","Allergic conjunctivitis"],"code":{"@type":"MedicalCode","codingSystem":"ICD-10","code":"H10.9","name":"Unspecified conjunctivitis"},"signOrSymptom":[{"@type":"MedicalSymptom","name":"Eye redness"},{"@type":"MedicalSymptom","name":"Watery or mucopurulent discharge"},{"@type":"MedicalSymptom","name":"Eyelids stuck shut"},{"@type":"MedicalSymptom","name":"Ocular itching"},{"@type":"MedicalSymptom","name":"Gritty sensation"}],"possibleTreatment":[{"@type":"MedicalTherapy","name":"Polymyxin B / trimethoprim ophthalmic (Polytrim)"},{"@type":"MedicalTherapy","name":"Erythromycin ophthalmic ointment"},{"@type":"MedicalTherapy","name":"Artificial tears"},{"@type":"MedicalTherapy","name":"Olopatadine or ketotifen ophthalmic"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HowTo","name":"How to Get Pink Eye Care Online","description":"Three-text process to get conjunctivitis guidance from a Licensed Nurse Practitioner. Antibiotic drops only if the bacterial pattern fits.","totalTime":"PT4H","estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"59"},"step":[{"@type":"HowToStep","position":1,"name":"Text us","text":"Text (480) 639-4722 with what's going on. Mention contacts, pain, or light sensitivity."},{"@type":"HowToStep","position":2,"name":"Chris reviews","text":"Chris Woods, a Licensed Nurse Practitioner, reads your text and sorts viral vs bacterial vs allergy vs in-person red flags."},{"@type":"HowToStep","position":3,"name":"Plan or pharmacy","text":"If a text visit fits, you get a plan. If drops are appropriate, the prescription is sent electronically to your pharmacy."}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Can pink eye be treated online?","acceptedAnswer":{"@type":"Answer","text":"Uncomplicated viral, bacterial, or allergic conjunctivitis in a non-contact-lens patient can be sorted by text with a licensed nurse practitioner. Contact-lens red eye, newborns, pain, photophobia, and trauma need in-person care."}},{"@type":"Question","name":"Do all cases of pink eye need prescription drops?","acceptedAnswer":{"@type":"Answer","text":"No. Viral and allergic conjunctivitis do not respond to antibiotic drops. Bacterial patterns may get Polytrim or erythromycin ophthalmic if the history fits. Antibiotic drops are not automatic."}},{"@type":"Question","name":"I wear contact lenses. Can I still text?","acceptedAnswer":{"@type":"Answer","text":"Leave the lenses out and seek in-person eye care today. Contact-lens red eye can be microbial keratitis, including Pseudomonas, which a text visit cannot rule out."}},{"@type":"Question","name":"Is this a chatbot?","acceptedAnswer":{"@type":"Answer","text":"No. Every message is read by Chris Woods, MSN, APRN, FNP-C, NPI 1285125468. Real NP. Not a chatbot."}},{"@type":"Question","name":"How much does a pink eye visit cost?","acceptedAnswer":{"@type":"Answer","text":"$59 flat. You only pay if he can treat you. Medication is separate at your pharmacy."}},{"@type":"Question","name":"When should I seek in-person eye care?","acceptedAnswer":{"@type":"Answer","text":"Eye pain, light sensitivity, blurred vision, injury, chemical splash, contact-lens red eye, newborns, or a worsening eye need prompt in-person care. Call 911 for emergencies."}}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://npcwoods.com/"},{"@type":"ListItem","position":2,"name":"Conditions","item":"https://npcwoods.com/conditions/"},{"@type":"ListItem","position":3,"name":"Pink Eye Treatment","item":"https://npcwoods.com/pink-eye-treatment/"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"MedicalWebPage","url":"https://npcwoods.com/pink-eye-treatment/","name":"Pink Eye Treatment Online","about":{"@id":"https://npcwoods.com/pink-eye-treatment/#condition"},"author":{"@type":"Person","@id":"https://npcwoods.com/#chris-woods","name":"Chris Woods","jobTitle":"MSN, APRN, FNP-C, double board-certified Nurse Practitioner","url":"https://npcwoods.com/about/"},"reviewedBy":{"@type":"Person","name":"Chris Woods, MSN, APRN, FNP-C","url":"https://npcwoods.com/credentials/"},"datePublished":"2025-01-01","dateModified":"2026-08-21","lastReviewed":"2026-08-21","mainEntityOfPage":true,"isPartOf":{"@type":"WebSite","name":"NPCWoods"}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
'''

MOBILE_CTA = ""


def main() -> None:
    uti = UTI.read_text(encoding="utf-8")
    body = BODY.read_text(encoding="utf-8")

    style_start = uti.find("<style>")
    style_end = uti.find("</style>") + len("</style>")
    style = uti[style_start:style_end].replace("</style>", EXTRA_CSS + "\n</style>")

    header_start = uti.find("<!-- ===== SHARED HEADER")
    header_end = uti.find("<!-- ===== END SHARED HEADER ===== -->") + len(
        "<!-- ===== END SHARED HEADER ===== -->"
    )
    header = uti[header_start:header_end]

    footer_start = uti.find("<!-- ===== INCLUDED SHARED FOOTER")
    footer_tail = uti[footer_start:]
    footer_tail = footer_tail.replace("<!-- NPCWoods Tracking: tracking.js -->\n", "")
    footer_tail = footer_tail.replace("<!-- NPCWoods Tracking: tracking.js -->", "")

    html = (
        HEAD
        + style
        + "\n</head>\n<body>\n\n"
        + header
        + "\n\n"
        + body
        + "\n\n"
        + footer_tail
    )
    html = html.replace("</body>", MOBILE_CTA + "\n</body>")
    if "/tracking.js" in html:
        raise SystemExit("refusing to write /tracking.js onto a health page")
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
