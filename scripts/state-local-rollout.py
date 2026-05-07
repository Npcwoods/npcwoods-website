#!/usr/bin/env python3
"""
state-local-rollout.py — Inject local hero + context + map + city cards + review band
into static state landing pages, then SFTP-upload.

Idempotent: reads from .pre-local.bak (created on first run); subsequent runs
re-splice from the pristine source. Re-running is safe.

Anchors on bounded HTML comment markers (not style tags). Validates:
- 30% size-shrink guard
- banned-word grep (doctor, insurance bare)
- HERO/CITIES blocks must be found before splicing

Usage:
    state-local-rollout.py --state az            # one state, splice + SFTP
    state-local-rollout.py --state az --dry-run  # local splice only
    state-local-rollout.py --all                 # all 11 states
    state-local-rollout.py --all --dry-run
"""
import argparse, os, re, sys, shutil
from pathlib import Path

REPO = Path('/Users/chriswoods/Desktop/Chris-HQ/npcwoods-website')
LANDING = REPO / 'landing-pages'

# ───────────────────────────── per-state config ──────────────────────────────
# Each state has: slug (folder + url), name, abbr, hero copy, hero image url,
# local-context cards, city pin coords on a 480x520 viewbox, city cards,
# real google review (or skip), top-stats.

STATES = {
    'az': {
        'slug': 'arizona-telemedicine',
        'name': 'Arizona', 'abbr': 'AZ',
        'hero_image': 'https://npcwoods.com/wp-content/uploads/2026/05/az-hero.png',
        'hero_caption': 'Sonoran Desert &mdash; Phoenix on the horizon',
        'hero_h1': 'UTI, sinus, strep <em>in Arizona?</em><br>Text Chris. $59. Same day.',
        'hero_lede': 'Real prescription, real nurse practitioner, no waiting room. From Phoenix to Tucson, Mesa to Surprise &mdash; if you&rsquo;re in Arizona right now, you can be picking up your antibiotic tonight.',
        'kicker': 'Licensed in Arizona &middot; Async telehealth approved',
        'population_eligible': '7.4M',
        'cities_count': '10+',
        'context_kicker': 'What we see most in Arizona',
        'context_title': 'The desert plays by <em>different rules.</em>',
        'context_sub': 'Three patterns we treat constantly across the state &mdash; whether you&rsquo;re a year-round Phoenix resident or a snowbird wintering in Scottsdale.',
        'context_cards': [
            {'cls': 'heat',  'title': 'Heat &amp; dehydration', 'body': 'UTIs spike when water intake drops. We see this every July, especially in Phoenix and Tucson when daytime temps stay above 110&deg;F.', 'tags': 'UTI &middot; dehydration headaches'},
            {'cls': 'dust',  'title': 'Dust &amp; dry sinuses', 'body': 'Monsoon dust storms + bone-dry winters = chronic sinus pressure that flips into bacterial infection. Don&rsquo;t white-knuckle it.', 'tags': 'Sinus infection &middot; dry-air bronchitis'},
            {'cls': 'snow',  'title': 'Snowbird season',       'body': 'You winter here, your primary care is back home. We can refill bridge medications and treat acute stuff without a return flight.', 'tags': 'UTI &middot; sinus &middot; ED &middot; GLP-1 continuity'},
        ],
        'map_kicker': 'Where Chris&rsquo;s patients text from',
        'map_title': 'Every corner of Arizona &mdash; from the Strip to the Rim.',
        'map_body': 'Async telehealth means you can be standing at a Costco in Goodyear or sitting on a porch in Bisbee. As long as you&rsquo;re physically in Arizona at the time of the visit, we can treat you.',
        'pins': [
            # name, x, y, primary?, pop_label
            ('Phoenix',   195, 320, True,  '1.6M residents'),
            ('Mesa',      232, 328, False, None),
            ('Scottsdale',222, 306, False, None),
            ('Surprise',  158, 296, False, None),
            ('Tucson',    240, 430, True,  '550K residents'),
            ('Flagstaff', 220, 140, False, None),
            ('Yuma',       80, 430, False, None),
            ('Prescott',  170, 200, False, None),
            ('Sedona',    195, 170, False, None),
            ('Havasu',     80, 220, False, None),
        ],
        'cities': [
            ('Mesa',       '~510K residents', 'UTI &middot; sinus &middot; strep',                         'https://npcwoods.com/uti-treatment/mesa-az/'),
            ('Scottsdale', '~241K residents', 'GLP-1 &middot; UTI &middot; ED',                            'https://npcwoods.com/uti-treatment/scottsdale-az/'),
            ('Surprise',   '~143K residents', 'UTI &middot; dental pain &middot; sinus',                   'https://npcwoods.com/uti-treatment/surprise-az/'),
            ('Phoenix',    '~1.6M residents', 'UTI &middot; sinus &middot; dehydration',                   None),
            ('Tucson',     '~550K residents', 'sinus &middot; UTI &middot; ear infection',                 None),
            ('Chandler',   '~280K residents', 'UTI &middot; strep &middot; pink eye',                      None),
            ('Gilbert',    '~268K residents', 'strep (kids over 12) &middot; UTI &middot; sinus',          None),
            ('Tempe',      '~180K residents', 'UTI &middot; STI screening &middot; strep',                 None),
            ('Peoria',     '~190K residents', 'UTI &middot; sinus &middot; bronchitis',                    None),
        ],
        'review': {
            'name': 'Sarah K.',
            'city': 'Phoenix, AZ',
            'quote': 'Texted my symptoms at 9pm. Prescription at my pharmacy by 9am. I&rsquo;ve never had healthcare be this easy.',
            'mark': 'A real review from <em>Phoenix</em>.',
            'sub': 'Not a marketing stock quote. Pulled from Google. Click to verify.',
            'href': 'https://share.google/XlmNvRT4vihOJ8KBH',
        },
    },
    'co': {
        'slug': 'colorado-telemedicine',
        'name': 'Colorado', 'abbr': 'CO',
        'hero_image': 'https://npcwoods.com/wp-content/uploads/2026/05/co-hero.png',
        'hero_caption': 'Colorado Rockies &mdash; Denver on the horizon',
        'hero_h1': 'UTI, sinus, strep <em>in Colorado?</em><br>Text Chris. $59. Same day.',
        'hero_lede': 'Real prescription, real nurse practitioner, no waiting room. Whether you&rsquo;re in Denver, Boulder, the Springs, or a mountain town &mdash; if you&rsquo;re in Colorado right now, we can get you treated tonight.',
        'kicker': 'Licensed in Colorado &middot; Async telehealth',
        'population_eligible': '5.8M', 'cities_count': '10+',
        'context_kicker': 'What we see most in Colorado',
        'context_title': 'Altitude and dry air <em>change everything.</em>',
        'context_sub': 'Three patterns we treat constantly across the state &mdash; from Front Range city dwellers to ski-town locals.',
        'context_cards': [
            {'cls': 'cool', 'title': 'Altitude &amp; dehydration', 'body': 'Higher elevation = drier mucous membranes + less perceived thirst. UTIs and sinus infections spike here.', 'tags': 'UTI &middot; sinus pressure'},
            {'cls': 'fog',  'title': 'Wildfire smoke',           'body': 'Late-summer smoke drifts into the Front Range and irritates airways. Bronchitis flares up early.', 'tags': 'Bronchitis &middot; sinus &middot; cough'},
            {'cls': 'snow', 'title': 'Mountain weekend warriors','body': 'Ski-trip lacerations and minor skin infections happen far from a clinic. We can start antibiotics by text while you drive home.', 'tags': 'Skin infection &middot; UTI'},
        ],
        'map_kicker': 'Where Chris&rsquo;s patients text from',
        'map_title': 'Front Range to the Western Slope.',
        'map_body': 'Async telehealth means you can be in a Denver high-rise or a cabin near Telluride. As long as you&rsquo;re physically in Colorado, we can treat you.',
        'pins': [
            ('Denver',          255, 250, True,  '716K residents'),
            ('Colorado Springs',255, 340, True,  '480K residents'),
            ('Aurora',          280, 250, False, None),
            ('Fort Collins',    255, 130, False, None),
            ('Lakewood',        225, 250, False, None),
            ('Boulder',         225, 175, False, None),
            ('Greeley',         300, 160, False, None),
            ('Pueblo',          280, 410, False, None),
            ('Grand Junction',   90, 280, False, None),
            ('Durango',         140, 430, False, None),
        ],
        'cities': [
            ('Denver',           '~716K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Colorado Springs', '~480K residents', 'sinus &middot; UTI &middot; strep', None),
            ('Aurora',           '~395K residents', 'UTI &middot; bronchitis &middot; sinus', None),
            ('Fort Collins',     '~170K residents', 'strep (college) &middot; UTI', None),
            ('Lakewood',         '~155K residents', 'UTI &middot; sinus &middot; pink eye', None),
            ('Boulder',          '~108K residents', 'UTI &middot; sinus &middot; GLP-1', None),
            ('Pueblo',           '~111K residents', 'UTI &middot; sinus &middot; dental pain', None),
            ('Grand Junction',    '~67K residents', 'sinus &middot; UTI &middot; bronchitis', None),
            ('Durango',           '~19K residents', 'UTI &middot; sinus &middot; skin infection', None),
        ],
        'review': None,
    },
    'ga': {
        'slug': 'georgia-telemedicine',
        'name': 'Georgia', 'abbr': 'GA',
        'hero_image': 'https://npcwoods.com/wp-content/uploads/2026/05/ga-hero.png',
        'hero_caption': 'Georgia pine forest &mdash; Atlanta in the distance',
        'hero_h1': 'UTI, sinus, strep <em>in Georgia?</em><br>Text Chris. $59. Same day.',
        'hero_lede': 'Real prescription, real nurse practitioner, no waiting room. From Atlanta to Savannah, Athens to Augusta &mdash; if you&rsquo;re in Georgia right now, you can be picking up your antibiotic today.',
        'kicker': 'Licensed in Georgia &middot; Async telehealth',
        'population_eligible': '10.8M', 'cities_count': '10+',
        'context_kicker': 'What we see most in Georgia',
        'context_title': 'Humid heat plays by <em>different rules.</em>',
        'context_sub': 'Three patterns we treat constantly across the state &mdash; from city to college town to coast.',
        'context_cards': [
            {'cls': 'heat',  'title': 'Heat &amp; humidity',   'body': 'Heat rashes flip into bacterial skin infections fast. We catch a lot of folate in summer.', 'tags': 'Skin infection &middot; UTI'},
            {'cls': 'green', 'title': 'Pollen &amp; allergies','body': 'Atlanta&rsquo;s spring pollen is legendary &mdash; and chronic sinus pressure quickly turns bacterial.', 'tags': 'Sinus infection &middot; allergies'},
            {'cls': 'cool',  'title': 'College town strep',    'body': 'Athens, Statesboro, Macon &mdash; sore throats spread fast in dorms. Strep over text in the same day.', 'tags': 'Strep throat &middot; sinus'},
        ],
        'map_kicker': 'Where Chris&rsquo;s patients text from',
        'map_title': 'Atlanta to the coast &mdash; treated where you stand.',
        'map_body': 'Async telehealth means you can be in a Buckhead condo or a Tybee Island rental. As long as you&rsquo;re physically in Georgia, we can treat you.',
        'pins': [
            ('Atlanta',         195, 195, True,  '498K residents'),
            ('Savannah',        385, 410, True,  '147K residents'),
            ('Augusta',         350, 245, False, None),
            ('Columbus',        130, 320, False, None),
            ('Macon',           240, 280, False, None),
            ('Athens',          250, 165, False, None),
            ('Roswell',         195, 165, False, None),
            ('Sandy Springs',   195, 175, False, None),
            ('Albany',          195, 380, False, None),
            ('Valdosta',        265, 440, False, None),
        ],
        'cities': [
            ('Atlanta',       '~498K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Savannah',      '~147K residents', 'sinus &middot; UTI &middot; skin infection', None),
            ('Augusta',       '~202K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Columbus',      '~206K residents', 'UTI &middot; strep &middot; pink eye', None),
            ('Macon',         '~157K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Athens',         '~127K residents', 'strep (college) &middot; UTI', None),
            ('Roswell',         '~95K residents', 'UTI &middot; sinus &middot; GLP-1', None),
            ('Sandy Springs',  '~108K residents', 'UTI &middot; sinus &middot; dental pain', None),
            ('Valdosta',        '~55K residents', 'UTI &middot; sinus &middot; strep', None),
        ],
        'review': None,
    },
    'id': {
        'slug': 'idaho-telemedicine',
        'name': 'Idaho', 'abbr': 'ID',
        'hero_image': 'https://npcwoods.com/wp-content/uploads/2026/05/id-hero.png',
        'hero_caption': 'Sawtooth Mountains &mdash; Boise valley below',
        'hero_h1': 'UTI, sinus, strep <em>in Idaho?</em><br>Text Chris. $59. Same day.',
        'hero_lede': 'Real prescription, real nurse practitioner, no waiting room. Boise, Coeur d&rsquo;Alene, Idaho Falls &mdash; if you&rsquo;re in Idaho right now, we can get you treated without a 60-mile drive.',
        'kicker': 'Licensed in Idaho &middot; Async telehealth',
        'population_eligible': '1.9M', 'cities_count': '10+',
        'context_kicker': 'What we see most in Idaho',
        'context_title': 'Distance to a clinic <em>shouldn&rsquo;t cost you a day.</em>',
        'context_sub': 'Three patterns we treat constantly across the state &mdash; rural, suburban, and outdoor.',
        'context_cards': [
            {'cls': 'cool',  'title': 'High desert dryness',  'body': 'Boise basin and the Snake River plain are bone-dry. Sinus pressure becomes bacterial before you notice.', 'tags': 'Sinus infection &middot; UTI'},
            {'cls': 'fog',   'title': 'Wildfire smoke',       'body': 'Summer smoke drifting in from western fires triggers cough that won&rsquo;t quit. We start antibiotics when it&rsquo;s appropriate.', 'tags': 'Bronchitis &middot; sinus'},
            {'cls': 'snow',  'title': 'Outdoor weekend',      'body': 'Hunting trips, river runs, ski weekends &mdash; far from a clinic when something flares. Text us before you drive home.', 'tags': 'Skin infection &middot; UTI'},
        ],
        'map_kicker': 'Where Chris&rsquo;s patients text from',
        'map_title': 'Treasure Valley to the Panhandle.',
        'map_body': 'Async telehealth in Idaho means you can be in a Boise office or a cabin near Stanley. As long as you&rsquo;re physically in Idaho, we can treat you.',
        'pins': [
            ('Boise',         195, 350, True,  '237K residents'),
            ("Coeur d'Alene", 200, 100, True,  '56K residents'),
            ('Meridian',      170, 350, False, None),
            ('Nampa',         150, 360, False, None),
            ('Idaho Falls',   330, 330, False, None),
            ('Pocatello',     310, 380, False, None),
            ('Twin Falls',    220, 410, False, None),
            ('Caldwell',      135, 350, False, None),
            ('Post Falls',    200, 110, False, None),
            ('Lewiston',      150, 160, False, None),
        ],
        'cities': [
            ('Boise',         '~237K residents', 'UTI &middot; sinus &middot; strep', None),
            ("Coeur d'Alene", '~56K residents',  'sinus &middot; UTI &middot; bronchitis', None),
            ('Meridian',      '~134K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Nampa',         '~106K residents', 'UTI &middot; sinus &middot; dental pain', None),
            ('Idaho Falls',    '~67K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Pocatello',      '~57K residents', 'sinus &middot; UTI &middot; skin infection', None),
            ('Twin Falls',     '~56K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Caldwell',       '~62K residents', 'UTI &middot; sinus &middot; pink eye', None),
            ('Lewiston',       '~33K residents', 'UTI &middot; sinus &middot; bronchitis', None),
        ],
        'review': None,
    },
    'ia': {
        'slug': 'iowa-telemedicine',
        'name': 'Iowa', 'abbr': 'IA',
        'hero_image': 'https://npcwoods.com/wp-content/uploads/2026/05/ia-hero.png',
        'hero_caption': 'Iowa farmland &mdash; Des Moines in the distance',
        'hero_h1': 'UTI, sinus, strep <em>in Iowa?</em><br>Text Chris. $59. Same day.',
        'hero_lede': 'Real prescription, real nurse practitioner, no waiting room. Des Moines, Cedar Rapids, Iowa City, Davenport &mdash; if you&rsquo;re in Iowa, we can get you treated tonight.',
        'kicker': 'Licensed in Iowa &middot; Async telehealth',
        'population_eligible': '3.2M', 'cities_count': '10+',
        'context_kicker': 'What we see most in Iowa',
        'context_title': 'Rural distance <em>shouldn&rsquo;t mean rural care.</em>',
        'context_sub': 'Three patterns we treat constantly across the state &mdash; urban, college, and rural.',
        'context_cards': [
            {'cls': 'green', 'title': 'Ag belt + tick season', 'body': 'Field work and farm life mean cuts and tick bites. Cellulitis catches up fast &mdash; we can start treatment by text.', 'tags': 'Skin infection &middot; UTI'},
            {'cls': 'cool',  'title': 'Cold-month bronchitis', 'body': 'Iowa winter dryness + indoor heating dries out airways. Bronchitis stretches into bacterial infection.', 'tags': 'Bronchitis &middot; sinus'},
            {'cls': 'snow',  'title': 'College town strep',    'body': 'Iowa City, Ames, Cedar Falls &mdash; dorm strep spreads fast. Text-in, antibiotic out by tonight.', 'tags': 'Strep throat &middot; sinus'},
        ],
        'map_kicker': 'Where Chris&rsquo;s patients text from',
        'map_title': 'From Des Moines to the Driftless.',
        'map_body': 'Async telehealth means you can be on a Des Moines block or a farm outside Decorah. As long as you&rsquo;re physically in Iowa, we can treat you.',
        'pins': [
            ('Des Moines',    220, 290, True,  '215K residents'),
            ('Cedar Rapids',  310, 245, True,  '136K residents'),
            ('Davenport',     360, 295, False, None),
            ('Sioux City',     90, 240, False, None),
            ('Iowa City',     325, 285, False, None),
            ('Ames',          230, 235, False, None),
            ('Waterloo',      290, 200, False, None),
            ('Council Bluffs', 80, 320, False, None),
            ('Dubuque',       370, 195, False, None),
            ('Cedar Falls',   285, 195, False, None),
        ],
        'cities': [
            ('Des Moines',    '~215K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Cedar Rapids',  '~136K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Davenport',     '~101K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Sioux City',     '~85K residents', 'UTI &middot; sinus &middot; skin infection', None),
            ('Iowa City',      '~75K residents', 'strep (college) &middot; UTI', None),
            ('Ames',           '~67K residents', 'strep (college) &middot; sinus &middot; UTI', None),
            ('Waterloo',       '~67K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Council Bluffs', '~63K residents', 'UTI &middot; sinus &middot; dental pain', None),
            ('Dubuque',        '~59K residents', 'UTI &middot; sinus &middot; bronchitis', None),
        ],
        'review': None,
    },
    'mt': {
        'slug': 'montana-telemedicine',
        'name': 'Montana', 'abbr': 'MT',
        'hero_image': 'https://npcwoods.com/wp-content/uploads/2026/05/mt-hero.png',
        'hero_caption': 'Big Sky country &mdash; Glacier on the horizon',
        'hero_h1': 'UTI, sinus, strep <em>in Montana?</em><br>Text Chris. $59. Same day.',
        'hero_lede': 'Real prescription, real nurse practitioner, no waiting room. Billings, Bozeman, Missoula &mdash; if you&rsquo;re in Montana, you don&rsquo;t need to drive an hour to get treated.',
        'kicker': 'Licensed in Montana &middot; Async telehealth',
        'population_eligible': '1.1M', 'cities_count': '10+',
        'context_kicker': 'What we see most in Montana',
        'context_title': 'Distance is the disease <em>amplifier.</em>',
        'context_sub': 'Three patterns we treat constantly across Big Sky &mdash; rural, mountain, and college.',
        'context_cards': [
            {'cls': 'cool',  'title': 'Cold-air bronchitis',  'body': 'Sub-zero winters dry out airways and turn coughs into bacterial bronchitis. Don&rsquo;t white-knuckle it.', 'tags': 'Bronchitis &middot; sinus'},
            {'cls': 'snow',  'title': 'Outdoor injury',       'body': 'Skiing, hunting, hiking &mdash; small wounds get big when the nearest clinic is 90 minutes away.', 'tags': 'Skin infection &middot; UTI'},
            {'cls': 'green', 'title': 'College town strep',   'body': 'Bozeman, Missoula, Billings &mdash; dorms and bars are strep factories. Text in, antibiotic out same day.', 'tags': 'Strep throat &middot; sinus'},
        ],
        'map_kicker': 'Where Chris&rsquo;s patients text from',
        'map_title': 'Helena to the Hi-Line &mdash; we cover it all.',
        'map_body': 'Async telehealth in Montana means you can be in a Bozeman coffee shop or a ranch outside Glasgow. As long as you&rsquo;re physically in Montana, we can treat you.',
        'pins': [
            ('Billings',     290, 350, True,  '117K residents'),
            ('Missoula',     120, 200, True,   '76K residents'),
            ('Great Falls',  230, 175, False, None),
            ('Bozeman',      210, 330, False, None),
            ('Butte',        180, 305, False, None),
            ('Helena',       195, 240, False, None),
            ('Kalispell',    115, 130, False, None),
            ('Belgrade',     205, 325, False, None),
            ('Havre',        260, 110, False, None),
            ('Anaconda',     170, 295, False, None),
        ],
        'cities': [
            ('Billings',    '~117K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Missoula',     '~76K residents', 'strep (college) &middot; sinus &middot; UTI', None),
            ('Great Falls',  '~60K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Bozeman',      '~57K residents', 'strep (college) &middot; UTI &middot; sinus', None),
            ('Butte',        '~34K residents', 'UTI &middot; sinus &middot; skin infection', None),
            ('Helena',       '~34K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Kalispell',    '~30K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Havre',        '~10K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Anaconda',      '~9K residents', 'UTI &middot; sinus &middot; skin infection', None),
        ],
        'review': None,
    },
    'nv': {
        'slug': 'nevada-telemedicine',
        'name': 'Nevada', 'abbr': 'NV',
        'hero_image': 'https://npcwoods.com/wp-content/uploads/2026/05/nv-hero.png',
        'hero_caption': 'Mojave + Spring Mountains &mdash; Las Vegas on the horizon',
        'hero_h1': 'UTI, sinus, strep <em>in Nevada?</em><br>Text Chris. $59. Same day.',
        'hero_lede': 'Real prescription, real nurse practitioner, no waiting room. Las Vegas, Henderson, Reno &mdash; if you&rsquo;re in Nevada, we can get you treated without sitting in a Strip-area urgent care.',
        'kicker': 'Licensed in Nevada &middot; Async telehealth',
        'population_eligible': '3.2M', 'cities_count': '10+',
        'context_kicker': 'What we see most in Nevada',
        'context_title': 'Heat, hotels, and <em>hauling water.</em>',
        'context_sub': 'Three patterns we treat constantly across the state &mdash; resident, traveler, and high-altitude.',
        'context_cards': [
            {'cls': 'heat', 'title': 'Desert dehydration',   'body': 'Vegas in July is brutal &mdash; UTIs spike in dehydrated patients within 24 hours of arriving.', 'tags': 'UTI &middot; dehydration'},
            {'cls': 'dust', 'title': 'Strip-pool sinus',     'body': 'Pool chlorine + AC + dry desert air = chronic sinus pressure that flips bacterial.', 'tags': 'Sinus infection &middot; UTI'},
            {'cls': 'cool', 'title': 'Reno mountain weather','body': 'Reno-Tahoe altitude + ski-trip exposure means more sinus, bronchitis, and skin infections.', 'tags': 'Bronchitis &middot; skin infection'},
        ],
        'map_kicker': 'Where Chris&rsquo;s patients text from',
        'map_title': 'Las Vegas Valley to the Truckee Meadows.',
        'map_body': 'Async telehealth means you can be on the Strip or in a Reno suburb. As long as you&rsquo;re physically in Nevada, we can treat you.',
        'pins': [
            ('Las Vegas',  220, 410, True, '660K residents'),
            ('Henderson',  240, 425, False, None),
            ('Reno',       110, 130, True,  '264K residents'),
            ('North Las Vegas', 215, 395, False, None),
            ('Sparks',     115, 130, False, None),
            ('Carson City',125, 165, False, None),
            ('Elko',       290, 130, False, None),
            ('Mesquite',   305, 380, False, None),
            ('Pahrump',    170, 380, False, None),
            ('Fallon',     145, 175, False, None),
        ],
        'cities': [
            ('Las Vegas',       '~660K residents', 'UTI &middot; sinus &middot; STI screening', None),
            ('Henderson',       '~322K residents', 'UTI &middot; sinus &middot; GLP-1', None),
            ('Reno',            '~264K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('North Las Vegas', '~262K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Sparks',          '~110K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Carson City',      '~58K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Elko',             '~20K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Mesquite',         '~21K residents', 'UTI &middot; sinus &middot; dental pain', None),
            ('Pahrump',          '~44K residents', 'UTI &middot; sinus &middot; skin infection', None),
        ],
        'review': {
            'name': 'Rachel D.',
            'city': 'Reno, NV',
            'quote': 'Urgent care would&rsquo;ve been 4 hours and $300. This was 40 minutes and $59. I&rsquo;m not going back.',
            'mark': 'A real review from <em>Reno</em>.',
            'sub': 'Not a marketing stock quote. Pulled from Google. Click to verify.',
            'href': 'https://share.google/XlmNvRT4vihOJ8KBH',
        },
    },
    'nm': {
        'slug': 'new-mexico-telemedicine',
        'name': 'New Mexico', 'abbr': 'NM',
        'hero_image': 'https://npcwoods.com/wp-content/uploads/2026/05/nm-hero.png',
        'hero_caption': 'High desert mesa &mdash; Albuquerque balloons in flight',
        'hero_h1': 'UTI, sinus, strep <em>in New Mexico?</em><br>Text Chris. $59. Same day.',
        'hero_lede': 'Real prescription, real nurse practitioner, no waiting room. From Albuquerque to Santa Fe, Las Cruces to Farmington &mdash; if you&rsquo;re in New Mexico, we can treat you tonight.',
        'kicker': 'Licensed in New Mexico &middot; Async telehealth',
        'population_eligible': '2.1M', 'cities_count': '10+',
        'context_kicker': 'What we see most in New Mexico',
        'context_title': 'High desert, <em>high stakes for sinuses.</em>',
        'context_sub': 'Three patterns we treat constantly across the state.',
        'context_cards': [
            {'cls': 'heat', 'title': 'Altitude + dust',     'body': 'Albuquerque sits over 5,000 ft. Dry mucous membranes + dust storms = sinus infections that fester quickly.', 'tags': 'Sinus infection &middot; UTI'},
            {'cls': 'dust', 'title': 'Sun + heat exposure', 'body': 'Las Cruces and Santa Teresa run hot. UTIs spike when water intake drops &mdash; we treat both.', 'tags': 'UTI &middot; dehydration'},
            {'cls': 'cool', 'title': 'Pueblo &amp; rural distance', 'body': 'Pueblos and small towns can be 60+ miles from a clinic. Text-in care is faster and easier.', 'tags': 'UTI &middot; sinus &middot; skin infection'},
        ],
        'map_kicker': 'Where Chris&rsquo;s patients text from',
        'map_title': 'From the Sandias to the Bootheel.',
        'map_body': 'Async telehealth means you can be in an ABQ apartment or a hogan in Window Rock. As long as you&rsquo;re physically in New Mexico, we can treat you.',
        'pins': [
            ('Albuquerque',   210, 240, True,  '562K residents'),
            ('Las Cruces',    195, 410, True,  '111K residents'),
            ('Rio Rancho',    195, 220, False, None),
            ('Santa Fe',      230, 195, False, None),
            ('Roswell',       310, 340, False, None),
            ('Farmington',    140, 110, False, None),
            ('Hobbs',         360, 360, False, None),
            ('Clovis',        360, 285, False, None),
            ('Carlsbad',      310, 410, False, None),
            ('Alamogordo',    230, 380, False, None),
        ],
        'cities': [
            ('Albuquerque',  '~562K residents', 'UTI &middot; sinus &middot; strep', 'https://npcwoods.com/uti-treatment/albuquerque-nm/'),
            ('Las Cruces',   '~111K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Rio Rancho',    '~99K residents', 'UTI &middot; sinus &middot; pink eye', None),
            ('Santa Fe',      '~88K residents', 'UTI &middot; sinus &middot; GLP-1', None),
            ('Roswell',       '~48K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Farmington',    '~46K residents', 'UTI &middot; sinus &middot; skin infection', None),
            ('Hobbs',         '~40K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Clovis',        '~38K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Alamogordo',    '~31K residents', 'UTI &middot; sinus &middot; dental pain', None),
        ],
        'review': None,
    },
    'nc': {
        'slug': 'north-carolina-telemedicine',
        'name': 'North Carolina', 'abbr': 'NC',
        'hero_image': 'https://npcwoods.com/wp-content/uploads/2026/05/nc-hero.png',
        'hero_caption': 'Blue Ridge Mountains &mdash; Charlotte at the horizon',
        'hero_h1': 'UTI, sinus, strep <em>in North Carolina?</em><br>Text Chris. $59. Same day.',
        'hero_lede': 'Real prescription, real nurse practitioner, no waiting room. Charlotte, Raleigh, Asheville, Wilmington &mdash; if you&rsquo;re in NC, we can get you treated tonight.',
        'kicker': 'Licensed in North Carolina &middot; Async telehealth',
        'population_eligible': '10.7M', 'cities_count': '10+',
        'context_kicker': 'What we see most in North Carolina',
        'context_title': 'Mountains, Piedmont, coast &mdash; <em>same care, different conditions.</em>',
        'context_sub': 'Three patterns we treat constantly across the state &mdash; urban, college, and outdoor.',
        'context_cards': [
            {'cls': 'green', 'title': 'Tick + skin season',  'body': 'Hiking the Blue Ridge or working a yard in summer &mdash; tick bites and skin infections need fast antibiotics.', 'tags': 'Skin infection &middot; UTI'},
            {'cls': 'heat',  'title': 'Coast humidity',       'body': 'Wilmington and the OBX in August: heat rashes flip bacterial fast. We catch them by text.', 'tags': 'Skin infection &middot; sinus'},
            {'cls': 'cool',  'title': 'College + research',   'body': 'Chapel Hill, Durham, Raleigh, Charlotte &mdash; dorm and office strep spreads fast. Same-day treatment.', 'tags': 'Strep throat &middot; sinus'},
        ],
        'map_kicker': 'Where Chris&rsquo;s patients text from',
        'map_title': 'Asheville to Wilmington &mdash; treated where you stand.',
        'map_body': 'Async telehealth means you can be in a Raleigh office or a beach rental in Nags Head. As long as you&rsquo;re physically in NC, we can treat you.',
        'pins': [
            ('Charlotte',    150, 380, True,  '897K residents'),
            ('Raleigh',      330, 290, True,  '467K residents'),
            ('Greensboro',   250, 250, False, None),
            ('Durham',       310, 270, False, None),
            ('Winston-Salem',230, 240, False, None),
            ('Fayetteville', 320, 380, False, None),
            ('Cary',         310, 290, False, None),
            ('Wilmington',   380, 430, False, None),
            ('Asheville',     85, 290, False, None),
            ('High Point',   240, 260, False, None),
        ],
        'cities': [
            ('Charlotte',    '~897K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Raleigh',      '~467K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Greensboro',   '~302K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Durham',       '~291K residents', 'strep (college) &middot; UTI', None),
            ('Winston-Salem','~250K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Fayetteville', '~209K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Cary',         '~177K residents', 'UTI &middot; sinus &middot; GLP-1', None),
            ('Wilmington',   '~117K residents', 'UTI &middot; sinus &middot; skin infection', None),
            ('Asheville',     '~94K residents', 'UTI &middot; sinus &middot; bronchitis', None),
        ],
        'review': None,
    },
    'or': {
        'slug': 'oregon-telemedicine',
        'name': 'Oregon', 'abbr': 'OR',
        'hero_image': 'https://npcwoods.com/wp-content/uploads/2026/05/or-hero.png',
        'hero_caption': 'Cascade range &mdash; Portland in the mist',
        'hero_h1': 'UTI, sinus, strep <em>in Oregon?</em><br>Text Chris. $59. Same day.',
        'hero_lede': 'Real prescription, real nurse practitioner, no waiting room. Portland, Salem, Eugene, Bend &mdash; if you&rsquo;re in Oregon, we can get you treated without leaving the house.',
        'kicker': 'Licensed in Oregon &middot; Async telehealth',
        'population_eligible': '4.3M', 'cities_count': '10+',
        'context_kicker': 'What we see most in Oregon',
        'context_title': 'Damp PNW + dry East &mdash; <em>two states in one.</em>',
        'context_sub': 'Three patterns we treat constantly across Oregon &mdash; valley, coast, and high desert.',
        'context_cards': [
            {'cls': 'fog',   'title': 'Damp + recurrent sinus', 'body': 'Willamette Valley winters are wet for months. Recurrent sinus infections are our most-treated condition here.', 'tags': 'Sinus infection &middot; bronchitis'},
            {'cls': 'cool',  'title': 'Wildfire smoke',         'body': 'Late-summer smoke shuts down outdoor life. Cough that won&rsquo;t quit + fever = time to text.', 'tags': 'Bronchitis &middot; sinus'},
            {'cls': 'snow',  'title': 'Outdoor + ski',          'body': 'Mt. Hood, Bend, the Coast Range &mdash; small wounds get big fast. Text us before driving back to town.', 'tags': 'Skin infection &middot; UTI'},
        ],
        'map_kicker': 'Where Chris&rsquo;s patients text from',
        'map_title': 'Portland Metro to the High Desert.',
        'map_body': 'Async telehealth means you can be in a Pearl District loft or a yurt outside Sisters. As long as you&rsquo;re physically in Oregon, we can treat you.',
        'pins': [
            ('Portland',   165, 130, True,  '635K residents'),
            ('Salem',      150, 200, True,  '177K residents'),
            ('Eugene',     150, 270, False, None),
            ('Gresham',    180, 130, False, None),
            ('Hillsboro',  140, 130, False, None),
            ('Beaverton',  150, 135, False, None),
            ('Bend',       290, 250, False, None),
            ('Medford',    160, 380, False, None),
            ('Springfield',155, 270, False, None),
            ('Corvallis',  140, 235, False, None),
        ],
        'cities': [
            ('Portland',     '~635K residents', 'sinus &middot; UTI &middot; bronchitis', None),
            ('Salem',        '~177K residents', 'sinus &middot; UTI &middot; strep', None),
            ('Eugene',       '~178K residents', 'strep (college) &middot; sinus &middot; UTI', None),
            ('Gresham',      '~111K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Hillsboro',     '~99K residents', 'UTI &middot; sinus &middot; GLP-1', None),
            ('Beaverton',     '~97K residents', 'UTI &middot; sinus &middot; pink eye', None),
            ('Bend',          '~99K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Medford',       '~85K residents', 'UTI &middot; sinus &middot; bronchitis', None),
            ('Springfield',   '~63K residents', 'UTI &middot; sinus &middot; strep', None),
        ],
        'review': None,
    },
    'ut': {
        'slug': 'utah-telemedicine',
        'name': 'Utah', 'abbr': 'UT',
        'hero_image': 'https://npcwoods.com/wp-content/uploads/2026/05/ut-hero.png',
        'hero_caption': 'Red rock canyon &mdash; the Wasatch Front beyond',
        'hero_h1': 'UTI, sinus, strep <em>in Utah?</em><br>Text Chris. $59. Same day.',
        'hero_lede': 'Real prescription, real nurse practitioner, no waiting room. Salt Lake, Provo, St. George, Park City &mdash; if you&rsquo;re in Utah, we can get you treated without an in-person visit.',
        'kicker': 'Licensed in Utah &middot; Async telehealth',
        'population_eligible': '3.4M', 'cities_count': '10+',
        'context_kicker': 'What we see most in Utah',
        'context_title': 'High altitude, high desert &mdash; <em>conditions stack up.</em>',
        'context_sub': 'Three patterns we treat constantly across the Beehive State.',
        'context_cards': [
            {'cls': 'heat',  'title': 'Altitude + dryness',  'body': 'SLC sits over 4,200 ft. Dry mucous membranes + dehydration accelerate UTIs and sinus infections.', 'tags': 'UTI &middot; sinus'},
            {'cls': 'snow',  'title': 'Ski + winter sport',  'body': 'Park City, Sundance, Snowbird &mdash; weekend warriors text us about wounds, sinus, and sore throats.', 'tags': 'Skin infection &middot; sinus'},
            {'cls': 'fog',   'title': 'Inversion bronchitis','body': 'Wasatch Front winter inversions trap pollutants. Bronchitis flares hard from January through March.', 'tags': 'Bronchitis &middot; sinus'},
        ],
        'map_kicker': 'Where Chris&rsquo;s patients text from',
        'map_title': 'Wasatch Front to red rock country.',
        'map_body': 'Async telehealth means you can be in a SLC apartment or a campground near Moab. As long as you&rsquo;re physically in Utah, we can treat you.',
        'pins': [
            ('Salt Lake City',195, 175, True,  '200K residents'),
            ('West Valley',   175, 180, False, None),
            ('Provo',         195, 250, True,  '116K residents'),
            ('West Jordan',   180, 200, False, None),
            ('Orem',          200, 240, False, None),
            ('Sandy',         200, 195, False, None),
            ('Ogden',         195, 130, False, None),
            ('St. George',    140, 430, False, None),
            ('Layton',        195, 140, False, None),
            ('Park City',     230, 175, False, None),
        ],
        'cities': [
            ('Salt Lake City','~200K residents', 'UTI &middot; sinus &middot; strep', None),
            ('West Valley',  '~140K residents', 'UTI &middot; sinus &middot; pink eye', None),
            ('Provo',        '~116K residents', 'strep (college) &middot; UTI &middot; sinus', None),
            ('West Jordan',  '~117K residents', 'UTI &middot; sinus &middot; strep', None),
            ('Orem',         '~98K residents',  'strep (college) &middot; UTI &middot; sinus', None),
            ('Sandy',        '~94K residents',  'UTI &middot; sinus &middot; GLP-1', None),
            ('Ogden',        '~87K residents',  'UTI &middot; sinus &middot; bronchitis', None),
            ('St. George',   '~99K residents',  'UTI &middot; sinus &middot; dental pain', None),
            ('Park City',    '~8K residents',   'sinus &middot; UTI &middot; skin infection', None),
        ],
        'review': {
            'name': 'Marcus T.',
            'city': 'Salt Lake City, UT',
            'quote': 'I expected a chatbot. Got a real NP who read my history and asked good questions. Worth ten times $59.',
            'mark': 'A real review from <em>Salt Lake City</em>.',
            'sub': 'Not a marketing stock quote. Pulled from Google. Click to verify.',
            'href': 'https://share.google/XlmNvRT4vihOJ8KBH',
        },
    },
}

# ──────────────────────────── HTML builders ──────────────────────────────

COMPONENT_CSS = """\
<style id="local-rollout-css">
  /* Local-rollout components — added 2026-05-04 */
  .nl-cream{ --nl-cream:#FDF8F4; --nl-cream-2:#F5EFE7; --nl-line:#E6DED3;
            --nl-line-2:#EFE7DA; --nl-ink:#1A1A2E; --nl-ink-soft:#3B3B52;
            --nl-muted:#6B6B7B; --nl-brand:#2563EB; --nl-brand-ink:#1D4ED8;
            --nl-coral:#C2614F; --nl-sage:#5B7553; --nl-sage-soft:#E6F0E0;
            --nl-coral-soft:#FBEDE8; --nl-amber:#F59E0B; --nl-amber-soft:#FEF3C7; }
  .nl-wrap{max-width:1180px;margin:0 auto;padding:0 28px}
  .nl-kicker{display:inline-block;font-size:12.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--nl-brand);margin-bottom:14px;font-family:'Inter',sans-serif}
  .nl-hero{background:var(--nl-cream);padding:64px 0 80px;border-bottom:1px solid var(--nl-line);font-family:'Inter',sans-serif;color:var(--nl-ink)}
  .nl-hero .nl-grid{display:grid;grid-template-columns:1.1fr 1fr;gap:56px;align-items:center}
  .nl-hero h1{font-family:'Source Serif 4','Source Serif Pro',Georgia,serif;font-weight:600;font-size:clamp(40px,5.4vw,68px);line-height:1.05;letter-spacing:-.025em;margin:14px 0 20px;color:var(--nl-ink)}
  .nl-hero h1 em{font-style:normal;color:var(--nl-brand);font-weight:700}
  .nl-hero .nl-lede{font-size:19px;color:var(--nl-ink-soft);max-width:540px;margin:0 0 28px;line-height:1.5}
  .nl-cta{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-bottom:30px}
  .nl-btn{display:inline-flex;align-items:center;gap:10px;padding:16px 28px;border-radius:10px;font-weight:600;font-size:16px;border:1px solid transparent;text-decoration:none;transition:transform .15s,box-shadow .15s,background .15s}
  .nl-btn-cta{background:var(--nl-brand);color:#fff;border-color:var(--nl-brand)}
  .nl-btn-cta:hover{background:var(--nl-brand-ink);transform:translateY(-1px);box-shadow:0 14px 30px -12px rgba(37,99,235,.5);color:#fff}
  .nl-btn-out{background:transparent;color:var(--nl-ink);border:1px solid var(--nl-ink)}
  .nl-btn-out:hover{background:var(--nl-ink);color:var(--nl-cream)}
  .nl-trust{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;padding-top:22px;border-top:1px solid var(--nl-line)}
  .nl-pill{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border-radius:999px;background:#fff;border:1px solid var(--nl-line);font-size:13.5px;color:var(--nl-ink-soft);font-weight:500}
  .nl-pill svg{width:14px;height:14px;color:var(--nl-brand);flex:none}
  .nl-card{background:#fff;border:1px solid var(--nl-line);border-radius:18px;box-shadow:0 28px 60px -32px rgba(26,26,46,.28),0 6px 16px -10px rgba(26,26,46,.12);padding:6px;position:relative;overflow:hidden}
  .nl-card .nl-photo{border-radius:14px;overflow:hidden;position:relative;aspect-ratio:1376/768}
  .nl-card .nl-photo img{width:100%;height:100%;object-fit:cover;display:block}
  .nl-card .nl-photo::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,26,46,0) 60%,rgba(26,26,46,.45));pointer-events:none}
  .nl-card .nl-cap{position:absolute;left:18px;bottom:14px;color:#fff;font-family:'Source Serif 4',Georgia,serif;font-style:italic;font-size:18px;letter-spacing:-.01em;text-shadow:0 2px 12px rgba(0,0,0,.4)}
  .nl-card .nl-stamp{position:absolute;top:14px;right:14px;background:rgba(253,248,244,.92);border:1px solid var(--nl-line);border-radius:999px;padding:6px 12px;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--nl-ink);display:inline-flex;align-items:center;gap:8px}
  .nl-card .nl-stamp .nl-dot{width:8px;height:8px;border-radius:50%;background:var(--nl-sage);box-shadow:0 0 0 4px var(--nl-sage-soft)}
  .nl-card .nl-meta{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:var(--nl-line-2);border-radius:0 0 12px 12px;margin-top:6px;overflow:hidden}
  .nl-card .nl-meta div{background:#fff;padding:14px 16px}
  .nl-card .nl-meta b{font-family:'Source Serif 4',Georgia,serif;font-size:18px;display:block;color:var(--nl-ink);letter-spacing:-.01em}
  .nl-card .nl-meta span{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--nl-muted)}
  .nl-local{padding:64px 0;border-bottom:1px solid var(--nl-line);background:var(--nl-cream);font-family:'Inter',sans-serif;color:var(--nl-ink)}
  .nl-local-head{text-align:center;max-width:640px;margin:0 auto 36px}
  .nl-local-head h2{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:clamp(28px,3.8vw,42px);line-height:1.1;letter-spacing:-.02em;margin:0 0 12px;color:var(--nl-ink)}
  .nl-local-head h2 em{color:var(--nl-coral);font-style:normal;font-weight:700}
  .nl-local-head p{color:var(--nl-ink-soft);font-size:17px;margin:0;line-height:1.55}
  .nl-local-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
  .nl-ctx{background:#fff;border:1px solid var(--nl-line);border-radius:14px;padding:24px 22px;display:flex;flex-direction:column;gap:10px}
  .nl-ctx .nl-ic{width:44px;height:44px;border-radius:10px;display:inline-flex;align-items:center;justify-content:center;margin-bottom:6px}
  .nl-ctx.heat .nl-ic{background:#FBEDE8;color:var(--nl-coral)}
  .nl-ctx.dust .nl-ic{background:#FEF3C7;color:#92400E}
  .nl-ctx.snow .nl-ic{background:#E6F4F1;color:#0E7C7B}
  .nl-ctx.cool .nl-ic{background:#DBEAFE;color:#1D4ED8}
  .nl-ctx.green .nl-ic{background:#DCFCE7;color:#15803D}
  .nl-ctx.fog .nl-ic{background:#E0E7EF;color:#4338CA}
  .nl-ctx h3{font-family:'Source Serif 4',Georgia,serif;font-size:20px;margin:0;font-weight:600;letter-spacing:-.01em;color:var(--nl-ink)}
  .nl-ctx p{font-size:14.5px;color:var(--nl-ink-soft);margin:0;line-height:1.55}
  .nl-ctx .nl-who{margin-top:auto;display:flex;align-items:center;gap:8px;padding-top:14px;border-top:1px dashed var(--nl-line);font-size:13px;color:var(--nl-muted)}
  .nl-map-sec{padding:80px 0;border-bottom:1px solid var(--nl-line);background:var(--nl-cream-2);font-family:'Inter',sans-serif;color:var(--nl-ink)}
  .nl-map-grid{display:grid;grid-template-columns:0.95fr 1.05fr;gap:48px;align-items:center}
  .nl-map-copy h2{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:clamp(28px,3.6vw,40px);line-height:1.1;letter-spacing:-.02em;margin:14px 0 14px;color:var(--nl-ink)}
  .nl-map-copy p{font-size:17px;color:var(--nl-ink-soft);max-width:480px;margin:0 0 22px;line-height:1.55}
  .nl-map-stats{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:24px;max-width:440px}
  .nl-map-stats .nl-stat{background:#fff;border:1px solid var(--nl-line);border-radius:12px;padding:14px 16px}
  .nl-map-stats .nl-stat .nl-n{font-family:'Source Serif 4',Georgia,serif;font-weight:700;font-size:26px;letter-spacing:-.01em;color:var(--nl-ink);line-height:1.05}
  .nl-map-stats .nl-stat .nl-l{font-size:12px;color:var(--nl-muted);margin-top:4px;letter-spacing:.04em;text-transform:uppercase}
  .nl-map-svg{background:#fff;border:1px solid var(--nl-line);border-radius:18px;padding:30px;box-shadow:0 28px 60px -36px rgba(26,26,46,.28)}
  .nl-map-svg svg{width:100%;height:auto;display:block}
  .nl-map-svg .nl-cap{font-size:13px;color:var(--nl-muted);text-align:center;margin-top:14px;letter-spacing:.04em}
  .nl-cities{padding:80px 0;border-bottom:1px solid var(--nl-line);background:var(--nl-cream);font-family:'Inter',sans-serif;color:var(--nl-ink)}
  .nl-city-head{text-align:center;max-width:620px;margin:0 auto 36px}
  .nl-city-head h2{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:clamp(28px,3.6vw,40px);line-height:1.1;letter-spacing:-.02em;margin:0 0 12px;color:var(--nl-ink)}
  .nl-city-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
  .nl-city{background:#fff;border:1px solid var(--nl-line);border-radius:14px;padding:22px;text-decoration:none;color:inherit;transition:transform .18s,box-shadow .18s,border-color .18s;display:flex;flex-direction:column;gap:10px}
  .nl-city:hover{transform:translateY(-3px);box-shadow:0 22px 50px -28px rgba(26,26,46,.3);border-color:#D7DDE8}
  .nl-city .nl-row{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
  .nl-city h3{font-family:'Source Serif 4',Georgia,serif;font-size:24px;margin:0;font-weight:600;letter-spacing:-.01em;color:var(--nl-ink)}
  .nl-city .nl-pop{font-size:12px;color:var(--nl-muted);letter-spacing:.06em;text-transform:uppercase}
  .nl-city .nl-top{margin-top:auto;padding-top:14px;border-top:1px dashed var(--nl-line);font-size:13.5px;color:var(--nl-ink-soft)}
  .nl-city .nl-top b{color:var(--nl-ink);font-weight:600}
  .nl-city .nl-arrow{color:var(--nl-brand);font-weight:700;font-size:18px;line-height:1}
  .nl-review{padding:60px 0;background:var(--nl-ink);color:var(--nl-cream);font-family:'Inter',sans-serif}
  .nl-review .nl-rg{display:grid;grid-template-columns:1fr 1.4fr;gap:40px;align-items:center}
  .nl-review h2{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:clamp(28px,3.6vw,40px);line-height:1.1;letter-spacing:-.02em;margin:0;color:#fff}
  .nl-review h2 em{color:#FCA5A5;font-style:normal;font-weight:700}
  .nl-review .nl-rsub{margin-top:14px;color:rgba(253,248,244,.7);font-size:15px;line-height:1.5;max-width:380px}
  .nl-review .nl-quote{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:24px 26px;text-decoration:none;color:inherit;display:block}
  .nl-review .nl-stars{color:#FCD34D;font-size:18px;letter-spacing:2px;margin-bottom:8px}
  .nl-review .nl-quote p{font-family:'Source Serif 4',Georgia,serif;font-size:18px;line-height:1.5;font-style:italic;margin:0 0 14px;color:#fff}
  .nl-review .nl-rwho{display:flex;align-items:center;gap:10px;font-size:13px;color:rgba(253,248,244,.7);flex-wrap:wrap}
  .nl-via{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;background:rgba(255,255,255,.06);border-radius:999px;font-size:12px;color:#cbd5e1}
  .nl-via svg{width:14px;height:14px}
  @media (max-width:880px){
    .nl-hero .nl-grid,.nl-map-grid,.nl-review .nl-rg{grid-template-columns:1fr;gap:32px}
    .nl-local-grid,.nl-city-grid{grid-template-columns:1fr 1fr}
  }
  @media (max-width:560px){
    .nl-local-grid,.nl-city-grid{grid-template-columns:1fr}
    .nl-card .nl-meta{grid-template-columns:1fr}
  }
</style>
"""

GOOGLE_LOGO_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.99.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.1c-.22-.66-.35-1.36-.35-2.1s.13-1.44.35-2.1V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.83z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.83c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>'

CONTEXT_ICONS = {
    'heat': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="6.34" y2="6.34"/><line x1="17.66" y1="17.66" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="6.34" y2="17.66"/><line x1="17.66" y1="6.34" x2="19.07" y2="4.93"/></svg>',
    'dust': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9.59 4.59A2 2 0 1 1 11 8H2"/><path d="M17.73 2.27A2.5 2.5 0 1 1 19.5 6.5H2"/><path d="M14.05 19.41A1.5 1.5 0 1 0 15.5 22H2"/></svg>',
    'snow': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h2l1.5-9 3 18 3-12 2 6h6"/></svg>',
    'cool': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 17.58A5 5 0 0 0 18 8h-1.26A8 8 0 1 0 4 16.25"/><line x1="8" y1="16" x2="8.01" y2="16"/><line x1="8" y1="20" x2="8.01" y2="20"/><line x1="12" y1="18" x2="12.01" y2="18"/><line x1="12" y1="22" x2="12.01" y2="22"/><line x1="16" y1="16" x2="16.01" y2="16"/><line x1="16" y1="20" x2="16.01" y2="20"/></svg>',
    'green':'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/></svg>',
    'fog':  '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="9" x2="19" y2="9"/><line x1="5" y1="15" x2="19" y2="15"/><line x1="3" y1="12" x2="17" y2="12"/></svg>',
}

def build_pin_group(name, x, y, primary, pop_label):
    if primary:
        return f'''
        <g>
          <circle cx="{x}" cy="{y}" r="34" fill="url(#nlPinGlow)"/>
          <circle cx="{x}" cy="{y}" r="9" fill="#2563EB"/>
          <circle cx="{x}" cy="{y}" r="3.5" fill="#fff"/>
          <text x="{x+13}" y="{y-4}" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="#1A1A2E">{name}</text>
          <text x="{x+13}" y="{y+12}" font-family="Inter, sans-serif" font-size="10" fill="#6B6B7B">{pop_label}</text>
        </g>'''
    else:
        return f'''
        <g>
          <circle cx="{x}" cy="{y}" r="6" fill="#2563EB" opacity=".82"/>
          <circle cx="{x}" cy="{y}" r="2" fill="#fff"/>
          <text x="{x+12}" y="{y+4}" font-family="Inter, sans-serif" font-size="11" fill="#3B3B52">{name}</text>
        </g>'''

def build_state_outline(state_abbr):
    """Simple stylized rounded-rectangle bounding box. Same shape for all states; pins do the locality work.
    Per-state real silhouettes can be added later (one path per state)."""
    return '<rect x="50" y="60" width="380" height="420" rx="14" ry="14" fill="url(#nlAzFill)" stroke="#C9BFAE" stroke-width="2"/>'

def build_hero(s):
    return f'''<!-- HERO (local-rollout 2026-05-04) -->
<section class="nl-hero nl-cream">
  <div class="nl-wrap">
    <div class="nl-grid">
      <div>
        <span class="nl-kicker"><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#2563EB;box-shadow:0 0 0 5px rgba(37,99,235,.15);margin-right:8px;vertical-align:middle"></span>{s["kicker"]}</span>
        <h1>{s["hero_h1"]}</h1>
        <p class="nl-lede">{s["hero_lede"]}</p>
        <div class="nl-cta">
          <a href="sms:4806394722" class="nl-btn nl-btn-cta">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            Text (480) 639-4722
          </a>
          <a href="#how-it-works" class="nl-btn nl-btn-out">How it works</a>
        </div>
        <div class="nl-trust">
          <span class="nl-pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>Licensed in {s["abbr"]}</span>
          <span class="nl-pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>Avg reply: under 30 min</span>
          <span class="nl-pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/></svg>50+ five-star reviews</span>
        </div>
      </div>
      <aside class="nl-card" aria-label="{s["name"]} service overview">
        <div class="nl-photo">
          <img src="{s["hero_image"]}" alt="{s["hero_caption"]}" loading="eager" decoding="async">
          <span class="nl-stamp"><span class="nl-dot"></span> Online &middot; {s["abbr"]}</span>
          <span class="nl-cap">{s["hero_caption"]}</span>
        </div>
        <div class="nl-meta">
          <div><b>{s["cities_count"]}</b><span>Cities served</span></div>
          <div><b>$59</b><span>Per visit, flat</span></div>
          <div><b>&lt;30 min</b><span>Avg reply</span></div>
        </div>
      </aside>
    </div>
  </div>
</section>
'''

def build_local(s):
    cards_html = ''
    for c in s['context_cards']:
        ic = CONTEXT_ICONS.get(c['cls'], CONTEXT_ICONS['heat'])
        cards_html += f'''
      <article class="nl-ctx {c["cls"]}">
        <div class="nl-ic">{ic}</div>
        <h3>{c["title"]}</h3>
        <p>{c["body"]}</p>
        <span class="nl-who"><b style="color:#1A1A2E;font-weight:600">{c["tags"]}</b></span>
      </article>'''
    return f'''<!-- LOCAL CONTEXT (local-rollout 2026-05-04) -->
<section class="nl-local nl-cream">
  <div class="nl-wrap">
    <div class="nl-local-head">
      <span class="nl-kicker">{s["context_kicker"]}</span>
      <h2>{s["context_title"]}</h2>
      <p>{s["context_sub"]}</p>
    </div>
    <div class="nl-local-grid">{cards_html}
    </div>
  </div>
</section>
'''

def build_map_and_cities(s):
    pins_html = ''.join(build_pin_group(*p) for p in s['pins'])
    state_outline = build_state_outline(s['abbr'])
    cities_html = ''
    for name, pop, top, href in s['cities']:
        h = href if href else '#'
        cities_html += f'''
      <a href="{h}" class="nl-city">
        <div class="nl-row"><h3>{name}</h3><span class="nl-arrow">&rarr;</span></div>
        <div class="nl-pop">{pop}</div>
        <div class="nl-top">Top text reasons: <b>{top}</b></div>
      </a>'''
    review = s.get('review')
    review_html = ''
    if review:
        review_html = f'''<!-- LOCAL REVIEW (local-rollout 2026-05-04) -->
<section class="nl-review">
  <div class="nl-wrap nl-rg">
    <div>
      <h2>{review["mark"]}</h2>
      <p class="nl-rsub">{review["sub"]}</p>
    </div>
    <a href="{review["href"]}" rel="noopener" class="nl-quote">
      <div class="nl-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
      <p>&ldquo;{review["quote"]}&rdquo;</p>
      <div class="nl-rwho">
        <span><b style="color:#fff">{review["name"]}</b> &middot; {review["city"]}</span>
        <span class="nl-via">{GOOGLE_LOGO_SVG} via Google</span>
      </div>
    </a>
  </div>
</section>
'''
    return f'''<!-- LOCAL MAP (local-rollout 2026-05-04) -->
<section class="nl-map-sec nl-cream">
  <div class="nl-wrap nl-map-grid">
    <div class="nl-map-copy">
      <span class="nl-kicker">{s["map_kicker"]}</span>
      <h2>{s["map_title"]}</h2>
      <p>{s["map_body"]}</p>
      <div class="nl-map-stats">
        <div class="nl-stat"><div class="nl-n">{s["cities_count"]}</div><div class="nl-l">Major cities served</div></div>
        <div class="nl-stat"><div class="nl-n">{s["population_eligible"]}</div><div class="nl-l">{s["abbr"]} residents eligible</div></div>
      </div>
    </div>
    <div class="nl-map-svg">
      <svg viewBox="0 0 480 520" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Map of {s["name"]} with city service markers">
        <defs>
          <linearGradient id="nlAzFill" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#F5EFE7"/><stop offset="100%" stop-color="#EFE7DA"/>
          </linearGradient>
          <radialGradient id="nlPinGlow" cx=".5" cy=".5" r=".5">
            <stop offset="0%" stop-color="#2563EB" stop-opacity=".35"/>
            <stop offset="100%" stop-color="#2563EB" stop-opacity="0"/>
          </radialGradient>
        </defs>
        {state_outline}
        <g stroke="#C9BFAE" stroke-width="0.6" opacity=".4">
          <line x1="60" y1="120" x2="420" y2="120"/>
          <line x1="60" y1="180" x2="420" y2="180"/>
          <line x1="60" y1="240" x2="420" y2="240"/>
          <line x1="60" y1="300" x2="420" y2="300"/>
          <line x1="60" y1="360" x2="370" y2="360"/>
          <line x1="60" y1="420" x2="370" y2="420"/>
        </g>
        {pins_html}
      </svg>
      <p class="nl-cap">Eligible anywhere in {s["name"]} &middot; not a complete city list</p>
    </div>
  </div>
</section>

<!-- LOCAL CITY CARDS (local-rollout 2026-05-04) -->
<section class="nl-cities nl-cream">
  <div class="nl-wrap">
    <div class="nl-city-head">
      <span class="nl-kicker">Cities we serve most</span>
      <h2>Find your city, see what we treat there.</h2>
    </div>
    <div class="nl-city-grid">{cities_html}
    </div>
  </div>
</section>
{review_html}'''

# ──────────────────────────── splice engine ──────────────────────────────

BANNED = re.compile(r'\b(doctor|insurance)\b', re.IGNORECASE)
ALLOWED_DBL = re.compile(r'double board-certified', re.IGNORECASE)  # "doctor"-free; "insurance"-free; bare "board-certified" not present after rewrite

# Bounded anchors — accept either a `<!-- HERO -->` / `<!-- HERO (...) -->` comment
# or a direct `<section class="hero...">`. Same for cities. Hero variants include `hero` and `hero-receipt`.
HERO_RE = re.compile(
    r'(?:<!-- HERO[^\n]*-->\s*\n)?<section class="hero(?:-receipt)?[^"]*"[^>]*>.*?</section>\s*\n',
    re.DOTALL,
)
CITIES_RE = re.compile(
    r'(?:<!-- CITIES[^\n]*-->\s*\n)?<section class="cities[^"]*"[^>]*>.*?</section>\s*\n',
    re.DOTALL,
)
HEAD_END_RE = re.compile(r'</head>')

def splice_state(state_code, dry_run=False):
    s = STATES[state_code]
    src = LANDING / s['slug'] / 'index.html'
    if not src.exists():
        raise SystemExit(f'NOT FOUND: {src}')
    backup = src.with_suffix('.html.pre-local.bak')
    # Idempotent: read from backup if present
    if backup.exists():
        original = backup.read_text(encoding='utf-8')
        print(f'  [{state_code}] reading from existing backup ({backup.name})')
    else:
        original = src.read_text(encoding='utf-8')
        backup.write_text(original, encoding='utf-8')
        print(f'  [{state_code}] created backup {backup.name}')

    # 1. Inject component CSS once (right before </head>) — but only if not already present
    work = original
    if 'id="local-rollout-css"' not in work:
        work = HEAD_END_RE.sub(COMPONENT_CSS + '\n</head>', work, count=1)

    # 2. Replace HERO + insert local-context band immediately after (one substitution)
    new_hero = build_hero(s)
    local_html = build_local(s)
    if not HERO_RE.search(work):
        raise SystemExit(f'  [{state_code}] HERO anchor not found; aborting')
    work = HERO_RE.sub(new_hero + local_html, work, count=1)

    # 4. Replace CITIES with map + city cards + review
    new_cities = build_map_and_cities(s)
    if not CITIES_RE.search(work):
        raise SystemExit(f'  [{state_code}] CITIES anchor not found; aborting')
    work = CITIES_RE.sub(new_cities, work, count=1)

    # Validate
    orig_size = len(original); new_size = len(work)
    shrink = (orig_size - new_size) / orig_size
    if shrink > 0.30:
        raise SystemExit(f'  [{state_code}] SIZE SHRINK GUARD: {shrink:.0%} (>30%); aborting')
    # Banned-word grep, but only in the new sections we added (HERO/LOCAL/MAP/CITIES/REVIEW)
    new_block = new_hero + local_html + new_cities  # already substituted above
    bad = BANNED.findall(new_block)
    if bad:
        raise SystemExit(f'  [{state_code}] BANNED WORDS in new sections: {set(bad)}; aborting')

    # Write
    if dry_run:
        out = LANDING / s['slug'] / 'index.html.local-preview'
        out.write_text(work, encoding='utf-8')
        print(f'  [{state_code}] dry-run wrote preview {out.name}  ({orig_size:,} → {new_size:,} bytes)')
    else:
        src.write_text(work, encoding='utf-8')
        print(f'  [{state_code}] WROTE {src.relative_to(REPO)}  ({orig_size:,} → {new_size:,} bytes)')
    return src, work, s['slug']

def sftp_push(local_path, slug):
    import paramiko
    env={}
    for line in open('/Users/chriswoods/Desktop/Chris-HQ/.env'):
        line=line.strip()
        if '=' not in line or line.startswith('#'): continue
        k,_,v=line.partition('=')
        env[k]=v.strip().strip('"').strip("'")
    t=paramiko.Transport((env['SFTP_HOST'],22))
    t.banner_timeout=30; t.auth_timeout=30
    t.connect(username=env['SFTP_USERNAME'], password=env['SFTP_PASSWORD'])
    sftp=paramiko.SFTPClient.from_transport(t)
    remote_dir = f'html/{slug}'
    remote = f'{remote_dir}/index.html'
    try:
        sftp.stat(remote_dir)
    except IOError:
        sftp.mkdir(remote_dir)
        print(f'  [SFTP] mkdir {remote_dir}')
    sftp.put(str(local_path), remote)
    sz = sftp.stat(remote).st_size
    t.close()
    print(f'  [SFTP] uploaded → {remote} ({sz:,} bytes)')

def cache_bust_verify(slug):
    import urllib.request, time
    url = f'https://npcwoods.com/{slug}/?v={int(time.time())}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read().decode('utf-8','replace')
            ok = ('id="local-rollout-css"' in body) and ('nl-hero' in body)
            print(f'  [VERIFY] {url[:60]}... {"OK" if ok else "MISSING NEW MARKERS"}')
            return ok
    except Exception as e:
        print(f'  [VERIFY] err: {e}')
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--state')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--no-sftp', action='store_true')
    args = ap.parse_args()

    targets = list(STATES) if args.all else [args.state]
    if not targets or targets == [None]:
        ap.error('--state or --all required')

    for code in targets:
        if code not in STATES:
            print(f'  [{code}] no config; skipping')
            continue
        local_path, _, slug = splice_state(code, dry_run=args.dry_run)
        if not args.dry_run and not args.no_sftp:
            sftp_push(local_path, slug)
            cache_bust_verify(slug)

if __name__ == '__main__':
    main()
