from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_waves

F = 'font-family="Inter, Arial, sans-serif"'

def stomach(x, y, s, bits):
    b = ''.join('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (bx, by, r, c) for bx, by, r, c in bits)
    return ('<g transform="translate(%d %d) scale(%.2f)"><path d="M48 0 V40 C48 60 10 70 10 120 C10 170 60 196 110 192 C160 188 186 160 184 128 '
            'C182 104 170 94 150 92 C120 88 96 70 84 40 V0" fill="#ffd9d2" stroke="#e05a4f" stroke-width="5"/>%s'
            '<path d="M184 128 H226" stroke="#e05a4f" stroke-width="14" stroke-linecap="round"/>'
            '<rect x="196" y="62" width="22" height="50" rx="7" fill="#2a2a2a"/><circle cx="207" cy="76" r="5" fill="#5a2a2a"/>'
            '<circle cx="207" cy="90" r="6" fill="#f5a524"/><circle cx="207" cy="103" r="5" fill="#1f3d2c"/></g>') % (x, y, s, b)

BIG = [(40,118,9,'#19a463'),(62,140,10,'#f5a524'),(86,118,9,'#c0392b'),(110,140,10,'#19a463'),(134,122,9,'#f5a524'),(58,162,9,'#c0392b'),
       (84,168,10,'#f5a524'),(110,166,9,'#19a463'),(136,160,10,'#c0392b'),(158,140,9,'#f5a524'),(40,96,8,'#f5a524'),(64,96,9,'#19a463'),(160,120,8,'#19a463'),(120,98,8,'#c0392b')]
SMALL = [(70,150,9,'#19a463'),(104,160,9,'#f5a524'),(130,146,8,'#c0392b')]

D_JAM = svg('d-jam', 'Big plate versus small plate at the yellow light',
  'Left: a stomach packed with a big meal while the exit is on a yellow light. It backs up and feels queasy. Right: a small meal fits and moves along smoothly.',
  '0 0 480 330', '''
<rect width="480" height="330" fill="#fff"/>
''' + stomach(4, 40, 0.98, BIG) + stomach(244, 40, 0.98, SMALL) + '''
<g ''' + F + ''' font-weight="800" font-size="19" fill="#111114"><text x="20" y="28">Big plate</text><text x="260" y="28">Small plate</text></g>
<g ''' + F + ''' font-weight="800" font-size="18"><text x="20" y="314" fill="#c62828">Backs up. Queasy.</text><text x="260" y="314" fill="#148a53">Fits. Moves along.</text></g>
<line x1="240" y1="20" x2="240" y2="320" stroke="#e5e5ea" stroke-width="2"/>''')

def wave_path():
    import math
    pts = []
    starts = [40, 190, 340]
    for i in range(0, 441, 4):
        x = 30 + i
        y = 0
        for k, s in enumerate(starts):
            if x >= s:
                t = (x - s) / 34.0
                y = max(y, (1.0 - 0.18 * k) * math.exp(-t * 0.55) * (1 - math.exp(-t * 3)))
        pts.append('%d,%.1f' % (x, 200 - 150 * y))
    return ' '.join(pts)

D_WAVES = svg('d-waves', 'When tummy side effects tend to show up',
  'A line rises after the first dose, then eases. It rises a bit again after each dose step, then eases again.',
  '0 0 480 280', '''
<rect width="480" height="280" fill="#fff"/>
<line x1="30" y1="200" x2="470" y2="200" stroke="#2a2a2a" stroke-width="3"/>
<line x1="30" y1="40" x2="30" y2="200" stroke="#2a2a2a" stroke-width="3"/>
<polyline points="''' + wave_path() + '''" fill="none" stroke="#0071e3" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>
<g stroke="#f5a524" stroke-width="3" stroke-dasharray="5 6"><line x1="40" y1="40" x2="40" y2="200"/><line x1="190" y1="40" x2="190" y2="200"/><line x1="340" y1="40" x2="340" y2="200"/></g>
<g ''' + F + ''' font-weight="800" font-size="17" fill="#111114"><text x="40" y="228" text-anchor="middle">Start</text><text x="190" y="228" text-anchor="middle">Dose step</text><text x="340" y="228" text-anchor="middle">Dose step</text></g>
<g ''' + F + ''' font-weight="600" font-size="16" fill="#5f5f68"><text x="44" y="30">Tummy effects</text><text x="470" y="262" text-anchor="end">Time</text></g>''')

D_THYROID = svg('d-thyroid', 'Where the thyroid sits',
  'The thyroid is a butterfly-shaped gland at the front of the neck, below the voice box. C-cells sit inside it.',
  '0 0 480 330', '''
<rect width="480" height="330" fill="#fff"/>
<path d="M150 0 C150 80 120 120 70 160 C40 184 30 240 30 330 H450 C450 240 440 184 410 160 C360 120 330 80 330 0" fill="#fbe3d4" stroke="#e7a77c" stroke-width="4"/>
<rect x="214" y="40" width="52" height="250" rx="22" fill="#f6cdb3" stroke="#e7a77c" stroke-width="3"/>
<g stroke="#e7a77c" stroke-width="3">''' + ''.join('<line x1="218" y1="%d" x2="262" y2="%d"/>' % (y, y) for y in range(130, 290, 22)) + '''</g>
<path d="M240 168 C222 140 168 132 160 170 C152 210 182 238 214 226 C230 220 236 200 240 196 C244 200 250 220 266 226 C298 238 328 210 320 170 C312 132 258 140 240 168 Z" fill="#f5a524" stroke="#8a5a00" stroke-width="4"/>
<g fill="#8a5a00"><circle cx="186" cy="176" r="5"/><circle cx="200" cy="200" r="5"/><circle cx="292" cy="176" r="5"/><circle cx="280" cy="202" r="5"/><circle cx="178" cy="200" r="4"/><circle cx="302" cy="198" r="4"/></g>
<path d="M326 186 C360 186 372 150 392 140" stroke="#111114" stroke-width="3" fill="none"/>
<g ''' + F + ''' font-weight="800" font-size="19" fill="#111114"><text x="330" y="112">Thyroid</text><text x="330" y="134" font-size="16" font-weight="600" fill="#3a3a42">dots = C-cells</text></g>
<text x="240" y="70" text-anchor="middle" ''' + F + ''' font-size="16" font-weight="700" fill="#5f5f68">Voice box</text>''')


S = [
 sec('cream', 'why', 'Why it happens', 'Why your tummy talks back.',
   '<p>Remember the yellow light? Food sits in your stomach longer than it used to. Add a big meal on top, and it\'s like rush hour at a yellow light. Traffic backs up, and hello, queasy.' + cite(1, 5) + '</p>'
   '<p>Your gut also needs time to get used to a brand-new signal, which is why I start low and go slow.' + cite(1, 2) + '</p>'
   + why('Most side effects live in your tummy. They\'re most common at the start and after a dose step, and for many people they ease with time.' + cite(1, 2)),
   fig(D_JAM, 'Same yellow light, two plates. A small plate fits through. A big one backs up.')),
 sec('white', 'common', 'The common list', 'What lots of people feel.',
   '<p>Here are the ones I hear about most. You may get none of them, or you may get a few.' + cite(1, 2) + '</p>',
   fig(D_WAVES, 'Tummy effects often rise at the start and after each dose step. Then they tend to ease. Everyone is different.'), flip=True,
   below=grid([
     tile('stomach', 'Most common', 'Feeling sick to your stomach, loose stools, getting backed up, and throwing up.'),
     tile('alert', 'Also common', 'Belly pain, heartburn or burping, feeling tired, headaches, and feeling dizzy.'),
     tile('syringe', 'At the shot spot', 'Some redness or itching, which often fades in a day or two.'),
   ], 'three')),
 sec('night', 'helps', 'What helps', 'Small moves. Big relief.',
   '<p>These tips come straight from how the medicine works. If your stomach is slower, give it less work to do.' + cite(1, 2) + '</p>',
   below=grid([
     tile('plate', 'Eat small', 'Use a smaller plate, and stop when you\'re almost full instead of stuffed.'),
     tile('clock', 'Slow down', 'Put your fork down between bites, because your brain needs a minute to catch up.'),
     tile('alert', 'Go easy on grease', 'Fried and fatty foods sit the longest, so they\'re a top queasy trigger.'),
     tile('glass', 'Sip all day', 'Water helps your gut and protects your kidneys, and small sips count.'),
     tile('leaf', 'Fiber plus water', 'If you\'re backed up, add veggies, fruit, and beans, then drink a little more.'),
     tile('bed', 'Stay upright', 'Wait a while after eating before you lie down.'),
     tile('drop', 'Bland when queasy', 'Crackers, toast, rice, and broth are boring, but boring is your friend.'),
     tile('chat', 'Text me early', 'Still feeling rough before a dose step? Tell me, because we can slow down.'),
   ])),
 sec('white', 'red-flags', 'Rare, but real', 'Know these red flags.',
   '<p>These are not common, but if one shows up, act fast. For most of them, that means the ER or 911.' + cite(1, 2, 3, 4) + '</p>',
   below=grid([
     tile('alert', 'Bad belly pain', 'Strong pain that won\'t quit and may spread to your back, with or without throwing up. This can be your pancreas.', 'red'),
     tile('alert', 'Upper right belly pain', 'Pain under your right ribs, a fever, or yellow skin or eyes. This can be your gallbladder.', 'red'),
     tile('drop', 'Can\'t keep fluids down', 'Very little pee, dark pee, or feeling dizzy when you stand. Losing too much fluid can hurt your kidneys.', 'red'),
     tile('heart', 'Allergic reaction', 'A swollen face, lips, tongue, or throat, trouble breathing, or a fast, bad rash.', 'red'),
     tile('drop', 'Low blood sugar', 'Feeling shaky, sweaty, or confused, or a racing heart. Eat or drink some sugar right away. The risk is higher with insulin or a sulfonylurea.', 'red'),
     tile('chat', 'Dark thoughts', 'New mood changes or thoughts of hurting yourself. Call or text 988 any time, day or night.', 'red'),
   ], 'three') + why('Before any surgery or sedation, tell the care team you take a GLP-1. Food can still be sitting in a slow stomach, which raises the risk of breathing it into your lungs.' + cite(3, 4), 'Surgery coming up?')),
 sec('orange', 'label-rules', 'Two label rules', 'The fine print, made plain.',
   '<h3>The boxed warning</h3>'
   '<p>In studies with rats and mice, these medicines caused thyroid C-cell tumors. We don\'t know if this happens in people.' + cite(3, 4) + '</p>'
   '<p>Don\'t take one if you or anyone in your family has had medullary thyroid cancer (MTC), or if you have a condition called MEN 2. Tell me about a lump in your neck, trouble swallowing, or a hoarse voice that won\'t go away.</p>'
   '<h3>Pregnancy and birth control</h3>'
   '<p>Planning a baby? With Wegovy®, stop at least 2 months before you start trying.' + cite(3) + ' Zepbound® can make birth control pills work less well, so add a backup like condoms for 4 weeks after you start. Then do it again for 4 weeks after each dose step.' + cite(4) + '</p>'
   '<p>If you get pregnant, text me right away.</p>',
   fig(D_THYROID, 'Your thyroid sits low in the front of your neck. The boxed warning is about its C-cells.'), flip=True),
 sec('blue', 'text-or-er', 'Who to call', 'Text me, or go to the ER?',
   '<p>Here\'s my simple rule. If it\'s annoying, text me. If it\'s scary, get help right now.</p>',
   below='<div class="ex-vs"><div class="txt"><h3>Text me</h3><ul><li>Queasy that won\'t ease</li><li>Backed up for more than a few days</li>'
   '<li>Can\'t eat much at all</li><li>Missed a dose</li><li>Planning a baby or surgery</li><li>New medicine from someone else</li></ul></div>'
   '<div class="er"><h3>ER or 911</h3><ul><li>Bad belly pain that won\'t quit</li><li>Can\'t keep any fluids down</li><li>Swelling of face or throat, or hard to breathe</li>'
   '<li>Fainting or chest pain</li><li>Thoughts of hurting yourself (or call or text 988)</li></ul></div></div>'),
]

PAGE = dict(
  title='GLP-1 Side Effects, Honestly: What Helps & Red Flags | NPCWoods',
  description='GLP-1 side effects in plain words: why the tummy talks back, what helps, red flags, the boxed warning, and when to text vs go to the ER.',
  about='Side effects of GLP-1 receptor agonist medicines',
  reviewed='2026-10-06', published='2026-10-01',
  pill='GLP-1 Explained · Side effects',
  h1_top='Side Effects,', h1_pop='Honestly',
  sub='Why your tummy talks back, what helps, and the rare signs that mean act now.',
  sticker1='Real talk <span aria-hidden="true">💬</span>', sticker2='What helps',
  jump_label='Start reading', crumb='Side Effects, Honestly',
  ghost_svg=ghost_waves(),
  lede='Last stop, your stomach got a yellow light. That one change explains most side effects, so here\'s the honest list and what to do about it.',
  tldr=[
    'Most side effects live in your tummy: queasy, loose, or backed up.',
    'They show up most at the start and after a dose step, then often ease.',
    'Small meals, slow bites, less grease, and plenty of water help a lot.',
    'A few rare signs mean you should act now, so learn them below.',
  ],
  sections=S,
  recap_title='The whole page in four cards.',
  recap=[
    ('Why', 'A slow stomach plus a big meal equals a traffic jam.'),
    ('When', 'Most often at the start and after each dose step.'),
    ('What helps', 'Eat small, eat slow, skip the grease, and sip water.'),
    ('Act now', 'Bad belly pain, no fluids staying down, or allergy signs mean the ER.'),
  ],
  faq=[
    ('Will feeling sick last forever?', 'For many people, it eases after the first few weeks. It can come back a little after a dose step, so tell me if it doesn\'t ease.'),
    ('Can I take something for nausea?', 'Text me first, and I\'ll check your other medicines to see what makes sense for you.'),
    ('Why tell my surgery team?', 'Your stomach empties more slowly, so food may still be there during sedation. That raises the risk of breathing it into your lungs.'),
    ('Is getting backed up normal?', 'It\'s common. Water, fiber, and moving your body all help. Text me if it lasts more than a few days or you have bad pain.'),
  ],
  sources=[SRC['wegovy_dm'], SRC['zepbound_dm'], SRC['wegovy_fda'], SRC['zepbound_fda'], SRC['statpearls_glp1'], SRC['statpearls_sema']],
  cta_title='Worried about a symptom? <span>Text me.</span>',
  cta_text='I\'m Chris, a nurse practitioner. Tell me what you\'re feeling, and I\'ll help you sort out what\'s normal and what\'s not.',
  disclaimer=DISCLAIMER,
)
