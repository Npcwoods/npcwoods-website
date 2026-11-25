"""Clean, LEAN-style SVG figures for the condition series. No clip art, no cartoons."""
from __future__ import annotations
import html, textwrap
FONT = "'DM Sans','Helvetica Neue',Helvetica,Arial,sans-serif"
SERIF = "'DM Serif Display',Georgia,serif"
INK, BODY, LINE, CREAM = "#1A1A2E", "#4A4A5A", "#E5E7EB", "#F6F3EE"
RED, AMBER, GREEN, BLUE = "#B42318", "#B45309", "#15803D", "#2563EB"
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
            f'<title>{e(title)}</title><rect width="{w}" height="{h}" rx="22" fill="#FFFFFF"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="21" fill="none" stroke="{LINE}" stroke-width="2"/>{inner}</svg>')
def header(title, accent, sub=None):
    t, th = text_block(36, 58, title, 40, size=30, color=INK, weight=400, family=SERIF, lh=36)
    out = f'<rect x="36" y="22" width="46" height="5" rx="2.5" fill="{accent}"/>' + t
    y = 58 + th
    if sub:
        s, sh = text_block(36, y + 2, sub, 62, size=16, color=BODY)
        out += s; y += sh + 4
    return out, y + 10

def rows(title, accent, items, sub=None, w=640):
    """items: (label, desc, color). Tall rows with a colored label pill."""
    head, y = header(title, accent, sub)
    out = [head]
    for label, desc, color in items:
        d, dh = text_block(200, y + 30, desc, 40, size=16, color=BODY, lh=21)
        rh = max(60, dh + 24)
        n = len(lines(label, 14))
        out.append(f'<rect x="28" y="{y}" width="{w-56}" height="{rh}" rx="14" fill="{CREAM}"/>')
        out.append(f'<rect x="40" y="{y+10}" width="144" height="{rh-20}" rx="10" fill="{color}"/>')
        lt, _ = text_block(112, y + rh/2 + 5 - (n-1)*9, label, 14, size=15, color="#FFFFFF", weight=800, anchor="middle", lh=18)
        out.append(lt + d)
        y += rh + 10
    return svg(w, y + 20, title, "".join(out)), y + 20

def columns(title, accent, cols, sub=None, w=640):
    """cols: (heading, color, [items])"""
    head, y = header(title, accent, sub)
    n = len(cols); gap = 14; cw = (w - 56 - gap*(n-1)) / n
    out = [head]; maxh = 0; parts = []
    for i, (hd, color, items) in enumerate(cols):
        x = 28 + i*(cw+gap)
        p = [f'<rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="8" rx="4" fill="{color}"/>']
        ht, hh = text_block(x + 12, y + 40, hd, int(cw/10.5), size=19, color=INK, weight=800, lh=23)
        p.append(ht); yy = y + 40 + hh + 4
        for it in items:
            tt, th = text_block(x + 28, yy, it, int(cw/9.0) - 3, size=15, color=BODY, lh=20)
            p.append(f'<circle cx="{x+16:.0f}" cy="{yy-5}" r="4" fill="{color}"/>' + tt)
            yy += th + 8
        parts.append((x, p, yy))
        maxh = max(maxh, yy - y)
    for x, p, yy in parts:
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="{maxh+10}" rx="14" fill="{CREAM}"/>')
        out.extend(p)
    h = y + maxh + 40
    return svg(w, h, title, "".join(out)), h

def range_bar(title, accent, segs, sub=None, w=640, footnote=None):
    """segs: (label, sublabel, color, frac)"""
    head, y = header(title, accent, sub)
    out = [head]; x = 36; bw = w - 72; y += 10
    for i, (label, sublabel, color, frac) in enumerate(segs):
        sw = bw * frac
        rx = 14
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{sw:.0f}" height="56" fill="{color}" rx="{rx if i in (0, len(segs)-1) else 0}"/>')
        if 0 < i < len(segs)-1:
            pass
        lt, _ = text_block(x + sw/2, y + 35, label, 18, size=17, color="#FFFFFF", weight=800, anchor="middle")
        out.append(lt)
        st, sh = text_block(x + sw/2, y + 86, sublabel, int(sw/8.5), size=15, color=INK, weight=700, anchor="middle", lh=19)
        out.append(st)
        x += sw
    y += 86 + 60
    if footnote:
        ft, fh = text_block(36, y, footnote, 64, size=15, color=BODY)
        out.append(ft); y += fh
    return svg(w, y + 20, title, "".join(out)), y + 20

def flow(title, accent, steps, sub=None, w=640):
    """Vertical numbered-free step flow: (heading, desc, color). Dotted connector."""
    head, y = header(title, accent, sub)
    out = [head]; prev = None
    for hd, desc, color in steps:
        ht, hh = text_block(96, y + 30, hd, 34, size=19, color=INK, weight=800, lh=23)
        dt, dh = text_block(96, y + 30 + hh + 2, desc, 46, size=15, color=BODY, lh=20)
        bh = 30 + hh + dh + 14
        if prev is not None:
            out.append(f'<path d="M58 {prev} V{y+22}" stroke="{accent}" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round"/>')
        out.append(f'<circle cx="58" cy="{y+26}" r="14" fill="#fff" stroke="{color}" stroke-width="4"/>')
        out.append(ht + dt)
        prev = y + 42
        y += bh + 8
    return svg(w, y + 16, title, "".join(out)), y + 16

def bell(title, accent, sub=None, w=640, labels=("Low flag", "Normal range: middle 95% of healthy people", "High flag")):
    head, y = header(title, accent, sub)
    import math
    cx, base, amp, sd = w/2, y + 210, 170, 92
    pts = []
    for i in range(0, 561):
        x = 40 + i
        z = (x - cx) / sd
        pts.append(f"{x},{base - amp*math.exp(-z*z/2):.1f}")
    lo, hi = cx - 1.96*sd, cx + 1.96*sd
    out = [head,
      f'<rect x="{lo:.0f}" y="{y}" width="{hi-lo:.0f}" height="{base-y}" fill="{accent}" fill-opacity=".10"/>',
      f'<polyline points="{" ".join(pts)}" fill="none" stroke="{accent}" stroke-width="4" stroke-linejoin="round"/>',
      f'<path d="M40 {base} H{w-40}" stroke="{INK}" stroke-width="2"/>',
      f'<path d="M{lo:.0f} {y} V{base}" stroke="{accent}" stroke-width="2" stroke-dasharray="4 6"/>',
      f'<path d="M{hi:.0f} {y} V{base}" stroke="{accent}" stroke-width="2" stroke-dasharray="4 6"/>']
    a, _ = text_block(cx, base + 30, labels[1], 46, size=15, color=INK, weight=700, anchor="middle")
    b, _ = text_block((40+lo)/2, base + 30, labels[0], 10, size=15, color=RED, weight=800, anchor="middle")
    c, _ = text_block((hi+w-40)/2, base + 30, labels[2], 10, size=15, color=RED, weight=800, anchor="middle")
    out += [a, b, c]
    return svg(w, base + 80, title, "".join(out)), base + 80
