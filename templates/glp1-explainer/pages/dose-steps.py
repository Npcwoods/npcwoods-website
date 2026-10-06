"""Dose Steps — why we climb the dose slowly."""
from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_stairs

F = 'font-family="Inter, Arial, sans-serif"'

def climb_stairs():
    out = []
    for i in range(5):
        x = 30 + i * 84; y = 250 - i * 40; h = 290 - y
        fill = '#e8f2fe' if i < 2 else ('#f5a524' if i == 2 else '#eef0f4')
        stroke = '#9fc6f2' if i < 2 else ('#8a5a00' if i == 2 else '#c5c5cc')
        out.append('<rect x="%d" y="%d" width="84" height="%d" fill="%s" stroke="%s" stroke-width="3"/>' % (x, y, h, fill, stroke))
    return ''.join(out)

D_CLIMB = svg('d-climb', 'Climbing one dose step at a time',
  'A staircase. The third step is lit. Lower steps are done. Higher steps are faded. You climb one at a time when your gut is ready.',
  '0 0 480 320', '''
<rect width="480" height="320" fill="#fff"/>
''' + climb_stairs() + '''
<path d="M100 220 C160 160 220 120 300 90" stroke="#0058b0" stroke-width="3" stroke-dasharray="6 7" fill="none"/>
<path d="M290 80 L304 90 L290 100" stroke="#0058b0" stroke-width="3" fill="none"/>
<g ''' + F + ''' font-weight="800" font-size="17" fill="#111114"><text x="20" y="36">You are here:</text><text x="20" y="56">one step at a time</text></g>
<g ''' + F + ''' font-weight="600" font-size="15" fill="#3a3a42"><text x="250" y="36">Higher steps come later,</text><text x="250" y="56">only when you feel ready</text></g>''')

D_LOCKSOFT = svg('d-locksoft', 'Slow key turns at the cell lock',
  'A soft lock on a cell wall. A key turns slowly. Small signal dots spread inside the cell.',
  '0 0 480 300', '''
<rect width="480" height="300" fill="#fff"/>
<rect x="40" y="60" width="200" height="200" rx="24" fill="#eef0f4" stroke="#9a9aa3" stroke-width="3"/>
<circle cx="140" cy="160" r="36" fill="none" stroke="#2997ff" stroke-width="8"/>
<path d="M176 160 H280" stroke="#f5a524" stroke-width="10" stroke-linecap="round"/>
<path d="M260 160 V200" stroke="#f5a524" stroke-width="8" stroke-linecap="round"/>
<g fill="#2997ff" fill-opacity=".45"><circle cx="340" cy="120" r="10"/><circle cx="380" cy="160" r="8"/><circle cx="350" cy="200" r="12"/><circle cx="400" cy="220" r="7"/></g>
<g ''' + F + ''' font-weight="800" font-size="16" fill="#111114"><text x="300" y="50">Signals ease in</text><text x="300" y="70">when we climb slow</text></g>''')

S = [
 sec('cream', 'boots', 'New boots', 'Why we start low.',
   '<p>Think of new hiking boots. You break them in. You do not race in them on day one.</p>'
   '<p>A GLP-1 slows how fast food leaves your stomach. It also talks to hunger centers in your brain. That is a big change. A low starter dose gives your gut time to adapt.' + cite(1, 2) + '</p>'
   + why('Starting low usually means fewer tummy troubles. Fit comes before speed.'),
   fig(D_CLIMB, 'Each dose step is one stair. We climb when your gut says it is ready.')),
 sec('white', 'stairs', 'The stairway', 'About four weeks per step.',
   '<p>Most brand labels use a step plan. You stay on one dose for about four weeks. Then we talk. If you feel okay, we may climb one step. If not, we hold or ease back.' + cite(1, 2, 3, 4) + '</p>'
   '<p>Your blood level builds over time. A weekly shot stacks a little more each week. After about a month on one dose, we see the real picture.</p>'
   + why('I never rush the stairs. A dose you can live with beats a dose that knocks you flat.')),
 sec('night', 'receptor', 'At the lock', 'What changes on the cell.',
   '<p>GLP-1 medicines fit a lock on cells called a receptor. When the key turns, the cell sends signals that slow the stomach and dial down hunger cues.' + cite(5, 6) + '</p>'
   '<p>If we flood that lock too fast, the gut signal can feel loud. You may feel sick. You may feel too full. Bathroom habits may change. A slow climb lets the lock and the gut settle.</p>'
   + why('This is why the labels start low and step up over months.'),
   fig(D_LOCKSOFT, 'Slow key turns mean calmer signals inside the cell.'), flip=True),
 sec('orange', 'feel', 'A step-up day', 'What you might notice.',
   '<p>Some people feel almost nothing at a new step. Others notice more fullness or a few days of queasiness. That often means your system is still adapting.</p>',
   below=grid([
     tile('chat', 'Text me', 'In the first week after a step-up, tell me if food sits heavy or fluids will not stay down.'),
     tile('alert', 'Red flags', 'Cannot keep fluids down, severe belly pain, or chest pain? Seek emergency care. Then tell me.'),
     tile('shield', 'Pause OK', 'If a dose feels like too much, we can hold or step back. That is smart care, not failure.'),
     tile('heart', 'Together', 'Every climb is a conversation. No autopilot.'),
   ]) + why('The goal is a dose that fits your body and your day-to-day life.')),
]

PAGE = dict(
  title='Why We Climb the Dose Slowly | GLP-1 Explained | NPCWoods',
  description='Why GLP-1 dose steps climb slowly, in plain words from Chris Woods, MSN, APRN, FNP-C — gut adapt, receptor signals, and when to pause.',
  about='GLP-1 dose titration and step-up plans',
  reviewed='2026-10-06', published='2026-10-06',
  pill='GLP-1 Explained · Dose steps',
  h1_top='Why We Climb the', h1_pop='Dose Slowly',
  sub='Your gut needs time to adapt. Climbing step by step helps you stay on the path.',
  sticker1='One step at a time <span aria-hidden="true">🪜</span>', sticker2='We decide together',
  jump_label='Why we climb', crumb='Dose Steps',
  ghost_svg=ghost_stairs(),
  lede='Last stop was month one. Now let\'s talk about why every climb after that stays slow on purpose.',
  tldr=[
    'We start low so your gut can adapt.',
    'Each step up is a small climb, not a leap.',
    'Your level builds over weeks, like a bathtub filling.',
    'If a step feels rough, we can pause or step back.',
  ],
  sections=S,
  recap_title='Dose steps, in four pictures.',
  recap=[
    ('New boots', 'Start low so your gut can break in.'),
    ('Stairs', 'Climb about once a month if you feel okay.'),
    ('The lock', 'Slow change at the receptor keeps signals calmer.'),
    ('Pause OK', 'Holding or stepping back is smart care.'),
  ],
  faq=[
    ('How long do I stay on each dose?', 'Often about four weeks, then we check in. Some people stay longer on a step that fits.'),
    ('What if I feel fine and want to jump ahead?', 'We still climb one step at a time. Jumping ahead raises the chance of hard side effects.'),
    ('Do higher doses always work better?', 'Not always. The right dose is the one that fits your body and your day-to-day life.'),
    ('Can we go back down?', 'Yes. Stepping down is a normal option if a dose feels too strong.'),
  ],
  sources=[SRC['wegovy_dm'], SRC['zepbound_dm'], SRC['wegovy_fda'], SRC['zepbound_fda'], SRC['statpearls_sema'], SRC['statpearls_glp1'], SRC['neeland']],
  cta_title='Ready to talk dose steps? <span>Text me.</span>',
  cta_text='I\'m Chris, a nurse practitioner. Text me your health history, and we\'ll see if a GLP-1 may fit you.',
  disclaimer=DISCLAIMER,
)
