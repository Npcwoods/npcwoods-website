#!/usr/bin/env python3
"""Build GLP-1 explainer pages from template.html + partials + pages/<slug>.py.

Usage:  python3 build.py                 # build every page in pages/
        python3 build.py first-30-days   # build one page
Output: out/<slug>/index.html  (deploy to html/learn/glp1/<slug>/index.html)
"""
import json, os, re, sys, html, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
def rd(*p): return open(os.path.join(HERE, *p), encoding='utf-8').read()

SERIES = json.loads(rd('series.json'))
CTA = SERIES['cta']

def strip_tags(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()

def roadmap(slug):
    out = []
    for st in SERIES['stops']:
        if st['slug'] == slug:
            out.append('            <li class="here" aria-current="step"><span class="dot" aria-hidden="true"></span><span class="t">%s</span><span class="vh"> (you are here)</span></li>' % st['label'])
        elif st['url']:
            out.append('            <li class="live"><span class="dot" aria-hidden="true"></span><a href="%s">%s</a></li>' % (st['url'], st['label']))
        else:
            out.append('            <li class="soon"><span class="dot" aria-hidden="true"></span><span class="t">%s</span><span class="vh"> (coming soon)</span></li>' % st['label'])
    return '\n'.join(out)

def prevnext(slug):
    stops = SERIES['stops']; i = [s['slug'] for s in stops].index(slug)
    prev = stops[i - 1]; nxt = stops[i + 1] if i + 1 < len(stops) else None
    p = ('          <a class="prev" href="%s"><small>← Last stop</small><strong>%s</strong><span class="d">%s</span></a>'
         % (prev['url'], prev['title'], prev['blurb']))
    if nxt and nxt['url']:
        n = ('          <a class="next" href="%s"><small>Next stop →</small><strong>%s</strong><span class="d">%s</span></a>'
             % (nxt['url'], nxt['title'], nxt['blurb']))
    elif nxt:
        n = ('          <div class="soon"><small>Next stop · coming soon</small><strong>%s</strong><span class="d">%s</span></div>'
             % (nxt['title'], nxt['blurb']))
    else:
        n = ''
    return p + '\n' + n

def jsonld(P, url):
    page = {
        "@context": "https://schema.org", "@type": "MedicalWebPage", "@id": url + "#webpage",
        "name": P['h1_text'], "headline": P['h1_text'], "url": url, "description": P['description'],
        "inLanguage": "en-US",
        "isPartOf": {"@type": "WebSite", "name": "NPCWoods Telemedicine", "url": "https://npcwoods.com/"},
        "author": {"@type": "Person", "@id": "https://npcwoods.com/#chris-woods", "name": "Chris Woods",
                    "honorificSuffix": "MSN, APRN, FNP-C", "jobTitle": "Nurse Practitioner", "url": "https://npcwoods.com/about/"},
        "reviewedBy": {"@id": "https://npcwoods.com/#chris-woods"},
        "lastReviewed": P['reviewed'], "datePublished": P.get('published', P['reviewed']), "dateModified": P['reviewed'],
        "about": {"@type": "MedicalCondition", "name": P['about']},
        "audience": {"@type": "PeopleAudience", "audienceType": "Patients"},
        "specialty": "Telemedicine",
        "citation": [{"@type": "CreativeWork", "name": strip_tags(re.sub(r'<a [^>]*>.*?</a>', '', s)).rstrip(' .'), "url": re.search(r'href="([^"]+)"', s).group(1)} for s in P['sources']],
    }
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://npcwoods.com/"},
            {"@type": "ListItem", "position": 2, "name": "Learn", "item": "https://npcwoods.com/learn/"},
            {"@type": "ListItem", "position": 3, "name": "GLP-1 Explained", "item": "https://npcwoods.com/learn/glp1/"},
            {"@type": "ListItem", "position": 4, "name": P['crumb'], "item": url},
        ]}
    blocks = [page, crumbs]
    if P.get('faq'):
        blocks.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in P['faq']]})
    return '\n'.join('  <script type="application/ld+json">\n%s\n  </script>' % json.dumps(b, indent=2, ensure_ascii=False) for b in blocks)

def load_page(slug):
    spec = importlib.util.spec_from_file_location('page_' + slug.replace('-', '_'), os.path.join(HERE, 'pages', slug + '.py'))
    m = importlib.util.module_from_spec(spec); sys.path[:0] = [HERE, os.path.join(HERE, 'pages')]; spec.loader.exec_module(m)
    return m.PAGE

MONTHS = 'January February March April May June July August September October November December'.split()
def human(d):
    y, m, dd = d.split('-'); return '%s %d, %s' % (MONTHS[int(m) - 1], int(dd), y)

def build(slug):
    P = load_page(slug)
    url = 'https://npcwoods.com/learn/glp1/%s/' % slug
    P['h1_text'] = (P['h1_top'] + ' ' + P['h1_pop']).strip()
    v = {
        'title': html.escape(P['title'], quote=True), 'description': html.escape(P['description'], quote=True), 'url': url,
        'jsonld': jsonld(P, url), 'css': rd('partials', 'explainer.css').rstrip(),
        'site_header': rd('partials', 'site-header.html').rstrip(), 'site_footer': rd('partials', 'site-footer.html').rstrip(),
        'ghost_svg': P['ghost_svg'].strip(), 'pill': P['pill'], 'h1_top': P['h1_top'], 'h1_pop': P['h1_pop'], 'sub': P['sub'],
        'cta_href': CTA['href'], 'cta_label': CTA['label'], 'cta_fine': CTA['fine'], 'jump_label': P.get('jump_label', 'Start reading'),
        'sticker1': P['sticker1'], 'sticker2': P['sticker2'], 'roadmap_items': roadmap(slug), 'crumb': P['crumb'],
        'reviewed_human': human(P['reviewed']), 'lede': P['lede'],
        'tldr_items': '\n'.join('            <li>%s</li>' % t for t in P['tldr']),
        'sections': '\n'.join(P['sections']), 'recap_title': P['recap_title'],
        'recap_items': '\n'.join('          <div class="ex-chip"><h3>%s</h3><p>%s</p></div>' % (h, p) for h, p in P['recap']),
        'faq_items': '\n'.join('        <details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in P['faq']),
        'source_items': '\n'.join('          <li id="src-%d">%s</li>' % (i + 1, s) for i, s in enumerate(P['sources'])),
        'prevnext': prevnext(slug), 'cta_title': P['cta_title'], 'cta_text': P['cta_text'], 'disclaimer': P['disclaimer'],
    }
    out = rd('template.html')
    for k, val in v.items():
        out = out.replace('{{%s}}' % k, val)
    left = re.findall(r'\{\{\w+\}\}', out)
    assert not left, 'unfilled placeholders: %s' % left
    os.makedirs(os.path.join(HERE, 'out', slug), exist_ok=True)
    dst = os.path.join(HERE, 'out', slug, 'index.html')
    open(dst, 'w', encoding='utf-8').write(out)
    print('built', dst, len(out), 'bytes')

if __name__ == '__main__':
    slugs = sys.argv[1:] or sorted(f[:-3] for f in os.listdir(os.path.join(HERE, 'pages')) if f.endswith('.py') and not f.startswith('_'))
    for s in slugs: build(s)
