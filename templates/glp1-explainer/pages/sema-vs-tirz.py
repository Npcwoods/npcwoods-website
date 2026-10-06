"""Semaglutide vs tirzepatide — one key vs two keys."""
from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_twokeys

F = 'font-family="Inter, Arial, sans-serif"'

D_ONEKEY = svg('d-onekey', 'Semaglutide: one key, one lock',
  'One key labeled GLP-1 fits one lock on a cell. Semaglutide is built to open the GLP-1 lock.',
  '0 0 480 280', '''
<rect width="480" height="280" fill="#fff"/>
<g fill="none" stroke="#2997ff" stroke-width="10" stroke-linecap="round"><circle cx="120" cy="140" r="48"/><path d="M168 140 H340"/><path d="M310 140 V180"/></g>
<rect x="360" y="90" width="70" height="100" rx="18" fill="#e8f2fe" stroke="#0058b0" stroke-width="4"/>
<circle cx="395" cy="130" r="14" fill="#2997ff"/>
<g ''' + F + ''' font-weight="800" font-size="18" fill="#111114"><text x="20" y="40">One key</text><text x="20" y="62">GLP-1 lock</text></g>
<g ''' + F + ''' font-size="15" fill="#3a3a42"><text x="360" y="220">Cell lock</text></g>''')

D_TWOKEYS = svg('d-twokeys', 'Tirzepatide: one key with two cuts',
  'One key with two cuts opens two locks: GLP-1 and GIP. Tirzepatide is built that way.',
  '0 0 480 300', '''
<rect width="480" height="300" fill="#fff"/>
<g fill="none" stroke="#f5a524" stroke-width="10" stroke-linecap="round"><circle cx="110" cy="150" r="48"/><path d="M158 150 H300"/><path d="M270 150 V120"/><path d="M290 150 V190"/></g>
<rect x="330" y="50" width="60" height="90" rx="16" fill="#e8f2fe" stroke="#0058b0" stroke-width="3"/>
<rect x="330" y="160" width="60" height="90" rx="16" fill="#fff4e0" stroke="#8a5a00" stroke-width="3"/>
<g ''' + F + ''' font-weight="800" font-size="17" fill="#111114"><text x="20" y="36">Two cuts</text><text x="20" y="56">GLP-1 + GIP</text></g>
<g ''' + F + ''' font-size="14" fill="#3a3a42"><text x="400" y="100">GLP-1</text><text x="400" y="210">GIP</text></g>''')

S = [
 sec('cream', 'keys', 'One key vs two', 'Same family. Different cuts.',
   '<p>Semaglutide is a GLP-1 key. It fits the GLP-1 lock on your cells.' + cite(1, 5) + '</p>'
   '<p>Tirzepatide is one key with two cuts. It can open the GLP-1 lock and the GIP lock.' + cite(2, 6) + '</p>'
   '<p>Both slow the stomach. Both talk to hunger centers. Tirzepatide adds a second path. That does not mean it is better for every person. It means the tools are different.</p>'
   + why('Think of two house keys. One opens the front door. The other opens the front door and the side door.'),
   fig(D_ONEKEY, 'Semaglutide: one key for the GLP-1 lock.')),
 sec('white', 'brands', 'Brand names you hear', 'Know the labels.',
   '<p>Semaglutide shows up in brands like Ozempic® and Wegovy®. Tirzepatide shows up in brands like Mounjaro® and Zepbound®. Those names belong to their owners. I am not tied to those companies.' + cite(1, 2, 3, 4) + '</p>'
   '<p>Some clinics talk about compounded versions. Compounded drugs are not FDA-approved, and FDA does not check them for safety or quality before they are sold. If we talk about options, I will say that out loud.</p>'
   + why('Brand vs compounded is a safety talk, not a sales talk.')),
 sec('night', 'science', 'At the receptor', 'What the second key adds.',
   '<p>GIP is another gut hormone. Its lock sits on cells too. When tirzepatide turns both locks, the signal mix can feel different.' + cite(6) + '</p>'
   '<p>Both medicines still need a slow dose climb. Side effects can look similar: fullness, nausea, bathroom changes. Your history, not a headline, picks the fit.</p>'
   + why('Receptor science helps you understand the tool. It does not promise a result.'),
   fig(D_TWOKEYS, 'Tirzepatide: one key, two locks — GLP-1 and GIP.'), flip=True),
 sec('orange', 'choose', 'How we choose', 'Fit beats fashion.',
   '<p>I look at your health history, other medicines, past side effects, and what you can access. You tell me your goals and what daily life can handle.</p>',
   below=grid([
     tile('shield', 'Safety first', 'Some histories rule a medicine out. We check that before any key talk.'),
     tile('chat', 'Your feel', 'How you did on a past GLP-1 matters more than a chart on social media.'),
     tile('note', 'Access', 'What your health plan covers, or cash cost, can shape the real choice.'),
     tile('heart', 'No race', 'We pick a starting tool. We can change later if it does not fit.'),
   ]) + why('There is no universal winner. There is a fit for you, or there is not.')),
]

PAGE = dict(
  title='Semaglutide vs Tirzepatide: One Key vs Two | GLP-1 Explained | NPCWoods',
  description='Semaglutide vs tirzepatide in plain words — one GLP-1 key vs two keys (GLP-1 + GIP), brand names, and how Chris Woods helps you choose.',
  about='Comparing semaglutide and tirzepatide',
  reviewed='2026-10-06', published='2026-10-06',
  pill='GLP-1 Explained · Sema vs tirz',
  h1_top='One Key vs', h1_pop='Two Keys',
  sub='Semaglutide opens one lock. Tirzepatide opens two. Here is what that means in plain talk.',
  sticker1='GLP-1 key <span aria-hidden="true">🔑</span>', sticker2='GLP-1 + GIP',
  jump_label='Compare the keys', crumb='Sema vs Tirz',
  ghost_svg=ghost_twokeys(),
  lede='You know why we climb the dose slowly. Next question I get a lot: which medicine — and why do people say one key vs two?',
  tldr=[
    'Semaglutide is a GLP-1 key for one lock.',
    'Tirzepatide is one key with two cuts: GLP-1 and GIP.',
    'Brand names you hear include Ozempic®, Wegovy®, Mounjaro®, and Zepbound®.',
    'We pick based on your history and access — not a social media winner.',
  ],
  sections=S,
  recap_title='One key vs two, in four pictures.',
  recap=[
    ('One key', 'Semaglutide fits the GLP-1 lock.'),
    ('Two cuts', 'Tirzepatide can open GLP-1 and GIP.'),
    ('Brands', 'Know the names — and the compounded caveat.'),
    ('Fit', 'Your history picks the tool, not a headline.'),
  ],
  faq=[
    ('Is tirzepatide always stronger?', 'Not for every person. Different pathways, different fits. We decide from your story.'),
    ('Can I switch from one to the other?', 'Sometimes. Timing and dose matter. Text me before you change anything.'),
    ('Are compounded versions the same?', 'No. Compounded drugs are not FDA-approved. FDA does not check them for safety or quality before they are sold.'),
    ('Do both need a slow dose climb?', 'Yes. Both families start low and step up for safety.'),
  ],
  sources=[SRC['wegovy_dm'], SRC['zepbound_dm'], SRC['wegovy_fda'], SRC['zepbound_fda'], SRC['statpearls_sema'], SRC['statpearls_compare'], SRC['statpearls_glp1']],
  cta_title='Want help picking a fit? <span>Text me.</span>',
  cta_text='I\'m Chris, a nurse practitioner. Text me your health history, and we\'ll see if a GLP-1 may fit you.',
  disclaimer=DISCLAIMER,
)
