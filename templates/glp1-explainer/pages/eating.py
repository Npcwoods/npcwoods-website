"""Eating on a GLP-1."""
from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_plate

F = 'font-family="Inter, Arial, sans-serif"'

D_PLATES = svg('d-plates', 'Big plate vs small plate at a slow stomach',
  'Two plates at a yellow light. The small plate fits. The big plate backs up. Your stomach exit is on yellow.',
  '0 0 480 300', '''
<rect width="480" height="300" fill="#fff"/>
<circle cx="120" cy="160" r="70" fill="#eef0f4" stroke="#9a9aa3" stroke-width="4"/>
<circle cx="120" cy="160" r="28" fill="#c5c5cc"/>
<circle cx="340" cy="160" r="48" fill="#e8f2fe" stroke="#0058b0" stroke-width="4"/>
<circle cx="340" cy="160" r="18" fill="#2997ff"/>
<rect x="210" y="40" width="50" height="130" rx="20" fill="#2a2a2a"/>
<circle cx="235" cy="70" r="14" fill="#ff6b6b"/>
<circle cx="235" cy="105" r="14" fill="#f5a524"/>
<circle cx="235" cy="140" r="14" fill="#19a463" fill-opacity=".35"/>
<g ''' + F + ''' font-weight="800" font-size="16" fill="#111114"><text x="70" y="260">Big plate</text><text x="300" y="260">Small plate</text></g>''')

S = [
 sec('cream', 'yellow', 'Yellow light', 'Your stomach is on slow.',
   '<p>A GLP-1 puts a yellow light on the exit from your stomach. Food leaves bit by bit. You feel full sooner.' + cite(1, 5) + '</p>'
   '<p>That is useful — until you pile on a big, greasy meal. Then the backup can feel like nausea or a rock in your gut.</p>'
   + why('Smaller plates match a slower exit. You are not "weak." Your plumbing changed.'),
   fig(D_PLATES, 'Same yellow light. A small plate fits. A big one backs up.')),
 sec('white', 'protein', 'Protein first', 'Make each bite count.',
   '<p>You may eat less now. Put protein on the plate first — eggs, fish, chicken, beans, Greek yogurt. Then veggies. Then the rest.' + cite(7) + '</p>'
   '<p>When people lose weight, some of it can be muscle. Protein plus simple strength moves can help you keep more muscle.</p>'
   + why('Muscle is not vanity. It helps energy, balance, and how your body handles sugar.')),
 sec('night', 'traps', 'Common traps', 'What tends to feel rough.',
   '<p>Greasy fried food sits longest. Big sugary drinks can hit hard. Eating past full is a fast path to queasy.</p>',
   below=grid([
     tile('alert', 'Grease', 'Fried food is a top queasy trigger on a slow stomach.'),
     tile('glass', 'Sip all day', 'Water keeps your gut moving and keeps your kidneys happier.'),
     tile('leaf', 'Fiber slow', 'Veggies, fruit, and beans help you go. Add them slowly.'),
     tile('plate', 'Stop early', 'Stop when you are almost full. Stuffed plus slow is a bad mix.'),
     tile('bed', 'Late meals', 'Huge late dinners can sit overnight. Keep the last plate lighter.'),
     tile('chat', 'Tell me', 'If one food always wrecks you, we note it and plan around it.'),
   ]) + why('These are comfort tips, not a diet plan or a promise about weight.')),
 sec('orange', 'constipation', 'Bathroom and fluids', 'Slow gut, slow go.',
   '<p>Constipation is common. The gut slows. You may eat less fiber. You may drink less water.' + cite(1, 2) + '</p>'
   '<p>Sip through the day. Walk a little. Add fiber slowly. If you go days without a bowel movement and feel bad, text me — do not wait in silence.</p>'
   + why('Hydration is boring and it matters. Your kidneys and gut both thank you.')),
]

PAGE = dict(
  title='Eating on a GLP-1 | GLP-1 Explained | NPCWoods',
  description='How to eat on a GLP-1 in plain words — smaller plates, protein first, greasy-food traps, fluids, and constipation tips from Chris Woods.',
  about='Eating patterns while taking a GLP-1 medicine',
  reviewed='2026-10-06', published='2026-10-06',
  pill='GLP-1 Explained · Eating',
  h1_top='Eating on a', h1_pop='GLP-1',
  sub='Smaller plates, protein first, and why grease is the usual villain.',
  sticker1='Small plates <span aria-hidden="true">🍽️</span>', sticker2='Protein first',
  jump_label='Eat smarter', crumb='Eating on a GLP-1',
  ghost_svg=ghost_plate(),
  lede='You know one key vs two. Now the day-to-day question: what do I eat when my stomach is on yellow?',
  tldr=[
    'Your stomach exit is on yellow — food leaves slowly.',
    'Smaller plates and protein first usually feel better.',
    'Greasy fried food is a top queasy trigger.',
    'Sip water all day; constipation is common and fixable.',
  ],
  sections=S,
  recap_title='Eating on a GLP-1, in four pictures.',
  recap=[
    ('Yellow light', 'Food leaves slowly, so big plates back up.'),
    ('Protein first', 'Make fewer bites count for muscle.'),
    ('Skip the grease', 'Fried food is the usual villain.'),
    ('Sip and go', 'Fluids and fiber keep the bathroom kinder.'),
  ],
  faq=[
    ('Do I need a special diet?', 'No special branded diet from me. Protein, plants, smaller plates, and less grease are the core.'),
    ('Can I still eat out?', 'Yes. Share a plate, box half, or pick grilled over fried. Stop when almost full.'),
    ('Why am I constipated?', 'Slower gut plus less food and less fluid. Sip more, add fiber slowly, and text me if it lasts.'),
    ('Should I skip meals?', 'Skipping and then overeating often feels worse. Smaller, steadier plates usually sit better.'),
  ],
  sources=[SRC['wegovy_dm'], SRC['zepbound_dm'], SRC['wegovy_fda'], SRC['zepbound_fda'], SRC['statpearls_glp1'], SRC['statpearls_sema'], SRC['neeland']],
  cta_title='Questions about eating on one? <span>Text me.</span>',
  cta_text='I\'m Chris, a nurse practitioner. Text me your health history, and we\'ll see if a GLP-1 may fit you.',
  disclaimer=DISCLAIMER,
)
