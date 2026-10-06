from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_soothe

F = 'font-family="Inter, Arial, sans-serif"'

D_BANDAGE = svg('d-band', 'Symptom relief is a bandage, not the cure',
  'Phenazopyridine can numb urinary pain while an antibiotic clears the infection. It does not kill the germs.',
  '0 0 480 320',
  '<rect width="480" height="320" fill="#fff"/>'
  '<rect x="40" y="80" width="180" height="140" rx="20" fill="#fff7e8"/><text x="130" y="140" text-anchor="middle" ' + F + ' font-size="18" font-weight="800">Relief</text><text x="130" y="170" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">numbs the burn</text>'
  '<text x="240" y="160" text-anchor="middle" ' + F + ' font-size="28" font-weight="900" fill="#c0392b">≠</text>'
  '<rect x="280" y="80" width="160" height="140" rx="20" fill="#e8f2fe"/><text x="360" y="140" text-anchor="middle" ' + F + ' font-size="18" font-weight="800">Cure</text><text x="360" y="170" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">kills the germs</text>'
  '<text x="240" y="280" text-anchor="middle" ' + F + ' font-size="16" font-weight="700" fill="#3a3a42">Phenazopyridine soothes. Antibiotics clear.</text>')

S = [
 sec('cream', 'bandage', 'The bandage idea', 'Quiet the alarm while the crew works.',
   '<p>Antibiotics need hours to days to knock germs down. Meanwhile your urethra still feels on fire.</p>'
   '<p><strong>Phenazopyridine</strong> is a pee-pain comfort medicine for burn, urgency, and pressure.' + cite(1, 2) + '</p>',
   fig(D_BANDAGE, 'Relief is not the same job as cure.')),
 sec('white', 'orange-pee', 'The famous orange pee', 'Harmless color show, real rules.',
   '<p>Phenazopyridine often turns pee bright orange or red-orange. It can stain underwear and contacts.' + cite(1) + '</p>'
   '<p>It is usually used for a short time (often about two days) while the antibiotic kicks in — not as forever candy.</p>'
   + why('If you only take the orange pill and skip antibiotics for a true bacterial UTI, the germs keep throwing a party.')),
 sec('orange', 'other-comfort', 'Other comfort moves', 'Heat, fluids, and rest still help.',
   '<p>A heating pad on the low belly, steady fluids, and avoiding harsh soaps can take the edge off.' + cite(2) + '</p>'
   '<p>Skip the "chug cranberry juice until you float" plan as your only therapy. Prevention talk comes later.</p>'),
 sec('night', 'limits', 'Limits and safety', 'When comfort meds are not enough.',
   '<p>Phenazopyridine does not treat kidney infection, STI, or yeast. Rising fever or side pain means stop guessing and get urgent help.' + cite(3) + '</p>'
   '<p>People with significant kidney problems need careful advice before using it. Read the label and tell me your full medicine list.</p>',
   below=grid([
     tile('flame', 'What it helps', 'Burn, urgency, pressure feelings.'),
     tile('ban', 'What it is not', 'Not an antibiotic. Not a cure.'),
     tile('clock', 'How long', 'Short bridge while antibiotics work.'),
     tile('alert', 'Stop & escalate', 'Fever, flank pain, vomiting — urgent path.'),
   ])),
]

PAGE = dict(
  title='UTI Relief While Antibiotics Work | NPCWoods',
  description='Phenazopyridine and comfort tips while antibiotics work — symptom relief, not a cure. By NP Chris Woods.',
  about='Symptomatic relief for urinary tract infection',
  reviewed='2026-10-06', published='2026-10-06',
  pill='UTI Explained · Relief',
  h1_top='Relief While It', h1_pop='Kicks In',
  sub='Orange pee comfort medicine is a bandage. Antibiotics are the cleanup crew.',
  sticker1='Not a cure', sticker2='Orange pee',
  jump_label='Learn the bandage', crumb='Relief',
  ghost_svg=ghost_soothe(),
  lede='Antibiotics need a little time. Here is how we quiet the burn without pretending comfort pills clear the infection.',
  tldr=[
    'Phenazopyridine can numb urinary pain short-term.',
    'It does not kill bacteria.',
    'Orange urine is expected with that medicine.',
    'Fever or flank pain means escalate — do not just add more comfort pills.',
  ],
  sections=S,
  recap_title='Relief rules.',
  recap=[
    ('Bandage', 'Numbs symptoms; does not cure.'),
    ('Orange pee', 'Common and expected with phenazopyridine.'),
    ('Short bridge', 'Usually brief while antibiotics work.'),
    ('Escalate', 'Red flags beat any comfort plan.'),
  ],
  faq=[
    ('Can I take phenazopyridine alone?', 'For a true bacterial UTI, you still need the right antibiotic plan. Relief alone leaves the germs in place.'),
    ('Is Azo® the same idea?', 'Many OTC urinary pain products use phenazopyridine. Read the active ingredient and the warnings.'),
    ('Why only a couple of days?', 'It is meant as a short bridge. Ongoing symptoms need a rethink of the diagnosis or antibiotic plan.'),
    ('Will it fix kidney infection pain?', 'No. Kidney infection needs a different level of care.'),
  ],
  sources=[SRC['pyridium_dm'], SRC['niddk_bladder'], SRC['cdc_uti'], SRC['idsa2011']],
  cta_title='Burning while you wait? <span>Text me.</span>',
  cta_text='I can help sort antibiotic fit and safe comfort options for your situation.',
  disclaimer=DISCLAIMER,
)
