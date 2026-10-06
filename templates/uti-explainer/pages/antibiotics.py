from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_pills

F = 'font-family="Inter, Arial, sans-serif"'

D_PICK = svg('d-pick', 'Common first-line choices for uncomplicated cystitis',
  'Nitrofurantoin for five days, TMP-SMX for three days when resistance is low, and other options when those do not fit.',
  '0 0 480 360',
  '<rect width="480" height="360" fill="#fff"/>'
  '<rect x="30" y="40" width="200" height="140" rx="18" fill="#fff7e8"/><text x="130" y="90" text-anchor="middle" ' + F + ' font-size="17" font-weight="800">Nitrofurantoin</text><text x="130" y="118" text-anchor="middle" ' + F + ' font-size="15" font-weight="600" fill="#5f5f68">often 5 days</text><text x="130" y="148" text-anchor="middle" ' + F + ' font-size="14" font-weight="700" fill="#8a5a00">Macrobid® family</text>'
  '<rect x="250" y="40" width="200" height="140" rx="18" fill="#e8f2fe"/><text x="350" y="90" text-anchor="middle" ' + F + ' font-size="17" font-weight="800">TMP-SMX</text><text x="350" y="118" text-anchor="middle" ' + F + ' font-size="15" font-weight="600" fill="#5f5f68">often 3 days*</text><text x="350" y="148" text-anchor="middle" ' + F + ' font-size="14" font-weight="700" fill="#0058b0">Bactrim® family</text>'
  '<rect x="90" y="220" width="300" height="90" rx="18" fill="#eaf8f0"/><text x="240" y="258" text-anchor="middle" ' + F + ' font-size="17" font-weight="800">Other picks exist</text><text x="240" y="286" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">allergy · resistance · kidney function</text>')

S = [
 sec('cream', 'why-abx', 'Why antibiotics', 'Bacteria started the fight. Antibiotics finish it.',
   '<p>A true bladder bug needs a medicine that reaches the pee and hits the likely germs.' + cite(1) + '</p>'
   '<p>Comfort pills can quiet the burn. They do not clear the camp. Next stop covers that.</p>'
   + why('I only recommend an antibiotic when the story fits and it looks safe for you. A consult does not guarantee a prescription.')),
 sec('white', 'first-line', 'First-line, plainly', 'Guidelines point to a short list.',
   '<p>For many healthy women who are not pregnant and have a simple bladder UTI, big guidelines point to <strong>nitrofurantoin</strong> (often five days; brand example Macrobid®) and <strong>trimethoprim-sulfamethoxazole (TMP-SMX)</strong> (often three days when local resistance is low; brand example Bactrim®).' + cite(1, 2, 3) + '</p>'
   '<p>Other picks show up too. Fluoroquinolones are often saved for harder cases because of side-effect baggage.</p>',
   fig(D_PICK, 'Common first-line lanes — your history picks the lane.'), flip=True),
 sec('orange', 'how-i-pick', 'How I pick', 'Allergy, kidneys, resistance, and your story.',
   '<p>I ask about sulfa allergy, past medicine reactions, kidney health, pregnancy, and recent UTI treatments.' + cite(1) + '</p>'
   '<p>Nitrofurantoin needs decent kidney filter power to work well in the bladder. TMP-SMX needs a resistance check in your area and does not fit everyone.</p>'
   + why('Brand names are labels on bottles. The molecule and the fit for your body matter more.')),
 sec('night', 'finish', 'Finish the course · no guarantees', 'Stopping early can invite a sequel.',
   '<p>If we start an antibiotic, finish the course unless we change the plan together for side effects or a wrong call.' + cite(4) + '</p>'
   '<p>I will also say no when the story is wrong for outpatient antibiotics — pregnancy, male UTI, catheter, kidney infection signs, or a lookalike. Saying no is care.</p>',
   below=grid([
     tile('pill', 'Nitrofurantoin', 'Common first-line for uncomplicated cystitis when it fits.'),
     tile('pill', 'TMP-SMX', 'Short course when resistance risk is acceptable.'),
     tile('ban', 'Not a vending machine', 'Consult ≠ automatic prescription.'),
     tile('check', 'Reassess', 'Worse after 48–72 hours? Tell me.'),
   ])),
]

PAGE = dict(
  title='UTI Antibiotics Plainly: Nitrofurantoin & TMP-SMX | NPCWoods',
  description='UTI antibiotics in plain words: nitrofurantoin (Macrobid®), TMP-SMX (Bactrim®), IDSA first-line ideas, and why a consult does not guarantee a Rx. By NP Chris Woods.',
  about='Antibiotic treatment of uncomplicated cystitis',
  reviewed='2026-10-06', published='2026-10-06',
  pill='UTI Explained · Antibiotics',
  h1_top='Antibiotics,', h1_pop='Plainly',
  sub='Nitrofurantoin, TMP-SMX, and why I pick one — or say not today.',
  sticker1='First-line', sticker2='No Rx promise',
  jump_label='See the short list', crumb='Antibiotics',
  ghost_svg=ghost_pills(),
  lede='If we are still on the bladder floor, antibiotics are often the clearing crew. Here is how that choice works in real life — without fairy tales.',
  tldr=[
    'Uncomplicated cystitis often uses short first-line regimens.',
    'Nitrofurantoin and TMP-SMX are common guideline options when they fit.',
    'Allergy, kidneys, pregnancy, and resistance change the pick.',
    'A consult does not guarantee a prescription.',
  ],
  sections=S,
  recap_title='Antibiotic cheat sheet.',
  recap=[
    ('Why', 'Kill the bladder germs; comfort meds do not.'),
    ('Nitrofurantoin', 'Common multi-day first-line when appropriate.'),
    ('TMP-SMX', 'Short course when resistance risk allows.'),
    ('Honesty', 'No automatic Rx. Finish what you start.'),
  ],
  faq=[
    ('Will you always send Macrobid®?', 'No. I choose based on your history. Macrobid® is one brand of nitrofurantoin products — not a promise.'),
    ('What about Bactrim®?', 'TMP-SMX can be a fit for some people. Sulfa allergy, resistance, and other factors can rule it out.'),
    ('Can I use leftover pills?', 'No. Wrong drug, wrong dose, wrong bug risk.'),
    ('How soon should I feel better?', 'Many people improve within a day or two. If you worsen or stay stuck, reassess — do not just wait it out.'),
  ],
  sources=[SRC['idsa2011'], SRC['macrobid_dm'], SRC['bactrim_dm'], SRC['cdc_uti'], SRC['niddk_bladder']],
  cta_title='Need a real review? <span>Text me.</span>',
  cta_text='Tell me your symptoms, allergies, and history. I\'ll say yes, no, or "needs in-person" — honestly.',
  disclaimer=DISCLAIMER,
)
