"""Who shouldn't take a GLP-1."""
from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_stop

F = 'font-family="Inter, Arial, sans-serif"'

D_THYROID = svg('d-thyroid2', 'Where the thyroid sits',
  'A simple neck outline. The thyroid sits low in the front of the neck, like a bow tie over the windpipe.',
  '0 0 480 300', '''
<rect width="480" height="300" fill="#fff"/>
<ellipse cx="240" cy="70" rx="50" ry="58" fill="#eef0f4" stroke="#9a9aa3" stroke-width="3"/>
<path d="M190 120 H290 C310 120 320 140 320 170 V240 H160 V170 C160 140 170 120 190 120 Z" fill="#eef0f4" stroke="#9a9aa3" stroke-width="3"/>
<path d="M200 150 C220 140 260 140 280 150 C270 175 250 185 240 185 C230 185 210 175 200 150 Z" fill="#ffb4b4" stroke="#c44" stroke-width="3"/>
<g ''' + F + ''' font-weight="800" font-size="17" fill="#111114"><text x="20" y="40">Thyroid</text><text x="20" y="60">low in the neck</text></g>
<path d="M300 160 L360 140" stroke="#111114" stroke-width="2"/><text x="365" y="145" ''' + F + ''' font-size="15" fill="#3a3a42">C-cells matter</text>''')

S = [
 sec('cream', 'clear', 'Clear stops', 'Some histories mean no.',
   '<p>I am Chris Woods, a nurse practitioner. Part of my job is saying no.</p>'
   '<p>Brand labels list hard stops. One is a personal or family history of medullary thyroid cancer (MTC). Another is MEN2, a rare hormone syndrome.' + cite(1, 2, 3, 4) + '</p>'
   + why('These are label rules, not vibes. If this is your history, we pick another path.'),
   fig(D_THYROID, 'The boxed warning is about C-cells in the thyroid. Tell me your family history.')),
 sec('white', 'pregnancy', 'Pregnancy and planning', 'Not for pregnancy.',
   '<p>These medicines are not for pregnancy. If you could get pregnant, we plan timing. We also plan when to stop before you try to conceive. We follow the label for your medicine.' + cite(1, 2) + '</p>'
   '<p>Breastfeeding has its own rules. Tell me if you nurse or plan to.</p>'
   + why('Growing a baby and changing gut hormones do not mix. We plan ahead.')),
 sec('night', 'caution', 'Extra caution lists', 'We dig deeper here.',
   '<p>Past pancreatitis needs a careful look. So does serious gallbladder disease. So does a stomach that already empties very slowly (gastroparesis). Eye and kidney history can matter too.' + cite(1, 2, 5) + '</p>'
   '<p>Other medicines matter. Ones that change blood sugar or stomach speed need a close look.</p>',
   below=grid([
     tile('alert', 'Pancreatitis history', 'Tell me about severe belly pain episodes in the past.'),
     tile('stomach', 'Slow stomach already', 'If food already sits for hours, stacking more slow may not fit.'),
     tile('drop', 'Blood sugar meds', 'We watch lows if you also use insulin or similar tools.'),
     tile('shield', 'Allergies', 'A past serious reaction to the same medicine class matters.'),
   ]) + why('Caution is not always a hard no. But it is never a shrug.')),
 sec('orange', 'honest', 'How I screen', 'Your story first.',
   '<p>Before we talk about a prescription, I ask about thyroid family history. I ask about pregnancy plans. I ask about pancreas and gallbladder history. I ask about other medicines. I ask what you hope for.</p>'
   '<p>A consult does not guarantee a prescription. If you are not a fit, I will say so. Then we talk about next steps.</p>'
   + why('Saying no is part of good care. I would rather keep you safe than rush a refill.')),
]

PAGE = dict(
  title="Who Shouldn't Take a GLP-1 | GLP-1 Explained | NPCWoods",
  description='Clear "not for you" situations for GLP-1 medicines — MTC/MEN2, pregnancy, pancreatitis and more — explained plainly by Chris Woods, MSN, APRN, FNP-C.',
  about='Contraindications and cautions for GLP-1 medicines',
  reviewed='2026-10-06', published='2026-10-06',
  pill="GLP-1 Explained · Who shouldn't",
  h1_top="Who Shouldn't", h1_pop='Take One',
  sub='Clear stop signs from the labels — and how I screen before we talk about a prescription.',
  sticker1='Safety first <span aria-hidden="true">🛑</span>', sticker2='History matters',
  jump_label='See the stops', crumb="Who Shouldn't",
  ghost_svg=ghost_stop(),
  lede='Eating tips help when a GLP-1 fits. First we make sure it is even on the table for you.',
  tldr=[
    'Personal or family MTC history, or MEN2, means these medicines are not for you.',
    'They are not for pregnancy — we plan timing if you could conceive.',
    'Pancreatitis, gallbladder, and severe gastroparesis need a careful look.',
    'A consult does not guarantee a prescription.',
  ],
  sections=S,
  recap_title='Who should not, in four pictures.',
  recap=[
    ('Hard stops', 'MTC and MEN2 history rule these out.'),
    ('Pregnancy', 'Not for pregnancy — plan ahead.'),
    ('Caution list', 'Pancreas, gallbladder, slow stomach, other meds.'),
    ('Honest screen', 'I may say no. That is care, not rejection.'),
  ],
  faq=[
    ('I had a thyroid nodule. Is that an automatic no?', 'Not always. MTC and MEN2 are the hard label stops. Bring your records so we can sort the type.'),
    ('Can I start if I might want a baby next year?', 'We plan timing and when to stop before trying. Tell me your timeline early.'),
    ('What if I had pancreatitis years ago?', 'It is a major caution. We may choose a different path. Do not hide it.'),
    ('Does a consult mean I get a prescription?', 'No. A consult is a fit check. A prescription only happens if it is safe and appropriate.'),
  ],
  sources=[SRC['wegovy_dm'], SRC['zepbound_dm'], SRC['wegovy_fda'], SRC['zepbound_fda'], SRC['statpearls_glp1'], SRC['statpearls_sema']],
  cta_title='Not sure if you are a fit? <span>Text me.</span>',
  cta_text='I\'m Chris, a nurse practitioner. Text me your health history, and we\'ll see if a GLP-1 may fit you.',
  disclaimer=DISCLAIMER,
)
