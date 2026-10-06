from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_masks

F = 'font-family="Inter, Arial, sans-serif"'

D_MASKS = svg('d-masks', 'Things that can mimic a UTI',
  'Yeast, STI, stones, and irritation can all cause pee discomfort that is not a classic bladder UTI.',
  '0 0 480 360',
  '<rect width="480" height="360" fill="#fff"/>'
  '<circle cx="120" cy="140" r="70" fill="#fff7e8" stroke="#f5a524" stroke-width="3"/><text x="120" y="136" text-anchor="middle" ' + F + ' font-size="17" font-weight="800">Yeast</text><text x="120" y="158" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">itch + discharge</text>'
  '<circle cx="240" cy="140" r="70" fill="#e8f2fe" stroke="#0071e3" stroke-width="3"/><text x="240" y="136" text-anchor="middle" ' + F + ' font-size="17" font-weight="800">STI</text><text x="240" y="158" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">burn ± discharge</text>'
  '<circle cx="360" cy="140" r="70" fill="#fdecea" stroke="#c0392b" stroke-width="3"/><text x="360" y="136" text-anchor="middle" ' + F + ' font-size="17" font-weight="800">Stone</text><text x="360" y="158" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">sharp wave pain</text>'
  '<rect x="90" y="250" width="300" height="70" rx="16" fill="#eaf8f0"/><text x="240" y="280" text-anchor="middle" ' + F + ' font-size="17" font-weight="800">Irritation / soap / sex friction</text><text x="240" y="302" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">sore without true infection</text>')

S = [
 sec('cream', 'not-always', 'The trap', 'Not everything that burns is a UTI.',
   '<p>Burn with pee feels like a UTI alarm. Sometimes it is. Sometimes it is yeast, an STI, a stone, or plain irritation.' + cite(1) + '</p>'
   '<p>Guessing wrong can mean the wrong medicine — or a delay when you needed a different plan.</p>'
   + why('I would rather ask a few awkward questions than treat the wrong problem.'),
   fig(D_MASKS, 'Four common lookalikes sit next to true bladder infection.')),
 sec('white', 'yeast', 'Lookalike · Yeast', 'Itch and thick discharge change the picture.',
   '<p>A yeast infection often brings itch, redness, and thick discharge. Pee can sting if the skin is raw, but the main story is usually outside the bladder.' + cite(2) + '</p>'
   '<p>Antibiotics for a UTI do not fix yeast. Yeast medicine does not fix a bacterial UTI.</p>',
   below=grid([
     tile('bug', 'Yeast clues', 'Itch, cottage-cheese or thick discharge, outer sore skin.'),
     tile('flame', 'UTI clues', 'Urgency, frequency, low pressure, burn with little discharge.'),
   ]), flip=False),
 sec('orange', 'sti', 'Lookalike · STI', 'Some STIs burn too.',
   '<p>Chlamydia, gonorrhea, and other infections can burn with pee or cause discharge. The history matters: new partner, unprotected sex, partner symptoms.' + cite(1) + '</p>'
   '<p>If that story fits, we should not slap a UTI label on it and move on.</p>'),
 sec('night', 'stone-irritation', 'Stones and irritation', 'Sharp waves vs soap sting.',
   '<p>A kidney stone can send sharp, rolling pain in the side or back, sometimes with blood in the pee. That is not a simple cystitis script.' + cite(3) + '</p>'
   '<p>Harsh soaps, bubble baths, spermicides, or friction after sex can irritate the urethra. Symptoms often ease when the irritant stops.</p>'
   + why('If your story is odd, saying "maybe not a UTI" is part of good care.')),
]

PAGE = dict(
  title='Not Everything That Burns Is a UTI | NPCWoods',
  description='Yeast, STI, stones, and irritation can mimic a UTI. How to tell lookalikes apart in plain words. By NP Chris Woods.',
  about='Differential diagnosis of dysuria',
  reviewed='2026-10-06', published='2026-10-06',
  pill='UTI Explained · Lookalikes',
  h1_top='Not Everything That Burns', h1_pop='Is a UTI',
  sub='Yeast, STI, stones, and soap sting can wear a UTI costume.',
  sticker1='Lookalikes', sticker2='Ask twice',
  jump_label='Sort the costume', crumb='Lookalikes',
  ghost_svg=ghost_masks(),
  lede='Last stop was the classic bladder feelings. This stop is the plot twist: sometimes the burn is a different character entirely.',
  tldr=[
    'Burn is a clue, not a final answer.',
    'Yeast often brings itch and discharge.',
    'STIs can burn and need a different workup.',
    'Stones and irritation can fool you too.',
  ],
  sections=S,
  recap_title='Four costumes to remember.',
  recap=[
    ('Yeast', 'Itch + discharge, outer sore skin.'),
    ('STI', 'Burn ± discharge; sexual history matters.'),
    ('Stone', 'Sharp wave pain, often flank.'),
    ('Irritation', 'Soap, friction, chemicals — no true bug.'),
  ],
  faq=[
    ('Can I have a UTI and yeast at the same time?', 'Yes. Antibiotics can also tip someone into yeast afterward.'),
    ('Should I just take leftover antibiotics?', 'No. Wrong drug, wrong bug, and leftover pills are a bad mix.'),
    ('When is discharge a big deal?', 'New, colored, foul, or paired with pelvic pain needs a careful review — not a shrug.'),
    ('Do home UTI strips settle it?', 'They can support the story. They do not replace a real history, and false results happen.'),
  ],
  sources=[SRC['statpearls_cystitis'], SRC['cdc_uti'], SRC['niddk_bladder'], SRC['niddk_kidney']],
  cta_title='Not sure which costume? <span>Text me.</span>',
  cta_text='Describe the burn, any discharge, fever, or side pain. I\'ll help sort UTI from lookalikes.',
  disclaimer=DISCLAIMER,
)
