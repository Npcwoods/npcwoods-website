from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_levels

F = 'font-family="Inter, Arial, sans-serif"'

D_LEVELS = svg('d-levels', 'Bladder infection vs kidney infection',
  'Bladder infection stays low. Kidney infection climbs higher with fever, flank pain, and often vomiting.',
  '0 0 480 400',
  '<rect width="480" height="400" fill="#fff"/>'
  '<path d="M140 80 C170 40 310 40 340 80 C330 130 150 130 140 80Z" fill="#fff7e8" stroke="#f5a524" stroke-width="4"/>'
  '<text x="240" y="95" text-anchor="middle" ' + F + ' font-size="18" font-weight="800">Kidneys</text>'
  '<line x1="240" y1="130" x2="240" y2="220" stroke="#2997ff" stroke-width="8"/>'
  '<ellipse cx="240" cy="290" rx="100" ry="55" fill="#e8f2fe" stroke="#0071e3" stroke-width="4"/>'
  '<text x="240" y="298" text-anchor="middle" ' + F + ' font-size="18" font-weight="800">Bladder</text>'
  '<text x="40" y="200" ' + F + ' font-size="15" font-weight="700" fill="#c0392b">Fever · flank</text>'
  '<text x="40" y="222" ' + F + ' font-size="15" font-weight="700" fill="#c0392b">pain · vomit</text>'
  '<text x="330" y="300" ' + F + ' font-size="15" font-weight="700" fill="#0071e3">Burn · urgency</text>'
  '<text x="330" y="322" ' + F + ' font-size="15" font-weight="700" fill="#0071e3">frequency</text>')

S = [
 sec('cream', 'two-floors', 'Two floors of the same building', 'Bladder is downstairs. Kidney is upstairs.',
   '<p><strong>Cystitis</strong> means the infection is mainly in the bladder. Uncomfortable. Usually not an ER story by itself.' + cite(1, 2) + '</p>'
   '<p><strong>Pyelonephritis</strong> means the infection has reached a kidney. That is a bigger deal.</p>',
   fig(D_LEVELS, 'Same plumbing. Very different floors.')),
 sec('white', 'text-ok', 'When text care can fit', 'Uncomplicated bladder symptoms in the right person.',
   '<p>Healthy non-pregnant women with classic burn, urgency, and frequency — and no red flags — are the group guidelines know best for outpatient care.' + cite(3) + '</p>'
   '<p>Even then, a consult is a real review. It is not a vending machine for pills.</p>'
   + why('If your story fits the simple bladder pattern, we can often plan care by text. If it does not, we change course.')),
 sec('night', 'red-flags', 'Red flags · think kidney / ER', 'Do not tough these out at home.',
   '<p>Seek urgent or emergency care for fever, shaking chills, pain in the side or back under the ribs (flank), vomiting, confusion, or feeling severely ill.' + cite(2, 4) + '</p>'
   '<p>Pregnancy, male sex, catheters, recent urologic procedures, kidney disease, or being immunocompromised also push you out of the "simple text UTI" lane.</p>',
   below=grid([
     tile('bladder', 'Bladder (cystitis)', 'Burn, urgency, frequency, low pressure. Often afebrile.'),
     tile('kidney', 'Kidney (pyelo)', 'Fever, flank pain, nausea or vomiting, looking sick.'),
     tile('er', 'Go now', 'Severe illness, dehydration, inability to keep fluids down.'),
     tile('chat', 'Text lane', 'Classic uncomplicated bladder symptoms without red flags.'),
   ])),
 sec('orange', 'bridge', 'Next stops', 'Meds only make sense after the floor is clear.',
   '<p>If we are still on the bladder floor, antibiotics and comfort meds are the next chapters.</p>'
   '<p>If we are upstairs at the kidney, the plan is different — and delaying in-person care is not toughness. It is risk.</p>'),
]

PAGE = dict(
  title='Bladder vs Kidney Infection: When to Text vs ER | NPCWoods',
  description='Cystitis vs pyelonephritis in plain words: when text care can fit and when fever or flank pain means urgent care. By NP Chris Woods.',
  about='Cystitis versus pyelonephritis',
  reviewed='2026-10-06', published='2026-10-06',
  pill='UTI Explained · Bladder vs kidney',
  h1_top='Bladder vs', h1_pop='Kidney',
  sub='Same plumbing. Different floors. Know which floor you are on.',
  sticker1='Cystitis', sticker2='Pyelo flags',
  jump_label='Find your floor', crumb='Bladder vs Kidney',
  ghost_svg=ghost_levels(),
  lede='You know the burn. Now the big fork: is this still a bladder problem, or has it climbed to a kidney?',
  tldr=[
    'Cystitis = bladder floor. Pyelonephritis = kidney floor.',
    'Fever, flank pain, and vomiting are kidney-worry signs.',
    'Uncomplicated bladder symptoms can fit text care for the right person.',
    'Red-flag or special situations need in-person or ER care.',
  ],
  sections=S,
  recap_title='Floor check.',
  recap=[
    ('Bladder', 'Burn, urgency, frequency — often no fever.'),
    ('Kidney', 'Fever, flank pain, vomiting, looking sick.'),
    ('Text lane', 'Classic uncomplicated cystitis pattern.'),
    ('ER lane', 'Severe illness or red-flag features.'),
  ],
  faq=[
    ('Can a bladder UTI become a kidney infection?', 'Yes. That is why red flags matter and why we reassess if you worsen.'),
    ('Is backache always pyelo?', 'No. Low backache has many causes. Flank pain with fever is the combo that worries me more.'),
    ('What if I am pregnant?', 'Pregnancy is not the simple text-cystitis lane. You need tailored in-person oriented care.'),
    ('What if I am a man with burning?', 'Male UTI symptoms need a deeper look. Do not treat it like a routine female cystitis.'),
  ],
  sources=[SRC['statpearls_cystitis'], SRC['statpearls_pyelo'], SRC['idsa2011'], SRC['niddk_kidney']],
  cta_title='Which floor are you on? <span>Text me.</span>',
  cta_text='Share symptoms, fever, side pain, and your situation. I will tell you honestly if text care fits — or if you need in-person help now.',
  disclaimer=DISCLAIMER,
)
