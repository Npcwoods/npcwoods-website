"""Mastitis series copy (Chris's voice). Generates series.json, content.json, art.json."""
import json, pathlib
OUT = pathlib.Path(__file__).resolve().parents[2].joinpath("landing-pages", "learn", "mastitis")
OUT.mkdir(parents=True, exist_ok=True)
HUB = "/learn/mastitis/"
LIC = "14 states, including Florida by telehealth registration (TPAN3355)"
stops = [
    ("", "Mastitis Explained", "The big picture", "hub"),
    ("how-it-starts", "How mastitis starts", "How it starts", "stop"),
    ("what-it-feels-like", "What mastitis feels like", "What it feels like", "stop"),
    ("lookalikes", "Lookalikes: engorgement, clogs, and more", "Lookalikes", "stop"),
    ("comfort-at-home", "Comfort at home: what helps, what to skip", "Comfort at home", "stop"),
    ("red-flags", "Red flags: when mastitis is an emergency", "Red flags", "stop"),
    ("keep-feeding", "Can I keep breastfeeding?", "Keep feeding", "stop"),
    ("text-vs-in-person", "Text visit vs in person: who fits", "Text vs in person", "stop"),
]
series = {
    "id": "mastitis",
    "name": "Mastitis Explained",
    "kicker": "Mastitis series",
    "tagline": "A plain-talk series from Chris Woods, NP. One story. Eight stops.",
    "reviewed": "2026-11-24",
    "reviewed_display": "November 24, 2026",
    "accent": {"name": "red", "hex": "#B42318"},
    "ghost_base": "drop",
    "og_alt_suffix": "Chris Woods, NP, with a soft milk-drop outline",
    "license_line": LIC,
    "sms": {"number": "4806394722", "display": "(480) 639-4722",
            "prefill": "Hi Chris, I'm breastfeeding and think I might have mastitis. I'd like a $59 text visit."},
    "cta_band": {"heading": "Sore, red, and worn out? Text me.",
                 "body": "Tell me how many days since the birth, which side hurts, your temperature, and how you feel overall. Words are enough. No photo needed. I read it myself and tell you if this fits a text visit or needs in-person care. You only pay the $59 if I can treat you by text."},
    "hub": {"slug": "", "path": HUB, "title": "Mastitis Explained", "nav_label": "The big picture", "episode": 1},
    "one_pager": {"path": "/mastitis-treatment/", "title": "Mastitis treatment by text", "nav_label": "$59 text visit"},
    "stops": [
        {"slug": s, "path": HUB + (s + "/" if s else ""), "title": t, "nav_label": n, "episode": i + 1, "kind": k}
        for i, (s, t, n, k) in enumerate(stops)
    ],
}
SRC = {
 "abm36": ("Mitchell KB, Johnson HM, et al. Academy of Breastfeeding Medicine Clinical Protocol #36: The Mastitis Spectrum (2022). Breastfeeding Medicine.", "https://doi.org/10.1089/bfm.2022.29207.kbm"),
 "statpearls": ("Blackmon MM, Nguyen H, Mukherji P. Acute Mastitis. StatPearls, NCBI Bookshelf.", "https://www.ncbi.nlm.nih.gov/books/NBK557782/"),
 "medline": ("MedlinePlus. Breast infection.", "https://medlineplus.gov/ency/article/001490.htm"),
 "acog": ("ACOG Committee Opinion 820. Breastfeeding challenges (2021).", "https://www.acog.org/clinical/clinical-guidance/committee-opinion/articles/2021/02/breastfeeding-challenges"),
 "cdc": ("CDC. What to expect while breastfeeding.", "https://www.cdc.gov/infant-toddler-nutrition/breastfeeding/what-to-expect-while-breastfeeding.html"),
 "owh": ("Office on Women's Health. Breastfeeding challenges.", "https://womenshealth.gov/breastfeeding/breastfeeding-challenges"),
 "nci_ibc": ("National Cancer Institute. Inflammatory breast cancer.", "https://www.cancer.gov/types/breast/ibc-fact-sheet"),
 "cdc_sepsis": ("CDC. About sepsis.", "https://www.cdc.gov/sepsis/about/"),
}
def src(*keys): return [{"label": SRC[k][0], "url": SRC[k][1]} for k in keys]
def b(you, chris): return [{"style": "blue", "who": "You", "text": you}, {"style": "black", "who": "Chris", "text": chris}]
def prose(h, *body): return {"type": "prose", "heading": h, "body": list(body)}
def lst(h, *items): return {"type": "list", "heading": h, "items": list(items)}
def safety(t, body): return {"type": "callout", "kind": "safety", "title": t, "body": body}
def ink(t, body): return {"type": "callout", "kind": "ink", "title": t, "body": body}
ER = safety("Go to the ER or call 911 now",
            "A fever of 103°F or higher, red streaks spreading fast, pus or a soft, growing lump, shaking chills, a racing heart, feeling faint or confused, or feeling very sick all over. Those need in-person care today, not a text.")
C = {}
C["hub"] = {
 "meta_title": "Mastitis Explained: Symptoms, Home Care, Red Flags | NPCWoods",
 "meta_description": "Breast pain, a red wedge, and fever while breastfeeding? Chris Woods, NP, explains mastitis plainly: causes, comfort at home, and when it is urgent.",
 "h1": "Mastitis, explained plainly",
 "lede": "You are feeding a baby around the clock, and now one breast is sore, warm, and red. Maybe you feel like you have the flu. That is often mastitis. It is common, it is treatable, and it is not your fault. Let me walk you through it.",
 "bubbles": b("One side is red and hot and I feel awful. Did I do something wrong?", "No. Mastitis is swelling in busy milk tissue. It happens to careful parents all the time. Tell me your temperature and how you feel. We will make a plan."),
 "stats": [{"num": "Up to 1 in 10", "label": "breastfeeding parents get mastitis, most often in the first 6 weeks"}, {"num": "12–24 hrs", "label": "of good comfort care often shows the trend"}, {"num": "$59", "label": "flat text visit with me"}],
 "sections": [
  prose("What mastitis is",
   "Mastitis means the breast tissue is inflamed. Inflamed means swollen, warm, red, and sore. Sometimes germs join in and it becomes an infection. Experts now see it as a spectrum: from a narrowed, swollen milk duct, to inflammation, to infection, and rarely to an abscess, which is a pocket of pus.",
   "Think of a busy highway at rush hour. A fender bender narrows one lane. Traffic backs up. Tempers rise. Most jams clear with time and gentle help. A few need a tow truck."),
  lst("The usual signs",
   "A tender, warm, red or darker wedge-shaped area on one breast. On brown or black skin, redness can look darker or purple, or be hard to see.",
   "A firm or swollen spot.",
   "Body aches, chills, and feeling run down, like the flu.",
   "A temperature of 100.4°F or higher."),
  prose("The good news",
   "Most mastitis gets better with rest, gentle care, and normal feeding. Some cases need a prescription. A few need an in-person exam or an ultrasound. This series helps you tell which is which, and when to reach out."),
  ER,
  prose("How the series flows",
   "We start with how it starts, then what it feels like, then what else it could be. Then comfort care at home, the red flags, whether you can keep feeding (usually yes), and when a text visit fits. Each stop links to the next."),
 ],
 "faqs": [
  {"q": "Is mastitis an infection?", "a": "Not always. Many cases are inflammation without germs. If it does not improve in 12 to 24 hours of good comfort care, or you feel very sick, infection is more likely and you should get care."},
  {"q": "Can I keep breastfeeding with mastitis?", "a": "Usually yes. Your milk is safe for your baby. Feeding on demand helps. Stop 7 explains."},
  {"q": "How fast should I get help?", "a": "Reach out the same day if you have a fever, feel sick, or are not better after 12 to 24 hours of comfort care. Go in now for any red flag."},
  {"q": "Does mastitis mean I have to stop nursing or pumping?", "a": "No. Stopping suddenly can make it worse. Keep your usual rhythm unless a clinician tells you otherwise."},
 ],
 "sources": src("abm36", "acog", "statpearls", "medline"),
}
C["how-it-starts"] = {
 "meta_title": "How Mastitis Starts: The Swelling Spectrum | NPCWoods",
 "meta_description": "Mastitis often starts with swelling that narrows milk ducts. Chris Woods, NP, explains the mastitis spectrum and common triggers in plain words.",
 "h1": "How mastitis starts",
 "lede": "For years people blamed a plug, like a cork in a bottle. The newer picture is different. It is more about swelling squeezing the ducts than a cork stuck inside. That small shift changes what helps.",
 "bubbles": b("I thought I had a clogged duct and needed to massage it out hard.", "That is the old advice. Hard massage can bruise tissue and add swelling. Gentle is the new rule. More on that in Stop 5."),
 "sections": [
  prose("Swelling squeezes the straws",
   "Your milk ducts are like soft straws. When the tissue around them swells, it pinches the straws narrow. Milk moves slower. Pressure builds. The area gets more swollen. That loop is how a sore spot can turn into a hot, red wedge.",
   "Squeezing harder does not fix a pinched straw. Calming the swelling does."),
  lst("The mastitis spectrum",
   "Narrowed duct: a tender lump, no fever, you feel fine.",
   "Inflammatory mastitis: a red, warm wedge, often with fever and aches.",
   "Bacterial mastitis: inflammation plus germs. Usually slower to improve.",
   "Abscess: a walled-off pocket of pus. Needs an ultrasound and often drainage.",
   "Galactocele: a milk-filled cyst. Usually painless."),
  lst("Common triggers",
   "Making a lot more milk than the baby takes, often from extra pumping.",
   "Long gaps between feeds, like the first night baby sleeps longer.",
   "A shallow latch or cracked nipples, which let germs in.",
   "A tight bra, bag strap, or sleeping position pressing on one spot.",
   "Stress, poor sleep, and being run down. Which is every new parent."),
  ink("Oversupply is a big one",
   "Pumping after every feed to empty the breast can tell your body to make even more. More milk means more fullness and more swelling. Feed the baby, not the freezer, unless your clinician or lactation consultant says otherwise."),
  ER,
 ],
 "faqs": [
  {"q": "Is mastitis caused by bad hygiene?", "a": "No. It is about swelling, milk flow, and sometimes skin germs that live on all of us. It is not about being unclean."},
  {"q": "Can I get mastitis if I am only pumping?", "a": "Yes. Pumping parents get it too, especially with high pump settings or pumping more than the baby needs."},
  {"q": "Can mastitis happen months later?", "a": "Yes, though it is most common in the first 6 weeks. Weaning fast or a sudden schedule change can trigger it later."},
 ],
 "sources": src("abm36", "statpearls"),
}
C["what-it-feels-like"] = {
 "meta_title": "Mastitis Symptoms: What It Feels Like | NPCWoods",
 "meta_description": "Red, warm wedge, breast pain, fever, chills, and aches. Chris Woods, NP, explains mastitis symptoms and what to watch hour by hour.",
 "h1": "What mastitis feels like",
 "lede": "Most parents describe two things at once: one sore spot on the breast, and feeling like the flu hit out of nowhere. The whole-body part can come first. If you feel sick and one breast is tender, think mastitis.",
 "bubbles": b("I have chills and aches. Is it the flu or my breast?", "Could be either, and the breast is often the answer. Check for a warm, sore wedge. Take your temperature. Text me both."),
 "sections": [
  lst("In the breast",
   "A tender, warm area, often wedge-shaped, usually on one side.",
   "Red, pink, or darker skin. On deeper skin tones, it may look purple or brown, or barely change color. Warmth and pain still count.",
   "A firm or swollen area.",
   "Pain or burning while feeding."),
  lst("In the body",
   "Fever of 100.4°F or higher.",
   "Chills, body aches, headache.",
   "Feeling wiped out, more than the usual new-parent tired."),
  prose("Track the trend",
   "Write down your temperature and how big the red area is, morning and night. A pen line around the edge of the redness helps you see if it is shrinking or spreading. Improving over 12 to 24 hours of comfort care is a good sign. Getting worse is your cue to reach out."),
  ink("Look and feel, not just look",
   "On brown or black skin, redness can be hard to see. Trust warmth, pain, swelling, and how you feel. Tell me your skin tone looks different or darker there. That is useful."),
  ER,
 ],
 "faqs": [
  {"q": "Can I have mastitis with no fever?", "a": "Yes. Early or mild inflammation may have no fever. A fever with a sore breast makes mastitis more likely."},
  {"q": "Both breasts are sore. Is that mastitis?", "a": "Both sides sore and full is more often engorgement. Mastitis in both breasts at once is less common and needs prompt care."},
  {"q": "My nipple has a white dot. Is that related?", "a": "That may be a milk bleb, a tiny blister at a duct opening. It can go along with a sore area. Avoid picking it. Tell me about it."},
 ],
 "sources": src("abm36", "medline", "owh"),
}
C["lookalikes"] = {
 "meta_title": "Mastitis vs Engorgement vs Clogged Duct | NPCWoods",
 "meta_description": "Engorgement, narrowed ducts, nipple damage, abscess, and rare lookalikes. Chris Woods, NP, explains how they differ from mastitis.",
 "h1": "Lookalikes: engorgement, clogs, and more",
 "lede": "A sore breast while feeding has a short list of causes. Most are common and calm down with care. One or two need an exam. Here is how I sort them.",
 "bubbles": b("Both sides feel like rocks on day 3. Is that mastitis?", "That sounds like engorgement: milk coming in. Both sides, full, tight. Usually no fever spike. It eases in a day or two."),
 "sections": [
  lst("The usual suspects",
   "Engorgement: both breasts full, firm, and tender, often days 2 to 5 after birth. Low fever at most.",
   "Narrowed duct: a tender lump in one spot. No fever. You feel fine.",
   "Mastitis: a red or warm wedge, often fever and flu-like aches.",
   "Nipple damage: cracks, scabs, or pain mostly at the nipple from latch trouble.",
   "Milk bleb: a tiny white dot on the nipple tip, sharp pain while feeding."),
  lst("Less common, need an exam",
   "Abscess: a lump that stays or grows, feels soft or squishy, sometimes with pus. Needs an ultrasound and often drainage.",
   "Galactocele: a milk-filled cyst. Smooth, usually not painful.",
   "Inflammatory breast cancer: rare, but it can look like mastitis. Redness and swelling over a large area, skin that looks pitted like an orange peel, and no fever. It does not get better with mastitis care."),
  ink("When redness does not fit",
   "Redness and swelling that is not getting better after a week or so of care, shows up when you are not breastfeeding, or comes with orange-peel skin needs a hands-on exam and imaging. Not to scare you. To be sure."),
  ER,
 ],
 "faqs": [
  {"q": "How do I tell engorgement from mastitis?", "a": "Engorgement is usually both sides, full all over, early on. Mastitis is usually one side, a hot wedge, often with fever and aches."},
  {"q": "Can a narrowed duct turn into mastitis?", "a": "It can, as swelling builds. Gentle care early helps keep it from moving down the spectrum."},
  {"q": "I am not breastfeeding and my breast is red. Is it mastitis?", "a": "It can happen, but it is less common and needs an in-person exam to rule out other causes."},
 ],
 "sources": src("abm36", "statpearls", "nci_ibc"),
}
C["comfort-at-home"] = {
 "meta_title": "Mastitis Comfort Care at Home: What Helps | NPCWoods",
 "meta_description": "Feed on demand, ice, gentle touch, and rest. Chris Woods, NP, explains comfort care for mastitis and the old habits to skip. General education.",
 "h1": "Comfort at home: what helps, what to skip",
 "lede": "This is general education, not a personal plan. A lot of old advice made swelling worse: hard massage, heat, pumping to empty. The newer approach is gentler. Treat it like a sprained ankle: calm the swelling, and keep things moving.",
 "bubbles": b("Everyone says hot showers and deep massage. Is that right?", "Not anymore. Cold helps swelling. Gentle, feather-light strokes toward the armpit. Feed like normal. Let's keep it calm."),
 "sections": [
  lst("What often helps",
   "Feed your baby on demand from both sides, the way you normally would.",
   "Cold packs or ice wrapped in a thin cloth, a few minutes at a time, between feeds.",
   "Feather-light strokes from the nipple toward the armpit, like petting a cat. This helps fluid drain.",
   "A supportive bra that is not tight. Skip underwire for now.",
   "Rest, fluids, and food. Let someone else handle everything that is not the baby.",
   "An over-the-counter pain and swelling reliever that is okay while breastfeeding. Ask your pharmacist which one fits you."),
  lst("What to skip",
   "Deep or hard massage. It can bruise tissue and add swelling.",
   "Heat packs and long hot soaks. Heat can increase swelling.",
   "Pumping extra to fully empty the breast. It can boost supply and feed the cycle.",
   "Stopping feeds on the sore side suddenly.",
   "Picking or poking a white dot on the nipple."),
  prose("Give it 12 to 24 hours, and watch",
   "If you feel better, the redness is shrinking, and any fever is coming down, keep going. If you are not improving after 12 to 24 hours, or you are getting worse, reach out the same day. That is when a clinician should take a look."),
  ink("A lactation consultant is gold",
   "If latch, pain, or supply keep causing trouble, an IBCLC (a board-certified lactation consultant) can watch a feed and fix the root problem. Many hospitals and WIC offices can connect you."),
  ER,
 ],
 "faqs": [
  {"q": "Should I use heat or cold?", "a": "Cold. Newer guidance favors cold for swelling. A brief warm compress right before a feed is okay if it helps let-down, but skip long heat."},
  {"q": "Should I pump after every feed to empty the breast?", "a": "Usually no. Extra pumping can make more milk and more swelling. Feed the baby on demand."},
  {"q": "What pain reliever can I take while breastfeeding?", "a": "Several common over-the-counter options are considered compatible with breastfeeding. Your pharmacist can help you pick one that fits your health history."},
 ],
 "sources": src("abm36", "acog", "owh"),
}
C["red-flags"] = {
 "meta_title": "Mastitis Red Flags: When It Is an Emergency | NPCWoods",
 "meta_description": "High fever, spreading red streaks, pus, a growing lump, or feeling very sick. Chris Woods, NP, lists when mastitis needs in-person or ER care.",
 "h1": "Red flags: when mastitis is an emergency",
 "lede": "Most mastitis is miserable and still manageable. A few cases spread, form an abscess, or tip into a body-wide infection called sepsis. I want this list on your fridge. If you meet it, you do not text me first. You go.",
 "bubbles": b("My fever is 103 and I'm shaking. Should I text you?", "No. Go to the ER now or call 911. A high fever with shaking chills needs in-person care tonight."),
 "sections": [
  safety("Go to the ER or call 911 now",
   "A fever of 103°F or higher. Red streaks spreading fast toward the armpit or chest. Shaking chills that will not stop. A racing heart or fast breathing. Feeling faint, dizzy, or confused. Feeling very sick all over. Those are not text-visit problems."),
  lst("Get in-person care today",
   "Pus draining from the breast or nipple.",
   "A soft, squishy, or growing lump: possible abscess. It needs an ultrasound.",
   "Redness spreading even with care.",
   "Both breasts red and hot at the same time.",
   "Not better after 48 hours of treatment.",
   "A weak immune system, diabetes, or a recent breast surgery."),
  prose("Why spreading matters",
   "Infection that spreads into skin and tissue can move fast. Sepsis is the body overreacting to an infection. Early signs are fever or feeling cold, a fast heartbeat, fast breathing, confusion, and extreme pain or discomfort. Sepsis is an emergency. Do not wait for morning."),
  prose("What a text visit is not for",
   "I will not talk you out of the ER. If your story sounds like any of the above, I send you in. You do not pay the $59 when I tell you text care is not safe."),
 ],
 "faqs": [
  {"q": "My fever is 101 and one breast is red. ER or text?", "a": "If you feel okay otherwise, can eat and drink, and the redness is not spreading fast, that often fits a same-day text visit. If you feel very sick, faint, or confused, go in now."},
  {"q": "How do I know if it is an abscess?", "a": "A lump that stays or grows, feels soft or fluid-filled, or drains pus. It needs an ultrasound, and often drainage with a needle."},
  {"q": "Should I stop breastfeeding if I go to the ER?", "a": "Usually no. Tell the ER team you are breastfeeding so they can choose care that fits."},
 ],
 "sources": src("abm36", "cdc_sepsis", "statpearls"),
}
C["keep-feeding"] = {
 "meta_title": "Can I Breastfeed With Mastitis? | NPCWoods",
 "meta_description": "Yes, usually. Your milk is safe for your baby, and normal feeding helps. Chris Woods, NP, explains breastfeeding with mastitis plainly.",
 "h1": "Can I keep breastfeeding?",
 "lede": "Short answer: yes, almost always. Your milk is still safe for your baby, even with mastitis. Keeping your normal rhythm helps your breast heal. Stopping suddenly can make it worse.",
 "bubbles": b("Will my milk make the baby sick?", "No. Your milk is safe. Babies are used to the germs on your skin. Keep feeding like normal, from both sides."),
 "sections": [
  prose("Why feeding helps",
   "Milk that keeps moving keeps pressure down. Pressure is what feeds the swelling loop. Your baby is the gentlest pump there is. If the sore side hurts, start on the other side and switch once let-down begins."),
  lst("Make feeding easier",
   "Try different holds so the baby's chin points toward the sore spot.",
   "Feed on demand. No need to empty the breast or add extra pumping.",
   "If your milk tastes saltier, some babies fuss. Keep offering. It passes.",
   "If baby will not feed on that side, hand express just enough to feel comfortable."),
  prose("If you need a prescription",
   "Many medicines are compatible with breastfeeding. If a prescription fits your case, I choose options that are considered safe while nursing, and I tell you what to watch for in your baby. A text visit is not a promise of a prescription. I only prescribe when it is the right call."),
  ink("Weaning? Go slow",
   "If you were planning to wean, wait until the mastitis settles, then taper slowly. Stopping fast is a common trigger."),
  ER,
 ],
 "faqs": [
  {"q": "Can I pump and dump instead?", "a": "There is usually no need. Your milk is safe for your baby during mastitis."},
  {"q": "What if there is pus or blood in the milk?", "a": "Pus means you need an in-person exam today. A little blood can come from cracked nipples. Tell your clinician either way."},
  {"q": "My baby is sick too. What now?", "a": "Call your baby's clinic. Babies under 3 months with a fever of 100.4°F or higher need care right away."},
 ],
 "sources": src("abm36", "cdc", "acog"),
}
C["text-vs-in-person"] = {
 "meta_title": "Mastitis: Text Visit vs In-Person Care | NPCWoods",
 "meta_description": "Who fits a $59 text visit for mastitis and who needs in-person care. Chris Woods, NP, explains plainly. You only pay if text care fits.",
 "h1": "Text visit vs in person: who fits",
 "lede": "A lot of mastitis can be handled by text: a clear story, a clear plan, and a clear list of when to go in. Some cases need hands and an ultrasound. Here is how I decide.",
 "bubbles": b("I have a newborn and no sitter. Can we do this by text?", "If your story fits, yes. That is exactly who I built this for. If it doesn't, I will say so and point you to the right door."),
 "sections": [
  lst("Often a good fit for text",
   "Breastfeeding or pumping, one breast sore, warm, red, or swollen.",
   "Fever under 103°F, and you can eat, drink, and think clearly.",
   "No pus, no soft or growing lump, no fast-spreading streaks.",
   "You are an adult, physically in a state I can treat at the time of the visit."),
  lst("Needs in-person care",
   "Any red flag from Stop 6.",
   "A lump that stays, grows, or feels soft: needs an ultrasound.",
   "Not better after 48 hours of treatment, or back again and again.",
   "Red, swollen breast when you are not breastfeeding.",
   "A weak immune system or a recent breast surgery."),
  prose("How a text visit works",
   "You text (480) 639-4722 with your story: how old the baby is, which side, when it started, your temperature, how you feel, your health history, and anything you are allergic to. I read it myself. If text care fits, I give you a clear plan, and if a prescription is the right call, I send it to your pharmacy. If not, I tell you where to go. You only pay the $59 if I can treat you by text."),
  ER,
 ],
 "faqs": [
  {"q": "Do I need to send a photo?", "a": "No. Words are enough to start. Temperature, which side, how big the red area is, and how you feel tell me a lot."},
  {"q": "What if I get worse after the visit?", "a": "Use the red-flag list. Go in for any of them. For slower worsening, text me and we decide next steps."},
  {"q": "What states?", "a": "14 states, including Florida by telehealth registration (TPAN3355). You need to be physically in one of them at the time of the visit."},
 ],
 "sources": src("abm36", "acog"),
}
C["one_pager"] = {
 "meta_title": "Mastitis Treatment by Text: $59 Visit With an NP | NPCWoods",
 "meta_description": "Breastfeeding with a sore, red, warm breast and fever? Text Chris Woods, NP. $59 flat. You only pay if text care fits. Red flags go to the ER.",
 "h1": "Sore, red breast while feeding? Text Chris.",
 "lede": "I am Chris Woods, a Nurse Practitioner. Mastitis is common, it is not your fault, and a lot of it can be handled from your couch with the baby on your chest. Text me your story. I will tell you if you fit a text visit, or if you need in-person care today.",
 "sticky": "Visit · $59 text · Mastitis",
 "bubbles": b("Day 12 postpartum. Left side hot, red, and I'm achy. 101 fever.", "Thank you for the details. Are you eating and drinking okay? Any pus or a soft lump? Let's figure out your plan."),
 "accent_block": {"h2": "A text visit is not a promise of a prescription", "p": "Many cases calm down with good comfort care. Some need a prescription, and I only send one when it fits. Some need an exam or an ultrasound. I will tell you which, plainly, and you only pay the $59 if I can treat you by text."},
 "sections": [
  lst("How it works",
   "Text (480) 639-4722 with your story: baby's age, which side, when it started, your temperature, how you feel, and your health history.",
   "I read it myself and ask follow-up questions.",
   "If text care fits, you get a clear plan. If a prescription is the right call, I send it to your pharmacy, choosing options considered safe while breastfeeding.",
   "If it does not fit, I tell you where to go. You do not pay."),
 ],
 "fits": {
  "yes_h": "Who often fits a text",
  "yes": ["Breastfeeding or pumping adults", "One sore, warm, red, or swollen area", "Fever under 103°F, eating and drinking okay", "No pus, no soft or growing lump", "Physically in a state I can treat"],
  "no_h": "Who needs another door",
  "no": ["Fever of 103°F or higher, shaking chills", "Red streaks spreading fast, pus, or a growing lump", "Faint, confused, or very sick: call 911", "Not breastfeeding with a red, swollen breast", "Not better after 48 hours of treatment"],
 },
 "plain_cards": [
  {"kicker": "Stop 1", "title": "The big picture", "text": "What mastitis is, and why it is not your fault.", "href": HUB},
  {"kicker": "Stop 5", "title": "Comfort at home", "text": "Cold, gentle, and keep feeding. What to skip.", "href": HUB + "comfort-at-home/"},
  {"kicker": "Stop 6", "title": "Red flags", "text": "When this is an emergency, not a text.", "href": HUB + "red-flags/"},
  {"kicker": "Stop 7", "title": "Keep feeding", "text": "Your milk is safe. Why feeding helps.", "href": HUB + "keep-feeding/"},
 ],
 "faqs": [
  {"q": "How much is the visit?", "a": "$59 flat. You only pay if I can treat you by text."},
  {"q": "Do I need to send a photo?", "a": "No. A text with words only is fine. Your temperature, which side, how big the sore area is, and how you feel tell me a lot."},
  {"q": "Will I get medicine?", "a": "Only if it is the right call. Many cases improve with comfort care. If a prescription fits, I choose options considered safe while breastfeeding."},
  {"q": "Can I keep breastfeeding?", "a": "Usually yes. Your milk is safe for your baby, and feeding helps you heal."},
  {"q": "What states?", "a": "14 states, including Florida by telehealth registration (TPAN3355). You must be in a state I can treat at the time of the visit."},
  {"q": "When do I skip this page and go to the ER?", "a": "Fever of 103°F or higher, shaking chills, fast-spreading red streaks, pus, a growing lump, or feeling faint, confused, or very sick. Call 911 or go now."},
 ],
 "cta_body": "Tell me what is going on. I will tell you if I am the right door, and if I am not, where to go.",
}
art = {
 "version": "20261124",
 "asset_base": "/learn/mastitis/assets/",
 "cutout": {"src600": "/assets/img/people/chris-cutout-600.webp", "src900": "/assets/img/people/chris-cutout-900.webp", "width": 900, "height": 1258,
            "alt": "Chris Woods, MSN, APRN, FNP-C, AGACNP-BC, smiling with a stethoscope"},
 "pages": {
  "hub": {"ghost": "hub", "stickers": ["Hey! I'm Chris", "Not your fault. Let's fix it 💛"], "figures": [
    {"src": "mastitis-spectrum.svg", "after_section": 0, "alt": "The mastitis spectrum from mild to serious: narrowed duct, inflammatory mastitis, bacterial mastitis, and abscess.", "caption": "Mastitis is a spectrum. Most cases stay near the top of it."}]},
  "how-it-starts": {"ghost": "rings", "stickers": ["Swelling pinches the straws", "Gentle beats hard 🧊"], "figures": [
    {"src": "swelling-loop.svg", "after_section": 0, "alt": "Swelling loop: tissue swells, ducts narrow, milk slows, pressure builds, more swelling. Calming the swelling breaks the loop.", "caption": "Calm the swelling and the loop starts to break."}]},
  "what-it-feels-like": {"ghost": "wave", "stickers": ["Flu feeling + sore spot", "Take your temp 🌡️"], "figures": [
    {"src": "symptom-map.svg", "after_section": 1, "alt": "Two lists. In the breast: warm, tender wedge, red or darker skin, firm area, pain while feeding. In the body: fever 100.4 or higher, chills, aches, wiped out.", "caption": "One sore spot plus flu-like aches is the classic pair."}]},
  "lookalikes": {"ghost": "checkx", "stickers": ["Both sides? Often engorgement", "One hot wedge? Think mastitis"], "figures": [
    {"src": "lookalikes-table.svg", "after_section": 0, "alt": "Comparison: engorgement affects both sides early on; narrowed duct is a tender lump without fever; mastitis is a hot red wedge with fever; abscess is a lump that stays or grows and needs an ultrasound.", "caption": "Quick sort for a sore breast while feeding."}]},
  "comfort-at-home": {"ghost": "path", "stickers": ["Cold, not hot 🧊", "Feed like normal"], "figures": [
    {"src": "comfort-do-skip.svg", "after_section": 1, "alt": "Two lists. Helps: feed on demand, cold packs, feather-light strokes toward the armpit, supportive bra, rest. Skip: deep massage, long heat, extra pumping, stopping feeds suddenly.", "caption": "Gentle care that calms swelling. General education, not a personal plan."}]},
  "red-flags": {"ghost": "warning", "stickers": ["103°F? Go now", "The ER beats a text here"], "figures": [
    {"src": "red-flags-er.svg", "after_section": 0, "alt": "Red warning list: fever 103 or higher, spreading red streaks, pus or a growing lump, shaking chills, racing heart, faint or confused. Go to the ER or call 911.", "caption": "Any of these? Skip the text. Go to the ER or call 911."}]},
  "keep-feeding": {"ghost": "loop", "stickers": ["Your milk is safe 🍼", "Keep your rhythm"], "figures": [
    {"src": "feeding-tips.svg", "after_section": 1, "alt": "Feeding tips: start on the comfortable side, point the baby's chin toward the sore spot, feed on demand, no extra pumping, hand express just for comfort.", "caption": "Small changes that make feeding easier while you heal."}]},
  "text-vs-in-person": {"ghost": "split", "stickers": ["Right door, right care", "Text me the story 📲"], "figures": [
    {"src": "text-vs-in-person.svg", "after_section": 1, "alt": "Two doors. Text visit: one sore red area, fever under 103, eating and drinking, no pus or lump. In person or ER: any red flag, a growing lump, not better after 48 hours, not breastfeeding.", "caption": "Where your story fits. When in doubt, go in."}]},
 },
}
(OUT / "series.json").write_text(json.dumps(series, indent=2, ensure_ascii=False) + "\n")
(OUT / "content.json").write_text(json.dumps(C, indent=1, ensure_ascii=False) + "\n")
(OUT / "art.json").write_text(json.dumps(art, indent=1, ensure_ascii=False) + "\n")
print("ok")
