from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_myths

F = 'font-family="Inter, Arial, sans-serif"'

D_MYTH = svg('d-myth', 'Myths vs facts grid',
  'Common myths: holding pee always causes UTI, cranberry cures infection, leftover antibiotics are fine, and $59 covers medicine.',
  '0 0 480 360',
  '<rect width="480" height="360" fill="#fff"/>'
  '<rect x="20" y="30" width="210" height="140" rx="16" fill="#fdecea"/><text x="125" y="80" text-anchor="middle" ' + F + ' font-size="16" font-weight="800" fill="#c0392b">MYTH</text><text x="125" y="110" text-anchor="middle" ' + F + ' font-size="14" font-weight="600">Juice cures UTI</text><text x="125" y="138" text-anchor="middle" ' + F + ' font-size="14" font-weight="600">Leftover pills are fine</text>'
  '<rect x="250" y="30" width="210" height="140" rx="16" fill="#eaf8f0"/><text x="355" y="80" text-anchor="middle" ' + F + ' font-size="16" font-weight="800" fill="#148a53">FACT</text><text x="355" y="110" text-anchor="middle" ' + F + ' font-size="14" font-weight="600">Antibiotics clear bugs</text><text x="355" y="138" text-anchor="middle" ' + F + ' font-size="14" font-weight="600">Right drug, right person</text>'
  '<rect x="70" y="200" width="340" height="110" rx="16" fill="#fff7e8"/><text x="240" y="250" text-anchor="middle" ' + F + ' font-size="17" font-weight="800">$59 visit ≠ medicine cost</text><text x="240" y="280" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">Pharmacy price is separate</text>')

S = [
 sec('cream', 'sort', 'Myth-busting without snark', 'Internet claims, sorted.',
   '<p>UTI advice online is a salad of half-truths. Let\'s plate the useful parts and compost the rest.' + cite(1) + '</p>',
   fig(D_MYTH, 'Myths on the left. Facts on the right. Money talk included.')),
 sec('white', 'list', 'Myths vs facts', 'A quick sorting hat.',
   '<p><strong>Myth:</strong> Holding pee always causes a UTI.<br><strong>Fact:</strong> Holding a lot, often, can raise risk. One busy afternoon is not destiny.' + cite(2) + '</p>'
   '<p><strong>Myth:</strong> Cranberry cures an active UTI.<br><strong>Fact:</strong> Mixed prevention data. Not a treatment for bacterial cystitis.</p>'
   '<p><strong>Myth:</strong> Leftover antibiotics are fine.<br><strong>Fact:</strong> Wrong drug and incomplete courses breed trouble.</p>'
   '<p><strong>Myth:</strong> If you burn, you must get antibiotics today.<br><strong>Fact:</strong> Lookalikes exist. Sometimes the right answer is a different plan — or in-person care.</p>'),
 sec('orange', 'money', 'Honest money talk', 'The $59 visit and the medicine are separate.',
   '<p>The NPCWoods UTI text visit is <strong>$59</strong>. That is for my review and plan.' + cite(3) + '</p>'
   '<p>If an antibiotic or comfort medicine is appropriate, the <strong>pharmacy cost is separate</strong>. I do not pocket your pharmacy bill, and I cannot honestly quote every store\'s cash price in advance.</p>'
   + why('Ask your pharmacy for the cash price. GoodRx-style coupons sometimes help. No surprises from me about what $59 covers.')),
 sec('night', 'close', 'Close the series', 'You now own the whole map.',
   '<p>Climb, feelings, lookalikes, bladder vs kidney, antibiotics, relief, recurrence, prevention, and when to go in.</p>'
   '<p>If you want care, text me. If you need the ER, go. If you just needed understanding, you are welcome here either way.</p>',
   below=grid([
     tile('ban', 'Myth', 'Juice cures infection.'),
     tile('check', 'Fact', 'Antibiotics treat bacterial UTI when appropriate.'),
     tile('money', 'Money', '$59 visit; medicine priced at pharmacy.'),
     tile('chat', 'Care', 'Consult does not guarantee a Rx.'),
   ])),
]

PAGE = dict(
  title='UTI Myths vs Facts + Honest $59 Talk | NPCWoods',
  description='UTI myths vs facts in plain words, plus honest talk about the $59 visit vs separate medicine cost. By NP Chris Woods.',
  about='Urinary tract infection education and cost transparency',
  reviewed='2026-10-06', published='2026-10-06',
  pill='UTI Explained · Myths',
  h1_top='Myths vs', h1_pop='Facts',
  sub='Internet claims, sorted. Plus honest talk about the $59 visit.',
  sticker1='Myth busted', sticker2='$59 ≠ Rx',
  jump_label='Sort the claims', crumb='Myths',
  ghost_svg=ghost_myths(),
  lede='Last stop on the map. Let\'s clear the folklore and talk money without squirming.',
  tldr=[
    'Cranberry does not cure an active bacterial UTI.',
    'Leftover antibiotics are a bad plan.',
    'Not every burn needs remote antibiotics.',
    'The $59 visit is separate from pharmacy medicine cost.',
  ],
  sections=S,
  recap_title='Final pocket card.',
  recap=[
    ('Myths', 'Juice cures, leftovers fix, every burn = Rx.'),
    ('Facts', 'Right drug, right person, right door.'),
    ('$59', 'Pays for the visit and plan.'),
    ('Medicine', 'Pharmacy price is separate.'),
  ],
  faq=[
    ('Does $59 include the antibiotic?', 'No. The visit is $59. Medicine, if prescribed, is paid at the pharmacy.'),
    ('Can you guarantee a prescription?', 'No. A consult does not guarantee a prescription.'),
    ('Is telehealth real care?', 'It is real clinical review with limits. Red-flag situations need in-person or ER care.'),
    ('Where should I start if I hurt now?', 'If you are severely ill, use urgent or emergency care. Otherwise text with a clear symptom list.'),
  ],
  sources=[SRC['cdc_uti'], SRC['niddk_bladder'], SRC['idsa2011'], SRC['statpearls_cystitis']],
  cta_title='Ready for a real review? <span>Text me.</span>',
  cta_text='I\'m Chris. $59 for the visit. Medicine cost separate. No folklore, no Rx promises — just plain care.',
  disclaimer=DISCLAIMER,
)
