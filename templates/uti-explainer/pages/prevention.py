from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_shield

F = 'font-family="Inter, Arial, sans-serif"'

D_SHIELD = svg('d-prev', 'Prevention habits with uneven evidence',
  'Pee after sex, do not hold urine forever, wipe front to back, and be skeptical of cranberry as a cure-all.',
  '0 0 480 340',
  '<rect width="480" height="340" fill="#fff"/>'
  '<rect x="30" y="40" width="130" height="110" rx="16" fill="#eaf8f0"/><text x="95" y="90" text-anchor="middle" ' + F + ' font-size="15" font-weight="800">Pee after</text><text x="95" y="112" text-anchor="middle" ' + F + ' font-size="15" font-weight="800">sex</text>'
  '<rect x="175" y="40" width="130" height="110" rx="16" fill="#e8f2fe"/><text x="240" y="90" text-anchor="middle" ' + F + ' font-size="15" font-weight="800">Don\'t hold</text><text x="240" y="112" text-anchor="middle" ' + F + ' font-size="15" font-weight="800">pee forever</text>'
  '<rect x="320" y="40" width="130" height="110" rx="16" fill="#fff7e8"/><text x="385" y="90" text-anchor="middle" ' + F + ' font-size="15" font-weight="800">Front to</text><text x="385" y="112" text-anchor="middle" ' + F + ' font-size="15" font-weight="800">back</text>'
  '<rect x="90" y="190" width="300" height="100" rx="16" fill="#fdecea"/><text x="240" y="235" text-anchor="middle" ' + F + ' font-size="17" font-weight="800">Cranberry ≠ cure-all</text><text x="240" y="262" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">evidence is mixed; not a treatment</text>')

S = [
 sec('cream', 'honest', 'Prevention without folklore', 'Some habits help. Some are juice myths.',
   '<p>You cannot wrap your urethra in bubble wrap. You can lower the odds.' + cite(1, 2) + '</p>'
   '<p>I care more about boring habits that make sense than about miracle bottles at checkout.</p>',
   fig(D_SHIELD, 'Practical habits first. Marketing later.')),
 sec('white', 'habits', 'Habits that make sense', 'Flush, do not incubate.',
   '<p>Pee after sex to flush germs that got nudged forward. Do not hold pee for trophy lengths of time. Wipe front to back. Stay decently hydrated.' + cite(2) + '</p>'
   '<p>Skip harsh soaps and douches on the urethra neighborhood. Irritation is not cleanliness.</p>'
   + why('These are low-cost moves. They are not a promise you will never get another UTI.')),
 sec('orange', 'cranberry', 'Cranberry, honestly', 'A maybe for prevention. Not a treatment.',
   '<p>Cranberry products have mixed proof for prevention in some groups. They are not a treatment once you already have a bacterial UTI.' + cite(1, 3) + '</p>'
   '<p>If you like a standardized product and it does not upset your stomach or mess with your warfarin, fine. Do not chug sugar soda "cranberry cocktails" and call it medicine.</p>'),
 sec('night', 'more', 'When prevention gets medical', 'Recurrent patterns may need more than tips.',
   '<p>For frequent loops, we sometimes talk post-sex antibiotics, vaginal estrogen in menopause, or other tailored plans — usually after a fuller look.' + cite(1) + '</p>'
   '<p>That is specialized territory. It is not the default first text visit for everyone.</p>',
   below=grid([
     tile('check', 'Do', 'Pee after sex, hydrate, gentle hygiene.'),
     tile('ban', 'Don\'t', 'Treat an active UTI with juice alone.'),
     tile('leaf', 'Cranberry', 'Mixed prevention data; not a cure.'),
     tile('chat', 'Recurrent', 'Ask about tailored plans if you loop.'),
   ])),
]

PAGE = dict(
  title='UTI Prevention That Isn\'t Folklore | NPCWoods',
  description='UTI prevention in plain words: habits that help, cranberry evidence vs myth, and when you need more than tips. By NP Chris Woods.',
  about='Prevention of urinary tract infections',
  reviewed='2026-10-06', published='2026-10-06',
  pill='UTI Explained · Prevention',
  h1_top='Prevention That Isn\'t', h1_pop='Folklore',
  sub='Flush habits beat juice legends. Here is the honest version.',
  sticker1='Pee after sex', sticker2='Skip myths',
  jump_label='See what helps', crumb='Prevention',
  ghost_svg=ghost_shield(),
  lede='You know the loop. Now the shield — without pretending cranberry is a superhero cape.',
  tldr=[
    'Pee after sex and do not hold urine forever.',
    'Gentle hygiene beats harsh "cleansing."',
    'Cranberry evidence is mixed; it is not a treatment.',
    'Frequent recurrences may need tailored medical plans.',
  ],
  sections=S,
  recap_title='Shield notes.',
  recap=[
    ('Flush', 'After sex and on a normal schedule.'),
    ('Be gentle', 'No harsh urethra chemistry.'),
    ('Cranberry', 'Maybe prevent; never cure.'),
    ('Escalate plan', 'Loops may need more than tips.'),
  ],
  faq=[
    ('Does drinking gallons of water fix a UTI?', 'Fluids help comfort and flushing. They do not replace antibiotics for true bacterial cystitis.'),
    ('Are probiotics proven?', 'Evidence is mixed and product-specific. I do not sell miracle capsules here.'),
    ('Should I avoid sex forever?', 'No. Timing, peeing afterward, and lubricants that do not irritate are more realistic talks.'),
    ('Do vitamins prevent UTIs?', 'No vitamin is a proven UTI vaccine. Be wary of big claims.'),
  ],
  sources=[SRC['statpearls_recur'], SRC['niddk_bladder'], SRC['cdc_uti'], SRC['idsa2011']],
  cta_title='Want a prevention plan? <span>Text me.</span>',
  cta_text='Tell me how often this happens. We will keep what helps and drop the folklore.',
  disclaimer=DISCLAIMER,
)
