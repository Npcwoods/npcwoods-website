import math
from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_calendar

F = 'font-family="Inter, Arial, sans-serif"'

def stairs():
    out = []
    for i in range(5):
        x = 30 + i * 84; y = 250 - i * 40; h = 290 - y
        fill = '#f5a524' if i == 0 else '#e8f2fe'
        stroke = '#8a5a00' if i == 0 else '#9fc6f2'
        out.append('<rect x="%d" y="%d" width="84" height="%d" fill="%s" stroke="%s" stroke-width="3"/>' % (x, y, h, fill, stroke))
    return ''.join(out)

D_STAIRS = svg('d-stairs', 'Starting on the first step',
  'A staircase. The first, lowest step is lit up. That is the starter dose. The higher steps are faded. They come later, only when your gut is ready.',
  '0 0 480 320', '''
<rect width="480" height="320" fill="#fff"/>
''' + stairs() + '''
<g transform="translate(52 196)"><path d="M6 0 V34 H40 C44 34 46 40 42 46 H0 V0 Z" fill="#2a2a2a"/><rect x="0" y="46" width="44" height="6" rx="2" fill="#5f5f68"/></g>
<path d="M130 196 C170 130 230 100 300 84" stroke="#0058b0" stroke-width="3" stroke-dasharray="6 7" fill="none"/>
<path d="M290 74 L304 84 L290 94" stroke="#0058b0" stroke-width="3" fill="none"/>
<g ''' + F + ''' font-weight="800" font-size="18" fill="#111114"><text x="20" y="36">You start here:</text><text x="20" y="58">the starter step</text></g>
<g ''' + F + ''' font-weight="600" font-size="16" fill="#3a3a42"><text x="262" y="36">Next steps come later,</text><text x="262" y="56">when your gut is ready</text></g>''')

def tub_levels():
    out = []
    for w in range(1, 5):
        lvl = 1 - math.exp(-w * 0.6)
        y = 296 - 170 * lvl
        right = (w % 2 == 1)
        out.append('<line x1="62" y1="%.0f" x2="400" y2="%.0f" stroke="#0058b0" stroke-width="2" stroke-dasharray="6 6"/>' % (y, y))
        out.append('<text x="%d" y="%.0f" text-anchor="%s" %s font-size="16" font-weight="700" fill="#0058b0">Week %d</text>'
                   % (408 if right else 56, y + 6, 'start' if right else 'end', F, w))
    top = 296 - 170 * (1 - math.exp(-4 * 0.6))
    return out, top

_lv, _top = tub_levels()
D_TUB = svg('d-tub', 'The bathtub: how your level builds up',
  'A tub with a tap and a drain. Each weekly shot adds water. The drain lets some out. The water line rises each week, then holds steady after about a month.',
  '0 0 480 340', '''
<rect width="480" height="340" fill="#fff"/>
<path d="M62 %.0f H400 V280 C400 300 384 310 364 310 H98 C78 310 62 300 62 280 Z" fill="#9fd0ff"/>''' % _top + '''
<path d="M50 110 H412 M62 110 V280 C62 300 78 314 98 314 H364 C384 314 400 300 400 280 V110" fill="none" stroke="#2a2a2a" stroke-width="7" stroke-linecap="round"/>
<path d="M90 110 V40 H150 V60" fill="none" stroke="#5f5f68" stroke-width="10" stroke-linejoin="round"/>
<g fill="#2997ff"><circle cx="150" cy="80" r="6"/><circle cx="150" cy="100" r="5"/></g>
<circle cx="350" cy="314" r="8" fill="#2a2a2a"/>
<path d="M350 322 V334" stroke="#2997ff" stroke-width="4" stroke-linecap="round"/>
''' + ''.join(_lv) + '''
<g ''' + F + ''' font-weight="800" font-size="17" fill="#111114"><text x="164" y="54">Weekly shot fills</text><text x="200" y="334" font-size="16" fill="#3a3a42">Body drains some</text></g>''')

D_SPOTS = svg('d-spots', 'Where the shot can go',
  'A body outline with three shaded areas: the belly, the front of the thighs, and the back of the upper arms. Switch spots each week.',
  '0 0 480 420', '''
<rect width="480" height="420" fill="#fff"/>
<g fill="#eef0f4" stroke="#9a9aa3" stroke-width="3">
<circle cx="240" cy="50" r="30"/>
<path d="M186 92 H294 C310 92 318 104 318 118 V220 H162 V118 C162 104 170 92 186 92 Z"/>
<path d="M162 104 C140 110 128 130 124 160 L114 250 H136 L150 170 L162 140 Z"/>
<path d="M318 104 C340 110 352 130 356 160 L366 250 H344 L330 170 L318 140 Z"/>
<path d="M164 220 H236 L230 404 H192 Z"/><path d="M244 220 H316 L288 404 H250 Z"/>
</g>
<g fill="#2997ff" fill-opacity=".55" stroke="#0058b0" stroke-width="2">
<rect x="184" y="150" width="112" height="56" rx="20"/>
<path d="M176 244 H226 L222 320 H186 Z"/><path d="M254 244 H304 L292 320 H258 Z"/>
<path d="M132 150 L148 152 L142 200 L126 198 Z"/><path d="M348 150 L332 152 L338 200 L354 198 Z"/>
</g>
<circle cx="240" cy="178" r="5" fill="#2a2a2a"/>
<g ''' + F + ''' font-weight="800" font-size="18" fill="#111114">
<text x="20" y="130">Back of</text><text x="20" y="150">upper arm</text>
<text x="370" y="130">Belly</text>
<text x="330" y="300">Front of</text><text x="330" y="320">thigh</text>
</g>
<g stroke="#111114" stroke-width="2"><path d="M100 146 L128 170"/><path d="M366 126 L296 170"/><path d="M326 296 L300 284"/></g>''')


S = [
 sec('cream', 'starter', 'The starter dose', 'Your first dose is a starter.',
   '<p>Think about new boots. You wouldn\'t run a race in them on day one, so you break them in first.</p>'
   '<p>The first dose works the same way. It\'s low on purpose, because its job is to help your gut get used to the medicine. It isn\'t meant to do the heavy lifting.' + cite(2, 4) + '</p>'
   '<p>Most plans stay on the starter dose for 4 weeks. After that, we talk about the next step together.' + cite(1, 2) + '</p>'
   + why('Starting low usually means fewer tummy troubles. Slow and steady really does win here.' + cite(1, 6)),
   fig(D_STAIRS, 'Month one lives on the first step. We only climb when your gut says it\'s ready.')),
 sec('white', 'bathtub', 'The bathtub', 'Your level fills up like a tub.',
   '<p>Picture a bathtub. Each shot pours water into the tub, and your body is the drain that lets some back out.</p>'
   '<p>One shot lasts about a week, so the tub never empties before your next shot. Week by week, the water rises, and in about a month it levels off. That\'s called steady state.' + cite(1, 2) + '</p>'
   + why('Week one may feel different from week four, and that\'s normal. Your tub is still filling up.'),
   fig(D_TUB, 'Each weekly shot adds a bit more than the drain lets out. After about a month, the line holds steady.'), flip=True),
 sec('night', 'shot-day', 'Shot day', 'Pick your shot day.',
   '<ol class="ex-steps">'
   '<li><strong>Pick a day you\'ll remember.</strong> Sunday? Taco Tuesday? It\'s your call, as long as you keep the same day each week.</li>'
   '<li><strong>Pick a spot.</strong> You can use your belly, the front of your thigh, or the back of your upper arm.' + cite(1, 2) + '</li>'
   '<li><strong>Switch spots each week.</strong> The same area is fine, just not the exact same spot.</li>'
   '<li><strong>Any time works.</strong> Morning or night is fine, with or without food.' + cite(1, 2) + '</li>'
   '<li><strong>Missed a dose?</strong> Text me, because the rule is different for each medicine. Don\'t double up.</li></ol>'
   + why('A steady shot day keeps your level steady, and switching spots is kinder to your skin.'),
   fig(D_SPOTS, 'Three spots to pick from. Switch it up each week.')),
 sec('orange', 'week-by-week', 'Week by week', 'What month one often feels like.',
   '<p>Every body is different, but here\'s what I hear a lot.</p>',
   below=grid([
     tile('syringe', 'Week 1', 'Your first shot. Some people feel a bit queasy a day or two later, and some feel nothing. Both are normal.'),
     tile('plate', 'Week 2', 'You may notice you fill up faster, so small plates start to make sense.'),
     tile('cal', 'Week 3', 'Your routine starts to click, and shot day feels like no big deal.'),
     tile('chat', 'Week 4', 'Your tub is close to steady, so we check in. Next step? We decide together.'),
   ]) + why('Month one is about fit, not results. The real question is whether this medicine is a good match for your body.', 'The big idea')),
 sec('white', 'eating', 'Eat to feel good', 'Eat for comfort and muscle.',
   '<p>You may eat less now, so try to make each bite count.</p>',
   below=grid([
     tile('muscle', 'Protein first', 'Eggs, fish, chicken, beans, or Greek yogurt. Eat your protein before the rest of your plate.'),
     tile('plate', 'Small plates', 'Stop when you\'re almost full, because a stuffed stomach and a slow stomach don\'t mix.'),
     tile('glass', 'Sip all day', 'Water keeps your gut moving and keeps your kidneys happy.'),
     tile('leaf', 'Fiber helps', 'Veggies, fruit, and beans help you go. Add them slowly.'),
     tile('alert', 'Go easy on grease', 'Fried food sits in your stomach the longest, so it\'s a top queasy trigger.'),
     tile('heart', 'Move your muscles', 'Do strength moves a few times a week. Squats and wall push-ups count.' + cite(7)),
   ], 'three') + why('When people lose weight, some of it can be muscle. Eating protein and doing strength moves can help you keep more of it.' + cite(7))),
 sec('cream', 'notes', 'Your notes', 'Jot it down. Then text me.',
   '<p>A quick note each day helps us both, so keep it short and simple.</p>'
   '<ul class="ex-steps checks"><li>How your tummy feels</li><li>What you ate when you felt off</li><li>How much water you drank</li>'
   '<li>Bathroom habits</li><li>Your energy and mood</li><li>Shot day and spot</li></ul>'
   '<p style="margin-top:20px">Text me before your first dose step. Together, we\'ll decide if it\'s time or if your gut needs a little longer.</p>'
   + why('Red flags don\'t wait for a text. Learn them on the <a href="https://npcwoods.com/learn/glp1/side-effects/">side effects page</a>.', 'Heads up')),
]

PAGE = dict(
  title='Your First 30 Days on a GLP-1: Week by Week | NPCWoods',
  description='Your first month on a GLP-1 in plain words: the starter dose, shot day, the bathtub level, eating for comfort and muscle, and what to tell me.',
  about='Starting a GLP-1 receptor agonist medicine',
  reviewed='2026-10-06', published='2026-10-06',
  pill='GLP-1 Explained · First 30 days',
  h1_top='Your First', h1_pop='30 Days',
  sub='Month one is a test drive, not a race. Here\'s what it often feels like, week by week.',
  sticker1='New boots <span aria-hidden="true">🥾</span>', sticker2='Same day weekly',
  jump_label='Start the month', crumb='Your First 30 Days',
  ghost_svg=ghost_calendar(),
  lede='Last stop, you learned the honest side effects. Now let\'s walk through month one together, and remember, it\'s a test drive, not a race.',
  tldr=[
    'Your first dose is a starter, and its job is to help your gut get used to it.',
    'Pick one shot day, and keep it the same each week.',
    'Your level builds up over about a month, like a bathtub filling.',
    'Month one is about fit, not results, so tell me how you feel.',
  ],
  sections=S,
  recap_title='Month one, in four pictures.',
  recap=[
    ('New boots', 'The starter dose breaks you in, so it\'s low on purpose.'),
    ('Bathtub', 'Your level fills up over about a month.'),
    ('Shot day', 'Keep the same day each week, and switch spots.'),
    ('Fit first', 'Month one is about fit, not results.'),
  ],
  faq=[
    ('Why don\'t I feel much in week one?', 'The starter dose is low on purpose, and your level is still filling up, like a tub.'),
    ('What if I miss a dose?', 'Text me, because the rule is different for each medicine. Don\'t double up.'),
    ('Can I change my shot day?', 'Often, yes, but you need some space between doses. The rule depends on your medicine, so text me first.'),
    ('Do I take it with food?', 'You don\'t need to. You can take it any time of day, with or without food.'),
  ],
  sources=[SRC['wegovy_dm'], SRC['zepbound_dm'], SRC['wegovy_fda'], SRC['zepbound_fda'], SRC['statpearls_sema'], SRC['statpearls_compare'], SRC['neeland']],
  cta_title='Thinking about starting? <span>Text me.</span>',
  cta_text='I\'m Chris, a nurse practitioner. Text me your health history, and we\'ll see if a GLP-1 may fit you.',
  disclaimer=DISCLAIMER,
)
