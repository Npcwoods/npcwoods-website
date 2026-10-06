from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_stop

F = 'font-family="Inter, Arial, sans-serif"'

D_STOP = svg('d-stop', 'Situations that need in-person or urgent care',
  'Pregnancy, male UTI symptoms, catheters, recent urologic procedures, and kidney-infection signs are not the simple text-cystitis lane.',
  '0 0 480 360',
  '<rect width="480" height="360" fill="#fff"/>'
  '<circle cx="240" cy="150" r="90" fill="none" stroke="#c0392b" stroke-width="14"/>'
  '<line x1="180" y1="210" x2="300" y2="90" stroke="#c0392b" stroke-width="14" stroke-linecap="round"/>'
  '<text x="240" y="300" text-anchor="middle" ' + F + ' font-size="18" font-weight="800">Saying no is care</text>'
  '<text x="240" y="328" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">Wrong lane beats wrong treatment</text>')

S = [
 sec('cream', 'no-is-care', 'Saying no is care', 'A text visit has lanes. Some doors stay closed on purpose.',
   '<p>I want to help. Helping sometimes means, "This is not safe to manage by text today."' + cite(1) + '</p>'
   '<p>That is not rejection. That is protecting you from a plan that is too small for the problem.</p>',
   fig(D_STOP, 'Some situations need a different door than a $59 text visit.')),
 sec('white', 'lists', 'Who needs in-person or urgent care', 'Know the short list.',
   '<p><strong>Pregnancy.</strong> UTIs in pregnancy need tailored evaluation and follow-up — not a casual outpatient shrug.' + cite(2) + '</p>'
   '<p><strong>Male UTI symptoms.</strong> Less common, higher chance of a complicated story.</p>'
   '<p><strong>Catheters, stents, recent urologic procedures.</strong> Different germs, different risks.</p>'
   '<p><strong>Kidney signs.</strong> Fever, flank pain, vomiting, looking very sick — urgent or emergency path.' + cite(3) + '</p>',
   below=grid([
     tile('baby', 'Pregnancy', 'Not the simple cystitis text lane.'),
     tile('person', 'Men', 'Burning pee needs a deeper look.'),
     tile('note', 'Catheter / procedure', 'Complicated by definition.'),
     tile('er', 'Sick / pyelo signs', 'Urgent or ER — do not wait on texts.'),
   ])),
 sec('orange', 'other', 'Other stop signs', 'Kids, immunocompromise, stones, failure to improve.',
   '<p>Children, people on strong immune-suppressing medicines, known stones with severe pain, or symptoms that worsen on treatment all push toward in-person care.' + cite(1, 4) + '</p>'
   '<p>If I tell you to go in, I will say why in plain words.</p>'),
 sec('night', 'what-text-fits', 'What text care is for', 'Uncomplicated bladder stories in the right person.',
   '<p>Healthy non-pregnant women with classic cystitis symptoms and no red flags are the group where thoughtful remote care is most often reasonable.' + cite(1) + '</p>'
   '<p>Even then: history first, prescription only if appropriate, and a clear escalate plan if you worsen.</p>'
   + why('I would rather lose a $59 visit than pretend every burn is a text-sized problem.')),
]

PAGE = dict(
  title='Who Needs In-Person UTI Care | NPCWoods',
  description='Who needs in-person or ER care for UTI symptoms: pregnancy, men, catheters, procedures, kidney signs. Saying no is care. By NP Chris Woods.',
  about='Complicated urinary tract infection referral criteria',
  reviewed='2026-10-06', published='2026-10-06',
  pill='UTI Explained · Who needs in-person',
  h1_top='Who Needs', h1_pop='In-Person Care',
  sub='Some doors stay closed on text on purpose. Saying no is care.',
  sticker1='Saying no', sticker2='Right door',
  jump_label='See the stop list', crumb='Who Needs In-Person',
  ghost_svg=ghost_stop(),
  lede='Prevention helps. Antibiotics help. Knowing when text care is the wrong tool protects you most of all.',
  tldr=[
    'Pregnancy, male UTI, catheters, and recent urologic procedures need more than a simple text plan.',
    'Fever, flank pain, and vomiting point to urgent or ER care.',
    'Saying no to remote treatment can be the safest answer.',
    'Classic uncomplicated cystitis in the right person is where text care may fit.',
  ],
  sections=S,
  recap_title='Door check.',
  recap=[
    ('Pregnancy', 'Needs tailored evaluation.'),
    ('Male symptoms', 'Dig deeper.'),
    ('Hardware / procedures', 'Complicated lane.'),
    ('Sick / pyelo', 'Urgent or ER now.'),
  ],
  faq=[
    ('If you say no, do I still pay?', 'Ask up front if you are unsure you fit. I would rather redirect early than pretend.'),
    ('Can I text first to triage?', 'Yes — describe red flags clearly. If you are severely ill, skip the line and use emergency care.'),
    ('What about kidney disease?', 'Chronic kidney disease changes antibiotic choices and risk. Often needs a closer look.'),
    ('Are teens the same as adults?', 'Younger patients can need different evaluation. When unsure, in-person is safer.'),
  ],
  sources=[SRC['idsa2011'], SRC['acog_uti'], SRC['statpearls_pyelo'], SRC['niddk_kidney']],
  cta_title='Not sure you fit? <span>Text me.</span>',
  cta_text='Tell me your situation. If text care is wrong, I will say so plainly — because saying no is care.',
  disclaimer=DISCLAIMER,
)
