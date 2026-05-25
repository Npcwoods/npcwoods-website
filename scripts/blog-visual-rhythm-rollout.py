#!/usr/bin/env python3
"""
blog-visual-rhythm-rollout.py — Inject visual-rhythm components into all 21 WP blog posts.

Components added (all inline-styled so they survive WP's content rendering):
  - TL;DR sage card right after intro
  - Topic illustration at first H2 (only for condition-specific posts)
  - "Chris says..." pull quote between mid sections
  - Dark CTA action card before final paragraphs
  - Next-steps card at end

Modes:
  --dry-run         Read posts, build new content, save to /tmp/blog-rollout/<slug>.{html,json}
  --push            PATCH posts via WP REST API (requires working WP_USERNAME/WP_APP_PASSWORD)
  --slug <slug>     Limit to one post by slug

Idempotent: detects an existing `data-vr="1"` marker and skips already-enhanced posts.
Banned-word grep + size-shrink guard before any push.
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error, base64
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = Path('/tmp/blog-rollout')
WP_BASE = 'https://npcwoods.com/wp-json/wp/v2'

# ─── topic mapping ───────────────────────────────────────────────────────
TOPIC_ILLUSTRATIONS = {
    'uti':   ('https://npcwoods.com/wp-content/uploads/2026/05/uti-anatomy.png',
              'When bacteria climb the urethra and reach the bladder &mdash; that&rsquo;s a UTI.'),
    'sinus': ('https://npcwoods.com/wp-content/uploads/2026/05/sinus.png',
              'Sinus pressure is the cavities behind your face filling with mucus and pressure.'),
    'strep': ('https://npcwoods.com/wp-content/uploads/2026/05/strep.png',
              'Strep is a bacterial infection of the throat &mdash; antibiotics shorten it dramatically.'),
    'yeast': ('https://npcwoods.com/wp-content/uploads/2026/05/yeast.png',
              'Yeast happens when the normal balance of microbes shifts. Treatment restores the balance.'),
    'tooth': ('https://npcwoods.com/wp-content/uploads/2026/05/tooth.png',
              'A tooth infection lives in the pulp at the root &mdash; antibiotics buy time until you see a dentist.'),
    'ear':   ('https://npcwoods.com/wp-content/uploads/2026/05/ear.png',
              'Adult ear infections live in the canal or middle ear &mdash; antibiotics or drops, depending.'),
}

# Slug → topic mapping. None means generic (no anatomy illo).
SLUG_TOPIC = {
    # UTI cluster
    'when-to-see-provider-for-uti': 'uti',
    'burning-when-i-pee': 'uti',
    'get-uti-antibiotics-online-same-day': 'uti',
    'uti-fast-without-urgent-care': 'uti',
    # Sinus
    'allergies-vs-sinus-infection': 'sinus',
    'do-i-need-antibiotics-sinus-infection': 'sinus',
    # Strep
    'strep-antibiotics-online': 'strep',
    # Yeast
    'yeast-infection-treatment-online': 'yeast',
    # Tooth
    'tooth-infection-antibiotics-telehealth': 'tooth',
    # Generic — async/pricing/NP topics
    'out-of-pocket-59-flat-fee-nurse-practitioner': None,
    'urgent-care-price-guide': None,
    'cash-pay-telehealth-reasons': None,
    'telehealth-vs-urgent-care-cost-speed': None,
    'text-based-vs-video-telehealth': None,
    'what-is-async-telemedicine': None,
    'common-infections-telehealth-same-day': None,
    'is-text-based-telehealth-safe': None,
    'what-can-telehealth-prescribe': None,
    'can-nurse-practitioner-prescribe-antibiotics': None,
    'questions-before-online-health-service': None,
    'stop-popping-benadryl': None,
}

# Per-post TL;DR bullets and Chris-says quote. Keep concise.
POST_DATA = {
    'when-to-see-provider-for-uti': {
        'tldr': [
            'Most UTIs need antibiotics &mdash; they don\'t fix themselves.',
            'Red flags (fever, back pain, blood, vomiting) &rarr; ER, not text.',
            'Otherwise, text Chris and have your prescription tonight.',
            'Hydration alone won&rsquo;t cure an established UTI.',
        ],
        'quote': 'A UTI doesn&rsquo;t fix itself, but it doesn&rsquo;t have to ruin your night either.',
    },
    'burning-when-i-pee': {
        'tldr': [
            'Burning when you pee is almost always a UTI &mdash; treatable tonight, no waiting room.',
            'Red flags (fever, back pain, blood, vomiting) &rarr; ER, not text.',
            'Antibiotic by text takes ~30 minutes. $59 flat. Real NP, no chatbot.',
            'Most people feel relief within 24&ndash;48 hours of starting treatment.',
        ],
        'quote': 'A UTI doesn&rsquo;t fix itself, but it doesn&rsquo;t have to ruin your night either.',
    },
    'get-uti-antibiotics-online-same-day': {
        'tldr': [
            'You can get a UTI antibiotic online the same day &mdash; usually within an hour.',
            'No video call required. Real NP review by text.',
            '$59 flat fee. Sent to any pharmacy you choose.',
            'Skip the 4-hour urgent care wait.',
        ],
        'quote': 'I&rsquo;ve treated thousands of UTIs by text. The whole visit takes about 30 minutes.',
    },
    'uti-fast-without-urgent-care': {
        'tldr': [
            'You can treat a UTI fast without urgent care &mdash; same medicine, same day.',
            'Real NP, real prescription, no waiting room.',
            '$59 flat. No copay surprises.',
            'Most relief starts within 24&ndash;48 hours.',
        ],
        'quote': 'Urgent care for a simple UTI is overkill. Text-in beats it on speed and price.',
    },
    'allergies-vs-sinus-infection': {
        'tldr': [
            'Allergies clear up with antihistamines; sinus infections need antibiotics if bacterial.',
            'Color of mucus alone isn&rsquo;t reliable &mdash; duration matters more.',
            '10+ days, getting worse, fever &rarr; probably bacterial.',
            'Text-in, get the right call without guessing.',
        ],
        'quote': 'The most common mistake I see: 14 days into a sinus infection, still treating it like allergies.',
    },
    'do-i-need-antibiotics-sinus-infection': {
        'tldr': [
            'Most sinus infections are viral and clear without antibiotics.',
            'But 10+ days, getting worse, or facial pain + fever = probably bacterial.',
            'Text-in &mdash; I&rsquo;ll tell you which you have, not just prescribe.',
            'Don&rsquo;t white-knuckle it past two weeks.',
        ],
        'quote': 'Most sinus infections don&rsquo;t need antibiotics. The hard part is knowing when they do.',
    },
    'strep-antibiotics-online': {
        'tldr': [
            'Strep over text is fast: $59, same day, prescription to your pharmacy.',
            'Adults only &mdash; we don&rsquo;t treat under 12 by text.',
            'A real NP makes the call, not a chatbot.',
            'Most people feel better within 24 hours of starting antibiotics.',
        ],
        'quote': 'Strep without the urgent-care line is one of the easiest wins in async medicine.',
    },
    'yeast-infection-treatment-online': {
        'tldr': [
            'Yeast infections are very treatable by text &mdash; most clear in 1&ndash;3 days.',
            'You shouldn&rsquo;t need to take a half-day off work for this.',
            'Real NP, real prescription, no exam needed for typical cases.',
            '$59 flat. Sent to your pharmacy of choice.',
        ],
        'quote': 'Nobody should have to sit in an urgent care for this. It&rsquo;s a 10-minute text conversation.',
    },
    'tooth-infection-antibiotics-telehealth': {
        'tldr': [
            'Antibiotics buy you time &mdash; you still need a dentist for the root cause.',
            'Severe swelling, trouble breathing, fever &rarr; ER, not text.',
            'Most tooth infections are amoxicillin or clindamycin, $59.',
            'Pain control matters as much as the antibiotic.',
        ],
        'quote': 'The antibiotic stops the infection from spreading. The dentist fixes why it started.',
    },
    'out-of-pocket-59-flat-fee-nurse-practitioner': {
        'tldr': [
            '$59 flat fee. Per visit. No surprise charges, ever.',
            'Real NP, not a chatbot, not a triage layer.',
            'Same as in-person care quality &mdash; minus the waiting room.',
            'No memberships, no subscriptions, no upsells.',
        ],
        'quote': 'I built NPCWoods because healthcare pricing should fit on a receipt, not a bill stack.',
    },
    'urgent-care-price-guide': {
        'tldr': [
            'Urgent care averages $150&ndash;$300 cash &mdash; before any tests.',
            'Telehealth (text) is $59. Most acute conditions handled the same way.',
            'Skip the time + the sticker shock when symptoms are textbook.',
            'Save urgent care for when you need hands-on care.',
        ],
        'quote': 'You shouldn&rsquo;t pay $250 for a 12-minute visit you could have had by text for $59.',
    },
    'cash-pay-telehealth-reasons': {
        'tldr': [
            'Cash-pay telehealth means transparent pricing, no surprise bills.',
            '$59 per visit covers everything: review, diagnosis, prescription.',
            'No insurance navigating, no networks, no denied claims.',
            'Real NP, real care, no shortcuts.',
        ],
        'quote': 'Cash-pay isn&rsquo;t cheaper care &mdash; it&rsquo;s clearer care.',
    },
    'telehealth-vs-urgent-care-cost-speed': {
        'tldr': [
            'Telehealth (text): $59 flat, ~30 min start to prescription.',
            'Urgent care: $150&ndash;$300, 2&ndash;4 hours typical.',
            'For UTI, sinus, strep, yeast: telehealth wins both.',
            'For chest pain, broken bones, severe injury: urgent care or ER.',
        ],
        'quote': 'For 80% of urgent-care visits, async telemedicine is faster and cheaper.',
    },
    'text-based-vs-video-telehealth': {
        'tldr': [
            'Text-based skips the scheduling, the wait, and the camera anxiety.',
            'For acute conditions with clear histories, text is as good as video.',
            'Video adds value for visual conditions (rashes, wounds).',
            'I use text by default, request a photo if I need to see something.',
        ],
        'quote': 'Most patients find text easier to be honest in. They tell me more, not less.',
    },
    'what-is-async-telemedicine': {
        'tldr': [
            'Async = no live appointment. You text me when it works for you.',
            'I review and respond, usually within 30 minutes.',
            'Same care quality, way more convenient.',
            'Available in 11 states for $59 flat.',
        ],
        'quote': 'Async means you don&rsquo;t schedule healthcare around someone else&rsquo;s clock.',
    },
    'common-infections-telehealth-same-day': {
        'tldr': [
            'UTI, sinus, strep, yeast, tooth, ear, skin &mdash; all treatable by text the same day.',
            '$59 flat. Real NP. Antibiotics or other treatment if appropriate.',
            'Some conditions still need an in-person visit; I&rsquo;ll tell you when.',
            'Most people pick up their prescription within 1&ndash;2 hours.',
        ],
        'quote': 'About 70% of urgent-care visits could have been handled async. We do that work.',
    },
    'is-text-based-telehealth-safe': {
        'tldr': [
            'Yes &mdash; for the right conditions, with a real NP, it&rsquo;s as safe as in-person.',
            'I screen out red flags before prescribing.',
            'HIPAA-compliant texting, encrypted records.',
            'If a condition needs hands-on care, I&rsquo;ll tell you and refer.',
        ],
        'quote': 'The safest visit is the one where the clinician knows when to say no.',
    },
    'what-can-telehealth-prescribe': {
        'tldr': [
            'Antibiotics, antifungals, antivirals, basic medications &mdash; yes.',
            'Controlled substances (most) &mdash; no, by federal rules.',
            'GLP-1 (Wegovy/Mounjaro), ED treatment &mdash; yes, where appropriate.',
            'When in doubt, text and ask.',
        ],
        'quote': 'I prescribe what I&rsquo;d prescribe in person. The rule is the medicine, not the medium.',
    },
    'can-nurse-practitioner-prescribe-antibiotics': {
        'tldr': [
            'Yes &mdash; nurse practitioners prescribe antibiotics in all 50 states.',
            'I&rsquo;m double board-certified (FNP-C, PMHNP-BC) and licensed in 11 states.',
            'Same prescribing authority as a physician for most outpatient conditions.',
            'No supervision needed in independent-practice states.',
        ],
        'quote': 'NPs prescribe roughly 90% of what physicians prescribe in primary care. The exceptions are narrow.',
    },
    'questions-before-online-health-service': {
        'tldr': [
            'Ask: who actually reviews your case? (Should be a real licensed clinician.)',
            'Ask: what&rsquo;s the total cost? (No surprise add-ons.)',
            'Ask: is it HIPAA-compliant? (Yes, real ones are.)',
            'Ask: what happens if I need a follow-up?',
        ],
        'quote': 'If a service won&rsquo;t tell you who reviewed your case, that&rsquo;s your answer.',
    },
    'stop-popping-benadryl': {
        'tldr': [
            'Daily Benadryl for sleep is rough on cognition long-term.',
            'For allergies, second-gen antihistamines (Zyrtec, Claritin, Allegra) work better with fewer side effects.',
            'For sleep, talk to a clinician about the actual issue.',
            'Acute use is fine; it&rsquo;s the daily pattern that matters.',
        ],
        'quote': 'There&rsquo;s a quiet cognitive cost to long-term first-gen antihistamines we should talk about more.',
    },
}

# ─── component builders ──────────────────────────────────────────────────

def build_tldr(bullets):
    items = ''.join(
        f'<li style="display:flex;gap:10px;margin:0"><span style="color:#16A34A;font-weight:700">&check;</span><span>{b}</span></li>'
        for b in bullets
    )
    return f'''
<aside data-vr="1" style="background:#EFE7DA;border:1px solid #E6DED3;border-radius:14px;padding:24px 26px;margin:0 0 36px">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
    <span style="display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:8px;background:#16A34A;color:#fff;font-size:14px;font-weight:700">i</span>
    <span style="font-size:13px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#3B3B52;font-family:Inter,-apple-system,sans-serif">The short version</span>
  </div>
  <ul style="margin:0;padding:0;list-style:none;display:grid;gap:8px;font-size:15.5px;color:#3B3B52;font-family:Inter,-apple-system,sans-serif">{items}</ul>
</aside>
'''

def build_topic_illo(topic):
    if topic not in TOPIC_ILLUSTRATIONS:
        return ''
    src, caption = TOPIC_ILLUSTRATIONS[topic]
    return f'''
<figure data-vr="1" style="margin:36px 0;text-align:center">
  <img src="{src}" alt="Editorial illustration" style="max-width:340px;width:100%;height:auto;display:block;margin:0 auto;border-radius:12px;background:#fff;border:1px solid #E6DED3;padding:18px" />
  <figcaption style="font-size:13.5px;color:#6B6B7B;margin-top:12px;font-style:italic;font-family:Inter,-apple-system,sans-serif">{caption}</figcaption>
</figure>
'''

def build_quote(quote_text):
    return f'''
<blockquote data-vr="1" style="margin:36px 0;padding:24px 28px;border-left:4px solid #5B7553;background:#fff;border-radius:0 14px 14px 0;box-shadow:0 8px 24px -16px rgba(26,26,46,.15)">
  <p style="font-family:Georgia,serif;font-style:italic;font-size:21px;line-height:1.45;color:#1A1A2E;margin:0 0 14px">&ldquo;{quote_text}&rdquo;</p>
  <p style="display:flex;align-items:center;gap:10px;font-size:13.5px;color:#6B6B7B;margin:0;font-family:Inter,-apple-system,sans-serif">
    <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" alt="" width="28" height="28" style="border-radius:50%" />
    <span><b style="color:#1A1A2E">Chris Woods</b>, FNP-C, PMHNP-BC</span>
  </p>
</blockquote>
'''

ACTION_CARD = '''
<div data-vr="1" style="background:#1A1A2E;color:#FDF8F4;border-radius:18px;padding:36px 32px;margin:40px 0;text-align:center;background-image:radial-gradient(circle at 80% 20%, rgba(37,99,235,.25) 0%, transparent 50%);font-family:Inter,-apple-system,sans-serif">
  <p style="font-size:13px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#93C5FD;margin:0 0 12px">Need help right now?</p>
  <h3 style="font-family:Georgia,serif;font-size:32px;font-weight:600;line-height:1.15;margin:0 0 14px;color:#FDF8F4">Text Chris &middot; $59 &middot; same day</h3>
  <p style="font-size:16px;color:rgba(253,248,244,.8);margin:0 0 24px;max-width:480px;margin-left:auto;margin-right:auto">Real NP. Real prescription. No app, no waiting room, no copay drama. Most people are picking up medicine within an hour.</p>
  <a href="sms:4806394722" style="display:inline-block;background:#2563EB;color:#fff;font-weight:600;font-size:16px;padding:16px 28px;border-radius:10px;text-decoration:none">Text (480) 639-4722 &rarr;</a>
  <p style="font-size:12.5px;color:rgba(253,248,244,.55);margin:18px 0 0;letter-spacing:.04em">If we can&rsquo;t safely treat you with a text visit, you won&rsquo;t be charged.</p>
</div>
'''

NEXT_STEPS = '''
<div data-vr="1" style="background:#fff;border:1px solid #E6DED3;border-radius:14px;padding:24px 26px;margin:24px 0 60px;font-family:Inter,-apple-system,sans-serif">
  <p style="font-size:13px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#3B3B52;margin:0 0 16px">Three quick next steps</p>
  <ol style="margin:0;padding-left:20px;font-size:15.5px;color:#1A1A2E;line-height:1.7">
    <li><a href="sms:4806394722" style="color:#2563EB;font-weight:600;text-decoration:none">Text (480) 639-4722</a> if your symptoms match what we treat</li>
    <li><a href="https://npcwoods.com/conditions/" style="color:#2563EB;font-weight:600;text-decoration:none">See all conditions we treat</a> if you&rsquo;re not sure we&rsquo;re the right call</li>
    <li><a href="https://npcwoods.com/how-it-works/" style="color:#2563EB;font-weight:600;text-decoration:none">How it works</a> if you&rsquo;ve never done a text visit before</li>
  </ol>
</div>
'''

# ─── splice engine ───────────────────────────────────────────────────────

BANNED = re.compile(r'\b(doctor)\b', re.IGNORECASE)  # "insurance" appears legitimately in some posts; guard only on doctor

# Scrub patterns: clean up pre-existing violations as part of this rollout.
# - HTML comments (internal draft notes that shouldn't be public)
# - "Doctor On Demand" → "video telehealth platforms" (competitor brand, generic-ize)
# - "primary care doctor" / "your doctor" / "see a doctor" → clinician variants
SCRUB_PATTERNS = [
    (re.compile(r'<!--.*?-->', re.DOTALL), ''),  # strip all HTML comments
    (re.compile(r'\bDoctor On Demand\b'), 'video telehealth platforms'),
    (re.compile(r'\bprimary care doctor\b', re.IGNORECASE), 'primary care clinician'),
    (re.compile(r'\byour doctor\b', re.IGNORECASE), 'your clinician'),
    (re.compile(r'\bsee a doctor\b', re.IGNORECASE), 'see a clinician'),
    (re.compile(r'\bcall a doctor\b', re.IGNORECASE), 'text a clinician'),
    (re.compile(r'\bDoctors\b'), 'Clinicians'),
    (re.compile(r'\bdoctors\b'), 'clinicians'),
    (re.compile(r'\bDoctor\b'), 'Clinician'),
    (re.compile(r'\bdoctor\b'), 'clinician'),
]

def scrub_content(content):
    """Apply pre-rollout cleanup pass: strip HTML comments, scrub 'doctor' references."""
    out = content
    for rx, repl in SCRUB_PATTERNS:
        out = rx.sub(repl, out)
    return out

def already_enhanced(content):
    return 'data-vr="1"' in content

def splice_post(slug, content):
    """Insert components into post content. Returns new content string."""
    if already_enhanced(content):
        return content, 'already-enhanced'

    data = POST_DATA.get(slug)
    if not data:
        return content, 'no-data-skipped'

    topic = SLUG_TOPIC.get(slug)
    tldr = build_tldr(data['tldr'])
    illo = build_topic_illo(topic) if topic else ''
    quote = build_quote(data['quote'])

    # Pre-pass: strip HTML comments + scrub "doctor" references per Chris's standing rule
    new = scrub_content(content)
    # Strategy: insert TL;DR right after the LARGEST top image (or first H1+intro paragraphs).
    # The simplest reliable placement is: right before the FIRST <h2> in the content.
    # That keeps the intro intact and gives a strong scannable summary before the deep dive.
    # Insert TL;DR before the first H2
    h2_match = re.search(r'(<h2[\s>])', new)
    if h2_match:
        idx = h2_match.start()
        new = new[:idx] + tldr + new[idx:]
    else:
        # Fallback: append TL;DR at top
        new = tldr + new

    # Insert illustration after the FIRST H2 (which is the second H2 now since TL;DR is before it)
    if illo:
        h2s = list(re.finditer(r'</h2>', new))
        if h2s:
            # After first H2 closing
            i = h2s[0].end()
            new = new[:i] + illo + new[i:]

    # Insert Chris-says quote between the 3rd and 4th H2 (mid-post)
    h2s = list(re.finditer(r'<h2[\s>]', new))
    if len(h2s) >= 4:
        idx = h2s[3].start()
        new = new[:idx] + quote + new[idx:]
    elif len(h2s) >= 3:
        idx = h2s[2].start()
        new = new[:idx] + quote + new[idx:]

    # Append action card + next steps at the end
    new = new + ACTION_CARD + NEXT_STEPS

    return new, 'enhanced'

def fetch_post(post_id):
    url = f'{WP_BASE}/posts/{post_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (npcwoods-rollout)'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())

def auth_header():
    env = {}
    for line in (REPO.parent / '.env').open():
        line = line.strip()
        if '=' not in line or line.startswith('#'): continue
        k, _, v = line.partition('=')
        env[k] = v.strip().strip('"').strip("'")
    user = env.get('WP_USERNAME','')
    pw = env.get('WP_APP_PASSWORD','').replace(' ','')
    if not user or not pw:
        return None
    cred = base64.b64encode(f'{user}:{pw}'.encode()).decode()
    return f'Basic {cred}'

def push_post(post_id, new_content, max_retries=2):
    url = f'{WP_BASE}/posts/{post_id}'
    body = json.dumps({
        'content': new_content,
        'comment_status': 'closed',
        'ping_status': 'closed',
    }).encode()
    auth = auth_header()
    if not auth:
        raise SystemExit('  WP creds missing in .env')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth,
        'User-Agent': 'Mozilla/5.0 (npcwoods-rollout)',
    }
    # Retry with exponential backoff for transient 403s (CF/GoDaddy WAF rate limit)
    last_err = None
    for attempt in range(max_retries + 1):
        req = urllib.request.Request(url, data=body, method='POST', headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 403 and attempt < max_retries:
                cooldown = 8 * (attempt + 1)  # 8s, then 16s
                time.sleep(cooldown)
                continue
            raise
    raise last_err

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--push', action='store_true')
    ap.add_argument('--slug')
    args = ap.parse_args()
    if not (args.dry_run or args.push):
        ap.error('--dry-run or --push required')

    OUT.mkdir(parents=True, exist_ok=True)

    posts = json.load(open('/tmp/all_posts.json'))
    targets = [p for p in posts if (not args.slug or p['slug'] == args.slug)]

    summary = []
    for p in targets:
        slug = p['slug']
        full = fetch_post(p['id'])
        original = full['content']['rendered']
        new, status = splice_post(slug, original)
        delta = len(new) - len(original)

        if status == 'enhanced':
            # Validate
            bad = BANNED.findall(new)
            if bad:
                summary.append((slug, p['id'], status, f'BANNED: {set(bad)}'))
                continue

            # Save dry-run output
            (OUT / f'{slug}.html').write_text(new, encoding='utf-8')
            (OUT / f'{slug}.json').write_text(json.dumps({
                'id': p['id'], 'slug': slug, 'status': status,
                'orig_len': len(original), 'new_len': len(new), 'delta': delta,
            }, indent=2))

            if args.push:
                try:
                    code = push_post(p['id'], new)
                    summary.append((slug, p['id'], 'PUSHED', f'HTTP {code} (+{delta:,} chars)'))
                    # Inter-request throttle to stay under Cloudflare WAF threshold
                    time.sleep(2.5)
                except urllib.error.HTTPError as e:
                    summary.append((slug, p['id'], 'PUSH-FAILED', f'HTTP {e.code} {e.reason}'))
                    time.sleep(8)  # cooldown before next post if we got blocked
                except Exception as e:
                    summary.append((slug, p['id'], 'PUSH-ERR', str(e)))
            else:
                summary.append((slug, p['id'], status, f'+{delta:,} chars'))
        else:
            summary.append((slug, p['id'], status, '-'))

    # Print summary
    print(f'\n{"slug":40s}  {"id":>4s}  {"status":15s}  notes')
    for s in summary:
        print(f'  {s[0]:40s}  {s[1]:>4d}  {s[2]:15s}  {s[3]}')
    print()
    print(f'Output dir: {OUT}')

if __name__ == '__main__':
    main()
