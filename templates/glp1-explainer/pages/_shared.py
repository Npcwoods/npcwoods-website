"""Shared sources + ghost-background generators for GLP-1 explainer pages."""
import math

def a(url, text):
    return '<a href="%s" rel="noopener">%s</a>' % (url, text)

SRC = {
 'statpearls_glp1': 'Collins L, Costello RA. Glucagon-Like Peptide-1 Receptor Agonists. StatPearls, NCBI Bookshelf (NIH). ' + a('https://www.ncbi.nlm.nih.gov/books/NBK551568/', 'NBK551568'),
 'statpearls_compare': 'Latif W, Lambrinos KJ, Patel P, et al. Compare and Contrast the GLP-1 Receptor Agonists. StatPearls, NCBI Bookshelf (NIH). ' + a('https://www.ncbi.nlm.nih.gov/books/NBK572151/', 'NBK572151'),
 'statpearls_sema': 'Kommu S, Whitfield P. Semaglutide. StatPearls, NCBI Bookshelf (NIH). ' + a('https://www.ncbi.nlm.nih.gov/books/NBK603723/', 'NBK603723'),
 'tanday': 'Tanday N, Flatt PR, Irwin N. Metabolic responses and benefits of GLP-1 receptor ligands. Br J Pharmacol. 2022. ' + a('https://pmc.ncbi.nlm.nih.gov/articles/PMC8820187/', 'PMC8820187'),
 'knudsen': 'Knudsen LB, Lau J. The discovery and development of liraglutide and semaglutide. Front Endocrinol. 2019;10:155. ' + a('https://pmc.ncbi.nlm.nih.gov/articles/PMC6474072/', 'PMC6474072'),
 'niddk': 'NIDDK (NIH). Story of discovery: how different medications for diabetes and obesity emerged from basic research on one pancreatic hormone. 2021. ' + a('https://www.niddk.nih.gov/news/archive/2021/story-discovery-medications-diabetes-obesity-emerged-research-pancreatic-hormone', 'niddk.nih.gov'),
 'neeland': 'Neeland IJ, Linge J, Birkenfeld AL. Changes in lean body mass with GLP-1-based therapies and mitigation strategies. Diabetes Obes Metab. 2024;26(Suppl 4):16-27. ' + a('https://pubmed.ncbi.nlm.nih.gov/38937282/', 'PubMed 38937282'),
 'wegovy_dm': 'Wegovy (semaglutide) injection, U.S. prescribing information and Medication Guide. ' + a('https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=ee06186f-2aa3-4990-a760-757579d8f77b', 'DailyMed'),
 'zepbound_dm': 'Zepbound (tirzepatide) injection, U.S. prescribing information and Medication Guide. ' + a('https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=487cd7e7-434c-4925-99fa-aa80b1cc776b', 'DailyMed'),
 'wegovy_fda': 'FDA. Wegovy prescribing information (label PDF). ' + a('https://www.accessdata.fda.gov/drugsatfda_docs/label/2026/215256s029lbl.pdf', 'accessdata.fda.gov'),
 'zepbound_fda': 'FDA. Zepbound prescribing information (label PDF). ' + a('https://www.accessdata.fda.gov/drugsatfda_docs/label/2026/217806s037lbl.pdf', 'accessdata.fda.gov'),
}

DISCLAIMER = ('This page is for learning. It is not medical advice. Ozempic®, Wegovy®, Mounjaro®, and Zepbound® are trademarks of their owners. '
              'NPCWoods is not tied to these companies. Compounded drugs are not FDA-approved, and FDA does not check them for safety or quality before they are sold. '
              'A consult does not guarantee a prescription. Results vary.')

def _grid():
    out = []
    for y in range(90, 720, 90):
        out.append('<line x1="0" y1="%d" x2="1440" y2="%d" stroke="rgba(255,255,255,.05)" stroke-dasharray="2 10"/>' % (y, y))
    for x in range(120, 1440, 120):
        out.append('<line x1="%d" y1="0" x2="%d" y2="720" stroke="rgba(255,255,255,.05)" stroke-dasharray="2 10"/>' % (x, x))
    return ''.join(out)

def _wrap(body):
    return ('    <svg class="gh-ghost" focusable="false" viewBox="0 0 1440 720" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            + _grid() + body + '</svg>')

def ghost_doorbell():
    """How they work: doorbell ripples + keyholes (lock and key)."""
    b = []
    cx, cy = 1060, 330
    for i, r in enumerate(range(70, 900, 70)):
        op = max(0.05, 0.34 - i * 0.025)
        b.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#2997ff" stroke-opacity="%.2f" stroke-width="%s" stroke-dasharray="%s"/>'
                 % (cx, cy, r, op, '3' if i % 3 == 0 else '1.5', '1 9' if i % 2 else '14 10'))
    for (x, y, s, op) in [(140, 140, 1.0, .16), (300, 560, .8, .13), (520, 250, .65, .11), (90, 420, .7, .12), (690, 620, .55, .10), (430, 60, .5, .09)]:
        b.append('<g transform="translate(%d %d) scale(%.2f)" fill="none" stroke="#7cc4ff" stroke-opacity="%.2f" stroke-width="5">'
                 '<rect x="-46" y="-56" width="92" height="112" rx="26"/><circle cx="0" cy="-10" r="15"/><path d="M-8 2 L-13 34 H13 L8 2"/></g>' % (x, y, s, op))
    return _wrap(''.join(b))

def ghost_waves():
    """Side effects: tummy waves + a traffic light outline."""
    b = []
    for i in range(9):
        y0 = 110 + i * 68; amp = 22 + (i % 3) * 10; ph = i * 0.7; op = 0.10 + 0.03 * (i % 4)
        pts = ' '.join('%.1f,%.1f' % (x, y0 + amp * math.sin(x / 120.0 + ph)) for x in range(-40, 1500, 20))
        b.append('<polyline points="%s" fill="none" stroke="#2997ff" stroke-opacity="%.2f" stroke-width="%s" stroke-linecap="round"/>' % (pts, op, '4' if i == 4 else '2'))
    b.append('<g fill="none" stroke-width="5"><rect x="1250" y="70" width="110" height="300" rx="40" stroke="#ffffff" stroke-opacity=".10"/>'
             '<circle cx="1305" cy="130" r="30" stroke="#ff6b6b" stroke-opacity=".28"/><circle cx="1305" cy="220" r="30" stroke="#f5a524" stroke-opacity=".55" fill="#f5a524" fill-opacity=".10"/>'
             '<circle cx="1305" cy="310" r="30" stroke="#19a463" stroke-opacity=".28"/></g>')
    return _wrap(''.join(b))

def ghost_calendar():
    """First 30 days: a blank month grid, one shot day per week, and a level that fills up then holds steady."""
    b = []
    x0, y0, w, h, gap = 70, 70, 168, 104, 16
    for r in range(5):
        for c in range(7):
            x = x0 + c * (w + gap); y = y0 + r * (h + gap)
            b.append('<rect x="%d" y="%d" width="%d" height="%d" rx="18" fill="none" stroke="#ffffff" stroke-opacity=".07" stroke-width="2"/>' % (x, y, w, h))
            if c == 2:
                b.append('<circle cx="%d" cy="%d" r="13" fill="#f5a524" fill-opacity="%.2f"/>' % (x + w / 2, y + h / 2, 0.22 + r * 0.06))
    pts = []
    for i in range(0, 61):
        t = i / 60.0; x = -20 + t * 1500
        lvl = 1 - math.exp(-t * 4.2)
        y = 660 - 430 * lvl + 16 * math.sin(t * 5 * 2 * math.pi) * (1 - lvl * 0.6)
        pts.append('%.1f,%.1f' % (x, y))
    b.append('<polyline points="%s" fill="none" stroke="#7cc4ff" stroke-opacity=".55" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>' % ' '.join(pts))
    return _wrap(''.join(b))


def ghost_stairs():
    """Dose steps: soft stair steps climbing right, no numbers."""
    b = []
    for i in range(6):
        x = 180 + i * 170; y = 520 - i * 70; w = 150; h = 70 + i * 8
        b.append('<rect x="%d" y="%d" width="%d" height="%d" rx="18" fill="none" stroke="#ffffff" stroke-opacity="%.2f" stroke-width="3"/>' % (x, y, w, h, 0.08 + i * 0.03))
        b.append('<circle cx="%d" cy="%d" r="10" fill="#f5a524" fill-opacity="%.2f"/>' % (x + w/2, y + 28, 0.18 + i * 0.05))
    b.append('<path d="M120 580 C400 520 700 360 1180 180" fill="none" stroke="#7cc4ff" stroke-opacity=".35" stroke-width="8" stroke-linecap="round"/>')
    return _wrap(''.join(b))

def ghost_twokeys():
    """Sema vs tirz: two soft key silhouettes."""
    b = []
    b.append('<g fill="none" stroke="#2997ff" stroke-opacity=".28" stroke-width="10" stroke-linecap="round"><circle cx="420" cy="300" r="70"/><path d="M490 300 H780 M720 300 V360"/></g>')
    b.append('<g fill="none" stroke="#f5a524" stroke-opacity=".35" stroke-width="10" stroke-linecap="round"><circle cx="420" cy="520" r="70"/><path d="M490 520 H780 M700 520 V460 M740 520 V580"/></g>')
    for x,y,op in [(980,220,.12),(1120,400,.10),(1280,280,.09),(980,520,.11)]:
        b.append('<rect x="%d" y="%d" width="90" height="110" rx="24" fill="none" stroke="#fff" stroke-opacity="%.2f" stroke-width="4"/>' % (x,y,op))
    return _wrap(''.join(b))

def ghost_plate():
    """Eating: soft plate rings + small bite dots."""
    b = []
    cx,cy=980,340
    for i,r in enumerate(range(60, 280, 40)):
        b.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#fff" stroke-opacity="%.2f" stroke-width="3"/>' % (cx, cy, r, 0.06+i*0.03))
    for (x,y,r,op) in [(200,180,18,.14),(280,420,14,.12),(160,520,20,.10),(420,260,16,.12),(520,560,12,.11)]:
        b.append('<circle cx="%d" cy="%d" r="%d" fill="#f5a524" fill-opacity="%.2f"/>' % (x,y,r,op))
    b.append('<path d="M700 160 C760 200 760 380 700 440" fill="none" stroke="#7cc4ff" stroke-opacity=".25" stroke-width="8"/>')
    return _wrap(''.join(b))

def ghost_stop():
    """Who shouldn't: soft stop-sign outlines, no text."""
    b = []
    for (x,y,s,op) in [(220,180,1.0,.14),(480,420,.75,.11),(180,480,.6,.10),(700,200,.85,.12)]:
        b.append('<g transform="translate(%d %d) scale(%.2f)" fill="none" stroke="#ff6b6b" stroke-opacity="%.2f" stroke-width="8">'
                 '<path d="M0 -70 L48 -48 L70 0 L48 48 L0 70 L-48 48 L-70 0 L-48 -48 Z"/></g>' % (x,y,s,op))
    b.append('<circle cx="1100" cy="320" r="120" fill="none" stroke="#fff" stroke-opacity=".08" stroke-width="4"/>')
    return _wrap(''.join(b))

def ghost_coins():
    """Cost: soft coin rings, no dollar amounts drawn as text."""
    b = []
    for i, (x,y,r) in enumerate([(240,220,70),(420,380,90),(300,520,55),(700,260,80),(900,480,100),(1100,300,65)]):
        b.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#f5a524" stroke-opacity="%.2f" stroke-width="5"/>' % (x,y,r, 0.10+ (i%3)*0.05))
        b.append('<circle cx="%d" cy="%d" r="%d" fill="#f5a524" fill-opacity=".06"/>' % (x,y,r-18))
    return _wrap(''.join(b))

def ghost_myths():
    """Myths: check and soft X marks floating."""
    b = []
    for (x,y,op) in [(200,200,.18),(480,360,.14),(320,520,.12),(700,220,.15)]:
        b.append('<g transform="translate(%d %d)" stroke="#19a463" stroke-opacity="%.2f" stroke-width="10" fill="none" stroke-linecap="round"><path d="M-30 0 L-8 22 L34 -30"/></g>' % (x,y,op))
    for (x,y,op) in [(980,240,.14),(1180,420,.12),(900,520,.10)]:
        b.append('<g transform="translate(%d %d)" stroke="#ff6b6b" stroke-opacity="%.2f" stroke-width="10" fill="none" stroke-linecap="round"><path d="M-24 -24 L24 24 M24 -24 L-24 24"/></g>' % (x,y,op))
    return _wrap(''.join(b))
