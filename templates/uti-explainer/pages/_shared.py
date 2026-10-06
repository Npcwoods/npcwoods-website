"""Shared sources + ghost-background generators for UTI explainer pages."""
import math

def a(url, text):
    return '<a href="%s" rel="noopener">%s</a>' % (url, text)

SRC = {
  'idsa2011': 'Gupta K, Hooton TM, Naber KG, et al. International clinical practice guidelines for the treatment of acute uncomplicated cystitis and pyelonephritis in women: A 2010 update by the Infectious Diseases Society of America and the European Society for Microbiology and Infectious Diseases. Clin Infect Dis. 2011;52(5):e103-e120. ' + a('https://doi.org/10.1093/cid/ciq257', 'doi:10.1093/cid/ciq257'),
  'cdc_uti': 'Centers for Disease Control and Prevention (CDC). Urinary Tract Infection. ' + a('https://www.cdc.gov/uti/', 'cdc.gov/uti'),
  'niddk_bladder': 'National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK/NIH). Bladder Infection (Urinary Tract Infection) in Adults. ' + a('https://www.niddk.nih.gov/health-information/urologic-diseases/bladder-infection-uti-in-adults', 'niddk.nih.gov'),
  'niddk_kidney': 'NIDDK (NIH). Kidney Infection (Pyelonephritis). ' + a('https://www.niddk.nih.gov/health-information/urologic-diseases/kidney-infection-pyelonephritis', 'niddk.nih.gov'),
  'macrobid_dm': 'Macrobid (nitrofurantoin monohydrate/macrocrystals) capsules. U.S. prescribing information. ' + a('https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1ed48c10-b85d-4dc7-bbaa-648f3e41b191', 'DailyMed'),
  'bactrim_dm': 'Bactrim / Bactrim DS (sulfamethoxazole and trimethoprim). U.S. prescribing information. ' + a('https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=9213ed48-c140-4609-81a1-033e52a21b18', 'DailyMed'),
  'pyridium_dm': 'Phenazopyridine hydrochloride. U.S. labeling / DailyMed. ' + a('https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=all&query=phenazopyridine', 'DailyMed'),
  'statpearls_cystitis': 'Li R, Leslie SW. Cystitis. StatPearls, NCBI Bookshelf (NIH). ' + a('https://www.ncbi.nlm.nih.gov/books/NBK482322/', 'NBK482322'),
  'statpearls_pyelo': 'Belyayeva M, Jeong JM. Acute Pyelonephritis. StatPearls, NCBI Bookshelf (NIH). ' + a('https://www.ncbi.nlm.nih.gov/books/NBK519537/', 'NBK519537'),
  'statpearls_recur': 'Aggarwal N, Leslie SW. Recurrent Urinary Tract Infections. StatPearls, NCBI Bookshelf (NIH). ' + a('https://www.ncbi.nlm.nih.gov/books/NBK557479/', 'NBK557479'),
  'fda_nitro': 'FDA. Nitrofurantoin labeling resources. ' + a('https://www.accessdata.fda.gov/scripts/cder/daf/', 'accessdata.fda.gov'),
  'acog_uti': 'American College of Obstetricians and Gynecologists. Urinary Tract Infections in Pregnant Individuals. Committee opinion / clinical guidance. ' + a('https://www.acog.org/', 'acog.org'),
}

DISCLAIMER = ('This page is for learning. It is not medical advice. Macrobid® is a trademark of its owner. Bactrim® is a trademark of its owner. '
              'NPCWoods is not tied to these companies. A consult does not guarantee a prescription. '
              'If you have fever, back or side pain, vomiting, or feel very sick, use urgent or emergency care. Results vary.')

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

def ghost_climb():
    """How it starts: upward climb dots along a short pipe."""
    b = []
    # urethra pipe
    b.append('<rect x="680" y="80" width="80" height="560" rx="40" fill="none" stroke="#f5a524" stroke-opacity=".35" stroke-width="4"/>')
    for i, y in enumerate(range(560, 120, -55)):
        op = 0.15 + i * 0.05
        b.append('<circle cx="720" cy="%d" r="14" fill="#f5a524" fill-opacity="%.2f"/>' % (y, min(op, 0.55)))
    # bladder bowl at top
    b.append('<ellipse cx="720" cy="100" rx="160" ry="70" fill="none" stroke="#7cc4ff" stroke-opacity=".35" stroke-width="5"/>')
    return _wrap(''.join(b))

def ghost_flame():
    """What it feels like: urgency ripples."""
    b = []
    cx, cy = 980, 360
    for i, r in enumerate(range(40, 420, 45)):
        op = max(0.06, 0.4 - i * 0.04)
        b.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#f5a524" stroke-opacity="%.2f" stroke-width="%s"/>'
                 % (cx, cy, r, op, '3' if i % 2 == 0 else '1.5'))
    return _wrap(''.join(b))

def ghost_masks():
    """Lookalikes: overlapping circles / masks."""
    b = []
    colors = ['#f5a524', '#2997ff', '#19a463', '#ff6b6b', '#c7c7ce']
    for i, (x, y, r) in enumerate([(400, 280, 140), (620, 340, 120), (820, 260, 130), (1000, 380, 110), (520, 480, 100)]):
        b.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-opacity=".28" stroke-width="4"/>' % (x, y, r, colors[i % 5]))
    return _wrap(''.join(b))

def ghost_levels():
    """Bladder vs kidney: two stacked zones."""
    b = []
    b.append('<ellipse cx="720" cy="480" rx="220" ry="100" fill="none" stroke="#2997ff" stroke-opacity=".4" stroke-width="5"/>')
    b.append('<path d="M520 200 C560 120 880 120 920 200 C900 280 540 280 520 200Z" fill="none" stroke="#f5a524" stroke-opacity=".45" stroke-width="5"/>')
    b.append('<line x1="720" y1="280" x2="720" y2="380" stroke="#7cc4ff" stroke-opacity=".35" stroke-width="6" stroke-dasharray="8 10"/>')
    return _wrap(''.join(b))

def ghost_pills():
    """Antibiotics: capsule outlines."""
    b = []
    for i, (x, y, rot) in enumerate([(200, 200, -35), (480, 360, 20), (780, 180, -15), (1080, 400, 40), (340, 520, 10)]):
        b.append('<g transform="translate(%d %d) rotate(%d)" fill="none" stroke="#f5a524" stroke-opacity=".3" stroke-width="5">'
                 '<rect x="-70" y="-24" width="140" height="48" rx="24"/><line x1="0" y1="-24" x2="0" y2="24"/></g>' % (x, y, rot))
    return _wrap(''.join(b))

def ghost_soothe():
    """Relief: soft wave bands."""
    b = []
    for i in range(8):
        y0 = 120 + i * 70; amp = 18 + (i % 3) * 8; ph = i * 0.6; op = 0.10 + 0.03 * (i % 4)
        pts = ' '.join('%.1f,%.1f' % (x, y0 + amp * math.sin(x / 130.0 + ph)) for x in range(-40, 1500, 20))
        b.append('<polyline points="%s" fill="none" stroke="#f5a524" stroke-opacity="%.2f" stroke-width="%s"/>' % (pts, op, '4' if i == 3 else '2'))
    return _wrap(''.join(b))

def ghost_loop():
    """Recurring: looping arrows."""
    b = []
    for i, r in enumerate([80, 140, 200, 280]):
        b.append('<circle cx="900" cy="340" r="%d" fill="none" stroke="#f5a524" stroke-opacity="%.2f" stroke-width="4" stroke-dasharray="12 14"/>'
                 % (r, 0.15 + i * 0.06))
    b.append('<path d="M900 60 L930 110 L870 110 Z" fill="#f5a524" fill-opacity=".35"/>')
    return _wrap(''.join(b))

def ghost_shield():
    """Prevention: shield + drops."""
    b = []
    b.append('<path d="M720 80 L980 180 V360 C980 480 720 600 720 600 C720 600 460 480 460 360 V180 Z" fill="none" stroke="#f5a524" stroke-opacity=".4" stroke-width="6"/>')
    for (x, y) in [(280, 400), (360, 520), (1080, 300), (1160, 460)]:
        b.append('<path d="M%d %d c0 20 20 40 20 40 s20-20 20-40 c0-16-10-28-20-28s-20 12-20 28z" fill="#2997ff" fill-opacity=".2"/>' % (x, y))
    return _wrap(''.join(b))

def ghost_stop():
    """Who needs in-person: stop / ban rings."""
    b = []
    cx, cy = 1000, 320
    b.append('<circle cx="%d" cy="%d" r="160" fill="none" stroke="#ff6b6b" stroke-opacity=".35" stroke-width="10"/>' % (cx, cy))
    b.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#ff6b6b" stroke-opacity=".4" stroke-width="12" stroke-linecap="round"/>'
             % (cx - 110, cy + 110, cx + 110, cy - 110))
    return _wrap(''.join(b))

def ghost_myths():
    """Myths: X marks and check dots."""
    b = []
    for (x, y) in [(200, 180), (500, 400), (900, 200), (1200, 480)]:
        b.append('<g stroke="#ff6b6b" stroke-opacity=".28" stroke-width="8" stroke-linecap="round">'
                 '<line x1="%d" y1="%d" x2="%d" y2="%d"/><line x1="%d" y1="%d" x2="%d" y2="%d"/></g>'
                 % (x-40, y-40, x+40, y+40, x+40, y-40, x-40, y+40))
    for (x, y) in [(350, 300), (700, 180), (1050, 360)]:
        b.append('<circle cx="%d" cy="%d" r="28" fill="none" stroke="#19a463" stroke-opacity=".35" stroke-width="6"/>' % (x, y))
        b.append('<path d="M%d %d l12 14 22-28" fill="none" stroke="#19a463" stroke-opacity=".4" stroke-width="6" stroke-linecap="round"/>' % (x-16, y))
    return _wrap(''.join(b))
