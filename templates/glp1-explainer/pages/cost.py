"""What it costs — honest; no promises."""
from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_coins

F = 'font-family="Inter, Arial, sans-serif"'

D_TWOPART = svg('d-twopart', 'Consult cost vs medicine cost',
  'Two boxes side by side. Left box is the consult. Right box is medicine and other outside costs. They are separate.',
  '0 0 480 280', '''
<rect width="480" height="280" fill="#fff"/>
<rect x="30" y="60" width="180" height="150" rx="24" fill="#e8f2fe" stroke="#0058b0" stroke-width="4"/>
<rect x="270" y="60" width="180" height="150" rx="24" fill="#fff4e0" stroke="#8a5a00" stroke-width="4"/>
<g ''' + F + ''' font-weight="800" font-size="20" fill="#111114"><text x="60" y="130">Consult</text><text x="70" y="158">$59</text></g>
<g ''' + F + ''' font-weight="800" font-size="18" fill="#111114"><text x="300" y="125">Medicine</text><text x="295" y="155">&amp; outside</text><text x="310" y="180">costs</text></g>
<g ''' + F + ''' font-size="14" fill="#3a3a42"><text x="50" y="240">My visit fee</text><text x="290" y="240">Separate if a plan fits</text></g>''')

S = [
 sec('cream', 'split', 'Two bills', 'Consult is not the medicine.',
   '<p>My GLP-1 consult is $59. That is the text visit. I review your health history. I review safety factors. I review fit.</p>'
   '<p>Medicine cost is separate. Pharmacy cash prices sit outside that $59. So do health-plan costs. So do labs. I will not pretend they are the same bill.</p>'
   + why('Clear split means no surprise math. You always know which number is mine.'),
   fig(D_TWOPART, 'Left: my $59 consult. Right: medicine and other outside costs.')),
 sec('white', 'coverage', 'Health plans and cash', 'Coverage varies a lot.',
   '<p>Some health plans cover certain brand GLP-1s. Many do not. Extra checks and denials are common. I cannot promise what your plan will pay.</p>'
   '<p>Cash prices change by brand, dose, and place. Maker savings cards sometimes help for brand products. They have their own rules. I can help you think it through. I cannot lock in a pharmacy price from this page.</p>'
   + why('Anyone who promises your plan will cover it is guessing. I will not guess.')),
 sec('night', 'compounded', 'Compounded pricing talk', 'Honesty over hype.',
   '<p>Some clinics advertise low monthly compounded prices. Compounded drugs are not FDA-approved. FDA does not check them for safety or quality before they are sold.' + cite(1, 2) + '</p>'
   '<p>If compounded options come up, I will say the FDA status out loud. Price is never the only question.</p>'
   + why('Cheap without context is not a care plan.')),
 sec('orange', 'states', 'Where I can see you', 'Thirteen states.',
   '<p>I can see you if you are in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT, or WA. Those are my state NP licenses. I can also see you in FL under Florida out-of-state telehealth registration (TPAN3355). I do not hold a Florida NP license.</p>',
   below=grid([
     tile('note', '$59 consult', 'Flat fee for the text visit. No hidden visit add-ons from me.'),
     tile('pill', 'Medicine separate', 'Pharmacy and labs are outside costs if a care plan fits.'),
     tile('shield', 'No guarantee', 'A consult does not guarantee a prescription.'),
     tile('chat', 'Ask me', 'Text with your state and rough goals. I will tell you what I can and cannot do.'),
   ]) + why('Results vary. I do not promise weight change or a covered refill.')),
]

PAGE = dict(
  title='What a GLP-1 Costs | Honest Pricing | NPCWoods',
  description='Honest GLP-1 cost talk from Chris Woods: $59 consult, medicine separate, health plans vs cash, compounded caveats — no coverage promises.',
  about='GLP-1 consult and medicine cost overview',
  reviewed='2026-10-06', published='2026-10-06',
  pill='GLP-1 Explained · Cost',
  h1_top='What It', h1_pop='Costs',
  sub='My consult is $59. Medicine and other costs are separate. No coverage promises.',
  sticker1='$59 consult <span aria-hidden="true">💬</span>', sticker2='Medicine separate',
  jump_label='See the costs', crumb='What It Costs',
  ghost_svg=ghost_coins(),
  lede='You know who should not take one. Next honest topic: money — what I charge, and what sits outside that fee.',
  tldr=[
    'My consult is $59 for the text visit.',
    'Medicine, pharmacy, and labs are separate if a plan fits.',
    'Health-plan coverage varies; I cannot promise yours.',
    'Compounded drugs are not FDA-approved — price is not the only question.',
  ],
  sections=S,
  recap_title='Cost, in four pictures.',
  recap=[
    ('$59 consult', 'That fee is my text visit.'),
    ('Medicine separate', 'Pharmacy and labs sit outside.'),
    ('Plans vary', 'I will not promise coverage.'),
    ('Compounded caveat', 'Not FDA-approved — ask about safety, not just price.'),
  ],
  faq=[
    ('Is $59 the full price of treatment?', 'No. $59 is my consult. Medicine and other outside costs are separate if a care plan fits.'),
    ('Will my health plan pay for the medicine?', 'Maybe. It depends on your plan and diagnosis. I cannot promise coverage from this page.'),
    ('Do you offer a monthly membership for meds?', 'My consult is a flat $59 visit fee. Medicine pricing, if any, is separate and discussed in care — never as a guarantee on a web page.'),
    ('Why mention compounded drugs?', 'Because low ads are common online. Compounded drugs are not FDA-approved. FDA does not check them for safety or quality before they are sold.'),
  ],
  sources=[SRC['wegovy_dm'], SRC['zepbound_dm'], SRC['wegovy_fda'], SRC['zepbound_fda'], SRC['statpearls_glp1']],
  cta_title='Want a clear cost talk? <span>Text me.</span>',
  cta_text='I\'m Chris, a nurse practitioner. Text me your health history, and we\'ll see if a GLP-1 may fit you.',
  disclaimer=DISCLAIMER,
)
