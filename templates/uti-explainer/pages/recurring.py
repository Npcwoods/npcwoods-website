from lib import sec, fig, svg, why, tile, grid, cite
from _shared import SRC, DISCLAIMER, ghost_loop

F = 'font-family="Inter, Arial, sans-serif"'

D_LOOP = svg('d-loop', 'Recurrent UTI means a repeating pattern',
  'Recurrent UTI is often defined as two or more infections in six months, or three or more in a year.',
  '0 0 480 300',
  '<rect width="480" height="300" fill="#fff"/>'
  '<circle cx="240" cy="140" r="90" fill="none" stroke="#f5a524" stroke-width="10" stroke-dasharray="18 14"/>'
  '<path d="M240 40 L258 70 L222 70 Z" fill="#f5a524"/>'
  '<text x="240" y="130" text-anchor="middle" ' + F + ' font-size="18" font-weight="800">Again?</text>'
  '<text x="240" y="158" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">2 in 6 months</text>'
  '<text x="240" y="180" text-anchor="middle" ' + F + ' font-size="14" font-weight="600" fill="#5f5f68">or 3 in a year</text>'
  '<text x="240" y="270" text-anchor="middle" ' + F + ' font-size="15" font-weight="700" fill="#3a3a42">Pattern matters more than panic.</text>')

S = [
 sec('cream', 'define', 'What "recurring" means', 'A pattern, not one bad month.',
   '<p>We often call UTIs <strong>recurrent</strong> when you get two or more in six months, or three or more in a year.' + cite(1) + '</p>'
   '<p>That bar keeps us from freaking out over one encore — and from shrugging at a true loop.</p>',
   fig(D_LOOP, 'Recurrence is a counting pattern with a clinical meaning.')),
 sec('white', 'why', 'Why it comes back', 'Same climb, same sticky tricks, new chances.',
   '<p>Sex, a short urethra, leftover pee, menopause tissue changes, and germs that stick well can all reopen the door.' + cite(1, 2) + '</p>'
   '<p>Sometimes the "new" UTI is a leftover that never fully cleared. Sometimes it is a brand-new climb.</p>'
   + why('Logging dates and symptoms helps us see the pattern instead of guessing.')),
 sec('orange', 'dig', 'When to dig deeper', 'Same script on repeat deserves a wider look.',
   '<p>Stones, incomplete emptying, body shape issues, tough germs, or another problem can hide under "UTI again."' + cite(1) + '</p>'
   '<p>Repeat antibiotics without a plan can also breed resistance. That is not a toughness badge.</p>'),
 sec('night', 'plan', 'A calmer plan', 'Prevention plus smart treatment beats fear.',
   '<p>We talk prevention next. For some people, strategies around sex timing, vaginal estrogen when appropriate, or other tailored plans come up with in-person partners.' + cite(3) + '</p>'
   '<p>Your job is not to memorize urology. Your job is to notice the loop and ask for a real review.</p>',
   below=grid([
     tile('clock', 'Count it', '2 / 6 months or 3 / year is the usual yardstick.'),
     tile('bug', 'Why', 'Anatomy, sex, emptying, hormones, sticky germs.'),
     tile('question', 'Dig deeper', 'Weird patterns, blood, stones, male UTI, kids.'),
     tile('shield', 'Next', 'Prevention that is not folklore.'),
   ])),
]

PAGE = dict(
  title='Why UTIs Keep Coming Back | NPCWoods',
  description='Recurrent UTI explained plainly: definitions, why infections return, and when to dig deeper. By NP Chris Woods.',
  about='Recurrent urinary tract infections',
  reviewed='2026-10-06', published='2026-10-06',
  pill='UTI Explained · Recurring',
  h1_top='Why It Keeps', h1_pop='Coming Back',
  sub='A loop has rules. Panic does not. Here is the calm version.',
  sticker1='2 in 6 months', sticker2='Pattern',
  jump_label='Understand the loop', crumb='Recurring',
  ghost_svg=ghost_loop(),
  lede='One UTI is miserable. A rerun schedule is exhausting. Let\'s define recurrence without fear-mongering.',
  tldr=[
    'Recurrent often means 2 in 6 months or 3 in a year.',
    'Anatomy and sticky germs help explain repeats.',
    'Repeats deserve pattern-tracking, not endless leftover pills.',
    'Some people need a deeper workup.',
  ],
  sections=S,
  recap_title='Loop lessons.',
  recap=[
    ('Definition', '2 / 6 months or 3 / year is a common bar.'),
    ('Drivers', 'Climb risk factors stack.'),
    ('Watch-outs', 'Resistance and wrong diagnoses.'),
    ('Path forward', 'Prevention + tailored care.'),
  ],
  faq=[
    ('Is one UTI "recurrent"?', 'No. Recurrence is about a repeating pattern over months.'),
    ('Should I stay on antibiotics forever?', 'Continuous antibiotics are a specialist-level decision with real downsides — not a default text plan.'),
    ('Does my partner need treatment?', 'Usually routine partner treatment is not needed for ordinary cystitis. Unusual STI stories are different.'),
    ('When do I need urology?', 'Frequent recurrences, stones, blood without infection, male UTI, or odd imaging clues — that is dig-deeper territory.'),
  ],
  sources=[SRC['statpearls_recur'], SRC['statpearls_cystitis'], SRC['niddk_bladder'], SRC['idsa2011']],
  cta_title='Stuck in a loop? <span>Text me.</span>',
  cta_text='Share how often this happens and what you have tried. We will sort next steps without the scare tactics.',
  disclaimer=DISCLAIMER,
)
