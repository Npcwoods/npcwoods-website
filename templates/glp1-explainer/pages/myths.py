"""Myths vs facts."""
from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_myths

F = 'font-family="Inter, Arial, sans-serif"'

D_SORT = svg('d-sort', 'Sorting claims into myth and fact',
  'Two bins. Left bin has an X for myths. Right bin has a check for facts. Loose claim cards float above.',
  '0 0 480 300', '''
<rect width="480" height="300" fill="#fff"/>
<rect x="40" y="140" width="160" height="120" rx="20" fill="#ffe8e8" stroke="#c44" stroke-width="4"/>
<rect x="280" y="140" width="160" height="120" rx="20" fill="#e6f7ee" stroke="#19a463" stroke-width="4"/>
<path d="M90 180 L130 220 L190 150" fill="none" stroke="#c44" stroke-width="8" stroke-linecap="round" transform="translate(10 10) scale(.55)"/>
<g stroke="#c44" stroke-width="8" stroke-linecap="round"><path d="M90 180 L150 240 M150 180 L90 240"/></g>
<g stroke="#19a463" stroke-width="8" stroke-linecap="round" fill="none"><path d="M320 210 L350 240 L420 160"/></g>
<rect x="100" y="40" width="100" height="50" rx="12" fill="#eef0f4" stroke="#9a9aa3" stroke-width="2"/>
<rect x="220" y="30" width="100" height="50" rx="12" fill="#eef0f4" stroke="#9a9aa3" stroke-width="2"/>
<rect x="340" y="50" width="100" height="50" rx="12" fill="#eef0f4" stroke="#9a9aa3" stroke-width="2"/>
<g ''' + F + ''' font-weight="800" font-size="18" fill="#111114"><text x="80" y="290">Myth</text><text x="325" y="290">Fact</text></g>''')

S = [
 sec('cream', 'sort', 'Internet claims', 'Let\'s sort them.',
   '<p>GLP-1s are everywhere online. Some posts are careful. Many are not. Here is how I sort the loudest claims when patients text me.</p>'
   + why('A viral clip is not a label, and a label is not your whole story.'),
   fig(D_SORT, 'We toss weak claims in the myth bin. We keep what the science and labels support.')),
 sec('white', 'body', 'Body myths', 'What these meds are — and are not.',
   '',
   below=grid([
     tile('alert', 'Myth: "It melts fat with zero effort"', 'Fact: These medicines change hunger and stomach speed. Food choices still matter. Protein still matters. Movement still matters.' + cite(5, 7)),
     tile('muscle', 'Myth: "You only lose fat"', 'Fact: Some lean mass can go too. Protein and strength moves help you keep more muscle.' + cite(7)),
     tile('pill', 'Myth: "It is just a shot, not a real medicine"', 'Fact: These are prescription medicines. They hit real receptors. They have real side effects. Labels carry real warnings.' + cite(1, 2)),
     tile('clock', 'Myth: "One week tells you everything"', 'Fact: Levels build over weeks. Month one is a test drive, not the whole movie.' + cite(1, 2)),
   ])),
 sec('night', 'access', 'Access myths', 'Money and shortcuts.',
   '',
   below=grid([
     tile('note', 'Myth: "Everyone\'s plan covers it"', 'Fact: Coverage varies widely. I cannot promise what your health plan will pay.'),
     tile('shield', 'Myth: "Compounded is the same as brand"', 'Fact: Compounded drugs are not FDA-approved. FDA does not check them for safety or quality before they are sold.'),
     tile('chat', 'Myth: "A consult means a prescription"', 'Fact: A consult is a fit check. I may say no.'),
     tile('heart', 'Myth: "Higher dose is always better"', 'Fact: The right dose is the one you can live with. Holding a step is often smart.' + cite(1, 2)),
   ])),
 sec('orange', 'safety', 'Safety myths', 'Red flags are real.',
   '<p>Myth: "Nausea means it is working harder." Fact: Nausea means your gut is unhappy. It is not a trophy.' + cite(1, 5) + '</p>'
   '<p>Myth: "Thyroid warnings are just lawyer talk." Fact: Labels carry a boxed warning about thyroid C-cell tumors seen in rodents, and hard stops for MTC and MEN2 history. We take that seriously.' + cite(1, 2, 3, 4) + '</p>'
   + why('If a claim shrugs at red flags, throw it in the myth bin.')),
]

PAGE = dict(
  title='GLP-1 Myths vs Facts | GLP-1 Explained | NPCWoods',
  description='GLP-1 myths vs facts in plain words from Chris Woods — effort, muscle, coverage, compounded drugs, dose climbs, and real safety warnings.',
  about='Common GLP-1 myths and evidence-based facts',
  reviewed='2026-10-06', published='2026-10-06',
  pill='GLP-1 Explained · Myths vs facts',
  h1_top='Myths vs', h1_pop='Facts',
  sub='Internet claims, sorted — without the hype or the scare tactics.',
  sticker1='Sort the noise <span aria-hidden="true">✅</span>', sticker2='Labels over memes',
  jump_label='Sort the myths', crumb='Myths vs Facts',
  ghost_svg=ghost_myths(),
  lede='Last stop was honest cost. Now we close the road map by sorting the loudest myths from the facts.',
  tldr=[
    'These are real medicines — not magic fat erasers.',
    'Some lean mass can go; protein and strength help.',
    'Coverage and compounded ads need clear eyes.',
    'Nausea is not a trophy, and label warnings are not a joke.',
  ],
  sections=S,
  recap_title='Myths vs facts, in four pictures.',
  recap=[
    ('Not magic', 'Appetite and stomach speed change — effort still matters.'),
    ('Muscle matters', 'Protein and strength help keep lean mass.'),
    ('Access myths', 'Coverage is not universal; compounded is not brand.'),
    ('Safety real', 'Red flags and boxed warnings deserve respect.'),
  ],
  faq=[
    ('Do GLP-1s mean I can eat anything?', 'No. A slow stomach still punishes huge greasy meals. Smaller plates feel better.'),
    ('Is nausea a sign it is working?', 'No. Nausea means your gut is unhappy. Tell me; we may hold or adjust.'),
    ('Are social media before-and-afters proof?', 'No. Those are ads or anecdotes. Your history and the label guide care.'),
    ('Should I buy the cheapest compounded option I see?', 'Price alone is a weak guide. Compounded drugs are not FDA-approved. Talk safety first.'),
  ],
  sources=[SRC['wegovy_dm'], SRC['zepbound_dm'], SRC['wegovy_fda'], SRC['zepbound_fda'], SRC['statpearls_glp1'], SRC['statpearls_sema'], SRC['neeland']],
  cta_title='Still sorting a claim you saw? <span>Text me.</span>',
  cta_text='I\'m Chris, a nurse practitioner. Text me your health history, and we\'ll see if a GLP-1 may fit you.',
  disclaimer=DISCLAIMER,
)
