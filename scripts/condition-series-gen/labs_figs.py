import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figs import *
D = pathlib.Path(__file__).resolve().parents[2].joinpath("landing-pages", "learn", "screening-labs")
ASSETS = pathlib.Path(__file__).resolve().parents[2].joinpath("assets", "learn", "screening-labs")
A = "#0369A1"; TEAL = "#0E7490"; SLATE = "#334155"
figs = {}
figs["panel-lineup.svg"] = rows("Five common screening tests", A, [
  ("Metabolic panel", "Kidneys, liver, salts like sodium and potassium, and blood sugar.", A),
  ("Cholesterol", "LDL, HDL, and triglycerides: the fats riding in your blood.", TEAL),
  ("A1c", "Your average blood sugar over about three months.", SLATE),
  ("TSH (thyroid)", "The signal that tells your thyroid how hard to work.", A),
  ("CBC", "Red cells, white cells, and platelets: the three crews in your blood.", TEAL),
], sub="What each one checks, in one line.")
figs["bmp-vs-cmp.svg"] = columns("BMP vs CMP", A, [
  ("Basic (BMP): 8 tests", A, ["Glucose (sugar)", "Calcium", "Sodium", "Potassium", "Chloride", "Carbon dioxide", "BUN (kidney)", "Creatinine (kidney)"]),
  ("CMP adds 6 more", TEAL, ["Albumin", "Total protein", "ALT (liver)", "AST (liver)", "ALP (liver and bone)", "Bilirubin (bile)"]),
], sub="Same tube. The CMP also checks liver and protein.")
figs["lipid-trucks.svg"] = rows("Lipid panel: common adult targets", A, [
  ("Total", "Under 200 mg/dL", SLATE),
  ("LDL", "Lower is better. Under 100 mg/dL for most adults. The drop-off trucks.", RED),
  ("HDL", "Higher is better. 40+ mg/dL for men, 50+ for women. The pickup trucks.", GREEN),
  ("Triglycerides", "Under 150 mg/dL", A),
], sub="Your own goal depends on your whole heart risk.")
figs["a1c-ranges.svg"] = range_bar("A1c ranges", A, [
  ("Normal", "Below 5.7%", GREEN, .42), ("Prediabetes", "5.7% to 6.4%", AMBER, .30), ("Diabetes", "6.5% or higher", RED, .28)],
  sub="Average blood sugar over about three months.", footnote="Diabetes is confirmed with two tests. Some conditions can make the A1c read falsely high or low.")
figs["tsh-thermostat.svg"] = flow("TSH: the thermostat signal", A, [
  ("Brain senses the level", "The pituitary gland checks how much thyroid hormone is in your blood.", A),
  ("Brain sends TSH", "TSH is the message: turn the furnace up.", TEAL),
  ("High TSH", "Usually means the thyroid is slow (underactive). The brain is yelling.", RED),
  ("Low TSH", "Usually means the thyroid is running hot (overactive). The brain is quiet.", AMBER),
])
figs["cbc-crews.svg"] = columns("The three crews in a CBC", A, [
  ("Red cells", RED, ["Deliver oxygen", "Hemoglobin", "Hematocrit", "MCV (size)"]),
  ("White cells", A, ["Fight germs", "WBC count", "Types of white cells"]),
  ("Platelets", SLATE, ["Plug leaks", "Platelet count"]),
])
figs["screening-schedule.svg"] = rows("A starting schedule for most adults", A, [
  ("Cholesterol", "About every 4 to 6 years from age 20. More often with risk.", TEAL),
  ("Sugar (A1c)", "From 35 if you carry extra weight. About every 3 years if normal.", SLATE),
  ("Hepatitis C", "Once for every adult 18 to 79.", A),
  ("HIV", "At least once from 15 to 65. More often with ongoing risk.", A),
  ("Kidney numbers", "At least yearly with high blood pressure or diabetes.", TEAL),
], sub="Risk factors and symptoms move these earlier.")
figs["reference-range.svg"] = bell("What a reference range means", A, sub="1 in 20 healthy people lands just outside the range on any single test.")
for name, (svg_text, h) in figs.items():
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / name).write_text(svg_text)
art = json.loads((D / "art.json").read_text())
for page in art["pages"].values():
    for f in page.get("figures", []):
        f["height"] = figs[f["src"]][1]; f["width"] = W
(D / "art.json").write_text(json.dumps(art, indent=1, ensure_ascii=False) + "\n")
print({k: v[1] for k, v in figs.items()})
