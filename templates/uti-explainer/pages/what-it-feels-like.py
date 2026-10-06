from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_flame

F = 'font-family="Inter, Arial, sans-serif"'

D_SYMP = svg('d-symp', 'Common bladder UTI feelings',
  'Four common feelings: burn when you pee, sudden urgency, going often, and pressure low in the belly.',
  '0 0 480 360',
  '<rect width="480" height="360" fill="#fff"/>'
  '<rect x="30" y="40" width="200" height="120" rx="18" fill="#fff7e8"/><text x="130" y="88" text-anchor="middle" ' + F + ' font-size="18" font-weight="800" fill="#111114">Burn</text><text x="130" y="118" text-anchor="middle" ' + F + ' font-size="15" font-weight="600" fill="#3a3a42">dysuria</text>'
  '<rect x="250" y="40" width="200" height="120" rx="18" fill="#e8f2fe"/><text x="350" y="88" text-anchor="middle" ' + F + ' font-size="18" font-weight="800" fill="#111114">Urgency</text><text x="350" y="118" text-anchor="middle" ' + F + ' font-size="15" font-weight="600" fill="#3a3a42">gotta go NOW</text>'
  '<rect x="30" y="200" width="200" height="120" rx="18" fill="#eaf8f0"/><text x="130" y="248" text-anchor="middle" ' + F + ' font-size="18" font-weight="800" fill="#111114">Frequency</text><text x="130" y="278" text-anchor="middle" ' + F + ' font-size="15" font-weight="600" fill="#3a3a42">again and again</text>'
  '<rect x="250" y="200" width="200" height="120" rx="18" fill="#fdecea"/><text x="350" y="248" text-anchor="middle" ' + F + ' font-size="18" font-weight="800" fill="#111114">Pressure</text><text x="350" y="278" text-anchor="middle" ' + F + ' font-size="15" font-weight="600" fill="#3a3a42">low belly</text>')

S = [
 sec('cream', 'burn', 'Feeling 1 · Burn', 'Pee that stings is the classic alarm.',
   '<p>Clinicians call it <strong>dysuria</strong>. You may say, "It burns when I pee." That burn is the angry bladder and urethra talking.' + cite(1, 2) + '</p>'
   '<p>It can feel like a hot scrape at the start of the stream, or all the way through.</p>'
   + why('Burn alone is not the whole story. Pair it with urgency and frequency, and a bladder UTI climbs the suspect list.')),
 sec('white', 'urge', 'Feeling 2 · Urgency + frequency', 'Your bladder hits the panic button.',
   '<p><strong>Urgency</strong> means the "I need a bathroom RIGHT NOW" wave. <strong>Frequency</strong> means you just went, and you need to go again.' + cite(1) + '</p>'
   '<p>Often only a little pee comes out. That is the irritated bladder wall, not a giant lake of urine.</p>',
   fig(D_SYMP, 'Burn, urgency, frequency, and pressure are the usual bladder cluster.'), flip=True),
 sec('orange', 'pressure', 'Feeling 3 · Pressure', 'A dull low-belly weight.',
   '<p>Many people feel pressure or mild pain above the pubic bone. It can feel like a small rock sitting there.' + cite(2) + '</p>'
   '<p>Blood in the pee can happen with a bladder UTI. Pink or rusty tint is possible. Big clots or heavy bleeding is a different problem — text me or get seen.</p>'),
 sec('night', 'not-this', 'Not the usual bladder script', 'Fever and flank pain change the story.',
   '<p>A simple bladder UTI (cystitis) usually keeps you out of the ER. Fever, shaking chills, side or back pain under the ribs, vomiting, or feeling wiped out can mean the kidney is involved.' + cite(3) + '</p>'
   '<p>That is the next big fork in the road: bladder vs kidney.</p>',
   below=grid([
     tile('flame', 'Common', 'Burn, urgency, frequency, low pressure.'),
     tile('alert', 'Red flags', 'Fever, flank pain, vomiting, feeling very sick.'),
     tile('water', 'Pee clues', 'Cloudy, strong smell, or pink tint can show up.'),
     tile('chat', 'Gray zone', 'Mild symptoms that are new still deserve a real review.'),
   ])),
]

PAGE = dict(
  title='What a UTI Feels Like: Burn, Urgency, Pressure | NPCWoods',
  description='What a bladder UTI feels like in plain words: dysuria, urgency, frequency, and pressure. By NP Chris Woods.',
  about='Urinary tract infection symptoms',
  reviewed='2026-10-06', published='2026-10-06',
  pill='UTI Explained · What it feels like',
  h1_top='What a UTI', h1_pop='Feels Like',
  sub='Burn, urgency, frequency, pressure. Four feelings. One angry bladder.',
  sticker1='Burn alert', sticker2='Gotta go',
  jump_label='Match your symptoms', crumb='What a UTI Feels Like',
  ghost_svg=ghost_flame(),
  lede='Last stop, the germ climbed. Now the bladder complains. Here is what that complaint usually sounds like in real life.',
  tldr=[
    'Burn when you pee is called dysuria.',
    'Urgency is the sudden "NOW" signal.',
    'Frequency means many trips with little pee.',
    'Fever or flank pain is not the simple bladder script.',
  ],
  sections=S,
  recap_title='Keep this pocket card.',
  recap=[
    ('Dysuria', 'Burn or sting with pee.'),
    ('Urgency', 'Sudden need to go.'),
    ('Frequency', 'Many trips, small amounts.'),
    ('Red flags', 'Fever, flank pain, vomiting — think kidney.'),
  ],
  faq=[
    ('Can a UTI cause back pain?', 'Low belly pressure is common. Pain in the side or back under the ribs with fever is more concerning for a kidney infection.'),
    ('Is cloudy pee enough to diagnose a UTI?', 'No. Smell and cloudiness can have other causes. Symptoms plus a careful history matter.'),
    ('Do I always see blood?', 'No. Some people do, some do not.'),
    ('How fast do symptoms show up?', 'Often over hours to a day or two after the climb begins.'),
  ],
  sources=[SRC['statpearls_cystitis'], SRC['niddk_bladder'], SRC['niddk_kidney'], SRC['cdc_uti']],
  cta_title='Burning right now? <span>Text me.</span>',
  cta_text='Tell me what you feel in plain words. I\'ll help sort the usual bladder cluster from lookalikes and red flags.',
  disclaimer=DISCLAIMER,
)
