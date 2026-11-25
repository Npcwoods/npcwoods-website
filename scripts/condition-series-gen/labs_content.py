"""Screening labs series copy (Chris's voice). Generates series.json, content.json, art.json."""
import json, pathlib
OUT = pathlib.Path(__file__).resolve().parents[2].joinpath("landing-pages", "learn", "screening-labs")
OUT.mkdir(parents=True, exist_ok=True)
HUB = "/learn/screening-labs/"
LIC = "14 states, including Florida by telehealth registration (TPAN3355)"

stops = [
    ("", "Screening Labs Explained", "The big picture", "hub"),
    ("metabolic-panel", "The metabolic panel: kidneys, liver, salts, and sugar", "Metabolic panel", "stop"),
    ("cholesterol", "Cholesterol: the fats riding in your blood", "Cholesterol", "stop"),
    ("a1c", "A1c: your three-month sugar report card", "A1c", "stop"),
    ("thyroid", "Thyroid tests: the body's thermostat", "Thyroid", "stop"),
    ("cbc", "The CBC: counting your blood cells", "CBC", "stop"),
    ("who-and-how-often", "Who should get labs, and how often", "Who and how often", "stop"),
    ("reading-results", "How to read your lab results", "Reading results", "stop"),
]
series = {
    "id": "screening-labs",
    "name": "Screening Labs Explained",
    "kicker": "Screening labs series",
    "tagline": "A plain-talk series from Chris Woods, NP. One story. Eight stops.",
    "reviewed": "2026-11-24",
    "reviewed_display": "November 24, 2026",
    "accent": {"name": "blue", "hex": "#0369A1"},
    "brand": {"ink": "#1A1A2E", "blue": "#2563EB", "cream": "#F6F3EE", "accent_soft": "#E0F0FA", "accent_wash": "#F0F8FD", "accent_deep": "#0C4A6E"},
    "ghost_base": "vial",
    "og_alt_suffix": "Chris Woods, NP, with a lab tube outline",
    "license_line": LIC,
    "sms": {"number": "4806394722", "display": "(480) 639-4722",
            "prefill": "Hi Chris, I have a question about screening labs and want a $59 text visit."},
    "cta_band": {"heading": "Want a second set of eyes on your labs?",
                 "body": "Text me your age, your family history, how you feel, and what you want checked. I read it myself and tell you what makes sense, what can wait, and what needs an in-person visit. You only pay the $59 if a text visit is the right fit."},
    "hub": {"slug": "", "path": HUB, "title": "Screening Labs Explained", "nav_label": "The big picture", "episode": 1},
    "one_pager": {"path": "/screening-labs/", "title": "Screening labs by text", "nav_label": "$59 text visit"},
    "stops": [
        {"slug": s, "path": HUB + (s + "/" if s else ""), "title": t, "nav_label": n, "episode": i + 1, "kind": k}
        for i, (s, t, n, k) in enumerate(stops)
    ],
}

SRC = {
 "uspstf_dm": ("US Preventive Services Task Force. Prediabetes and type 2 diabetes: screening (2021).", "https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/screening-for-prediabetes-and-type-2-diabetes"),
 "cdc_a1c": ("CDC. Diabetes testing: the A1C test.", "https://www.cdc.gov/diabetes/diabetes-testing/prediabetes-a1c-test.html"),
 "ml_a1c": ("MedlinePlus. Hemoglobin A1C (HbA1c) test.", "https://medlineplus.gov/lab-tests/hemoglobin-a1c-hba1c-test/"),
 "ml_cmp": ("MedlinePlus. Comprehensive metabolic panel (CMP).", "https://medlineplus.gov/lab-tests/comprehensive-metabolic-panel-cmp/"),
 "ml_bmp": ("MedlinePlus. Basic metabolic panel (BMP).", "https://medlineplus.gov/lab-tests/basic-metabolic-panel-bmp/"),
 "ml_cbc": ("MedlinePlus. Complete blood count (CBC).", "https://medlineplus.gov/lab-tests/complete-blood-count-cbc/"),
 "ml_chol": ("MedlinePlus. Cholesterol levels.", "https://medlineplus.gov/lab-tests/cholesterol-levels/"),
 "aha_chol": ("American Heart Association. How to get your cholesterol tested.", "https://www.heart.org/en/health-topics/cholesterol/about-cholesterol/how-to-get-your-cholesterol-tested"),
 "ml_tsh": ("MedlinePlus. TSH (thyroid-stimulating hormone) test.", "https://medlineplus.gov/lab-tests/tsh-thyroid-stimulating-hormone-test/"),
 "uspstf_thy": ("US Preventive Services Task Force. Thyroid dysfunction: screening (2015).", "https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/thyroid-dysfunction-screening"),
 "uspstf_hcv": ("US Preventive Services Task Force. Hepatitis C virus infection in adolescents and adults: screening (2020).", "https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/hepatitis-c-screening"),
 "uspstf_hiv": ("US Preventive Services Task Force. HIV infection: screening (2019).", "https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/human-immunodeficiency-virus-hiv-infection-screening"),
 "ml_results": ("MedlinePlus. How to understand your lab results.", "https://medlineplus.gov/lab-tests/how-to-understand-your-lab-results/"),
 "niddk_kid": ("NIDDK. Kidney disease: tests and diagnosis.", "https://www.niddk.nih.gov/health-information/kidney-disease/chronic-kidney-disease-ckd/tests-diagnosis"),
}
def src(*keys):
    return [{"label": SRC[k][0], "url": SRC[k][1]} for k in keys]
def b(you, chris):
    return [{"style": "blue", "who": "You", "text": you}, {"style": "black", "who": "Chris", "text": chris}]
def prose(h, *body): return {"type": "prose", "heading": h, "body": list(body)}
def lst(h, *items): return {"type": "list", "heading": h, "items": list(items)}
def safety(t, body): return {"type": "callout", "kind": "safety", "title": t, "body": body}
def ink(t, body): return {"type": "callout", "kind": "ink", "title": t, "body": body}
ER = safety("Labs are not for emergencies. Call 911.",
            "Chest pain, trouble breathing, fainting, sudden weakness on one side, confusion, or a very fast or pounding heartbeat do not wait for a blood draw. Call 911 or go to the ER now.")

C = {}
C["hub"] = {
 "meta_title": "Screening Labs Explained: What Blood Work Checks | NPCWoods",
 "meta_description": "Metabolic panel, cholesterol, A1c, thyroid, and CBC in plain words. Chris Woods, NP, explains what screening labs check, who needs them, and how often.",
 "h1": "Screening labs, explained plainly",
 "lede": "A blood draw is a peek under the hood. A few tubes can show how your kidneys, liver, sugar, fats, thyroid, and blood cells are doing, often before you feel a thing. I will walk you through each one, stop by stop.",
 "bubbles": b("My last checkup was years ago. Which labs do I even need?", "Depends on your age, your family, and how you feel. Text me the story. I will tell you what makes sense and what can wait."),
 "stats": [{"num": "5", "label": "common screening tests in this series"}, {"num": "35+", "label": "age when sugar screening often starts if you carry extra weight"}, {"num": "$59", "label": "flat text visit with me"}],
 "sections": [
  prose("Why check blood when you feel fine?",
   "Most early problems are quiet. High sugar does not hurt. High cholesterol does not hurt. A slow thyroid can feel like being tired, which everyone is. Labs catch the quiet stuff early, while small changes still make a big difference.",
   "Think of it like the dashboard lights in your car. You do not wait for smoke from the hood. You glance at the gauges now and then."),
  lst("The five tests I get asked about most",
   "Metabolic panel: kidneys, liver, salts like sodium and potassium, and blood sugar.",
   "Cholesterol (lipid panel): the fats riding in your blood, good and bad.",
   "A1c: your average blood sugar over about three months.",
   "Thyroid (TSH): the signal that tells your body's thermostat how hard to work.",
   "CBC: a count of your red cells, white cells, and platelets."),
  prose("Not everyone needs every test",
   "More tubes is not always better. A test that does not fit you can come back a little off and send you chasing nothing. I would rather pick the right few for your age, your risks, and your symptoms. Stop 7 lays out who should get what, and how often."),
  ER,
  prose("How the series flows",
   "We start with the big panel, then cholesterol, then sugar, then the thyroid, then the blood count. After that we talk timing, and last, how to read the page of numbers when it lands in your inbox. Each stop links to the next."),
 ],
 "faqs": [
  {"q": "Do I need to fast before screening labs?", "a": "For many tests, no. Cholesterol is often checked without fasting now. A fasting sugar test needs about 8 hours with only water. Follow the instructions on your lab order."},
  {"q": "Can you order labs by text?", "a": "If labs make sense for you, I can write a lab order and send it to you, and you get your blood drawn at a lab. The lab charges its own fee, separate from my $59 visit."},
  {"q": "Are screening labs a full checkup?", "a": "No. Labs are one piece. Blood pressure, weight, cancer screenings, shots, and a hands-on exam still matter. Keep a regular clinic for those."},
  {"q": "What if something comes back high or low?", "a": "Many flags are small and expected. Some need a repeat. A few need care soon. Stop 8 walks through how to read the page, and I can go over it with you."},
 ],
 "sources": src("uspstf_dm", "ml_cmp", "ml_chol", "ml_tsh", "ml_cbc", "ml_results"),
}
C["metabolic-panel"] = {
 "meta_title": "Metabolic Panel (CMP/BMP) Explained Plainly | NPCWoods",
 "meta_description": "What a metabolic panel checks: kidneys, liver, sodium, potassium, and blood sugar. Chris Woods, NP, explains the CMP and BMP in plain words.",
 "h1": "The metabolic panel: kidneys, liver, salts, and sugar",
 "lede": "This is the workhorse test. One tube, more than a dozen numbers. It tells me how your filters are filtering, how your liver is working, and whether your body's salt and sugar balance is steady.",
 "bubbles": b("My report says CMP. Is that the same as BMP?", "Close cousins. The BMP is the short list. The CMP adds liver and protein numbers. Same tube, more answers."),
 "sections": [
  prose("Two sizes: BMP and CMP",
   "The basic metabolic panel (BMP) has 8 numbers: sugar, calcium, sodium, potassium, chloride, carbon dioxide, and two kidney numbers. The comprehensive metabolic panel (CMP) adds 6 more: two proteins and four liver numbers.",
   "Picture a car inspection. The BMP checks the fluids and the battery. The CMP also pops the hood on the engine."),
  lst("What the main numbers tell me",
   "Glucose: sugar in your blood right now. Fasting changes it a lot.",
   "Sodium and potassium: salts that keep your nerves and heart firing on time.",
   "BUN and creatinine: waste your kidneys should clear. If they climb, the filters may be slowing down.",
   "eGFR: a math estimate of how well your kidneys filter, built from creatinine, age, and sex.",
   "ALT, AST, ALP, and bilirubin: liver and bile flow signals.",
   "Albumin and total protein: building blocks your liver makes."),
  prose("Your kidneys are coffee filters",
   "Blood runs through millions of tiny filters in each kidney. Waste goes out in urine. Good stuff stays in. Creatinine is like coffee grounds. If the grounds start showing up in the cup, the filter is not catching them as well. That is when I look closer."),
  prose("Who this test fits",
   "Adults with high blood pressure or diabetes should get kidney numbers checked at least once a year. People on certain long-term medicines need them too. Some healthy adults get a CMP with a yearly checkup. If you feel fine and have no risks, it is a reasonable baseline, not a must."),
  ink("A single odd number is not a diagnosis",
   "Dehydration, a hard workout, a big steak, or a slow draw can nudge these numbers. Often the right next step is a repeat in a few weeks, not panic."),
  ER,
 ],
 "faqs": [
  {"q": "Do I need to fast for a metabolic panel?", "a": "If your clinician wants a fasting sugar from it, yes, about 8 hours with water only. Otherwise it can often be drawn any time. Check your lab order."},
  {"q": "What does a low eGFR mean?", "a": "eGFR under 60 for 3 months or more can mean chronic kidney disease. One low reading can come from dehydration. A repeat and a urine test help sort it out."},
  {"q": "Why is my potassium high when I feel fine?", "a": "Sometimes the sample sat too long or cells broke during the draw. A repeat often fixes it. A truly high potassium needs prompt care."},
 ],
 "sources": src("ml_cmp", "ml_bmp", "niddk_kid"),
}
C["cholesterol"] = {
 "meta_title": "Cholesterol Test (Lipid Panel) Explained Plainly | NPCWoods",
 "meta_description": "LDL, HDL, and triglycerides in plain words. Chris Woods, NP, explains what a cholesterol test shows, who should get one, and how often.",
 "h1": "Cholesterol: the fats riding in your blood",
 "lede": "Cholesterol is not the enemy. Your body uses it to build cells and hormones. The trouble is too much of the wrong kind, parked in your arteries for years. A lipid panel shows me the traffic.",
 "bubbles": b("My total cholesterol is 210. Am I in trouble?", "Not by itself. I care more about the LDL, the HDL, and the rest of your story. Send me the whole page."),
 "sections": [
  prose("Delivery trucks on the highway",
   "Cholesterol rides in little delivery trucks called lipoproteins. LDL trucks drop cholesterol off in the walls of your arteries. HDL trucks pick it up and haul it back to the liver. Too many LDL trucks, for too long, and the drop-offs pile up into plaque.",
   "Plaque narrows the road. If a piece breaks loose, it can block blood flow to the heart or brain. That is why I watch this number years before anything hurts."),
  lst("What is on the page",
   "Total cholesterol: everything added up. Under 200 mg/dL is the usual goal.",
   "LDL: the drop-off trucks. Lower is better. Under 100 mg/dL is a common target for most adults.",
   "HDL: the pickup trucks. Higher is better. 40 mg/dL or more for men, 50 or more for women.",
   "Triglycerides: fat from recent food and extra calories. Under 150 mg/dL is the usual goal.",
   "Non-HDL: total minus HDL. A good catch-all for the bad trucks."),
  prose("Who should check, and how often",
   "The American Heart Association suggests most adults check every 4 to 6 years starting around age 20. If you have diabetes, high blood pressure, smoke, carry extra weight, or have a parent or sibling with early heart disease, it is checked more often. Kids get one check between ages 9 and 11 and again between 17 and 21."),
  prose("Do I have to fast?",
   "Most people do not. Non-fasting panels are fine for screening. If your triglycerides come back high, I may ask for a fasting repeat to get a clean read."),
  ink("Numbers are one piece",
   "Your heart risk comes from the whole picture: age, blood pressure, sugar, smoking, family history, and these numbers. Two people with the same LDL can have very different risk. That is the talk worth having."),
  ER,
 ],
 "faqs": [
  {"q": "Can I lower cholesterol without medicine?", "a": "Often some, yes. More fiber, fewer fried and fatty processed foods, more movement, and quitting smoking help. How much depends on your genes. Whether medicine fits is a separate talk based on your full risk."},
  {"q": "Is high HDL always good?", "a": "Mostly. Very high HDL does not erase other risks, so I still look at the whole picture."},
  {"q": "Why did my numbers change so much since last year?", "a": "Diet, weight, alcohol, thyroid changes, pregnancy, and some medicines all move these numbers. Labs also vary a little day to day."},
 ],
 "sources": src("aha_chol", "ml_chol"),
}
C["a1c"] = {
 "meta_title": "A1c Test Explained: Prediabetes and Diabetes Ranges | NPCWoods",
 "meta_description": "What an A1c shows, what the prediabetes and diabetes ranges mean, and who should get screened. Chris Woods, NP, explains in plain words.",
 "h1": "A1c: your three-month sugar report card",
 "lede": "A finger-stick sugar is a snapshot. The A1c is the whole photo album. It shows your average blood sugar over roughly the last three months, no fasting needed.",
 "bubbles": b("My A1c is 5.9. My friend says that is basically fine.", "That is prediabetes. Good news: it is the stage where small changes work best. Let us talk about it."),
 "sections": [
  prose("Sugar sticks to your red cells",
   "Red blood cells live about three months. While they float around, sugar sticks to them, like powdered sugar on a donut. The more sugar in your blood, the more coating. The A1c measures the coating, as a percent.",
   "That is why one big dessert does not wreck it, and one good week does not fix it. It is the long game."),
  lst("The ranges",
   "Below 5.7%: normal.",
   "5.7% to 6.4%: prediabetes. Your sugar is running higher than it should.",
   "6.5% or higher on two tests: diabetes.",
   "A fasting glucose of 100 to 125 mg/dL also points to prediabetes. 126 or higher on two tests points to diabetes."),
  prose("Who should be screened",
   "The US Preventive Services Task Force says adults 35 to 70 who carry extra weight should be screened. Many groups screen all adults starting at 35. Screen earlier if you had diabetes in pregnancy, have a parent or sibling with diabetes, or have high blood pressure. If normal, repeat about every 3 years."),
  prose("Prediabetes is a fork in the road",
   "About 1 in 3 US adults has prediabetes, and most do not know it. It does not mean diabetes is coming for sure. Losing a small amount of weight, walking most days, and sleeping better can bring the number back down. Catching it here is the whole point of screening."),
  ink("When the A1c can fool you",
   "Anemia, recent heavy bleeding, a blood transfusion, pregnancy, kidney disease, and some inherited hemoglobin types can push the A1c falsely high or low. If your A1c does not match the rest of your story, I may use a different sugar test."),
  safety("Very high sugar can be an emergency. Call 911.",
   "Extreme thirst, peeing all the time, vomiting, fruity breath, fast breathing, or confusion can mean dangerously high sugar. Call 911 or go to the ER now."),
 ],
 "faqs": [
  {"q": "Do I need to fast for an A1c?", "a": "No. You can eat before an A1c. A fasting glucose test is different and needs about 8 hours without food."},
  {"q": "Can an A1c at home replace a lab test?", "a": "Home kits can be a start, but a lab A1c is the one used to diagnose prediabetes and diabetes."},
  {"q": "How fast can my A1c come down?", "a": "Because red cells live about three months, a fair recheck is about 3 months after you make changes."},
 ],
 "sources": src("uspstf_dm", "cdc_a1c", "ml_a1c"),
}
C["thyroid"] = {
 "meta_title": "Thyroid Test (TSH) Explained Plainly | NPCWoods",
 "meta_description": "What a TSH test checks, what high and low TSH mean, and when a thyroid test makes sense. Chris Woods, NP, explains in plain words.",
 "h1": "Thyroid tests: the body's thermostat",
 "lede": "Your thyroid sets the pace for almost everything: heat, heart rate, energy, weight, mood, even hair and skin. The TSH test is how I check whether the thermostat is set right.",
 "bubbles": b("I am tired all the time. Can you just check my thyroid?", "Maybe. Tired has a hundred causes. Tell me about sleep, periods, weight, and mood. If the thyroid fits the story, we test it."),
 "sections": [
  prose("A thermostat and a furnace",
   "Your brain is the thermostat. Your thyroid, a small butterfly-shaped gland in your neck, is the furnace. When the brain senses the house is cold, it sends a signal called TSH: turn up the heat. When it is warm enough, it quiets down.",
   "So TSH runs backward from what people expect. A high TSH usually means the furnace is slow and the brain is yelling. A low TSH usually means the furnace is running hot."),
  lst("What the numbers usually mean",
   "Normal TSH is roughly 0.4 to 4.0 mIU/L. Each lab prints its own range.",
   "High TSH: often an underactive thyroid (hypothyroidism). Think tired, cold, constipated, dry skin, weight gain, heavy periods.",
   "Low TSH: often an overactive thyroid (hyperthyroidism). Think shaky, hot, sweaty, racing heart, weight loss, trouble sleeping.",
   "Free T4: the actual thyroid hormone. I add it when TSH is off to see how off."),
  prose("Should everyone get a thyroid test?",
   "No. The US Preventive Services Task Force did not find enough evidence to screen adults who have no symptoms. I check the thyroid when the story fits: symptoms like the ones above, a strong family history, a lump in the neck, trying to get pregnant, or recent pregnancy."),
  ink("Supplements can scramble the result",
   "Some hair, skin, and nail vitamins can throw off thyroid tests. Tell me what you take. You may need to pause it a couple of days before the draw."),
  safety("When the thyroid is an emergency. Call 911.",
   "A racing or irregular heartbeat with chest pain, fainting, high fever with confusion, or trouble breathing needs the ER now. Call 911."),
 ],
 "faqs": [
  {"q": "Can thyroid problems cause weight gain?", "a": "An underactive thyroid can add a few pounds, mostly from fluid. It is rarely the whole reason for big weight changes."},
  {"q": "My TSH is slightly high but I feel fine. Now what?", "a": "Mild changes often get a repeat in 6 to 8 weeks before anyone decides on treatment. Illness and recent pregnancy can shift it for a while."},
  {"q": "Is a lump in my neck a thyroid thing?", "a": "It might be. A new neck lump needs a hands-on exam and often an ultrasound. That is an in-person visit."},
 ],
 "sources": src("ml_tsh", "uspstf_thy"),
}
C["cbc"] = {
 "meta_title": "CBC Blood Test Explained Plainly | NPCWoods",
 "meta_description": "What a complete blood count checks: red cells, white cells, hemoglobin, and platelets. Chris Woods, NP, explains the CBC in plain words.",
 "h1": "The CBC: counting your blood cells",
 "lede": "A complete blood count is a headcount of the three crews in your blood: the delivery crew, the defense crew, and the repair crew. When one crew is short or crowded, it tells me where to look next.",
 "bubbles": b("My CBC says low hemoglobin. Is that anemia?", "It can be. Next question is why. Heavy periods, low iron, and a few other things are on my list. Send me the full page."),
 "sections": [
  prose("Three crews",
   "Red blood cells are the delivery crew. They carry oxygen from your lungs to every cell. White blood cells are the defense crew. They fight germs. Platelets are the repair crew. They plug leaks when you get cut.",
   "The CBC counts each crew and checks their size and shape."),
  lst("What is on the page",
   "Hemoglobin and hematocrit: how much oxygen-carrying power you have. Low can mean anemia.",
   "MCV: the size of your red cells. Small cells hint at low iron. Big cells hint at low B12 or folate, alcohol, or thyroid issues.",
   "White blood cell count (WBC): high can mean infection, stress, or inflammation. Low can mean a virus or a marrow issue.",
   "Platelets: low can mean easy bruising and bleeding. High can follow inflammation or low iron."),
  prose("Who needs a CBC?",
   "A CBC is not a routine screen for healthy adults with no symptoms. I order it when the story points there: tired and short of breath, heavy periods, easy bruising, frequent infections, weight loss, or night sweats. It is also common before surgery and with some long-term conditions."),
  ink("Low iron is common and sneaky",
   "Heavy periods, pregnancy, eating little red meat, and slow bleeding in the gut can all drain iron. The CBC may look normal at first. A separate test called ferritin can catch low iron earlier."),
  safety("When a blood count is an emergency. Call 911.",
   "Black or bloody stools, vomiting blood, fainting, a racing heart with shortness of breath, or bleeding you cannot stop needs the ER now. Call 911."),
 ],
 "faqs": [
  {"q": "Can stress change my CBC?", "a": "Yes. Stress, a recent workout, smoking, and some medicines can bump the white count a little."},
  {"q": "My platelets are a little low. Should I worry?", "a": "Mildly low platelets are often rechecked first. Easy bruising, nosebleeds, or tiny red dots on the skin make it more urgent."},
  {"q": "Does a normal CBC mean I am healthy?", "a": "It means your blood counts look fine today. It does not check sugar, cholesterol, kidneys, or cancer screenings."},
 ],
 "sources": src("ml_cbc", "ml_results"),
}
C["who-and-how-often"] = {
 "meta_title": "Who Needs Screening Labs, and How Often? | NPCWoods",
 "meta_description": "A plain schedule for sugar, cholesterol, kidney, hepatitis C, and HIV screening by age and risk. Chris Woods, NP, explains who needs what.",
 "h1": "Who should get labs, and how often",
 "lede": "There is no single lab menu for everyone. A healthy 25-year-old and a 55-year-old with high blood pressure need different things. Here is the plain map I use.",
 "bubbles": b("I am 42 and healthy. What should I actually get?", "Probably sugar and cholesterol, plus a one-time hepatitis C and HIV check if you never had them. Text me your family history and I will tailor it."),
 "sections": [
  lst("Most adults",
   "Cholesterol: about every 4 to 6 years starting around age 20. More often with risk factors.",
   "Sugar (A1c or fasting glucose): starting at 35 if you carry extra weight, about every 3 years if normal. Earlier with risk factors.",
   "Hepatitis C: once for every adult 18 to 79.",
   "HIV: at least once for everyone 15 to 65. More often with ongoing risk."),
  lst("If you have a long-term condition",
   "High blood pressure or diabetes: kidney numbers (metabolic panel) and a urine protein check at least yearly.",
   "Diabetes: A1c every 3 to 6 months until steady, then about twice a year.",
   "On long-term medicines: the labs your prescriber names, on their schedule."),
  lst("When symptoms point the way",
   "Tired, cold, hair thinning, or a racing heart: thyroid.",
   "Tired, short of breath, heavy periods, or easy bruising: CBC and often ferritin.",
   "Always thirsty and peeing a lot: sugar, today, not in three years."),
  prose("Getting ready for the draw",
   "Drink water. It plumps your veins and makes the draw easier. Fast only if your order says so, usually 8 hours with water only. Take your usual medicines unless told otherwise. Tell the lab and me about supplements, especially hair, skin, and nail vitamins."),
  ink("More is not always better",
   "Testing for everything can turn up small, harmless flags that lead to more tests, more worry, and more bills. I would rather choose the tests that answer a real question for you."),
  ER,
 ],
 "faqs": [
  {"q": "Do I need yearly blood work?", "a": "Not always. Many healthy adults do fine with the schedule above. Long-term conditions and symptoms change that."},
  {"q": "What about vitamin D or testosterone?", "a": "Those are not routine screens for most people. I check them when symptoms or history make the result useful."},
  {"q": "Should kids get labs?", "a": "Kids get a cholesterol check between 9 and 11 and again between 17 and 21, plus others based on risk. Their regular clinic handles that."},
 ],
 "sources": src("uspstf_dm", "aha_chol", "uspstf_hcv", "uspstf_hiv", "niddk_kid"),
}
C["reading-results"] = {
 "meta_title": "How to Read Your Lab Results, in Plain Words | NPCWoods",
 "meta_description": "Reference ranges, H and L flags, and what to do when a number is off. Chris Woods, NP, explains how to read your blood work without panicking.",
 "h1": "How to read your lab results",
 "lede": "Results often hit your phone before anyone explains them. A wall of numbers with red H and L flags can feel scary. Most of the time, it is less dramatic than it looks. Here is how I read the page.",
 "bubbles": b("My portal shows six red flags. Should I freak out?", "Not yet. Most flags are a hair outside the range. Send me the page and your story. We go line by line."),
 "sections": [
  prose("What a reference range really is",
   "Each lab tests a big group of healthy people. The middle 95% becomes the normal range. That means 1 in 20 healthy people lands just outside it on any single test, just by chance. Run 20 tests and a flag or two is expected.",
   "So an H or L is a nudge to look, not a verdict."),
  lst("How I read each line",
   "How far off is it? A hair outside the range is different from double.",
   "Does it fit your story? A low iron number in someone with heavy periods makes sense.",
   "Do the numbers agree? Kidney, liver, and blood numbers usually move in groups.",
   "What changed? A trend over a few years tells more than one result."),
  prose("Common harmless reasons for a flag",
   "Not fasting when you were supposed to. A hard workout the day before. Being a little dehydrated. A sample that sat too long. A recent cold. Pregnancy. These can all nudge a number."),
  prose("What happens next",
   "Many small flags just need a repeat in a few weeks. Some point to a follow-up test. A few need care soon. If something needs a hands-on exam, an imaging test, or ongoing management, I tell you so and point you to the right place."),
  safety("Some results cannot wait. Call 911 if you feel very sick.",
   "If a lab calls you about a critical result, or you have chest pain, trouble breathing, fainting, confusion, or heavy bleeding, call 911 or go to the ER now."),
 ],
 "faqs": [
  {"q": "Can you look at labs another clinic ordered?", "a": "Yes. Text me the results and your story. I will explain what they mean in plain words and tell you if anything needs follow-up."},
  {"q": "Why do two labs give different ranges?", "a": "Different machines and methods. Always read your number against the range printed on your own report."},
  {"q": "Is a result in range always fine?", "a": "Usually, but a number climbing toward the edge over a few years is worth noticing. Trends matter."},
 ],
 "sources": src("ml_results", "ml_cmp", "ml_cbc"),
}
C["one_pager"] = {
 "meta_title": "Screening Labs by Text: $59 Visit With an NP | NPCWoods",
 "meta_description": "Not sure which blood work you need? Text Chris Woods, NP. $59 flat. I review your history and order labs where appropriate. Lab fees are separate.",
 "h1": "Blood work questions? Text Chris.",
 "lede": "I am Chris Woods, a Nurse Practitioner. Text me your age, your family history, how you feel, and what you want checked. I read it myself, tell you which screening labs make sense, and can order labs where appropriate.",
 "sticky": "Visit · $59 text · Screening labs",
 "bubbles": b("I have not had blood work in years. Where do I start?", "Text me the story. If labs make sense, I tell you which ones and why. You only pay the $59 if a text visit is the right fit."),
 "accent_block": {"h2": "Labs are a tool, not a promise", "p": "I order tests that answer a real question for you, not a long menu. Some results need a repeat, a follow-up test, or an in-person visit. I will tell you which, plainly."},
 "sections": [
  lst("How it works",
   "Text (480) 639-4722 with your age, history, symptoms, and what you want checked.",
   "I read it myself and tell you which labs make sense, and which can wait.",
   "If labs fit, I send you a lab order. You get your blood drawn at a lab.",
   "When results come back, text them to me and I walk you through them in plain words."),
  prose("What it costs",
   "My text visit is $59 flat. You only pay if a text visit is the right fit. The lab charges its own fee for the blood draw and the tests, separate from my $59."),
 ],
 "fits": {
  "yes_h": "Who often fits a text",
  "yes": ["Adults who feel well and want a screening plan", "Due for sugar or cholesterol checks", "Mild, steady symptoms like being tired for weeks", "Already have results and want them explained", "Physically in a state I can treat"],
  "no_h": "Who needs another door",
  "no": ["Chest pain, fainting, or trouble breathing: call 911", "A lab called you about a critical result", "Ongoing care for a long-term condition", "A new lump that needs a hands-on exam", "Children (their regular clinic is the right place)"],
 },
 "plain_cards": [
  {"kicker": "Stop 1", "title": "The big picture", "text": "What five common blood tests check.", "href": HUB},
  {"kicker": "Stop 4", "title": "A1c", "text": "Your three-month sugar report card.", "href": HUB + "a1c/"},
  {"kicker": "Stop 7", "title": "Who and how often", "text": "A plain schedule by age and risk.", "href": HUB + "who-and-how-often/"},
  {"kicker": "Stop 8", "title": "Reading results", "text": "What H and L flags really mean.", "href": HUB + "reading-results/"},
 ],
 "faqs": [
  {"q": "How much is the visit?", "a": "$59 flat for the text visit. You only pay if a text visit is the right fit. Lab fees are separate and set by the lab."},
  {"q": "Which labs can you order?", "a": "Common screening labs like a metabolic panel, cholesterol, A1c, thyroid, and a blood count, when they make sense for you."},
  {"q": "Do I need to fast?", "a": "Only for some tests. Your lab order will say. Cholesterol and A1c usually do not need fasting."},
  {"q": "What states?", "a": "14 states, including Florida by telehealth registration (TPAN3355). You must be in a state I can treat at the time of the visit."},
  {"q": "Can you replace my regular clinic?", "a": "No. I am a good place to start or to get a second set of eyes. Ongoing care, a hands-on exam, and cancer screenings still need a regular clinic."},
  {"q": "What if I feel really sick?", "a": "Chest pain, trouble breathing, fainting, or confusion is a 911 call, not a lab order."},
 ],
 "cta_body": "Tell me what you want checked and why. I will tell you what makes sense and what can wait.",
}
art = {
 "version": "20261124",
 "asset_base": "/learn/screening-labs/assets/",
 "cutout": {"src600": "/assets/img/people/chris-cutout-600.webp", "src900": "/assets/img/people/chris-cutout-900.webp", "width": 900, "height": 1258,
            "alt": "Chris Woods, MSN, APRN, FNP-C, AGACNP-BC, smiling with a stethoscope"},
 "pages": {
  "hub": {"ghost": "hub", "stickers": ["Hey! I'm Chris", "Let's read your gauges 🧪"], "figures": [
    {"src": "panel-lineup.svg", "width": 640, "height": 560, "after_section": 1, "alt": "Chart of five common screening tests and what each checks: metabolic panel for kidneys, liver, salts, and sugar; cholesterol for blood fats; A1c for three-month average sugar; TSH for the thyroid; CBC for red cells, white cells, and platelets.", "caption": "Five common screening tests and the question each one answers."}]},
  "metabolic-panel": {"ghost": "bars", "stickers": ["One tube, 14 numbers", "Your filters, checked ✅"], "figures": [
    {"src": "bmp-vs-cmp.svg", "width": 640, "height": 520, "after_section": 0, "alt": "Two columns comparing the basic metabolic panel with 8 tests and the comprehensive metabolic panel, which adds 6 liver and protein tests.", "caption": "The CMP is the BMP plus liver and protein numbers."}]},
  "cholesterol": {"ghost": "wave", "stickers": ["LDL drops off", "HDL hauls away 🚚"], "figures": [
    {"src": "lipid-trucks.svg", "width": 640, "height": 520, "after_section": 1, "alt": "Lipid panel targets for most adults: total cholesterol under 200, LDL under 100, HDL 40 or more for men and 50 or more for women, triglycerides under 150, all in milligrams per deciliter.", "caption": "Common targets for most adults. Your own goal depends on your full risk."}]},
  "a1c": {"ghost": "range", "stickers": ["3 months in one number", "No fasting needed 🙌"], "figures": [
    {"src": "a1c-ranges.svg", "width": 640, "height": 420, "after_section": 1, "alt": "A1c range bar: below 5.7 percent normal, 5.7 to 6.4 percent prediabetes, 6.5 percent or higher diabetes.", "caption": "A1c ranges. Diabetes is confirmed with two tests."}]},
  "thyroid": {"ghost": "butterfly", "stickers": ["High TSH = slow furnace", "Tell me your symptoms 🌡️"], "figures": [
    {"src": "tsh-thermostat.svg", "width": 640, "height": 480, "after_section": 0, "alt": "Diagram of the brain sending TSH to the thyroid. High TSH usually means an underactive thyroid. Low TSH usually means an overactive thyroid.", "caption": "TSH runs backward: high usually means slow, low usually means fast."}]},
  "cbc": {"ghost": "cells", "stickers": ["Three crews, one count", "Tired? Let's look 🩸"], "figures": [
    {"src": "cbc-crews.svg", "width": 640, "height": 480, "after_section": 0, "alt": "Three columns: red blood cells deliver oxygen, white blood cells fight germs, platelets plug leaks.", "caption": "The CBC counts the delivery crew, the defense crew, and the repair crew."}]},
  "who-and-how-often": {"ghost": "grid", "stickers": ["Not everyone needs everything", "Let's build your list 📋"], "figures": [
    {"src": "screening-schedule.svg", "width": 640, "height": 600, "after_section": 0, "alt": "Screening schedule for most adults: cholesterol every 4 to 6 years from about age 20, sugar every 3 years from 35 if carrying extra weight, hepatitis C once from 18 to 79, HIV at least once from 15 to 65.", "caption": "A plain starting schedule. Risk factors and symptoms move it earlier."}]},
  "reading-results": {"ghost": "checkx", "stickers": ["An H is a nudge, not a verdict", "Send me the page 📲"], "figures": [
    {"src": "reference-range.svg", "width": 640, "height": 420, "after_section": 0, "alt": "Bell curve showing the middle 95 percent of healthy people as the normal range, with 1 in 20 healthy people landing just outside it.", "caption": "1 in 20 healthy people lands outside the range on any single test."}]},
 },
}
(OUT / "series.json").write_text(json.dumps(series, indent=2, ensure_ascii=False) + "\n")
(OUT / "content.json").write_text(json.dumps(C, indent=1, ensure_ascii=False) + "\n")
(OUT / "art.json").write_text(json.dumps(art, indent=1, ensure_ascii=False) + "\n")
print("ok")
