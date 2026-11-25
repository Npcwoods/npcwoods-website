import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figs import *
D = pathlib.Path(__file__).resolve().parents[2].joinpath("landing-pages", "learn", "mastitis")
ASSETS = pathlib.Path(__file__).resolve().parents[2].joinpath("assets", "learn", "mastitis")
A = "#B42318"; ROSE = "#9F1239"; SLATE = "#334155"; SOFT = "#C2410C"
figs = {}
figs["mastitis-spectrum.svg"] = flow("The mastitis spectrum", A, [
  ("Narrowed duct", "A tender lump. No fever. You feel fine.", BLUE),
  ("Inflammatory mastitis", "A red or warm wedge. Often fever and aches.", AMBER),
  ("Bacterial mastitis", "Inflammation plus germs. Slower to improve.", SOFT),
  ("Abscess", "A pocket of pus. Needs an ultrasound and often drainage.", RED),
], sub="From mild to serious. Most cases stay near the top.")
figs["swelling-loop.svg"] = flow("The swelling loop", A, [
  ("Tissue swells", "Busy milk tissue gets inflamed.", AMBER),
  ("Ducts narrow", "Swelling pinches the soft milk straws.", SOFT),
  ("Milk slows, pressure builds", "Fullness adds to the swelling, and the loop repeats.", RED),
  ("Break the loop", "Cold, gentle touch, rest, and normal feeding calm the swelling.", GREEN),
])
figs["symptom-map.svg"] = columns("What mastitis feels like", A, [
  ("In the breast", A, ["Warm, tender wedge", "Red, pink, or darker skin", "Firm or swollen area", "Pain while feeding"]),
  ("In the body", SLATE, ["Fever 100.4°F or higher", "Chills and aches", "Headache", "Wiped out"]),
])
figs["lookalikes-table.svg"] = rows("Sore breast while feeding: quick sort", A, [
  ("Engorgement", "Both sides full and firm, days 2 to 5. Low fever at most.", BLUE),
  ("Narrowed duct", "One tender lump. No fever. You feel fine.", SLATE),
  ("Mastitis", "Hot, red wedge on one side. Often fever and aches.", AMBER),
  ("Abscess", "A lump that stays or grows, may feel soft. Needs an ultrasound.", RED),
])
figs["comfort-do-skip.svg"] = columns("Comfort care: helps vs skip", A, [
  ("Often helps", GREEN, ["Feed on demand", "Cold packs between feeds", "Feather-light strokes toward the armpit", "Supportive, loose bra", "Rest and fluids"]),
  ("Skip", A, ["Deep, hard massage", "Long heat or hot soaks", "Extra pumping to empty", "Stopping feeds suddenly", "Picking a nipple white dot"]),
], sub="General education, not a personal plan.")
figs["red-flags-er.svg"] = rows("Go to the ER or call 911", A, [
  ("Fever", "103°F or higher, or shaking chills that will not stop.", RED),
  ("Spreading", "Red streaks spreading fast toward the armpit or chest.", RED),
  ("Pus or lump", "Pus draining, or a soft lump that is growing.", RED),
  ("Whole body", "Racing heart, fast breathing, faint, dizzy, or confused.", RED),
], sub="Do not text first. Go.")
figs["feeding-tips.svg"] = rows("Feeding while you heal", A, [
  ("Start easy", "Begin on the comfortable side. Switch once milk is flowing.", SLATE),
  ("Aim the chin", "Point the baby's chin toward the sore spot.", BLUE),
  ("On demand", "Feed when the baby wants. No extra pumping to empty.", GREEN),
  ("Just comfort", "If baby won't feed on that side, hand express just enough to feel better.", AMBER),
])
figs["text-vs-in-person.svg"] = columns("Which door fits?", A, [
  ("Text visit", BLUE, ["One sore, red, warm area", "Fever under 103°F", "Eating and drinking okay", "No pus, no growing lump", "In a state I treat"]),
  ("In person or ER", A, ["Any red flag", "A lump that stays or grows", "Not better after 48 hours", "Not breastfeeding", "Weak immune system"]),
], sub="When in doubt, go in.")
ASSETS.mkdir(parents=True, exist_ok=True)
for name, (svg_text, h) in figs.items():
    (ASSETS / name).write_text(svg_text)
art = json.loads((D / "art.json").read_text())
for page in art["pages"].values():
    for f in page.get("figures", []):
        f["height"] = figs[f["src"]][1]; f["width"] = W
(D / "art.json").write_text(json.dumps(art, indent=1, ensure_ascii=False) + "\n")
print("figs ok")
