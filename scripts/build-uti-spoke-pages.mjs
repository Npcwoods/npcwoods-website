#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const header = fs.readFileSync(path.join(root, 'html/shared/header-snippet.html'), 'utf8').replaceAll('\u2014', '-');
const footer = fs.readFileSync(path.join(root, 'html/shared/footer-snippet.html'), 'utf8').replaceAll('\u2014', '-');
const outRoot = path.join(root, 'landing-pages/uti-treatment');
const updated = '2026-05-21';
const updatedDisplay = 'May 21, 2026';
const phone = '4806394722';

const states = ['Arizona', 'Colorado', 'Georgia', 'Idaho', 'Iowa', 'Montana', 'Nevada', 'New Mexico', 'North Carolina', 'Oregon', 'Utah'];

const pages = [
  {
    slug: 'burning-when-i-pee',
    title: 'Burning When You Pee? UTI Help | NPCWoods',
    description: 'Burning when you pee can be a UTI. Learn what symptoms fit text-based UTI care, red flags, and how to start a $59 visit.',
    eyebrow: 'UTI symptom guide',
    h1: 'Burning when you pee?',
    lede: 'That burning feeling is one of the most common UTI clues. If your symptoms fit a simple bladder infection, Chris can review your story by text and send treatment when appropriate.',
    sms: 'Hi Chris, it burns when I pee and I think it may be a UTI. Can you review my symptoms?',
    primaryIntent: 'burning when I pee UTI',
    answer: 'Usually. Burning with urination, urgency, frequent trips, bladder pressure, cloudy urine, or a familiar UTI pattern can fit text-based UTI care. Fever, back pain, pregnancy, vomiting, severe pain, or symptoms in men usually need more careful evaluation.',
    sections: [
      {
        heading: 'When does burning point toward a UTI?',
        body: [
          'Burning with urination is called dysuria. It can happen with a UTI, irritation, dehydration, sexually transmitted infections, yeast symptoms, kidney stones, or other causes.',
          'A simple UTI pattern is more likely when burning comes with urgency, frequent urination, bladder pressure, cloudy urine, strong odor, or the same feeling you have had with past UTIs.'
        ],
        bullets: ['Burning or stinging while urinating', 'Feeling like you have to go again right after going', 'Lower belly or bladder pressure', 'Cloudy or stronger-smelling urine', 'A familiar pattern from a previous UTI']
      },
      {
        heading: 'When should you avoid text-only care?',
        body: [
          'Some urinary symptoms need in-person testing or urgent evaluation. Text-based care is best for straightforward lower UTI symptoms, not signs of a kidney infection or a more complicated problem.'
        ],
        bullets: ['Fever, chills, flank pain, or vomiting', 'Pregnancy', 'Symptoms in men', 'Severe pelvic, abdominal, or back pain', 'Blood in urine that is heavy or worsening', 'New vaginal discharge, sores, or STI concern']
      },
      {
        heading: 'How NPCWoods handles this by text',
        body: [
          'You text what is happening. Chris asks follow-up questions, checks for red flags, and decides whether telehealth treatment fits. If antibiotics make sense, the prescription is sent electronically to the pharmacy you choose.',
          'If your story does not fit a simple UTI, Chris will tell you what kind of care makes more sense.'
        ]
      }
    ],
    faqs: [
      ['Can burning when I pee go away without antibiotics?', 'Sometimes, but true bacterial UTIs often need treatment. If symptoms are mild and improving, hydration and symptom monitoring may be reasonable. If burning, urgency, or frequency is worsening, get reviewed.'],
      ['Can dehydration cause burning?', 'Yes. Concentrated urine can sting, especially if you have not been drinking much. Burning that comes with urgency, frequency, bladder pressure, or cloudy urine is more suspicious for a UTI.'],
      ['Can I start with a text visit?', 'Yes, if you are in a state NPCWoods serves and your symptoms sound like an uncomplicated UTI. Chris will screen for red flags before recommending treatment.']
    ],
    related: ['uti-antibiotics-online', 'how-fast-do-uti-antibiotics-work', 'is-my-uti-getting-worse']
  },
  {
    slug: 'uti-antibiotics-online',
    title: 'UTI Antibiotics Online, $59 Visit | NPCWoods',
    description: 'Need UTI antibiotics online? Text Chris for a $59 UTI visit. If appropriate, treatment is sent to your pharmacy.',
    eyebrow: 'Online UTI treatment',
    h1: 'UTI antibiotics online, without the waiting room',
    lede: 'If this feels like a straightforward UTI, you should not have to spend half a day finding care. Text Chris your symptoms, answer follow-up questions, and get a clear next step.',
    sms: 'Hi Chris, I think I have a UTI and I want to know if antibiotics are appropriate.',
    primaryIntent: 'UTI antibiotics online',
    answer: 'Yes, UTI antibiotics can be prescribed online when symptoms fit an uncomplicated UTI and no red flags are present. NPCWoods charges a $59 flat fee. If treatment is appropriate, the prescription is sent to your chosen pharmacy.',
    sections: [
      {
        heading: 'Who is a good fit for online UTI antibiotics?',
        body: [
          'Text-based UTI care fits best when symptoms point toward a simple lower urinary tract infection. That usually means burning, urgency, frequent urination, bladder pressure, or a familiar UTI pattern.',
          'Chris still has to ask the right questions. The goal is not to throw antibiotics at every urinary symptom. The goal is fast, appropriate care.'
        ],
        bullets: ['Adult patient in one of the 11 states NPCWoods serves', 'Burning, urgency, frequency, or bladder pressure', 'No fever, flank pain, vomiting, pregnancy, or severe symptoms', 'Able to use a local pharmacy for pickup']
      },
      {
        heading: 'What antibiotics are commonly used for UTIs?',
        body: [
          'Common options include nitrofurantoin, TMP-SMX, cephalexin, and other medications depending on symptoms, history, allergies, local patterns, and whether the story is uncomplicated.',
          'Chris chooses based on the actual history. If your symptoms suggest something else, you may need testing instead of an automatic prescription.'
        ]
      },
      {
        heading: 'How fast does the visit work?',
        body: [
          'Most patients start by sending one text with the symptom pattern. Chris replies with focused follow-up questions, then gives the next step. If treatment fits, the prescription is sent electronically to your pharmacy.',
          'Pharmacy pickup timing depends on the pharmacy, but many patients can pick up the same day.'
        ]
      }
    ],
    faqs: [
      ['Do I need a video call for UTI antibiotics?', 'Usually no. Many straightforward UTI visits can be handled by secure text when the symptom story is clear and no red flags are present.'],
      ['Is the visit really $59?', 'Yes. NPCWoods uses a $59 flat fee for the text visit. Medication cost is separate and depends on the pharmacy.'],
      ['Are antibiotics guaranteed?', 'No. Chris only recommends antibiotics when the history fits. If symptoms suggest kidney infection, pregnancy-related risk, STI concern, or another issue, he will direct you to the right level of care.']
    ],
    related: ['burning-when-i-pee', 'how-fast-do-uti-antibiotics-work', 'no-video-uti-treatment']
  },
  {
    slug: 'how-fast-do-uti-antibiotics-work',
    title: 'How Fast Do UTI Antibiotics Work? | NPCWoods',
    description: 'Many UTI symptoms start improving within 24 to 48 hours on the right antibiotic. Learn what is normal and when to get rechecked.',
    eyebrow: 'UTI treatment timing',
    h1: 'How fast do UTI antibiotics work?',
    lede: 'When a UTI is the right diagnosis and the antibiotic matches the bacteria, many people start feeling some relief within a day or two. The key is knowing what improvement should look like.',
    sms: 'Hi Chris, I have UTI symptoms and want to know if treatment is appropriate.',
    primaryIntent: 'how fast do UTI antibiotics work',
    answer: 'Many uncomplicated UTI symptoms start improving within 24 to 48 hours after starting the right antibiotic. Burning and urgency may fade gradually. Fever, back pain, vomiting, or worsening symptoms are not normal and need prompt evaluation.',
    sections: [
      {
        heading: 'What improvement usually looks like',
        body: [
          'The first signs are often less burning, less urgency, fewer bathroom trips, and less bladder pressure. Some symptoms may linger while the bladder lining calms down.',
          'Finish the medication exactly as prescribed unless Chris or another clinician tells you otherwise.'
        ],
        bullets: ['Some relief in 24 to 48 hours is common', 'Frequency may improve before all burning disappears', 'Bladder irritation can lag behind the infection', 'Hydration can help dilute irritating urine']
      },
      {
        heading: 'When symptoms are not improving',
        body: [
          'If symptoms are the same or worse after 48 hours, the diagnosis may be wrong, the bacteria may not match the medication, or the infection may be more complicated.',
          'Do not just wait it out if you are getting worse. Worsening UTI symptoms are a signal to get rechecked.'
        ],
        bullets: ['No improvement after 48 hours', 'New fever, chills, back pain, or vomiting', 'Worsening pain or blood in urine', 'New vaginal symptoms or STI concern']
      },
      {
        heading: 'Can NPCWoods help before symptoms get worse?',
        body: [
          'Yes, if your symptom pattern fits a simple UTI and you are in a state NPCWoods serves. Chris can review the story by text and recommend treatment when appropriate.',
          'If your symptoms sound complicated, he will tell you what kind of testing or in-person care is smarter.'
        ]
      }
    ],
    faqs: [
      ['Should I feel completely better after one dose?', 'Not always. Some people notice relief quickly, but complete improvement can take longer. The trend matters: symptoms should be moving in the right direction.'],
      ['What if I feel worse after starting antibiotics?', 'Worsening symptoms, fever, back pain, vomiting, or severe pain need prompt evaluation. That can mean the infection is more complicated or something else is going on.'],
      ['Can I take leftover antibiotics?', 'No. Leftover medication may be the wrong choice, wrong dose, or wrong duration. It can also delay proper care if symptoms are not from a simple UTI.']
    ],
    related: ['uti-antibiotics-online', 'is-my-uti-getting-worse', 'burning-when-i-pee']
  },
  {
    slug: 'is-my-uti-getting-worse',
    title: 'Is My UTI Getting Worse? Red Flags | NPCWoods',
    description: 'Learn UTI red flags: fever, back pain, vomiting, pregnancy, worsening pain, or no improvement after treatment. Know when text care fits.',
    eyebrow: 'UTI red flags',
    h1: 'Is my UTI getting worse?',
    lede: 'Some UTI symptoms are miserable but still straightforward. Others are red flags. This page helps you separate a simple bladder infection pattern from signs that need faster or in-person care.',
    sms: 'Hi Chris, I have UTI symptoms and I am worried they may be getting worse.',
    primaryIntent: 'is my UTI getting worse',
    answer: 'A UTI may be getting worse if burning, urgency, pain, or blood in urine is increasing, or if fever, chills, back pain, nausea, vomiting, or weakness appear. Those red flags can mean a kidney infection or another problem.',
    sections: [
      {
        heading: 'UTI symptoms that can still fit text care',
        body: [
          'Text care can fit when symptoms are lower urinary symptoms only: burning, urgency, frequency, bladder pressure, or cloudy urine.',
          'The safer the story, the better the fit. Chris screens for the red flags before recommending treatment.'
        ],
        bullets: ['Burning while urinating', 'Urgency or frequent urination', 'Lower bladder pressure', 'Mild blood-tinged urine with classic UTI symptoms', 'A familiar uncomplicated UTI pattern']
      },
      {
        heading: 'Red flags that need more urgent care',
        body: [
          'Fever, chills, flank pain, vomiting, severe pain, pregnancy, or symptoms in men can change the risk level. Those patterns may need urine testing, imaging, IV medication, or a hands-on exam.',
          'If you feel very sick, do not wait on a text response. Use urgent or emergency care.'
        ],
        bullets: ['Fever or chills', 'Back or side pain near the ribs', 'Vomiting or unable to keep fluids down', 'Pregnancy', 'Confusion, weakness, or feeling severely ill', 'Symptoms in men or after a urologic procedure']
      },
      {
        heading: 'What to do if symptoms are worsening',
        body: [
          'If symptoms are worsening but you are not in an emergency pattern, text Chris and describe exactly what changed and when. Include fever, pain location, pregnancy status, allergies, and any medication already taken.',
          'That helps Chris decide whether a text visit fits or whether you need a different level of care.'
        ]
      }
    ],
    faqs: [
      ['Does back pain always mean kidney infection?', 'No, but back or flank pain with UTI symptoms is a red flag, especially with fever, chills, nausea, or vomiting. It needs more careful evaluation.'],
      ['Can I use NPCWoods if I have fever?', 'Fever with urinary symptoms may signal a kidney infection or more complicated illness. Chris may direct you to urgent or emergency care instead of text-only treatment.'],
      ['What if my UTI symptoms are mild but getting worse?', 'If symptoms are moving the wrong direction, get reviewed. Mild symptoms can still become more uncomfortable, and early treatment may be appropriate when the story fits.']
    ],
    related: ['burning-when-i-pee', 'how-fast-do-uti-antibiotics-work', 'uti-antibiotics-online']
  },
  {
    slug: 'no-video-uti-treatment',
    title: 'No-Video UTI Treatment Online | NPCWoods',
    description: 'Need private UTI care without a video call? NPCWoods offers text-based UTI visits for $59 when symptoms fit.',
    eyebrow: 'Private UTI care',
    h1: 'No-video UTI treatment, handled by text',
    lede: 'UTI symptoms are personal. If the story is straightforward, you can text Chris instead of sitting on a video call explaining burning, urgency, and bathroom trips out loud.',
    sms: 'Hi Chris, I would like a private text-based UTI visit without a video call.',
    primaryIntent: 'no video UTI treatment online',
    answer: 'Yes. Many uncomplicated UTI visits can be handled without a video call. NPCWoods uses text-based history, red-flag screening, and pharmacy-based treatment when appropriate. The visit is $59 flat.',
    sections: [
      {
        heading: 'Why text works well for many UTIs',
        body: [
          'UTI care often depends on the history: burning, urgency, frequency, bladder pressure, prior UTI pattern, allergies, pregnancy status, fever, and back pain. Those details can be handled clearly by text.',
          'A text visit is not a shortcut around safety. It is a focused way to gather the information that matters.'
        ],
        bullets: ['Private and discreet', 'No waiting room', 'No video call', 'Clear follow-up questions', '$59 flat fee']
      },
      {
        heading: 'When no-video care is not enough',
        body: [
          'Some urinary symptoms need testing or hands-on care. If your story includes red flags, Chris will tell you directly that text care is not the right fit.'
        ],
        bullets: ['Pregnancy', 'Fever, chills, or flank pain', 'Vomiting or severe illness', 'Symptoms in men', 'STI concern or new vaginal symptoms', 'Repeated symptoms that keep coming back']
      },
      {
        heading: 'How to start',
        body: [
          'Tap the text button and describe your symptoms in plain language. Include when it started, what you feel, whether you have fever or back pain, your medication allergies, and your preferred pharmacy.',
          'Chris will review and reply with the next step.'
        ]
      }
    ],
    faqs: [
      ['Do I need to download an app?', 'No. Start by text. Chris can ask follow-up questions and tell you what information is needed.'],
      ['Will I have to show anything on camera?', 'Usually no. Straightforward UTI visits are often history-based. If your symptoms require visual exam, testing, or in-person care, Chris will tell you.'],
      ['Can I use this from any state?', 'NPCWoods serves patients located in Arizona, Colorado, Georgia, Idaho, Iowa, Montana, Nevada, New Mexico, North Carolina, Oregon, and Utah.']
    ],
    related: ['uti-antibiotics-online', 'burning-when-i-pee', 'is-my-uti-getting-worse']
  }
];

const bySlug = Object.fromEntries(pages.map((page) => [page.slug, page]));

function esc(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function smsHref(message) {
  return `sms:${phone}?body=${encodeURIComponent(message)}`;
}

function jsonLd(data) {
  return `<script type="application/ld+json">\n${JSON.stringify(data, null, 2)}\n</script>`;
}

function renderPage(page) {
  const url = `https://npcwoods.com/uti-treatment/${page.slug}/`;
  const related = page.related.map((slug) => bySlug[slug]).filter(Boolean);
  const breadcrumbs = jsonLd({
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://npcwoods.com/' },
      { '@type': 'ListItem', position: 2, name: 'UTI Treatment', item: 'https://npcwoods.com/uti-treatment/' },
      { '@type': 'ListItem', position: 3, name: page.h1, item: url }
    ]
  });
  const medicalPage = jsonLd({
    '@context': 'https://schema.org',
    '@type': 'MedicalWebPage',
    '@id': `${url}#webpage`,
    url,
    name: page.title,
    description: page.description,
    lastReviewed: updated,
    reviewedBy: {
      '@type': 'Person',
      name: 'Chris Woods',
      honorificSuffix: 'MSN, APRN, FNP-C',
      identifier: {
        '@type': 'PropertyValue',
        propertyID: 'NPI',
        value: '1285125468'
      }
    },
    about: {
      '@type': 'MedicalCondition',
      name: 'Urinary Tract Infection',
      alternateName: ['UTI', 'bladder infection', 'acute cystitis']
    },
    isPartOf: {
      '@type': 'MedicalBusiness',
      name: 'NPCWoods Telemedicine',
      url: 'https://npcwoods.com/',
      telephone: '+14806394722',
      priceRange: '$59'
    }
  });
  const article = jsonLd({
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: page.title,
    description: page.description,
    datePublished: updated,
    dateModified: updated,
    author: { '@type': 'Person', name: 'Chris Woods, MSN, APRN, FNP-C' },
    reviewedBy: { '@type': 'Person', name: 'Chris Woods, MSN, APRN, FNP-C' },
    publisher: { '@type': 'Organization', name: 'NPCWoods Telemedicine', url: 'https://npcwoods.com/' },
    mainEntityOfPage: `${url}#webpage`
  });
  const faq = jsonLd({
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: page.faqs.map(([question, answer]) => ({
      '@type': 'Question',
      name: question,
      acceptedAnswer: { '@type': 'Answer', text: answer }
    }))
  });

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${esc(page.title)}</title>
  <meta name="description" content="${esc(page.description)}">
  <link rel="canonical" href="${url}">
  <link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
  <link rel="apple-touch-icon" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
  <meta property="og:title" content="${esc(page.title)}">
  <meta property="og:description" content="${esc(page.description)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="${url}">
  <meta property="og:site_name" content="NPCWoods Telemedicine">
  <meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/03/chris-woods-headshot.png">
  <meta property="og:image:alt" content="Chris Woods, MSN, APRN, FNP-C at NPCWoods Telemedicine">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${esc(page.title)}">
  <meta name="twitter:description" content="${esc(page.description)}">
  <meta name="twitter:image" content="https://npcwoods.com/wp-content/uploads/2026/03/chris-woods-headshot.png">
  ${breadcrumbs}
  ${medicalPage}
  ${article}
  ${faq}
  <style>
    :root {
      --text-primary: #1A1A2E;
      --text-body: #4A4A5A;
      --text-muted: #8E8E9A;
      --brand: #2563EB;
      --brand-hover: #1D4ED8;
      --brand-light: #EFF6FF;
      --border: #E5E7EB;
      --warm-white: #FDF8F4;
      --success: #16A34A;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--text-body);
      background: #FFFFFF;
      line-height: 1.7;
      -webkit-font-smoothing: antialiased;
    }
    a { color: var(--brand); }
    .uti-hero {
      padding: 72px 20px 52px;
      background:
        radial-gradient(circle at 20% 10%, rgba(37, 99, 235, 0.08), transparent 28%),
        linear-gradient(180deg, #FFFFFF 0%, #F7F8FA 100%);
    }
    .uti-wrap {
      width: min(1120px, 100%);
      margin: 0 auto;
    }
    .crumbs {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      margin-bottom: 22px;
      color: var(--text-muted);
      font-size: 0.9rem;
    }
    .crumbs a {
      color: var(--text-muted);
      text-decoration: none;
    }
    .hero-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.2fr) 360px;
      gap: 40px;
      align-items: center;
    }
    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 999px;
      background: var(--brand-light);
      color: var(--brand);
      font-weight: 800;
      font-size: 0.76rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 16px;
    }
    .eyebrow::before {
      content: "";
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: var(--success);
      box-shadow: 0 0 0 4px #DCFCE7;
    }
    h1 {
      margin: 0 0 18px;
      color: var(--text-primary);
      font-size: clamp(2.4rem, 6vw, 4.4rem);
      line-height: 1.02;
      letter-spacing: 0;
      max-width: 760px;
    }
    .lede {
      margin: 0 0 24px;
      max-width: 680px;
      color: var(--text-body);
      font-size: 1.18rem;
      line-height: 1.65;
    }
    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
    }
    .primary-cta, .secondary-cta {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 52px;
      padding: 14px 24px;
      border-radius: 999px;
      font-weight: 800;
      text-decoration: none;
      transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
    }
    .primary-cta {
      background: var(--brand);
      color: #FFFFFF;
      box-shadow: 0 8px 22px rgba(37, 99, 235, 0.24);
    }
    .primary-cta:hover {
      background: var(--brand-hover);
      transform: translateY(-1px);
      text-decoration: none;
    }
    .secondary-cta {
      background: #FFFFFF;
      color: var(--brand);
      border: 1px solid #BFDBFE;
    }
    .hero-card {
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 8px 30px rgba(26, 26, 46, 0.08);
    }
    .hero-card img {
      width: 72px;
      height: 72px;
      border-radius: 50%;
      object-fit: cover;
      object-position: 50% 22%;
      display: block;
      margin-bottom: 14px;
    }
    .hero-card h2 {
      margin: 0 0 10px;
      color: var(--text-primary);
      font-size: 1.2rem;
      line-height: 1.25;
    }
    .hero-card p {
      margin: 0;
      color: var(--text-body);
      font-size: 0.98rem;
    }
    .quick-answer {
      padding: 34px 20px;
      background: var(--text-primary);
      color: #FFFFFF;
    }
    .quick-answer .uti-wrap {
      display: grid;
      grid-template-columns: 220px minmax(0, 1fr);
      gap: 28px;
      align-items: start;
    }
    .quick-answer strong {
      color: #FFFFFF;
      display: block;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }
    .quick-answer p {
      margin: 0;
      color: #E5E7EB;
      font-size: 1.08rem;
      line-height: 1.65;
    }
    .content {
      padding: 64px 20px;
    }
    .content-grid {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 320px;
      gap: 48px;
      align-items: start;
    }
    article {
      max-width: 760px;
    }
    article h2 {
      margin: 0 0 14px;
      color: var(--text-primary);
      font-size: clamp(1.65rem, 3vw, 2.25rem);
      line-height: 1.14;
      letter-spacing: 0;
    }
    article section {
      padding-bottom: 40px;
      margin-bottom: 40px;
      border-bottom: 1px solid var(--border);
    }
    article p {
      margin: 0 0 16px;
      font-size: 1.04rem;
    }
    .bullet-panel {
      list-style: none;
      margin: 20px 0 0;
      padding: 0;
      display: grid;
      gap: 10px;
    }
    .bullet-panel li {
      padding: 12px 14px;
      border: 1px solid #DBEAFE;
      border-radius: 12px;
      background: #F8FBFF;
      color: var(--text-primary);
      font-weight: 650;
    }
    .side-card {
      position: sticky;
      top: 86px;
      background: var(--warm-white);
      border: 1px solid #F0E5D8;
      border-radius: 16px;
      padding: 22px;
    }
    .side-card h2 {
      margin: 0 0 10px;
      color: var(--text-primary);
      font-size: 1.25rem;
      line-height: 1.2;
    }
    .side-card ul {
      margin: 16px 0 18px;
      padding-left: 20px;
    }
    .side-card li {
      margin-bottom: 8px;
    }
    .related {
      background: #F7F8FA;
      padding: 56px 20px;
    }
    .related h2, .faq h2 {
      margin: 0 0 22px;
      color: var(--text-primary);
      font-size: clamp(1.75rem, 4vw, 2.5rem);
      line-height: 1.15;
      text-align: center;
    }
    .related-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
    }
    .related-card {
      display: block;
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 20px;
      text-decoration: none;
      color: var(--text-primary);
      min-height: 130px;
      transition: transform 0.18s ease, border-color 0.18s ease;
    }
    .related-card:hover {
      transform: translateY(-2px);
      border-color: #BFDBFE;
      text-decoration: none;
    }
    .related-card span {
      display: block;
      color: var(--brand);
      font-weight: 800;
      margin-bottom: 8px;
    }
    .faq {
      padding: 64px 20px;
    }
    .faq-list {
      max-width: 820px;
      margin: 0 auto;
      display: grid;
      gap: 14px;
    }
    details {
      border: 1px solid var(--border);
      border-radius: 14px;
      background: #FFFFFF;
      padding: 18px 20px;
    }
    summary {
      cursor: pointer;
      color: var(--text-primary);
      font-weight: 800;
      line-height: 1.35;
    }
    details p {
      margin: 12px 0 0;
    }
    .bottom-cta {
      padding: 64px 20px;
      text-align: center;
      background: var(--brand);
      color: #FFFFFF;
    }
    .bottom-cta h2 {
      margin: 0 0 12px;
      font-size: clamp(1.8rem, 4vw, 2.6rem);
      line-height: 1.1;
      letter-spacing: 0;
    }
    .bottom-cta p {
      max-width: 680px;
      margin: 0 auto 22px;
      color: #EAF1FF;
    }
    .bottom-cta .primary-cta {
      background: #FFFFFF;
      color: var(--brand);
      box-shadow: none;
    }
    .trust-line {
      padding: 18px 20px;
      text-align: center;
      color: var(--text-muted);
      border-top: 1px solid var(--border);
      font-size: 0.92rem;
    }
    .mobile-floating-cta {
      display: none;
    }
    @media (max-width: 860px) {
      .hero-grid, .content-grid, .quick-answer .uti-wrap {
        grid-template-columns: 1fr;
      }
      .side-card {
        position: static;
      }
      .related-grid {
        grid-template-columns: 1fr;
      }
      .hero-card {
        max-width: 420px;
      }
      .mobile-floating-cta {
        display: block;
        position: fixed;
        left: 12px;
        right: 12px;
        bottom: 12px;
        z-index: 9998;
      }
      .mobile-floating-cta a {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 52px;
        border-radius: 999px;
        background: var(--brand);
        color: #FFFFFF;
        text-decoration: none;
        font-weight: 800;
        box-shadow: 0 10px 28px rgba(37, 99, 235, 0.32);
      }
    }
  </style>
</head>
<body>
${header}
  <main>
    <section class="uti-hero">
      <div class="uti-wrap">
        <nav class="crumbs" aria-label="Breadcrumb">
          <a href="https://npcwoods.com/">Home</a>
          <span>/</span>
          <a href="https://npcwoods.com/uti-treatment/">UTI Treatment</a>
          <span>/</span>
          <span>${esc(page.eyebrow)}</span>
        </nav>
        <div class="hero-grid">
          <div>
            <span class="eyebrow">${esc(page.eyebrow)}</span>
            <h1>${esc(page.h1)}</h1>
            <p class="lede">${esc(page.lede)}</p>
            <div class="hero-actions">
              <a class="primary-cta" href="${smsHref(page.sms)}">Start My $59 UTI Visit</a>
              <a class="secondary-cta" href="https://npcwoods.com/uti-treatment/">Back to UTI Hub</a>
            </div>
          </div>
          <aside class="hero-card" aria-label="Clinician review">
            <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" alt="Chris Woods, MSN, APRN, FNP-C" width="72" height="72">
            <h2>Reviewed by Chris Woods, MSN, APRN, FNP-C</h2>
            <p>$59 flat fee. Text-based UTI visits in ${states.length} states. If your symptoms need in-person care, Chris will say that clearly.</p>
          </aside>
        </div>
      </div>
    </section>

    <section class="quick-answer">
      <div class="uti-wrap">
        <strong>Short answer</strong>
        <p>${esc(page.answer)}</p>
      </div>
    </section>

    <section class="content">
      <div class="uti-wrap content-grid">
        <article>
          ${page.sections.map((section) => `<section>
            <h2>${esc(section.heading)}</h2>
            ${section.body.map((paragraph) => `<p>${esc(paragraph)}</p>`).join('\n            ')}
            ${section.bullets ? `<ul class="bullet-panel">${section.bullets.map((item) => `<li>${esc(item)}</li>`).join('')}</ul>` : ''}
          </section>`).join('\n          ')}
        </article>

        <aside class="side-card">
          <h2>Think this fits your symptoms?</h2>
          <p>Text Chris the symptom pattern, when it started, your allergies, and your preferred pharmacy.</p>
          <ul>
            <li>$59 flat visit</li>
            <li>No video call for most simple UTI visits</li>
            <li>Pharmacy treatment when appropriate</li>
          </ul>
          <a class="primary-cta" href="${smsHref(page.sms)}">Text Chris</a>
        </aside>
      </div>
    </section>

    <section class="related">
      <div class="uti-wrap">
        <h2>Related UTI guides</h2>
        <div class="related-grid">
          ${related.map((item) => `<a class="related-card" href="https://npcwoods.com/uti-treatment/${item.slug}/"><span>${esc(item.eyebrow)}</span>${esc(item.h1)}</a>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="faq">
      <div class="uti-wrap">
        <h2>Quick questions</h2>
        <div class="faq-list">
          ${page.faqs.map(([question, answer]) => `<details>
            <summary>${esc(question)}</summary>
            <p>${esc(answer)}</p>
          </details>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="bottom-cta">
      <div class="uti-wrap">
        <h2>Ready to skip the waiting room?</h2>
        <p>Start a text-based UTI visit for $59. Chris will review your symptoms and tell you the safest next step.</p>
        <a class="primary-cta" href="${smsHref(page.sms)}">Start My $59 UTI Visit</a>
      </div>
    </section>

    <div class="trust-line">
      Reviewed by Chris Woods, MSN, APRN, FNP-C. Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT. Last updated: <time datetime="${updated}">${updatedDisplay}</time>.
    </div>
  </main>
${footer}
  <div class="mobile-floating-cta">
    <a href="${smsHref(page.sms)}">$59. Text Chris About UTI Symptoms</a>
  </div>
  <script src="/tracking.js"></script>
</body>
</html>
`;
}

for (const page of pages) {
  const dir = path.join(outRoot, page.slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), renderPage(page));
  console.log(`wrote landing-pages/uti-treatment/${page.slug}/index.html`);
}
