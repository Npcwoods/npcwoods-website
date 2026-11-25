"""Clean, LEAN-style SVG figures for the condition series. No clip art, no cartoons.

Phone-first: every figure is drawn on a narrow 360-unit canvas and stacks top to
bottom, so on a 390px phone it renders near 1:1 and body text stays >= 15px.
"""
from __future__ import annotations
import html, textwrap
FONT = "'DM Sans','Helvetica Neue',Helvetica,Arial,sans-serif"
SERIF = "'DM Serif Display',Georgia,serif"
INK, BODY, LINE, CREAM = "#1A1A2E", "#4A4A5A", "#E5E7EB", "#F6F3EE"
RED, AMBER, GREEN, BLUE = "#B42318", "#B45309", "#15803D", "#2563EB"
W = 360          # canvas width (viewBox units)
PAD = 20         # outer padding
MIN_TEXT = 16    # smallest body text on the canvas
def e(t): return html.escape(str(t), quote=True)
def lines(t, width): return textwrap.wrap(str(t), width) or [""]
def text_block(x, y, t, width, size=17, color=BODY, weight=500, lh=None, anchor="start", family=FONT):
    lh = lh or int(size * 1.35)
    out = []
    for i, ln in enumerate(lines(t, width)):
        out.append(f'<text x="{x}" y="{y + i*lh}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}" font-family="{family}">{e(ln)}</text>')
    return "".join(out), len(lines(t, width)) * lh
def svg(w, h, title, inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" font-family="{FONT}">'
            f'<title>{e(title)}</title><rect width="{w}" height="{h}" rx="20" fill="#FFFFFF"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="19" fill="none" stroke="{LINE}" stroke-width="2"/>{inner}</svg>')
def header(title, accent, sub=None):
    t, th = text_block(PAD + 4, 56, title, 24, size=26, color=INK, weight=400, family=SERIF, lh=31)
    out = f'<rect x="{PAD+4}" y="22" width="40" height="5" rx="2.5" fill="{accent}"/>' + t
    y = 56 + th - 6
    if sub:
        s, sh = text_block(PAD + 4, y + 18, sub, 36, size=MIN_TEXT, color=BODY, lh=22)
        out += s; y += sh + 8
    return out, y + 14

def _pill(x, y, label, color):
    pw = int(len(label) * 9.4 + 28)
    return (f'<rect x="{x}" y="{y}" width="{pw}" height="28" rx="14" fill="{color}"/>'
            f'<text x="{x + pw/2:.0f}" y="{y+19}" font-size="16" fill="#FFFFFF" font-weight="800" text-anchor="middle" font-family="{FONT}">{e(label)}</text>')

def rows(title, accent, items, sub=None, w=W):
    """items: (label, desc, color). Stacked cards: colored label pill on top, text under it."""
    head, y = header(title, accent, sub)
    out = [head]
    for label, desc, color in items:
        d, dh = text_block(PAD + 16, y + 62, desc, 34, size=MIN_TEXT, color=BODY, lh=22)
        rh = 62 + dh - 6
        out.append(f'<rect x="{PAD}" y="{y}" width="{w-2*PAD}" height="{rh}" rx="14" fill="{CREAM}"/>')
        out.append(_pill(PAD + 14, y + 14, label, color) + d)
        y += rh + 10
    return svg(w, y + 12, title, "".join(out)), y + 12

def columns(title, accent, cols, sub=None, w=W):
    """cols: (heading, color, [items]). On the narrow canvas each column is its own stacked card."""
    head, y = header(title, accent, sub)
    out = [head]
    for hd, color, items in cols:
        top = y
        p = []
        ht, hh = text_block(PAD + 16, y + 40, hd, 28, size=19, color=INK, weight=800, lh=24)
        p.append(ht); yy = y + 40 + hh + 4
        for it in items:
            tt, th = text_block(PAD + 36, yy, it, 31, size=MIN_TEXT, color=BODY, lh=22)
            p.append(f'<circle cx="{PAD+22}" cy="{yy-5}" r="4.5" fill="{color}"/>' + tt)
            yy += th + 6
        ch = yy - top + 4
        out.append(f'<rect x="{PAD}" y="{top}" width="{w-2*PAD}" height="{ch}" rx="14" fill="{CREAM}"/>')
        out.append(f'<rect x="{PAD}" y="{top}" width="8" height="{ch}" rx="4" fill="{color}"/>')
        out.extend(p)
        y = top + ch + 12
    return svg(w, y + 8, title, "".join(out)), y + 8

def range_bar(title, accent, segs, sub=None, w=W, footnote=None):
    """segs: (label, sublabel, color, frac). A full-width bar, then a stacked key under it."""
    head, y = header(title, accent, sub)
    out = [head]; x = PAD; bw = w - 2*PAD; bar = []
    for label, sublabel, color, frac in segs:
        sw = bw * frac
        bar.append(f'<rect x="{x:.1f}" y="{y}" width="{sw+0.5:.1f}" height="22" fill="{color}"/>')
        x += sw
    out.append(f'<clipPath id="rb"><rect x="{PAD}" y="{y}" width="{bw}" height="22" rx="11"/></clipPath>'
               f'<g clip-path="url(#rb)">' + "".join(bar) + '</g>')
    y += 22 + 20
    for label, sublabel, color, frac in segs:
        out.append(f'<rect x="{PAD}" y="{y}" width="{w-2*PAD}" height="56" rx="14" fill="{CREAM}"/>')
        out.append(f'<rect x="{PAD+14}" y="{y+16}" width="24" height="24" rx="6" fill="{color}"/>')
        out.append(f'<text x="{PAD+50}" y="{y+25}" font-size="18" fill="{INK}" font-weight="800" font-family="{FONT}">{e(label)}</text>')
        out.append(f'<text x="{PAD+50}" y="{y+46}" font-size="{MIN_TEXT}" fill="{BODY}" font-weight="600" font-family="{FONT}">{e(sublabel)}</text>')
        y += 56 + 10
    y += 14
    if footnote:
        ft, fh = text_block(PAD + 4, y + 4, footnote, 36, size=MIN_TEXT, color=BODY, lh=22)
        out.append(ft); y += fh
    return svg(w, y + 14, title, "".join(out)), y + 14

def flow(title, accent, steps, sub=None, w=W):
    """Vertical step flow: (heading, desc, color). Dotted connector."""
    head, y = header(title, accent, sub)
    out = [head]; prev = None
    for hd, desc, color in steps:
        ht, hh = text_block(PAD + 52, y + 30, hd, 24, size=19, color=INK, weight=800, lh=24)
        dt, dh = text_block(PAD + 52, y + 30 + hh + 2, desc, 30, size=MIN_TEXT, color=BODY, lh=22)
        bh = 30 + hh + dh + 10
        if prev is not None:
            out.append(f'<path d="M{PAD+20} {prev} V{y+10}" stroke="{accent}" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round"/>')
        out.append(f'<circle cx="{PAD+20}" cy="{y+24}" r="13" fill="#fff" stroke="{color}" stroke-width="4"/>')
        out.append(ht + dt)
        prev = y + 42
        y += bh + 8
    return svg(w, y + 12, title, "".join(out)), y + 12

def bell(title, accent, sub=None, w=W, labels=("Low flag", "Normal range: the middle 95% of healthy people", "High flag")):
    head, y = header(title, accent, sub)
    import math
    left, right = PAD + 4, w - PAD - 4
    cx, base, amp, sd = w/2, y + 150, 124, 64
    pts = []
    for i in range(0, int(right - left) + 1):
        x = left + i
        z = (x - cx) / sd
        pts.append(f"{x},{base - amp*math.exp(-z*z/2):.1f}")
    lo, hi = cx - 1.96*sd, cx + 1.96*sd
    out = [head,
      f'<rect x="{lo:.0f}" y="{y}" width="{hi-lo:.0f}" height="{base-y}" fill="{accent}" fill-opacity=".10"/>',
      f'<polyline points="{" ".join(pts)}" fill="none" stroke="{accent}" stroke-width="4" stroke-linejoin="round"/>',
      f'<path d="M{left} {base} H{right}" stroke="{INK}" stroke-width="2"/>',
      f'<path d="M{lo:.0f} {y} V{base}" stroke="{accent}" stroke-width="2" stroke-dasharray="4 6"/>',
      f'<path d="M{hi:.0f} {y} V{base}" stroke="{accent}" stroke-width="2" stroke-dasharray="4 6"/>']
    b, _ = text_block(left, base + 28, labels[0], 10, size=MIN_TEXT, color=RED, weight=800)
    c, _ = text_block(right, base + 28, labels[2], 10, size=MIN_TEXT, color=RED, weight=800, anchor="end")
    a, ah = text_block(cx, base + 62, labels[1], 30, size=MIN_TEXT, color=INK, weight=700, anchor="middle", lh=22)
    out += [a, b, c]
    h = base + 62 + ah + 12
    return svg(w, h, title, "".join(out)), h
