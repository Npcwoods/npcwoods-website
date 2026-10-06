from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_climb

F = 'font-family="Inter, Arial, sans-serif"'

D_PIPE = svg('d-pipe', 'The short pipe climb',
  'Bacteria from near the anus climb the short urethra into the bladder and stick to the wall.',
  '0 0 480 400', '''
<rect width="480" height="400" fill="#fff"/>
<ellipse cx="240" cy="70" rx="110" ry="48" fill="#e8f2fe" stroke="#0071e3" stroke-width="4"/>
<text x="240" y="78" text-anchor="middle" ''' + F + ''' font-size="18" font-weight="800" fill="#111114">Bladder</text>
<rect x="210" y="118" width="60" height="220" rx="30" fill="#fff7e8" stroke="#f5a524" stroke-width="4"/>
''' + ''.join('<circle cx="240" cy="%d" r="10" fill="#c0392b"/>' % y for y in (300, 260, 220, 180, 150)) + '''
<text x="290" y="200" ''' + F + ''' font-size="17" font-weight="700" fill="#5f5f68">Urethra</text>
<text x="290" y="222" ''' + F + ''' font-size="17" font-weight="700" fill="#5f5f68">(short pipe)</text>
<text x="40" y="360" ''' + F + ''' font-size="17" font-weight="700" fill="#3a3a42">E. coli starts near the anus,</text>
<text x="40" y="382" ''' + F + ''' font-size="17" font-weight="700" fill="#3a3a42">then climbs up.</text>
''')

D_LOCK = svg('d-adhesin', 'Adhesins lock onto bladder cells',
  'E. coli uses sticky tip proteins called adhesins that fit receptors on bladder cells like a lock and key.',
  '0 0 480 360', '''
<rect width="480" height="360" fill="#fff"/>
<rect x="0" y="160" width="480" height="40" fill="#fdf1e4"/>
''' + ''.join('<circle cx="%d" cy="160" r="8" fill="#f2c9a8"/><circle cx="%d" cy="200" r="8" fill="#f2c9a8"/>' % (x,x) for x in range(16,480,20)) + '''
<g transform="translate(120 70)"><circle r="28" fill="#c0392b"/><path d="M0 28 V70 M-10 50 H10" stroke="#8a1c1c" stroke-width="8" stroke-linecap="round"/><text x="0" y="-40" text-anchor="middle" ''' + F + ''' font-size="16" font-weight="800">E. coli</text></g>
<path d="M160 140 L200 150" stroke="#8a5a00" stroke-width="3" stroke-dasharray="4 4"/>
<g transform="translate(240 120)"><rect x="-36" y="-20" width="72" height="50" rx="10" fill="#0071e3"/><circle cx="0" cy="-8" r="10" fill="#9fd0ff"/><text x="0" y="70" text-anchor="middle" ''' + F + ''' font-size="16" font-weight="800">Receptor</text></g>
<text x="320" y="100" ''' + F + ''' font-size="18" font-weight="800" fill="#111114">Adhesin = key</text>
<text x="320" y="124" ''' + F + ''' font-size="18" font-weight="800" fill="#111114">Receptor = lock</text>
<text x="40" y="280" ''' + F + ''' font-size="17" font-weight="600" fill="#3a3a42">Once it locks on, peeing does not</text>
<text x="40" y="302" ''' + F + ''' font-size="17" font-weight="600" fill="#3a3a42">wash every bug away.</text>
''')

S = [
 sec('cream', 'climb', 'Step 1 · The climb', 'Most UTIs start with a short climb.',
   '<p>Your urethra is the thin pipe that carries pee out of the bladder. In many women it is short, so germs from near the anus do not have far to go.' + cite(1, 2) + '</p>'
   '<p>The usual climber is a gut germ named <strong>E. coli</strong>. It lives near the opening, then works its way up into the bladder.</p>'
   + why('A short pipe plus nearby gut germs is why bladder infections are common after sex, or when you hold pee a long time.'),
   fig(D_PIPE, 'E. coli climbs the urethra and sets up camp in the bladder.')),
 sec('white', 'lock', 'Step 2 · Lock and key', 'The germ sticks on purpose.',
   '<p>E. coli is not just floating. It uses sticky tip proteins called <strong>adhesins</strong>. Think of them as keys.</p>'
   '<p>Bladder cells have receptors that fit those keys. Lock clicks, and the germ hangs on while you pee.' + cite(1, 3) + '</p>'
   + why('That stickiness is why "just drink water" is not always enough once a real infection has started.'),
   fig(D_LOCK, 'Adhesins on E. coli fit receptors on bladder cells.'), flip=True),
 sec('night', 'why-women', 'Step 3 · Why it hits some people more', 'Anatomy stacks the odds.',
   '<p>A shorter urethra means a shorter hike. Sex can push germs closer to the opening. Holding pee lets germs hang around longer.' + cite(2) + '</p>'
   '<p>Men have a longer urethra, so simple bladder UTIs are less common for them. When a man gets UTI symptoms, I dig deeper.</p>'
   + why('That is also why the "who needs in-person care" stop matters later in this series.')),
 sec('orange', 'next', 'Next stop', 'You will feel it before you see it.',
   '<p>Once those bugs stick and multiply, the bladder wall gets angry. Burn, urgency, and pressure show up.</p>'
   '<p>Next stop, I walk through what a bladder UTI usually feels like — and what is not normal.</p>'),
]

PAGE = dict(
  title='How a UTI Starts: E. coli, Urethra & Adhesins | NPCWoods',
  description='How a UTI starts in plain words: E. coli climbs the short urethra and sticks with adhesins. By NP Chris Woods.',
  about='Urinary tract infection pathogenesis',
  reviewed='2026-10-06', published='2026-10-06',
  pill='UTI Explained · How it starts',
  h1_top='How a UTI', h1_pop='Starts',
  sub='A short pipe, a gut germ, and sticky lock-and-key tips. That is the whole opening scene.',
  sticker1='Short pipe', sticker2='E. coli climb',
  jump_label='Start the story', crumb='How a UTI Starts',
  ghost_svg=ghost_climb(),
  lede='Hey — I\'m Chris. Before we talk meds, let\'s watch how a bladder UTI usually begins. Spoiler: it is a climb, not a mystery.',
  tldr=[
    'Most bladder UTIs start when gut germs climb the urethra.',
    'E. coli is the usual climber.',
    'Adhesins help the germ stick to bladder cells like a lock and key.',
    'A shorter urethra is one reason this is common in many women.',
  ],
  sections=S,
  recap_title='Three pictures. That\'s it.',
  recap=[
    ('Short pipe', 'The urethra is the climb path into the bladder.'),
    ('E. coli', 'A gut germ is the most common climber.'),
    ('Adhesins', 'Sticky tips lock onto bladder cell receptors.'),
    ('Why it sticks', 'Peeing does not always wash a locked-on germ away.'),
  ],
  faq=[
    ('Is every UTI from E. coli?', 'Most uncomplicated bladder UTIs are. Other germs can do it too, but E. coli is the usual one.'),
    ('Does wiping the wrong way cause UTIs?', 'Wiping front to back lowers the chance of dragging gut germs forward. It is one helpful habit, not a guarantee.'),
    ('Can men get this kind of climb?', 'Yes, but it is less common because the urethra is longer. Male UTI symptoms need a careful look.'),
    ('Will cranberry stop the climb?', 'Evidence is mixed. We cover prevention later. Do not count on juice alone once you already burn.'),
  ],
  sources=[SRC['statpearls_cystitis'], SRC['cdc_uti'], SRC['niddk_bladder'], SRC['idsa2011']],
  cta_title='Think you\'re mid-climb? <span>Text me.</span>',
  cta_text='I\'m Chris, a nurse practitioner. Text me what you feel, and I\'ll help sort bladder UTI vs something else.',
  disclaimer=DISCLAIMER,
)
