"""Small helpers that page files use to build story blocks. Keep markup consistent across the series."""
import html as _h

ICONS = {
  'pancreas': '<path d="M3 13c2-4 6-5 9-4s5 0 7-2c1 3-1 7-5 8s-6 0-8 1-3 0-3-3z"/>',
  'stomach': '<path d="M9 3v4c0 2-4 3-4 8a5 5 0 0 0 10 0c0-2 2-3 4-3V9c-3 0-4-2-4-4"/>',
  'brain': '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 1V5a3 3 0 0 0-3-1zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 1"/>',
  'drop': '<path d="M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z"/>',
  'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  'alert': '<path d="M12 3 2 20h20L12 3z"/><path d="M12 10v4M12 17h.01"/>',
  'heart': '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>',
  'plate': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/>',
  'cal': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  'note': '<path d="M5 3h10l4 4v14H5z"/><path d="M9 11h6M9 15h6"/>',
  'chat': '<path d="M4 5h16v11H8l-4 4z"/>',
  'muscle': '<path d="M4 15c3-1 4-5 4-8l3-2 2 2-2 2c1 2 3 3 6 3 2 0 3 2 3 4-6 2-12 2-16-1z"/>',
  'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
  'baby': '<circle cx="12" cy="8" r="4"/><path d="M5 21c0-4 3-7 7-7s7 3 7 7"/>',
  'pill': '<rect x="3" y="9" width="18" height="6" rx="3" transform="rotate(-35 12 12)"/>',
  'glass': '<path d="M6 3h12l-2 18H8z"/><path d="M7 8h10"/>',
  'leaf': '<path d="M5 19C5 9 11 4 20 4c0 9-5 15-15 15z"/><path d="M5 19 14 10"/>',
  'syringe': '<path d="M18 2l4 4M15 5l4 4M17 7 8 16l-3-3 9-9M5 13l-3 3 3 3 3-3"/>',
  'bed': '<path d="M3 18V6M3 14h18v4M7 10h4v4H7zM13 11h6a2 2 0 0 1 2 2v1"/>',
  'bladder': '<path d="M8 8c0-3 2-5 4-5s4 2 4 5c2 1 4 3 4 6 0 4-3 7-8 7s-8-3-8-7c0-3 2-5 4-6z"/><path d="M10 20v2M14 20v2"/>',
  'bug': '<circle cx="12" cy="12" r="4"/><path d="M12 8V4M12 16v4M8 12H4M16 12h4M6 7l-2-2M18 7l2-2M6 17l-2 2M18 17l2 2"/>',
  'flame': '<path d="M12 3c2 4-2 5 0 9 3-2 6 1 6 5a6 6 0 0 1-12 0c0-4 3-7 6-14z"/>',
  'water': '<path d="M12 3s7 8 7 12a7 7 0 0 1-14 0c0-4 7-12 7-12z"/>',
  'kidney': '<path d="M8 5c-3 0-5 3-5 6 0 4 2 7 5 8 1-3 2-6 2-9S9 5 8 5zM16 5c3 0 5 3 5 6 0 4-2 7-5 8-1-3-2-6-2-9s1-5 2-5z"/>',
  'ban': '<circle cx="12" cy="12" r="9"/><path d="M6 6l12 12"/>',
  'check': '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
  'question': '<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 1-1 1.7M12 17h.01"/>',
  'person': '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.5-7 8-7s8 3 8 7"/>',
  'er': '<path d="M3 12h18M12 3v18"/><rect x="3" y="3" width="18" height="18" rx="3"/>',
  'money': '<circle cx="12" cy="12" r="9"/><path d="M12 7v10M9 10h4.5a1.5 1.5 0 0 1 0 3H9m0 0h5"/>',
  'book': '<path d="M4 5a2 2 0 0 1 2-2h12v18H6a2 2 0 0 0-2 2z"/><path d="M6 3v18"/>',
}

def icon(name):
    return ('<span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false">%s</svg></span>' % ICONS[name])

def cite(*ns):
    return ''.join('<sup><a href="#src-%d" aria-label="Source %d">[%d]</a></sup>' % (n, n, n) for n in ns)

def why(text, label='Why it matters'):
    return '<p class="ex-why"><b>%s</b>%s</p>' % (label, text)

def tile(ic, h, p, cls=''):
    return '<div class="ex-tile %s">%s<h3>%s</h3><p>%s</p></div>' % (cls, icon(ic) if ic else '', h, p)

def grid(tiles, cols=''):
    return '<div class="ex-grid %s">%s</div>' % (cols, ''.join(tiles))

def fig(svg, caption, card=True):
    return '<figure class="ex-fig%s">%s<figcaption>%s</figcaption></figure>' % (' ex-card-fig' if card else '', svg, caption)

def svg(fid, title, desc, viewbox, body):
    """Accessible inline diagram. title/desc are read by screen readers."""
    return ('<svg viewBox="%s" role="img" aria-labelledby="%s-t %s-d" focusable="false"><title id="%s-t">%s</title>'
            '<desc id="%s-d">%s</desc>%s</svg>' % (viewbox, fid, fid, fid, _h.escape(title), fid, _h.escape(desc), body))

def sec(theme, sid, kicker, h2, copy, figure='', flip=False, below=''):
    """One story block. theme: cream | white | night | blue | orange."""
    inner = '<div class="ex-copy"><span class="ex-kick">%s</span><h2 id="%s-h">%s</h2>%s</div>' % (kicker, sid, h2, copy)
    if figure:
        body = '<div class="ex-split%s">%s%s</div>' % (' flip' if flip else '', inner, figure)
    else:
        body = inner
    return ('    <section class="ex-sec ex-%s" id="%s" aria-labelledby="%s-h">\n      <div class="ex-in">%s%s</div>\n    </section>\n'
            % (theme, sid, sid, body, below))
