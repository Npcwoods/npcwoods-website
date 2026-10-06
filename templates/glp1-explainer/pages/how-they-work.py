from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_doorbell

F = 'font-family="Inter, Arial, sans-serif"'

D_DOORBELL = svg('d-bell', 'The GLP-1 doorbell',
  'Food moves through the small gut. L-cells in the gut wall release GLP-1 into the blood. The blood carries it to the brain, stomach, and pancreas.',
  '0 0 480 400', '''
<rect x="0" y="0" width="480" height="400" fill="#fff"/>
<path d="M24 300 C70 250 110 350 160 300 S240 250 262 300" fill="none" stroke="#f2c9a8" stroke-width="44" stroke-linecap="round"/>
<path d="M24 300 C70 250 110 350 160 300 S240 250 262 300" fill="none" stroke="#e7a77c" stroke-width="2" stroke-dasharray="4 6"/>
<circle cx="52" cy="290" r="7" fill="#19a463"/><circle cx="96" cy="306" r="6" fill="#f5a524"/><circle cx="140" cy="312" r="7" fill="#c0392b"/><circle cx="196" cy="286" r="6" fill="#19a463"/>
<g fill="#f5a524" stroke="#8a5a00" stroke-width="2"><circle cx="118" cy="333" r="11"/><circle cx="178" cy="275" r="11"/><circle cx="236" cy="278" r="11"/></g>
<g fill="#2997ff"><circle cx="190" cy="248" r="6"/><circle cx="214" cy="222" r="6"/><circle cx="250" cy="246" r="6"/><circle cx="268" cy="214" r="6"/><circle cx="296" cy="180" r="6"/><circle cx="300" cy="120" r="6"/><circle cx="300" cy="300" r="6"/></g>
<line x1="300" y1="60" x2="300" y2="340" stroke="#e05a4f" stroke-width="10" stroke-linecap="round"/>
<g stroke="#e05a4f" stroke-width="5" stroke-linecap="round" fill="none"><path d="M300 76 H340"/><path d="M300 192 H340"/><path d="M300 308 H340"/></g>
<g ''' + F + ''' font-weight="800" font-size="19" fill="#111114">
<rect x="340" y="56" width="124" height="40" rx="20" fill="#e8f2fe"/><text x="402" y="82" text-anchor="middle">Brain</text>
<rect x="340" y="172" width="124" height="40" rx="20" fill="#e8f2fe"/><text x="402" y="198" text-anchor="middle">Stomach</text>
<rect x="340" y="288" width="124" height="40" rx="20" fill="#e8f2fe"/><text x="402" y="314" text-anchor="middle">Pancreas</text>
</g>
<g ''' + F + ''' font-size="17" fill="#3a3a42" font-weight="600">
<text x="20" y="236">Food in the</text><text x="20" y="256">small gut</text>
<text x="40" y="380">L-cells ring the bell</text>
<text x="180" y="40">GLP-1 rides</text><text x="180" y="60">the blood</text>
</g>''')

D_LOCK = svg('d-lock', 'Lock and key on a cell',
  'GLP-1, the key, fits the GLP-1 receptor, the lock, which sits in the cell wall. Inside the cell, a G protein turns on cAMP, which spreads the message.',
  '0 0 480 420', '''
<rect width="480" height="420" fill="#fff"/>
<g ''' + F + ''' font-size="16" font-weight="700" fill="#5f5f68"><text x="16" y="28">OUTSIDE THE CELL</text><text x="16" y="404">INSIDE THE CELL</text></g>
<rect x="0" y="206" width="480" height="44" fill="#fdf1e4"/>
<g fill="#f2c9a8">''' + ''.join('<circle cx="%d" cy="206" r="7"/><circle cx="%d" cy="250" r="7"/>' % (x, x) for x in range(8, 480, 18)) + '''</g>
<path d="M150 130 C150 92 250 92 250 130 L250 150 L232 150 L232 136 L212 136 L212 150 L150 150 Z" fill="#0071e3"/>
<path d="M170 150 V300 C170 316 188 316 188 300 V170 C188 156 206 156 206 170 V300 C206 316 224 316 224 300 V170 C224 156 242 156 242 170 V300" fill="none" stroke="#0071e3" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
<g transform="translate(300 60) rotate(28)"><circle cx="0" cy="0" r="24" fill="none" stroke="#f5a524" stroke-width="12"/><path d="M0 24 V96 M0 70 H14 M0 86 H12" stroke="#f5a524" stroke-width="12" stroke-linecap="round" fill="none"/></g>
<path d="M262 132 L240 142" stroke="#8a5a00" stroke-width="3" stroke-dasharray="4 4"/>
<ellipse cx="320" cy="320" rx="46" ry="30" fill="#7fdcaa"/>
<path d="M246 300 C270 300 280 312 290 314" stroke="#148a53" stroke-width="4" fill="none"/>
<g stroke="#f5a524" stroke-width="5" stroke-linecap="round"><path d="M400 300 l16 -12"/><path d="M404 324 h22"/><path d="M398 346 l16 12"/><path d="M380 286 l4 -18"/><path d="M380 358 l4 18"/></g>
<circle cx="386" cy="322" r="18" fill="#f5a524"/>
<g ''' + F + ''' font-weight="800" fill="#111114" font-size="18">
<text x="330" y="40">Key: GLP-1</text>
<text x="20" y="96">Lock:</text><text x="20" y="118">GLP-1 receptor</text>
<text x="290" y="326" text-anchor="middle" font-size="15">G protein</text>
<text x="352" y="392" font-size="17">cAMP: the</text><text x="352" y="412" font-size="17">group text</text>
</g>''')

def beads(y, special=None, gap_after=None):
    out = []; x = 60
    for i in range(9):
        if gap_after is not None and i == gap_after + 1: x += 30
        fill = '#f5a524' if i == special else '#2997ff'
        out.append('<circle cx="%d" cy="%d" r="12" fill="%s"/>' % (x, y, fill))
        if i < 8 and not (gap_after is not None and i == gap_after):
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#0058b0" stroke-width="3"/>' % (x + 12, y, x + 16, y))
        x += 28
    return ''.join(out)

D_BOUNCER = svg('d-bouncer', 'The DPP-4 bouncer',
  'Top: DPP-4 snips your own GLP-1 near the front of the chain, so it is gone in about two minutes. Bottom: the medicine has a swapped link the bouncer cannot grab, plus a fatty tail that rides on albumin, so it lasts about a week.',
  '0 0 480 420', '''
<rect width="480" height="420" fill="#fff"/>
<g ''' + F + ''' font-weight="800" fill="#111114" font-size="19"><text x="20" y="36">Your own GLP-1</text><text x="20" y="190">The medicine</text></g>
''' + beads(86, gap_after=1) + '''
<path d="M114 64 l8 10 l-8 10 l8 10 l-8 10" stroke="#c62828" stroke-width="4" fill="none"/>
<circle cx="118" cy="140" r="22" fill="#2a2a2a"/><text x="118" y="146" text-anchor="middle" ''' + F + ''' font-size="13" font-weight="800" fill="#fff">DPP-4</text>
<text x="150" y="146" ''' + F + ''' font-size="17" font-weight="600" fill="#c62828">Snip! Gone in about 2 minutes.</text>
''' + beads(276, special=1) + '''
<circle cx="88" cy="276" r="19" fill="none" stroke="#148a53" stroke-width="4"/>
<circle cx="88" cy="234" r="20" fill="#2a2a2a"/><text x="88" y="240" text-anchor="middle" ''' + F + ''' font-size="12" font-weight="800" fill="#fff">DPP-4</text>
<text x="118" y="240" ''' + F + ''' font-size="17" font-weight="700" fill="#5f5f68">Can't grab it.</text>
<path d="M228 288 l10 12 l-10 12 l10 12 l-10 12" stroke="#8a5a00" stroke-width="4" fill="none" stroke-linecap="round"/>
<rect x="190" y="346" width="200" height="46" rx="16" fill="#7fdcaa"/>
<circle cx="226" cy="396" r="9" fill="#2a2a2a"/><circle cx="354" cy="396" r="9" fill="#2a2a2a"/>
<text x="290" y="375" text-anchor="middle" ''' + F + ''' font-size="17" font-weight="800" fill="#0b3d24">Albumin bus</text>
<g ''' + F + ''' font-size="16" font-weight="600" fill="#3a3a42"><text x="246" y="320">fatty tail</text><text x="20" y="324">swapped link</text></g>
<text x="400" y="372" ''' + F + ''' font-size="16" font-weight="800" fill="#148a53">About</text><text x="400" y="392" ''' + F + ''' font-size="16" font-weight="800" fill="#148a53">a week</text>''')

D_YELLOW = svg('d-yellow', 'The yellow light on your stomach',
  'The stomach holds food. GLP-1 slows the exit valve to the gut, like a yellow light. Food leaves slower, and the brain gets the full signal.',
  '0 0 480 380', '''
<rect width="480" height="380" fill="#fff"/>
<path d="M118 20 V96 C118 130 70 150 70 220 C70 300 140 340 220 336 C300 332 352 290 350 236 C348 200 330 180 300 176 C240 168 200 150 186 110 L186 20" fill="#ffd9d2" stroke="#e05a4f" stroke-width="5"/>
<circle cx="140" cy="250" r="12" fill="#19a463"/><circle cx="190" cy="282" r="10" fill="#f5a524"/><circle cx="236" cy="246" r="11" fill="#c0392b"/><circle cx="170" cy="210" r="9" fill="#f5a524"/><circle cx="276" cy="270" r="9" fill="#19a463"/>
<path d="M350 236 H460" stroke="#e05a4f" stroke-width="22" stroke-linecap="round"/>
<g fill="#2a2a2a"><rect x="392" y="120" width="40" height="96" rx="12"/></g>
<circle cx="412" cy="140" r="10" fill="#5a2a2a"/><circle cx="412" cy="168" r="11" fill="#f5a524"/><circle cx="412" cy="196" r="10" fill="#1f3d2c"/>
<g fill="#8a5a00"><circle cx="372" cy="236" r="4"/><circle cx="392" cy="236" r="4"/><circle cx="412" cy="236" r="4"/></g>
<path d="M300 18 h150 a14 14 0 0 1 14 14 v32 a14 14 0 0 1 -14 14 h-104 l-20 18 v-18 h-26 a14 14 0 0 1 -14 -14 v-32 a14 14 0 0 1 14 -14z" fill="#e8f2fe"/>
<g ''' + F + ''' font-weight="800" fill="#111114"><text x="375" y="54" text-anchor="middle" font-size="19">Brain: "I'm full."</text>
<text x="356" y="284" font-size="18">Food leaves</text><text x="356" y="306" font-size="18">slower</text>
<text x="20" y="372" font-size="17" fill="#5f5f68">Stomach</text></g>''')

def padlock(x, y, label, color):
    return ('<g transform="translate(%d %d)"><path d="M-16 0 V-14 a16 16 0 0 1 32 0 V0" fill="none" stroke="#2a2a2a" stroke-width="6"/>'
            '<rect x="-26" y="0" width="52" height="42" rx="9" fill="%s"/><text x="0" y="66" text-anchor="middle" %s font-size="17" font-weight="800" fill="#111114">%s</text></g>' % (x, y, color, F, label))

D_KEYS = svg('d-keys', 'One key versus two keys',
  'Semaglutide is one key that fits the GLP-1 lock. Tirzepatide is one key with two cuts that fits both the GLP-1 lock and the GIP lock.',
  '0 0 480 330', '''
<rect width="480" height="330" fill="#fff"/>
<g ''' + F + ''' font-weight="800" fill="#111114" font-size="18"><text x="20" y="34">Semaglutide</text><text x="20" y="196">Tirzepatide</text></g>
<g transform="translate(40 78)"><circle r="18" fill="none" stroke="#2997ff" stroke-width="10"/><path d="M18 0 H130 M110 0 V16" stroke="#2997ff" stroke-width="10" stroke-linecap="round"/></g>
<path d="M190 78 H270" stroke="#9a9aa3" stroke-width="3" stroke-dasharray="5 6"/>
''' + padlock(320, 70, 'GLP-1', '#9fd0ff') + '''
<g transform="translate(40 240)"><circle r="18" fill="none" stroke="#f5a524" stroke-width="10"/><path d="M18 0 H130 M110 0 V16 M88 0 V-16" stroke="#f5a524" stroke-width="10" stroke-linecap="round"/></g>
<path d="M190 240 C220 240 236 214 266 212" stroke="#9a9aa3" stroke-width="3" stroke-dasharray="5 6" fill="none"/>
<path d="M190 240 C260 244 330 262 370 252" stroke="#9a9aa3" stroke-width="3" stroke-dasharray="5 6" fill="none"/>
''' + padlock(300, 214, 'GLP-1', '#9fd0ff') + padlock(410, 214, 'GIP', '#7fdcaa'))


S = [
 sec('cream', 'doorbell', 'Step 1 · The doorbell', 'You eat. Your gut rings the bell.',
   '<p>When food reaches your small gut, special cells in the gut wall called L-cells notice it. Yes, your gut can sort of "taste" food. Weird, but true.</p>'
   '<p>The L-cells answer by sending out a tiny hormone messenger called GLP-1. Think of it as a doorbell that tells your whole body, "Food is here!"' + cite(1, 2) + '</p>'
   + why('The medicines copy this real signal from your own body. They don\'t invent a brand-new one.'),
   fig(D_DOORBELL, 'After a meal, L-cells send out GLP-1. Your blood carries it to the brain, stomach, and pancreas.')),
 sec('white', 'lock-and-key', 'Step 2 · Lock and key', 'GLP-1 is a key. Your cells have the lock.',
   '<p>The lock is called the GLP-1 receptor. It\'s a protein that snakes back and forth through the cell wall, like a lock built into a front door.' + cite(1) + '</p>'
   '<p>When the key turns, a G protein inside the cell switches on a helper called cAMP. Think of cAMP as the cell\'s group text, because one ping tells the whole cell what to do.' + cite(2) + '</p>',
   fig(D_LOCK, 'The receptor snakes through the cell wall. Key in, and cAMP spreads the news inside.'), flip=True,
   below=grid([
     tile('pancreas', 'Pancreas: beta cells', 'They release more insulin, but mostly when your blood sugar is high.'),
     tile('drop', 'Pancreas: alpha cells', 'They release less glucagon, the hormone that pushes blood sugar up.'),
     tile('stomach', 'Stomach', 'It empties more slowly. You\'ll see why that matters in Step 4.'),
     tile('brain', 'Brain', 'Your hypothalamus and brainstem, the hunger and fullness centers, get the "I\'m full" memo.'),
   ]) + why('The insulin push mostly happens when sugar is high, so low blood sugar is not common on these medicines alone. The risk goes up if you also take insulin or a sulfonylurea.' + cite(1))),
 sec('night', 'bouncer', 'Step 3 · The bouncer', 'Meet DPP-4, the bouncer.',
   '<p>Your body has a bouncer, an enzyme named DPP-4, and its whole job is to toss GLP-1 out fast. Your own GLP-1 lasts only about two minutes before it\'s gone.' + cite(1, 3) + '</p>'
   '<p>So scientists gave the medicine two clever upgrades.</p>'
   '<ol class="ex-steps"><li><strong>A swapped link.</strong> They changed one building block near the front of the chain, right where the bouncer grabs. Now he can\'t get a grip.</li>'
   '<li><strong>A fatty tail.</strong> It hangs onto albumin, a big protein that floats in your blood. The medicine rides it like a bus, so your kidneys can\'t flush it out quickly.' + cite(3) + '</li></ol>'
   + why('Semaglutide lasts about a week, and tirzepatide lasts about five days. That\'s why the shot is once a week instead of every meal.' + cite(5, 6)),
   fig(D_BOUNCER, 'Same key, two upgrades. The bouncer can\'t cut it, and the bus keeps it around.')),
 sec('orange', 'yellow-light', 'Step 4 · The yellow light', 'Your stomach hits a yellow light.',
   '<p>GLP-1 tells your stomach to empty more slowly. Think yellow light, not red light, because food still moves along. It just takes its time.' + cite(1) + '</p>'
   '<p>Since food stays in your stomach longer, you tend to feel full longer. Your brain gets the "full" memo too, so it often gets easier to stop eating.' + cite(2) + '</p>'
   '<p>Here\'s the catch. A slower stomach is also a big reason some people feel queasy at first, and that\'s our next stop.</p>',
   fig(D_YELLOW, 'The exit valve slows down. Food leaves bit by bit, and you feel full sooner.'), flip=True),
 sec('blue', 'two-keys', 'Bonus · Two keys', 'Tirzepatide carries a second key.',
   '<p>Semaglutide fits one lock, the GLP-1 receptor. Tirzepatide fits two locks: the GLP-1 receptor and the GIP receptor.' + cite(4, 6) + '</p>'
   '<p>GIP is another gut doorbell, and it also helps your pancreas release insulin after you eat. So tirzepatide is like one key with two cuts.</p>'
   '<p>Is two keys better for you? That depends on your health history, and it\'s something we sort out together.</p>'
   + why('Semaglutide is in Ozempic® and Wegovy®. Tirzepatide is in Mounjaro® and Zepbound®.', 'Brand names'),
   fig(D_KEYS, 'One key, one lock. Or one key with two cuts that opens two locks.')),
]

PAGE = dict(
  title='How GLP-1s Work: Doorbell, Lock & Key | NPCWoods',
  description='How GLP-1 medicines work, in plain words: L-cells, the GLP-1 receptor, the DPP-4 bouncer, and a slower stomach. By NP Chris Woods.',
  about='Obesity and overweight management with GLP-1 medicines',
  reviewed='2026-10-06', published='2026-10-01',
  pill='GLP-1 Explained · How they work',
  h1_top='How GLP-1s', h1_pop='Really Work',
  sub='A doorbell, a lock, a key, and a bouncer. That\'s the whole story. Promise.',
  sticker1='Doorbell <span aria-hidden="true">🔔</span>', sticker2='Lock &amp; key',
  jump_label='Start the story', crumb='How GLP-1s Work',
  ghost_svg=ghost_doorbell(),
  lede='Last stop, you got the big picture. Now let\'s follow GLP-1 all the way from your fork to your brain, and you won\'t need a science degree.',
  tldr=[
    'You eat, and your gut rings a doorbell called GLP-1.',
    'GLP-1 is a key that fits a lock on cells in your pancreas, stomach, and brain.',
    'A bouncer named DPP-4 tosses your own GLP-1 out in about two minutes.',
    'The medicine dodges the bouncer, so one shot lasts about a week.',
  ],
  sections=S,
  recap_title='Four pictures. That\'s it.',
  recap=[
    ('Doorbell', 'After you eat, L-cells in your gut send out GLP-1.'),
    ('Lock and key', 'GLP-1 fits its receptor on your pancreas, stomach, and brain.'),
    ('Bouncer', 'DPP-4 cuts your own GLP-1 fast, but the medicine dodges it.'),
    ('Yellow light', 'Your stomach empties more slowly, so you feel full sooner.'),
  ],
  faq=[
    ('Where does my own GLP-1 come from?', 'L-cells in your gut make it after you eat, and it only lasts about two minutes.'),
    ('Why does one shot last a week?', 'The medicine dodges the DPP-4 bouncer and rides on albumin in your blood, so it sticks around for days.'),
    ('What is different about tirzepatide?', 'It fits two locks, GLP-1 and GIP. Think of one key with two cuts.'),
    ('Can it drop my blood sugar too low?', 'On its own, not often, because it mostly works when your sugar is high. The risk goes up with insulin or a sulfonylurea, so tell me every medicine you take.'),
  ],
  sources=[SRC['statpearls_glp1'], SRC['tanday'], SRC['knudsen'], SRC['statpearls_compare'], SRC['wegovy_dm'], SRC['zepbound_dm'], SRC['niddk']],
  cta_title='Got questions? <span>Text me.</span>',
  cta_text='I\'m Chris, a nurse practitioner. Text me your health history, and I\'ll tell you in plain words whether a GLP-1 may fit.',
  disclaimer=DISCLAIMER,
)
