#!/usr/bin/env python3
"""Draw the dental-abscess series body illustrations as static SVG files.

Writes landing-pages/learn/dental-abscess/assets/*.svg. Kitchen only, never
deploys. Clean, light SVG in the homepage palette (ink, blue, cream, white)
with the series red #B42318 on accents only. Anatomy is kept simple on
purpose: enamel, dentin, pulp, nerve and blood vessels, root, gum, jawbone.
No drug names, no product names, no numbers-as-promises.
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "landing-pages" / "learn" / "dental-abscess" / "assets"

INK = "#1A1A2E"
BODY = "#4A4A5A"
BLUE = "#2563EB"
BLUE_DARK = "#1D4ED8"
IMSG = "#007AFF"
CREAM = "#F6F3EE"
WHITE = "#FFFFFF"
RED = "#B42318"
RED_SOFT = "#F3E8E8"
RED_WASH = "#FFF1F0"
FONT = "'DM Sans','Helvetica Neue',Helvetica,Arial,sans-serif"


def defs(uid: str) -> str:
    return f"""<defs>
<linearGradient id="{uid}en" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DCE4F0"/></linearGradient>
<linearGradient id="{uid}de" gradientUnits="userSpaceOnUse" x1="0" y1="20" x2="0" y2="340"><stop offset="0" stop-color="#F5EAD3"/><stop offset="1" stop-color="#E6D3AE"/></linearGradient>
<linearGradient id="{uid}pu" gradientUnits="userSpaceOnUse" x1="0" y1="80" x2="0" y2="330"><stop offset="0" stop-color="#F7B9B1"/><stop offset="1" stop-color="#EE958B"/></linearGradient>
<linearGradient id="{uid}pd" gradientUnits="userSpaceOnUse" x1="0" y1="80" x2="0" y2="330"><stop offset="0" stop-color="#B9ADA2"/><stop offset="1" stop-color="#8F8379"/></linearGradient>
<linearGradient id="{uid}pi" gradientUnits="userSpaceOnUse" x1="0" y1="80" x2="0" y2="330"><stop offset="0" stop-color="#F59A8F"/><stop offset="1" stop-color="#E06F63"/></linearGradient>
<linearGradient id="{uid}gu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4B3B0"/><stop offset="1" stop-color="#E59591"/></linearGradient>
<linearGradient id="{uid}bo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F1E9DC"/><stop offset="1" stop-color="#E4D8C4"/></linearGradient>
<radialGradient id="{uid}ps" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#FFF6DA"/><stop offset="1" stop-color="#F1CF7A"/></radialGradient>
<linearGradient id="{uid}bl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3B82F6"/><stop offset="1" stop-color="{BLUE_DARK}"/></linearGradient>
<linearGradient id="{uid}rd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C8321F"/><stop offset="1" stop-color="#8F1C12"/></linearGradient>
<pattern id="{uid}dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="2.4" fill="#D8C9B0"/><circle cx="14" cy="13" r="1.8" fill="#D8C9B0"/></pattern>
<filter id="{uid}sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="{INK}" flood-opacity=".16"/></filter>
<filter id="{uid}sm" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="{INK}" flood-opacity=".14"/></filter>
</defs>"""


def svg(w: int, h: int, title: str, body: str, uid: str = "a") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" font-family="{FONT}">'
        f"<title>{escape(title)}</title>{defs(uid)}{body}</svg>\n"
    )


def text(x, y, s, size=20, weight=600, fill=INK, anchor="start", extra=""):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}"{extra}>{escape(s)}</text>'
    )


def lines(x, y, rows, size=20, weight=600, fill=INK, anchor="start", lh=1.25):
    out = [f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">']
    for i, row in enumerate(rows):
        dy = 0 if i == 0 else round(size * lh, 1)
        out.append(f'<tspan x="{x}" dy="{dy}">{escape(row)}</tspan>')
    out.append("</text>")
    return "".join(out)


def card(x, y, w, h, fill=WHITE, stroke="rgba(26,26,46,.10)", r=22, uid="a", shadow=True, sw=1.5):
    f = f' filter="url(#{uid}sm)"' if shadow else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{f}/>'


def leader(x1, y1, x2, y2, color=BODY):
    return (
        f'<circle cx="{x1}" cy="{y1}" r="4.5" fill="{WHITE}" stroke="{color}" stroke-width="2.5"/>'
        f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="2" fill="none"/>'
    )


def chip(x, y, label, fill=BLUE, color=WHITE, size=17, pad=12, w=None):
    w = w or int(len(label) * size * 0.56 + pad * 2)
    h = size + 16
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}"/>'
        + text(x + w / 2, y + h / 2 + size * 0.36, label, size=size, weight=800, fill=color, anchor="middle")
    )


# ---------------------------------------------------------------- the tooth
# Local coordinates: a lower molar, crown up, two roots down.
# x 20..180, y 8..338. Gum line about y 132. Bone crest about y 168.
TOOTH = (
    "M20 60 C20 25 40 8 60 14 C75 18 85 28 100 22 C115 16 125 10 140 14 "
    "C165 20 180 35 180 60 C180 95 172 120 165 140 C160 190 158 250 150 320 "
    "C148 338 129 338 127 322 C122 270 115 222 100 202 C85 222 78 270 73 322 "
    "C71 338 52 338 50 320 C42 250 40 190 35 140 C28 120 20 95 20 60 Z"
)
DENTIN_CROWN = (
    "M37 64 C37 42 50 32 62 34 C76 37 86 44 100 40 C114 36 126 32 138 34 "
    "C152 37 163 46 163 64 C163 92 162 118 166 137 L34 137 C38 118 37 92 37 64 Z"
)
PULP_CHAMBER = (
    "M70 100 C69 84 76 76 86 84 C93 90 107 90 114 84 C124 76 131 84 130 100 "
    "C130 126 128 150 126 166 L74 166 C72 150 70 126 70 100 Z"
)
CANAL_L = "M74 160 C70 205 66 262 61.5 326"
CANAL_R = "M126 160 C130 205 134 262 138.5 326"
APEX_L = (61.5, 342)
APEX_R = (138.5, 342)


def jaw(uid, bone_loss_right=False):
    crest_r = "Q200 186 270 196" if bone_loss_right else "Q200 170 270 180"
    right_top = 206 if bone_loss_right else 168
    bone = (
        f'<path d="M-70 180 Q0 170 36 168 L164 168 L166 {right_top} {crest_r} L270 372 Q270 402 240 402 '
        f'L-40 402 Q-70 402 -70 372 Z" fill="url(#{uid}bo)"/>'
        f'<path d="M-70 180 Q0 170 36 168 L164 168 L166 {right_top} {crest_r} L270 372 Q270 402 240 402 '
        f'L-40 402 Q-70 402 -70 372 Z" fill="url(#{uid}dots)" opacity=".75"/>'
    )
    gum = (
        f'<path d="M-70 152 Q-10 144 20 129 Q30 123 38 133 L162 133 Q170 123 180 129 Q210 144 270 152 '
        f'L270 210 Q200 200 160 200 L40 200 Q0 200 -70 210 Z" fill="url(#{uid}gu)"/>'
    )
    return bone + gum


def tooth(uid, pulp="healthy", cavity=None, crack=False, apex_abscess=False,
          gum_abscess=False, vessels=True, filled=False, germs=False, drain=False):
    pulp_fill = {"healthy": f"url(#{uid}pu)", "dead": f"url(#{uid}pd)", "angry": f"url(#{uid}pi)"}[pulp]
    if filled:
        pulp_fill = "#6B7A99"
    parts = [f'<g filter="url(#{uid}sh)"><path d="{TOOTH}" fill="url(#{uid}de)" stroke="#C9B48C" stroke-width="2"/></g>']
    parts.append(
        f'<clipPath id="{uid}cc"><rect x="0" y="0" width="200" height="137"/></clipPath>'
        f'<path d="{TOOTH}" clip-path="url(#{uid}cc)" fill="url(#{uid}en)"/>'
        f'<path d="{DENTIN_CROWN}" fill="url(#{uid}de)"/>'
        f'<path d="M30 52 C34 34 46 24 58 24" stroke="#fff" stroke-width="6" stroke-linecap="round" fill="none" opacity=".9"/>'
    )
    parts.append(f'<path d="{PULP_CHAMBER}" fill="{pulp_fill}"/>')
    parts.append(
        f'<path d="{CANAL_L}" stroke="{pulp_fill}" stroke-width="11" stroke-linecap="round" fill="none"/>'
        f'<path d="{CANAL_R}" stroke="{pulp_fill}" stroke-width="11" stroke-linecap="round" fill="none"/>'
    )
    if filled:
        parts.append(
            '<path d="M60 70 Q100 54 140 70 L140 30 Q100 16 60 30 Z" fill="#C7CFDD" opacity=".9"/>'
        )
    if vessels and pulp != "dead" and not filled:
        for dx, col in ((-2.2, "#C8321F"), (2.2, "#2F6FE4")):
            parts.append(
                f'<path d="M{86+dx} 104 C{80+dx} 130 {74+dx} 150 {74+dx} 162 C{70+dx} 205 {66+dx} 262 {61.5+dx} 330 '
                f'C{60+dx} 352 {40+dx} 362 {10+dx} 366" stroke="{col}" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
                f'<path d="M{114+dx} 104 C{120+dx} 130 {126+dx} 150 {126+dx} 162 C{130+dx} 205 {134+dx} 262 {138.5+dx} 330 '
                f'C{140+dx} 352 {160+dx} 362 {190+dx} 366" stroke="{col}" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
            )
    if cavity:
        depth = {"shallow": 36, "mid": 60, "deep": 88}[cavity]
        parts.append(
            f'<path d="M76 21 C78 17 92 15 95 21 C96 {depth*0.55:.0f} {92} {depth-6} {86} {depth} '
            f'C{80} {depth-6} {75} {depth*0.55:.0f} 76 21 Z" fill="#3E3446"/>'
        )
    if crack:
        parts.append(
            '<path d="M118 16 L112 40 L120 58 L110 80 L116 98" stroke="#3E3446" stroke-width="4" '
            'fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
        )
    if germs:
        for gx, gy in ((84, 30), (88, 52), (83, 72), (92, 96), (80, 120), (72, 170), (68, 230), (64, 290)):
            parts.append(f'<ellipse cx="{gx}" cy="{gy}" rx="5" ry="3" fill="{BLUE_DARK}" transform="rotate(30 {gx} {gy})"/>')
    if apex_abscess:
        cx, cy = APEX_L
        parts.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="25" fill="none" stroke="{RED}" stroke-width="2" '
            f'stroke-dasharray="3 6" opacity=".7"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="25" ry="18" fill="url(#{uid}ps)" stroke="{RED}" stroke-width="3.5"/>'
        )
        if drain:
            parts.append(
                f'<path d="M{cx} {cy-14} C{cx+2} 260 {cx+8} 190 {cx+16} 120" stroke="{RED}" stroke-width="3" '
                f'stroke-dasharray="6 6" fill="none"/>'
            )
    if gum_abscess:
        parts.append(
            f'<path d="M166 136 C170 160 168 196 162 222" stroke="#5A3F3F" stroke-width="5" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="184" cy="178" rx="20" ry="30" fill="url(#{uid}ps)" stroke="{RED}" stroke-width="3.5"/>'
        )
    return "".join(parts)


def tooth_scene(uid, tx, ty, s, jaw_on=True, bone_loss_right=False, **kw):
    inner = (jaw(uid, bone_loss_right) if jaw_on else "") + tooth(uid, **kw)
    clip = (
        f'<clipPath id="{uid}jc"><rect x="-70" y="0" width="340" height="402" rx="26"/></clipPath>'
    )
    return f'<g transform="translate({tx} {ty}) scale({s})">{clip}<g clip-path="url(#{uid}jc)">{inner}</g></g>'


def pt(tx, ty, s, x, y):
    return round(tx + x * s, 1), round(ty + y * s, 1)


# ---------------------------------------------------------------- figures

def fig_tooth_map():
    uid = "tm"
    W, H = 640, 600
    s, tx, ty = 1.12, 208, 70
    b = [card(8, 8, W - 16, H - 16, fill=CREAM, uid=uid, shadow=False, stroke="rgba(26,26,46,.08)")]
    b.append(text(32, 50, "INSIDE A TOOTH", size=16, weight=800, fill=RED, extra=' letter-spacing="2"'))
    b.append(tooth_scene(uid, tx, ty, s))
    # target markers (where an abscess forms)
    ax, ay = pt(tx, ty, s, *APEX_L)
    gx, gy = pt(tx, ty, s, 186, 176)
    for (cx, cy, r) in ((ax, ay, 30), (gx, gy, 28)):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(180,35,24,.10)" stroke="{RED}" stroke-width="3" stroke-dasharray="7 6"/>')
        b.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{RED}"/>')
    # left labels
    L = [
        ("Enamel", "hard white shell", (34, 70), 100),
        ("Dentin", "softer layer", (52, 118), 180),
        ("Pulp", "the nerve room", (98, 124), 260),
        ("Nerve and", "blood vessels", (68, 250), 340),
    ]
    for title, sub, (lx, ly), y in L:
        px, py = pt(tx, ty, s, lx, ly)
        b.append(leader(px, py, 150, y - 6))
        b.append(text(144, y - 6, title, size=21, weight=800, anchor="end"))
        b.append(text(144, y + 16, sub, size=16, weight=500, fill=BODY, anchor="end"))
    R = [
        ("Gum", "pink cover", (240, 150), 150),
        ("Root", "holds the tooth", (152, 280), 392),
        ("Jawbone", "the socket", (232, 370), 470),
    ]
    for title, sub, (lx, ly), y in R:
        px, py = pt(tx, ty, s, lx, ly)
        b.append(leader(px, py, 490, y - 6))
        b.append(text(496, y - 6, title, size=21, weight=800))
        b.append(text(496, y + 16, sub, size=16, weight=500, fill=BODY))
    # abscess keys
    b.append(f'<path d="M{ax} {ay+30} L{ax} 540 L150 540" stroke="{RED}" stroke-width="2" fill="none"/>')
    b.append(lines(144, 532, ["Tooth abscess:", "at the root tip"], size=18, weight=800, fill=RED, anchor="end"))
    b.append(f'<path d="M{gx+28} {gy} L490 {gy+10}" stroke="{RED}" stroke-width="2" fill="none"/>')
    b.append(lines(496, gy + 4, ["Gum abscess:", "beside the", "tooth"], size=18, weight=800, fill=RED))
    return svg(W, H, "Labeled tooth cross-section", "".join(b), uid)


def fig_cavity_steps():
    uid = "cs"
    W, H = 640, 780
    b = []
    steps = [
        ("Acid digs a hole", "in the enamel shell.", dict(cavity="shallow")),
        ("The hole reaches", "the softer dentin.", dict(cavity="mid")),
        ("Germs reach the pulp.", "The nerve gets angry.", dict(cavity="deep", pulp="angry", germs=True)),
        ("The nerve dies. A pus", "pocket forms at the root tip.", dict(cavity="deep", pulp="dead", apex_abscess=True)),
    ]
    for i, (a, c, kw) in enumerate(steps):
        col, row = i % 2, i // 2
        x0, y0 = 12 + col * 314, 12 + row * 384
        b.append(card(x0, y0, 302, 370, fill=WHITE, uid=uid))
        b.append(f'<circle cx="{x0+34}" cy="{y0+34}" r="18" fill="url(#{uid}bl)"/>')
        b.append(text(x0 + 34, y0 + 41, str(i + 1), size=19, weight=800, fill=WHITE, anchor="middle"))
        b.append(tooth_scene(f"{uid}{i}", x0 + 92, y0 + 22, 0.62, **kw))
        b.append(lines(x0 + 151, y0 + 312, [a, c], size=18, weight=700, anchor="middle"))
    body = "".join(b)
    # every scene uses its own uid defs for clip ids, but shares gradients
    return svg(W, H, "Four steps from cavity to abscess", body.replace(f"url(#{uid}0", f"url(#{uid}").replace(f"url(#{uid}1", f"url(#{uid}").replace(f"url(#{uid}2", f"url(#{uid}").replace(f"url(#{uid}3", f"url(#{uid}"), uid)


def multi(uid, scenes):
    """Render several tooth scenes that share one defs block."""
    out = []
    for i, (tx, ty, s, kw) in enumerate(scenes):
        g = tooth_scene(uid, tx, ty, s, **kw)
        g = g.replace(f'id="{uid}jc"', f'id="{uid}jc{i}"').replace(f"url(#{uid}jc)", f"url(#{uid}jc{i})")
        g = g.replace(f'id="{uid}cc"', f'id="{uid}cc{i}"').replace(f"url(#{uid}cc)", f"url(#{uid}cc{i})")
        out.append(g)
    return "".join(out)


def fig_cavity_steps2():
    uid = "cs"
    W, H = 640, 780
    b = []
    steps = [
        ("Acid digs a hole", "in the enamel shell.", dict(cavity="shallow")),
        ("The hole reaches", "the softer dentin.", dict(cavity="mid")),
        ("Germs reach the pulp.", "The nerve gets angry.", dict(cavity="deep", pulp="angry", germs=True)),
        ("The nerve dies. A pus", "pocket forms at the root tip.", dict(cavity="deep", pulp="dead", apex_abscess=True)),
    ]
    scenes = []
    for i, (a, c, kw) in enumerate(steps):
        col, row = i % 2, i // 2
        x0, y0 = 12 + col * 314, 12 + row * 384
        b.append(card(x0, y0, 302, 370, fill=WHITE, uid=uid))
        scenes.append((x0 + 98, y0 + 30, 0.6, kw))
    b.append(multi(uid, scenes))
    for i, (a, c, kw) in enumerate(steps):
        col, row = i % 2, i // 2
        x0, y0 = 12 + col * 314, 12 + row * 384
        b.append(f'<circle cx="{x0+32}" cy="{y0+32}" r="18" fill="url(#{uid}bl)"/>')
        b.append(text(x0 + 32, y0 + 39, str(i + 1), size=19, weight=800, fill=WHITE, anchor="middle"))
        b.append(lines(x0 + 151, y0 + 314, [a, c], size=18, weight=700, anchor="middle"))
    return svg(W, H, "Four steps from cavity to abscess", "".join(b), uid)


def fig_three_doors():
    uid = "td"
    W, H = 640, 400
    b = []
    doors = [
        ("Deep cavity", "a hole that", "went too far", dict(cavity="deep", pulp="angry")),
        ("Crack", "even a hairline", "split counts", dict(crack=True, pulp="angry")),
        ("Gum pocket", "germs slide down", "beside the root", dict(gum_abscess=True, bone_loss_right=True)),
    ]
    scenes = []
    for i, d in enumerate(doors):
        x0 = 10 + i * 210
        b.append(card(x0, 10, 200, 380, fill=WHITE, uid=uid))
        scenes.append((x0 + 50, 30, 0.5, d[3]))
    b.append(multi(uid, scenes))
    for i, (t, l1, l2, kw) in enumerate(doors):
        x0 = 10 + i * 210
        b.append(chip(x0 + 100 - 70, 252, t, fill=INK, w=140, size=17))
        b.append(lines(x0 + 100, 316, [l1, l2], size=17, weight=600, fill=BODY, anchor="middle"))
    return svg(W, H, "Three doors germs use to get in", "".join(b), uid)


def fig_tooth_vs_gum():
    uid = "tg"
    W, H = 640, 640
    b = []
    for i in range(2):
        b.append(card(10 + i * 316, 10, 304, 500, fill=WHITE, uid=uid))
    b.append(multi(uid, [
        (10 + 96, 74, 0.66, dict(cavity="deep", pulp="dead", apex_abscess=True)),
        (326 + 96, 74, 0.66, dict(gum_abscess=True, bone_loss_right=True)),
    ]))
    b.append(chip(34, 26, "Tooth abscess", fill=RED, w=180, size=18))
    b.append(chip(350, 26, "Gum abscess", fill=BLUE, w=170, size=18))
    b.append(lines(162, 384, ["Nerve inside died.", "Pocket sits at the", "root tip, in bone."], size=18, weight=700, anchor="middle"))
    b.append(lines(478, 384, ["Nerve may be alive.", "Pocket sits in the gum,", "beside the root."], size=18, weight=700, anchor="middle"))
    b.append(lines(162, 470, ["Fix: dentist opens", "or removes the tooth"], size=16, weight=600, fill=BODY, anchor="middle"))
    b.append(lines(478, 470, ["Fix: dentist drains and", "cleans the pocket"], size=16, weight=600, fill=BODY, anchor="middle"))
    # flood strip
    b.append(f'<rect x="10" y="526" width="620" height="104" rx="22" fill="{RED_WASH}" stroke="{RED}" stroke-width="2.5"/>')
    b.append(f'<g transform="translate(40 548)"><path d="M30 0 L60 54 L0 54 Z" fill="{RED}"/>'
             f'<rect x="27" y="16" width="6" height="22" rx="3" fill="#fff"/><circle cx="30" cy="45" r="3.5" fill="#fff"/></g>')
    b.append(lines(120, 566, ["Swelling that spreads into the face,", "eye, or neck is a flood. Go to the ER."], size=19, weight=800, fill="#7A271A"))
    return svg(W, H, "Tooth abscess versus gum abscess", "".join(b), uid)


def head_profile(x, y, s, uid):
    p = (
        "M150 20 C100 15 62 40 58 85 C56 100 54 110 50 122 L36 148 C34 154 40 158 48 158 "
        "C49 165 46 170 44 174 C48 178 49 182 45 187 C46 194 50 200 54 207 C58 215 70 220 88 218 "
        "C104 216 118 214 124 214 L128 300 L214 300 C206 262 206 236 218 208 C240 172 244 112 226 72 "
        "C208 36 184 22 150 20 Z"
    )
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<path d="{p}" fill="#E9EEF8" stroke="#B8C3D9" stroke-width="2.5"/>'
        f'<path d="M58 206 C90 206 132 204 150 196 C162 188 164 168 160 152" stroke="#B8C3D9" stroke-width="2.5" fill="none" stroke-dasharray="5 6"/>'
        f'<ellipse cx="170" cy="136" rx="13" ry="22" fill="#DCE4F2" stroke="#B8C3D9" stroke-width="2.5"/>'
        f'</g>'
    )


def fig_feeling_map():
    uid = "fm"
    W, H = 640, 720
    b = [card(8, 8, W - 16, H - 16, fill=CREAM, uid=uid, shadow=False, stroke="rgba(26,26,46,.08)")]
    b.append(text(32, 50, "THE FEELING MAP", size=16, weight=800, fill=RED, extra=' letter-spacing="2"'))
    # tooth with pulse rings
    tx, ty, s = 86, 150, 0.6
    b.append(multi(uid, [(tx, ty, s, dict(cavity="deep", pulp="angry", apex_abscess=True))]))
    cx, cy = pt(tx, ty, s, 100, 150)
    for r, o in ((100, .18), (124, .12), (148, .07)):
        b.append(f'<path d="M{cx-r*0.55} {cy-r*0.84} A{r} {r} 0 0 1 {cx+r*0.55} {cy-r*0.84}" stroke="{RED}" stroke-width="4" fill="none" opacity="{o*4:.2f}" stroke-linecap="round"/>')
    # gum boil
    bx, by = pt(tx, ty, s, 16, 160)
    b.append(f'<circle cx="{bx}" cy="{by}" r="11" fill="url(#{uid}ps)" stroke="{RED}" stroke-width="2.5"/>')
    # callouts right column
    items = [
        ("Throb like a heartbeat", "pressure with nowhere to go"),
        ("Hurts to bite or tap", "like stepping on a bruise"),
        ("Hot can make it roar", "cold may calm it for a minute"),
        ("Puffy gum or a bump", "like a pimple on the gum"),
        ("Bad taste or smell", "when the pocket leaks a little"),
    ]
    y = 120
    for t, sub in items:
        b.append(f'<circle cx="330" cy="{y-7}" r="7" fill="{RED}"/>')
        b.append(text(348, y, t, size=20, weight=800))
        b.append(text(348, y + 23, sub, size=16, weight=500, fill=BODY))
        y += 66
    # head with spread lines
    hx, hy, hs = 360, 448, 0.9
    b.append(f'<clipPath id="{uid}hc"><rect x="8" y="8" width="{W-16}" height="{H-16}" rx="22"/></clipPath>')
    b.append(f'<g clip-path="url(#{uid}hc)">' + head_profile(hx, hy, hs, uid) + '</g>')
    mx, my = hx + 122 * hs, hy + 192 * hs
    targets = [((hx + 170 * hs, hy + 136 * hs), "ear"), ((hx + 128 * hs, hy + 100 * hs), "temple"), ((hx + 150 * hs, hy + 262 * hs), "neck")]
    for (ex, ey), _ in targets:
        b.append(f'<path d="M{mx} {my} L{ex} {ey}" stroke="{RED}" stroke-width="3" stroke-dasharray="6 6" fill="none"/>')
        b.append(f'<circle cx="{ex}" cy="{ey}" r="6" fill="{RED}"/>')
    b.append(f'<circle cx="{mx}" cy="{my}" r="9" fill="{WHITE}" stroke="{RED}" stroke-width="4"/>')
    b.append(lines(40, 512, ["Pain can travel", "to the ear, temple,", "or neck on the", "same side."], size=21, weight=800))
    b.append(lines(40, 634, ["Swelling toward the eye", "or neck: red flag stop."], size=17, weight=700, fill=RED))
    return svg(W, H, "What a dental abscess feels like", "".join(b), uid)


def icon_sinus():
    return (
        '<path d="M20 70 C20 30 60 20 80 40 C100 20 140 30 140 70 Z" fill="#E3ECFB" stroke="#7FA6E8" stroke-width="3"/>'
        '<path d="M50 52 l0 14 M80 46 l0 16 M110 52 l0 14" stroke="#2563EB" stroke-width="4" stroke-linecap="round"/>'
        '<path d="M44 62 l6 8 l6 -8 M74 58 l6 8 l6 -8 M104 62 l6 8 l6 -8" stroke="#2563EB" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M14 92 H146" stroke="#E59591" stroke-width="16" stroke-linecap="round"/>'
        + "".join(
            f'<path d="M{x} 86 C{x} 76 {x+24} 76 {x+24} 86 L{x+22} 104 C{x+16} 110 {x+8} 110 {x+2} 104 Z" fill="#fff" stroke="#C9B48C" stroke-width="2.5"/>'
            for x in (22, 56, 90, 124 - 10)
        )
    )


def icon_jaw():
    return (
        '<ellipse cx="128" cy="50" rx="13" ry="22" fill="#E3ECFB" stroke="#7FA6E8" stroke-width="3"/>'
        '<path d="M70 30 C80 22 100 22 108 32" stroke="#B8C3D9" stroke-width="5" fill="none" stroke-linecap="round"/>'
        '<path d="M98 44 C100 70 102 92 96 106 L22 112 C14 112 12 100 20 98 L84 92 C88 76 86 58 88 44 Z" fill="#F5EAD3" stroke="#C9B48C" stroke-width="3" stroke-linejoin="round"/>'
        '<circle cx="93" cy="40" r="10" fill="#F5EAD3" stroke="#C9B48C" stroke-width="3"/>'
        '<path d="M78 34 A16 16 0 0 1 108 34" stroke="#B42318" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
        '<path d="M60 22 l-10 -8 M58 38 l-14 0 M62 52 l-10 8" stroke="#B42318" stroke-width="3.5" stroke-linecap="round"/>'
    )


def icon_canker():
    return (
        '<path d="M14 40 C40 20 120 20 146 40 C150 80 120 110 80 112 C40 110 10 80 14 40 Z" fill="#F4B3B0" stroke="#E59591" stroke-width="3"/>'
        '<path d="M30 46 C60 34 100 34 130 46" stroke="#E59591" stroke-width="3" fill="none"/>'
        '<ellipse cx="80" cy="76" rx="22" ry="15" fill="none" stroke="#B42318" stroke-width="4"/>'
        '<ellipse cx="80" cy="76" rx="15" ry="9" fill="#FBF3D9" stroke="#E8D8A8" stroke-width="2"/>'
    )


def icon_ear():
    return (
        '<path d="M70 20 C104 18 122 44 118 72 C116 90 102 96 98 110 C94 124 76 128 66 116" stroke="#7FA6E8" stroke-width="5" fill="#E3ECFB" stroke-linecap="round"/>'
        '<path d="M80 50 C96 46 104 60 96 72 C90 80 84 84 86 94" stroke="#7FA6E8" stroke-width="4" fill="none" stroke-linecap="round"/>'
        '<circle cx="84" cy="86" r="7" fill="#B42318"/>'
        '<path d="M40 60 l-14 -6 M38 76 l-16 0 M40 92 l-14 6" stroke="#B42318" stroke-width="3.5" stroke-linecap="round"/>'
    )


def fig_lookalikes():
    uid = "lk"
    W, H = 640, 820
    cards = [
        ("Sinus pressure", ["Several upper teeth", "ache together. Worse", "when you bend over."], icon_sinus()),
        ("Jaw joint", ["Sore hinge in front", "of the ear. May click", "or pop. Gum is calm."], icon_jaw()),
        ("Canker sore", ["Shallow sore on soft", "skin. Stings. No deep", "throb in the bone."], icon_canker()),
        ("Ear trouble", ["The ear itself hurts.", "The teeth check out", "calm."], icon_ear()),
    ]
    b = []
    for i, (t, rows, ico) in enumerate(cards):
        col, row = i % 2, i // 2
        x0, y0 = 10 + col * 316, 10 + row * 346
        b.append(card(x0, y0, 304, 332, fill=WHITE, uid=uid))
        b.append(f'<rect x="{x0}" y="{y0}" width="304" height="8" rx="4" fill="{INK}"/>')
        b.append(f'<g transform="translate({x0+72} {y0+30})">{ico}</g>')
        b.append(text(x0 + 24, y0 + 196, t, size=23, weight=800))
        b.append(lines(x0 + 24, y0 + 230, rows, size=18, weight=500, fill=BODY))
    b.append(f'<rect x="10" y="704" width="620" height="106" rx="22" fill="{RED_WASH}" stroke="{RED}" stroke-width="2.5"/>')
    b.append(f'<g transform="translate(36 728)"><path d="M30 0 L60 54 L0 54 Z" fill="{RED}"/>'
             f'<rect x="27" y="16" width="6" height="22" rx="3" fill="#fff"/><circle cx="30" cy="45" r="3.5" fill="#fff"/></g>')
    b.append(lines(116, 746, ["Jaw pain with chest pressure, sweating,", "or short of breath: call 911."], size=19, weight=800, fill="#7A271A"))
    return svg(W, H, "Four lookalikes of a dental abscess", "".join(b), uid)


def flag_icon(kind):
    I, R = INK, RED
    if kind == "breath":
        return (f'<path d="M40 10 V40" stroke="{I}" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M40 38 C26 38 14 52 14 74 C14 86 28 88 36 80 L38 46" fill="#E3ECFB" stroke="{I}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M40 38 C54 38 66 52 66 74 C66 86 52 88 44 80 L42 46" fill="#E3ECFB" stroke="{I}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M30 20 L50 20" stroke="{R}" stroke-width="5" stroke-linecap="round"/>')
    if kind == "swallow":
        return (f'<path d="M24 8 C24 40 20 60 28 90 M56 8 C56 40 60 60 52 90" stroke="{I}" stroke-width="4" fill="none" stroke-linecap="round"/>'
                f'<path d="M30 46 C36 40 44 40 50 46" stroke="{R}" stroke-width="6" fill="none" stroke-linecap="round"/>'
                f'<circle cx="40" cy="26" r="6" fill="#7FA6E8"/>'
                f'<path d="M14 40 L66 52" stroke="{R}" stroke-width="5" stroke-linecap="round"/>')
    if kind == "tongue":
        return (f'<path d="M8 40 C20 20 60 20 72 40" stroke="{I}" stroke-width="4" fill="none"/>'
                f'<path d="M14 62 C20 40 60 40 66 62 C60 70 20 70 14 62 Z" fill="#F4B3B0" stroke="{I}" stroke-width="3.5"/>'
                f'<path d="M14 76 C26 92 54 92 66 76" fill="url(#rfps)" stroke="{R}" stroke-width="4"/>'
                f'<path d="M40 74 V50 M32 58 L40 48 L48 58" stroke="{R}" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "neck":
        return (f'<path d="M22 6 C22 30 18 50 10 90 M58 6 C58 30 62 50 70 90" stroke="{I}" stroke-width="4" fill="none" stroke-linecap="round"/>'
                f'<path d="M58 30 C76 34 78 64 62 70" fill="rgba(180,35,24,.16)" stroke="{R}" stroke-width="4"/>'
                f'<path d="M22 30 C4 34 2 64 18 70" fill="rgba(180,35,24,.16)" stroke="{R}" stroke-width="4"/>')
    if kind == "eye":
        return (f'<path d="M8 50 C24 30 56 30 72 50 C56 60 24 60 8 50 Z" fill="#fff" stroke="{I}" stroke-width="4"/>'
                f'<path d="M8 50 C24 46 56 46 72 50" stroke="{I}" stroke-width="4" fill="none"/>'
                f'<path d="M4 44 C20 10 60 10 76 44" fill="rgba(180,35,24,.16)" stroke="{R}" stroke-width="4"/>'
                f'<path d="M14 66 C30 80 50 80 66 66" stroke="{R}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    if kind == "fever":
        return (f'<rect x="32" y="6" width="16" height="60" rx="8" fill="#fff" stroke="{I}" stroke-width="4"/>'
                f'<circle cx="40" cy="74" r="14" fill="{R}" stroke="{I}" stroke-width="4"/>'
                f'<rect x="37" y="26" width="6" height="44" rx="3" fill="{R}"/>'
                f'<path d="M58 20 h10 M58 34 h14 M58 48 h10" stroke="{I}" stroke-width="3.5" stroke-linecap="round"/>')
    return ""


def fig_red_flags():
    uid = "rf"
    W, H = 640, 720
    b = [f'<rect x="8" y="8" width="{W-16}" height="{H-16}" rx="26" fill="{WHITE}" stroke="{RED}" stroke-width="3"/>']
    b.append(f'<path d="M8 34 Q8 8 34 8 H606 Q632 8 632 34 V104 H8 Z" fill="url(#{uid}rd)"/>')
    b.append(f'<g transform="translate(34 26)"><path d="M28 0 L56 50 L0 50 Z" fill="#fff"/>'
             f'<rect x="25" y="15" width="6" height="20" rx="3" fill="{RED}"/><circle cx="28" cy="42" r="3.5" fill="{RED}"/></g>')
    b.append(text(108, 54, "Go to the ER or call 911", size=28, weight=800, fill=WHITE))
    b.append(text(108, 84, "Do not text first. Go.", size=18, weight=600, fill="#FFE4E0"))
    flags = [
        ("breath", "Trouble breathing"),
        ("swallow", "Can't swallow spit"),
        ("tongue", "Floor of mouth rising"),
        ("neck", "Neck hard or swelling"),
        ("eye", "Eye swelling shut"),
        ("fever", "High fever, confused"),
    ]
    for i, (k, t) in enumerate(flags):
        col, row = i % 2, i // 2
        x0, y0 = 28 + col * 298, 126 + row * 194
        b.append(f'<rect x="{x0}" y="{y0}" width="286" height="178" rx="20" fill="{RED_WASH}" stroke="rgba(180,35,24,.25)" stroke-width="1.5"/>')
        b.append(f'<g transform="translate({x0+103} {y0+16})">{flag_icon(k)}</g>')
        b.append(text(x0 + 143, y0 + 150, t, size=20, weight=800, fill="#7A271A", anchor="middle"))
    return svg(W, H, "Red flags that mean go to the ER", "".join(b).replace("url(#rfps)", f"url(#{uid}ps)"), uid)


def step_icon(kind, uid):
    if kind == "xray":
        return (f'<rect x="4" y="8" width="72" height="60" rx="10" fill="{INK}"/>'
                f'<path d="M26 22 C26 16 34 14 40 18 C46 14 54 16 54 22 C54 34 50 40 48 56 C46 60 42 58 42 52 L40 44 L38 52 C38 58 34 60 32 56 C30 40 26 34 26 22 Z" fill="#E8EEF8"/>'
                f'<circle cx="34" cy="62" r="5" fill="{RED}" opacity=".9"/>')
    if kind == "drain":
        return (f'<path d="M20 10 C20 0 60 0 60 10 C60 34 54 48 50 70 C48 76 44 74 44 68 L40 50 L36 68 C36 74 32 76 30 70 C26 48 20 34 20 10 Z" fill="#F5EAD3" stroke="#C9B48C" stroke-width="2.5"/>'
                f'<path d="M40 8 V48" stroke="{RED}" stroke-width="4" stroke-dasharray="5 5"/>'
                f'<path d="M30 18 L40 6 L50 18" stroke="{RED}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "fix":
        return (f'<path d="M20 10 C20 0 60 0 60 10 C60 34 54 48 50 70 C48 76 44 74 44 68 L40 50 L36 68 C36 74 32 76 30 70 C26 48 20 34 20 10 Z" fill="#F5EAD3" stroke="#C9B48C" stroke-width="2.5"/>'
                f'<path d="M34 16 L34 66 M46 16 L46 66" stroke="#6B7A99" stroke-width="5" stroke-linecap="round"/>'
                f'<path d="M22 8 C30 2 50 2 58 8 L58 16 L22 16 Z" fill="#C7CFDD"/>')
    if kind == "helper":
        return (f'<path d="M10 40 C20 20 60 20 70 40" stroke="{BLUE}" stroke-width="6" fill="none" stroke-linecap="round"/>'
                f'<path d="M10 40 L10 66 M70 40 L70 66 M40 26 L40 66" stroke="{BLUE}" stroke-width="5" stroke-linecap="round"/>'
                f'<path d="M2 66 H78" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    return ""


def fig_care_steps():
    uid = "cr"
    W, H = 640, 816
    steps = [
        ("xray", "Find the source", ["A dentist checks the tooth", "and takes an X-ray."]),
        ("drain", "Let the pus out", ["Open the tooth, or a small", "cut in the gum drains it."]),
        ("fix", "Fix the source", ["Root canal: clean and seal", "the nerve room. Or remove", "the tooth if it can't be saved."]),
        ("helper", "Helper medicine, if it fits", ["Calms germs as a bridge.", "It is not the repair."]),
    ]
    b = [f'<path d="M64 80 V680" stroke="{RED}" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>']
    y = 12
    hs = [168, 168, 196, 168]
    for i, (k, t, rows) in enumerate(steps):
        h = hs[i]
        fill = WHITE if i < 3 else "#EEF4FF"
        b.append(card(10, y, 620, h, fill=fill, uid=uid))
        b.append(f'<circle cx="64" cy="{y+44}" r="24" fill="url(#{uid}bl)"/>')
        b.append(text(64, y + 52, str(i + 1), size=22, weight=800, fill=WHITE, anchor="middle"))
        b.append(f'<g transform="translate(520 {y + (h-80)/2})">{step_icon(k, uid)}</g>')
        b.append(text(110, y + 52, t, size=24, weight=800))
        b.append(lines(110, y + 88, rows, size=19, weight=500, fill=BODY))
        y += h + 16
    b.append(text(320, y + 22, "Steps 1 to 3 are the dentist. Step 4 never replaces them.", size=17, weight=700, fill=RED, anchor="middle"))
    return svg(W, H, "What dental abscess care looks like, step by step", "".join(b), uid)


def fig_who_does_what():
    uid = "wd"
    W, H = 640, 672
    rows = [
        ("Dentist", "fixes the tooth", INK, WHITE,
         ["Exam and X-ray", "Opens and drains the pocket", "Root canal or removes the tooth"]),
        ("Text visit with Chris", "the bridge", IMSG, WHITE,
         ["Asks the red-flag questions", "Symptom care plan for tonight", "Helper medicine only if it fits", "Points you to the right door"]),
        ("ER", "the airway door", f"url(#{uid}rd)", WHITE,
         ["Trouble breathing or swallowing", "Swelling spreading in face or neck"]),
    ]
    b = []
    y = 10
    for i, (t, sub, fill, fg, items) in enumerate(rows):
        h = 76 + 40 * len(items)
        b.append(f'<rect x="10" y="{y}" width="620" height="{h}" rx="24" fill="{fill}" filter="url(#{uid}sm)"/>')
        if i == 1:
            b.append(f'<rect x="10" y="{y}" width="620" height="{h}" rx="24" fill="none" stroke="#fff" stroke-width="2"/>')
        b.append(text(38, y + 46, t, size=26, weight=800, fill=fg))
        b.append(text(602, y + 46, sub, size=17, weight=700, fill="rgba(255,255,255,.85)", anchor="end"))
        b.append(f'<path d="M38 {y+62} H602" stroke="rgba(255,255,255,.3)" stroke-width="1.5"/>')
        for j, it in enumerate(items):
            yy = y + 98 + j * 40
            b.append(f'<circle cx="50" cy="{yy-7}" r="9" fill="rgba(255,255,255,.22)"/>'
                     f'<path d="M45 {yy-7} l4 4 l7 -8" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
            b.append(text(72, yy, it, size=20, weight=600, fill=fg))
        y += h + 18
    return svg(W, H, "Who does what: dentist, text visit, ER", "".join(b), uid)


def fig_loop():
    uid = "lp"
    W, H = 640, 700
    cx, cy, r = 320, 330, 205
    b = [card(8, 8, W - 16, H - 16, fill=CREAM, uid=uid, shadow=False, stroke="rgba(26,26,46,.08)")]
    # circular arrows (4 arcs)
    import math
    angs = [-90, 0, 90, 180]
    for a in angs:
        a1, a2 = math.radians(a + 22), math.radians(a + 68)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        b.append(f'<path d="M{x1:.1f} {y1:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}" stroke="{RED}" stroke-width="6" fill="none" stroke-linecap="round"/>')
        # arrow head at end
        t = a2 + math.pi / 2
        hx, hy = x2, y2
        p1 = (hx - 16 * math.cos(t) + 10 * math.cos(t + math.pi / 2), hy - 16 * math.sin(t) + 10 * math.sin(t + math.pi / 2))
        p2 = (hx - 16 * math.cos(t) - 10 * math.cos(t + math.pi / 2), hy - 16 * math.sin(t) - 10 * math.sin(t + math.pi / 2))
        b.append(f'<path d="M{hx:.1f} {hy:.1f} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} Z" fill="{RED}"/>')
    b.append(multi(uid, [(cx - 45, cy - 92, 0.45, dict(cavity="deep", pulp="dead", apex_abscess=True, jaw_on=False))]))
    nodes = [
        (cx, cy - r, ["Source still open", "dead nerve, crack,", "or gum pocket"]),
        (cx + r, cy, ["Germs", "grow back"]),
        (cx, cy + r, ["Pocket refills.", "The throb returns."]),
        (cx - r, cy, ["Helper calms", "it for a while"]),
    ]
    for i, (nx, ny, rows) in enumerate(nodes):
        w = 196 if i in (0, 2) else 150
        h = 30 + 24 * len(rows)
        b.append(card(nx - w / 2, ny - h / 2, w, h, fill=WHITE, uid=uid, r=18))
        b.append(lines(nx, ny - h / 2 + 30, rows, size=18 if i else 18, weight=800 if True else 600, anchor="middle"))
    # exit
    b.append(f'<rect x="40" y="606" width="560" height="68" rx="34" fill="url(#{uid}bl)" filter="url(#{uid}sm)"/>')
    b.append(text(320, 648, "Break the loop: a dentist fixes the source", size=21, weight=800, fill=WHITE, anchor="middle"))
    return svg(W, H, "Why a dental abscess comes back: the loop", "".join(b), uid)


def fig_myths():
    uid = "my"
    W, H = 640, 900
    pairs = [
        (["If it drains,", "it is over."], ["A drain is a pressure", "valve. The source", "is still open."]),
        (["No pain means", "it healed."], ["A dead nerve can go", "quiet while germs", "keep working."]),
        (["Salt water", "will cure it."], ["A rinse is comfort.", "It is not a repair."]),
        (["A text visit replaces", "a dentist."], ["Text can be a bridge.", "A dentist fixes", "the tooth."]),
    ]
    b = []
    y = 10
    for m, f in pairs:
        h = 200
        b.append(card(10, y, 300, h, fill=CREAM, uid=uid))
        b.append(chip(30, y + 20, "MYTH", fill="#8E8E9A", w=92, size=16))
        b.append(lines(30, y + 92, m, size=21, weight=700, fill="#5f5f68"))
        b.append(f'<path d="M282 {y+28} l-18 18 M264 {y+28} l18 18" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>')
        b.append(f'<rect x="330" y="{y}" width="300" height="{h}" rx="22" fill="url(#{uid}bl)" filter="url(#{uid}sm)"/>')
        b.append(chip(350, y + 20, "FACT", fill=WHITE, color=BLUE_DARK, w=88, size=16))
        b.append(f'<path d="M588 {y+38} l8 8 l16 -18" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append(lines(350, y + 92, f, size=21, weight=700, fill=WHITE))
        y += h + 22
    return svg(W, 896, "Dental abscess myths and facts", "".join(b), uid)


FIGURES = {
    "tooth-anatomy-map.svg": fig_tooth_map,
    "cavity-to-abscess-steps.svg": fig_cavity_steps2,
    "three-doors-germs-get-in.svg": fig_three_doors,
    "feeling-map.svg": fig_feeling_map,
    "tooth-vs-gum-abscess.svg": fig_tooth_vs_gum,
    "lookalikes-cards.svg": fig_lookalikes,
    "red-flags-er.svg": fig_red_flags,
    "care-steps.svg": fig_care_steps,
    "dentist-text-er-who-does-what.svg": fig_who_does_what,
    "why-it-comes-back-loop.svg": fig_loop,
    "myths-vs-facts.svg": fig_myths,
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGURES.items():
        data = fn()
        (OUT / name).write_text(data, encoding="utf-8")
        print(f"wrote assets/{name} ({len(data.encode())} bytes)")


if __name__ == "__main__":
    main()
