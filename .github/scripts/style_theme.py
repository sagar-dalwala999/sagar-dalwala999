"""Fun-account style: chemistry lab × desert case file. Own drawings, own layout — no logos, no characters."""
from base import *
from svgkit import Doc, face, svg, reveal, fade, rise, draw_line, minify
import content as C
import math

P = dict(sky1="#1b1030", sky2="#7b2d5e", sky3="#f3722c", sky4="#f9c74f", sun="#ffd166",
         mesa="#2a1638", mesa2="#1c0f26", ground="#1a1224", ground2="#0d1117",
         tile="#0b3b2e", tile2="#0f4d3a", border="#8ff0a4", tiletext="#eafff0",
         acid="#8ff0a4", green="#3ddc84", paper="#0f1f1a", hair="#1e3a2f", hair2="#173026",
         ink="#e6efe9", ink2="#9fb8aa", ink3="#6b8577", red="#d63b2f", amber="#f9c74f", blue="#4cc9f0", orange="#f3722c",
         page="#0d1117")
GROUP = {"frontend": "#8ff0a4", "backend": "#4cc9f0", "ai": "#f9c74f", "infra": "#f3722c"}
ELEMENT_NAMES = {"Se": "selenium", "Re": "rhenium", "As": "arsenic", "O": "oxygen", "Cl": "chlorine", "K": "potassium",
                 "Na": "sodium", "Fr": "francium", "Cr": "chromium", "Rg": "roentgenium", "S": "sulfur", "Ag": "silver", "Ar": "argon"}

DIST = ('<filter id="dist" x="-6%" y="-14%" width="112%" height="128%">'
        '<feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="3" seed="9" result="n"/>'
        '<feColorMatrix in="n" type="luminanceToAlpha" result="l"/>'
        '<feComponentTransfer in="l" result="m"><feFuncA type="discrete" tableValues="0 1 1 1 1 1 1 1 1 1"/></feComponentTransfer>'
        '<feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="3" result="w"/>'
        '<feDisplacementMap in="SourceGraphic" in2="w" scale="2.5" xChannelSelector="R" yChannelSelector="G" result="d"/>'
        '<feComposite in="d" in2="m" operator="in"/></filter>')
GLOW = ('<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def stamp(doc, f, txt, cx, cy, size=18, color=P["red"], rot=-3, pad=14, begin=None, tracking=2.5):
    """Rubber-stamp box; optional SMIL slam-in at `begin` seconds."""
    m, w = doc.text(f, txt, 0, size * 0.36, size, fill=color, tracking=tracking, anchor="middle")
    bw, bh = w + pad * 2, size + pad * 1.2
    body = (f'<g filter="url(#dist)"><rect x="{-bw/2:.1f}" y="{-bh/2:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="4" fill="none" stroke="{color}" stroke-width="3"/>'
            f'<rect x="{-bw/2+5:.1f}" y="{-bh/2+5:.1f}" width="{bw-10:.1f}" height="{bh-10:.1f}" rx="2" fill="none" stroke="{color}" stroke-width="1" opacity=".7"/>{m}</g>')
    if begin is None:
        return f'<g transform="translate({cx} {cy}) rotate({rot})" opacity=".92">{body}</g>', bw
    anim = (f'<g transform="translate({cx} {cy}) rotate({rot})"><g opacity="0">'
            f'<animate attributeName="opacity" values="0;.92" begin="{begin:.2f}s" dur=".18s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="scale" values="1.7;.94;1" keyTimes="0;.7;1" begin="{begin:.2f}s" dur=".22s" fill="freeze"/>'
            f'{body}</g></g>')
    return anim, bw


class Lab(Style):
    id, name = "lab", "Lab"
    pal = P

    def __init__(self):
        super().__init__()
        self.cond = face("BarlowCondensed-Bold.ttf")
        self.condm = face("BarlowCondensed-Medium.ttf")
        self.condx = face("BarlowCondensed-ExtraBold.ttf")
        self.type = face("SpecialElite.ttf")
        self.mono = face("JetBrainsMono.ttf", 400)

    # ---------------------------------------------------------------- pieces
    def tile(self, doc, x, y, w, h, sym, num, name, mass=None, fill=None, border=None, textc=None, dashed=False, sym_size=None):
        border = border or P["border"]; fill = fill or P["tile"]; textc = textc or P["tiletext"]
        b = [rr(x, y, w, h, 6, fill, border, 2.5, 'stroke-dasharray="6 4"' if dashed else "")]
        b.append(self.T(doc, self.condm, str(num), x + 8, y + 16, h * 0.13, textc))
        ss = sym_size or h * 0.5
        b.append(self.T(doc, self.cond, sym, x + w / 2, y + h * 0.62, ss, textc, anchor="middle"))
        b.append(self.T(doc, self.condm, name, x + w / 2, y + h - 12, max(h * 0.1, 9), P["acid"], anchor="middle"))
        if mass:
            b.append(self.T(doc, self.condm, mass, x + w - 8, y + 16, h * 0.11, P["ink2"], anchor="end"))
        return "".join(b)

    # ------------------------------------------------------------------ hero
    def hero(self):
        doc = Doc(); H = 340; b = []
        hz = 238
        defs = [f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["sky1"]}"/><stop offset=".42" stop-color="{P["sky2"]}"/><stop offset=".78" stop-color="{P["sky3"]}"/><stop offset="1" stop-color="{P["sky4"]}"/></linearGradient>',
                f'<linearGradient id="gnd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["ground"]}"/><stop offset="1" stop-color="{P["ground2"]}"/></linearGradient>',
                f'<radialGradient id="sunglow"><stop offset="0" stop-color="{P["sun"]}" stop-opacity=".55"/><stop offset="1" stop-color="{P["sun"]}" stop-opacity="0"/></radialGradient>',
                '<clipPath id="skyclip"><rect x="0" y="0" width="848" height="%d"/></clipPath>' % hz, DIST, GLOW]
        b.append(rr(0, 0, W, hz, 0, "url(#sky)"))
        # stars
        for i, (sx, sy, r) in enumerate([(60, 30, 1.4), (140, 62, 1), (230, 24, 1.2), (520, 40, 1.3), (610, 18, 1), (700, 70, 1.4), (790, 36, 1.1), (450, 80, 1), (360, 20, 1)]):
            b.append(f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="#fff"><animate attributeName="opacity" values=".2;1;.2" dur="{2 + (i % 4) * .7:.1f}s" begin="{i * .3:.1f}s" repeatCount="indefinite"/></circle>')
        # sun + glow, clipped to sky
        b.append(f'<g clip-path="url(#skyclip)"><circle cx="612" cy="{hz + 6}" r="150" fill="url(#sunglow)"/><circle cx="612" cy="{hz + 6}" r="62" fill="{P["sun"]}"/></g>')
        # mesas
        b.append(f'<polygon points="0,{hz} 0,200 60,196 92,170 150,170 176,196 250,206 300,210 340,{hz}" fill="{P["mesa2"]}"/>')
        b.append(f'<polygon points="380,{hz} 430,214 470,214 500,196 560,196 590,214 700,214 740,190 800,190 826,214 848,220 848,{hz}" fill="{P["mesa"]}"/>')
        # ground + road with moving centre line
        b.append(rr(0, hz, W, H - hz, 0, "url(#gnd)"))
        b.append(f'<polygon points="470,{hz} 500,{hz} 620,{H} 300,{H}" fill="#15101c"/>')
        b.append(f'<line x1="485" y1="{hz}" x2="460" y2="{H}" stroke="{P["amber"]}" stroke-width="2" stroke-dasharray="10 14" opacity=".8">'
                 f'<animate attributeName="stroke-dashoffset" from="24" to="0" dur=".9s" repeatCount="indefinite"/></line>')
        # camper van silhouette (own drawing) with lit windows + smoke from the roof vent
        vx, vy = 632, hz - 2
        van = [f'<path d="M{vx},{vy} L{vx},{vy-56} Q{vx},{vy-68} {vx+12},{vy-68} L{vx+120},{vy-68} Q{vx+134},{vy-68} {vx+136},{vy-56} L{vx+152},{vy-40} L{vx+152},{vy} Z" fill="#0d0912" stroke="#3a2450" stroke-width="1.5"/>',
               rr(vx + 14, vy - 56, 26, 18, 2, P["amber"], extra='opacity=".85"><animate attributeName="opacity" values=".85;.5;.85" dur="3s" repeatCount="indefinite"/></rect><rect width="0" height="0"'),
               rr(vx + 50, vy - 56, 26, 18, 2, P["amber"], extra='opacity=".7"'),
               rr(vx + 120, vy - 50, 22, 14, 2, P["amber"], extra='opacity=".6"'),
               rr(vx + 84, vy - 74, 18, 8, 1, "#3a2450"),
               f'<circle cx="{vx+30}" cy="{vy}" r="10" fill="#0d0912" stroke="#3a2450" stroke-width="2"/><circle cx="{vx+118}" cy="{vy}" r="10" fill="#0d0912" stroke="#3a2450" stroke-width="2"/>']
        for i in range(3):
            van.append(f'<circle cx="{vx+93}" cy="{vy-78}" r="{3+i}" fill="#cfd3d8" opacity="0">'
                       f'<animate attributeName="cy" values="{vy-78};{vy-120}" dur="2.4s" begin="{i*.8:.1f}s" repeatCount="indefinite"/>'
                       f'<animate attributeName="cx" values="{vx+93};{vx+104}" dur="2.4s" begin="{i*.8:.1f}s" repeatCount="indefinite"/>'
                       f'<animate attributeName="opacity" values="0;.55;0" dur="2.4s" begin="{i*.8:.1f}s" repeatCount="indefinite"/></circle>')
        b.append("".join(van))
        # element tiles dropping in
        tw, th, gap, x0, y0 = 116, 132, 12, 40, 54
        for i, (sym, num, name, mass) in enumerate(C.ELEMENTS):
            x = x0 + i * (tw + gap)
            t = self.tile(doc, x, y0, tw, th, sym, num, name, mass, sym_size=66)
            b.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1" begin="{.2+i*.25:.2f}s" dur=".05s" fill="freeze"/>'
                     f'<animateTransform attributeName="transform" type="translate" values="0 -420;0 10;0 -4;0 0" keyTimes="0;.62;.82;1" begin="{.2+i*.25:.2f}s" dur=".85s" fill="freeze" calcMode="spline" keySplines="0.3 0 0.7 1;0.4 0 0.6 1;0.4 0 0.6 1"/>{t}</g>')
        # typewriter line under the tiles
        line_txt = f"{C.HANDLE}  ·  a.k.a. {C.PERSONA}"
        m, w = self.TW(doc, self.type, line_txt, x0 + 2, 276, 17, P["tiletext"], per_glyph=True,
                       glyph_fn=lambda i, ch, use: reveal(1.3 + i * 0.035, use))
        b.append(f'<g filter="url(#glow)">{m}</g>')
        tend = 1.3 + len(line_txt) * 0.035
        b.append(f'<rect x="{x0 + 4 + w:.1f}" y="264" width="10" height="14" fill="{P["acid"]}" opacity="0"><set attributeName="opacity" to="1" begin="1.3s"/>'
                 f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin="{tend:.2f}s" repeatCount="indefinite"/></rect>')
        # caption
        b.append(self.T(doc, self.mono, "fig. 1 — the lab  ·  35.0844° N, 106.6504° W  ·  dusk", 16, H - 12, 10, P["ink3"]))
        return svg(W, H, "".join(b), defs_extra="".join(defs), doc=doc)

    # --------------------------------------------------------------- section
    TITLES = {"about": "SUBJECT", "featured": "EXPERIMENTS", "wins": "LAB RESULTS", "stack": "REAGENTS", "stats": "LAB REPORT", "contact": "CONTACT"}

    def section(self, idx, title):
        doc = Doc(); H = 56; y = 30
        # amber label tab with the number, then the title in acid green — like a specimen label on a beaker
        tab_w = 44
        b = [rr(0, y - 19, tab_w, 28, 4, P["amber"]),
             self.T(doc, self.condx, f"{idx:02d}", tab_w / 2, y + 1, 17, P["ground2"], anchor="middle", tracking=1)]
        m, w = self.TW(doc, self.cond, self.TITLES[title], tab_w + 14, y + 1, 19, P["acid"], tracking=3)
        b.append(m)
        x = tab_w + 14 + w + 18
        b.append(line(x, y - 5, W - 4, y - 5, P["hair"], 1))
        b.append(self.T(doc, self.type, f"case file · {C.HANDLE}", W - 6, y + 1, 12, P["ink3"], anchor="end"))
        return svg(W, H, "".join(b), doc=doc)

    # ------------------------------------------------------------------ about
    def about(self):
        doc = Doc(); H = 40 + len(C.ABOUT) * 26 + 20; b = [rr(1, 1, W - 2, H - 2, 6, P["paper"], P["hair"], 1)]
        # paperclip
        b.append(f'<path d="M40,10 L40,54 Q40,66 52,66 Q64,66 64,54 L64,22 Q64,14 56,14 Q48,14 48,22 L48,50" fill="none" stroke="{P["ink2"]}" stroke-width="2.5" stroke-linecap="round" transform="rotate(-12 52 38)"/>')
        y = 44
        for i, (k, v) in enumerate(C.ABOUT):
            m1, w1 = self.TW(doc, self.cond, k, 92, y, 13, P["acid"], tracking=1.5)
            xd = 92 + w1 + 8; dots = "".join(f'<circle cx="{x}" cy="{y-4}" r="1" fill="{P["ink3"]}"/>' for x in range(int(xd), 236, 6))
            m2, _ = self.TW(doc, self.type, v, 246, y, 14, P["ink"])
            b.append(fade(0.2 + i * 0.18, m1 + dots + m2))
            y += 26
        return svg(W, H, "".join(b), doc=doc)

    # ------------------------------------------------------------------ card
    def card(self, idx, p):
        sym, num, name, url, desc, tags, fork = p
        doc = Doc(); H = 166; b = [rr(1, 1, CARD_W - 2, H - 2, 6, P["paper"], P["hair"], 1)]
        b.append(self.tile(doc, 16, 18, 92, 106, sym, num, ELEMENT_NAMES.get(sym, "?"), sym_size=44))
        b.append(self.T(doc, self.cond, name, 124, 44, 21, P["tiletext"]))
        y = 66
        for ln in wrap(self.type, desc, 12, CARD_W - 140)[:3]:
            b.append(self.T(doc, self.type, ln, 124, y, 12, P["ink2"])); y += 16
        x = 124
        for tg in tags:
            tw = self.mono.measure(tg, 10) + 12
            b.append(rr(x, 132, tw, 18, 3, "none", P["hair"], 1))
            b.append(self.T(doc, self.mono, tg, x + 6, 145, 10, P["acid"])); x += tw + 6
        if fork:
            b.append(rr(CARD_W - 62, 12, 48, 18, 3, "none", P["amber"], 1.2))
            b.append(self.T(doc, self.condx, "FORK", CARD_W - 38, 25.5, 11, P["amber"], tracking=1.5, anchor="middle"))
        return svg(CARD_W, H, "".join(b), doc=doc)

    # ------------------------------------------------------------------ wins
    def wins(self):
        doc = Doc(); H = 172; b = [rr(1, 1, W - 2, H - 2, 6, P["paper"], P["hair"], 1)]
        b.append(self.T(doc, self.cond, "LAB RESULTS · 3 SAMPLES TESTED", 20, 30, 13, P["ink3"], tracking=1.5))
        cols = {"blue": P["blue"], "green": P["acid"], "amber": P["amber"]}
        defs = []
        for i, (name, year, what, col) in enumerate(C.WINS):
            x = 30 + i * 276; c = cols[col]; tx, ty, tw, th = x, 48, 30, 104
            defs.append(f'<clipPath id="tube{i}"><path d="M{tx},{ty} L{tx},{ty+th-15} A15,15 0 0 0 {tx+tw},{ty+th-15} L{tx+tw},{ty} Z"/></clipPath>')
            # liquid rises
            b.append(f'<g clip-path="url(#tube{i})"><rect x="{tx}" y="{ty+th}" width="{tw}" height="{th}" fill="{c}" opacity=".85">'
                     f'<animate attributeName="y" from="{ty+th}" to="{ty+38}" begin="{.3+i*.25:.2f}s" dur="1.1s" fill="freeze" calcMode="spline" keySplines="0.2 0.7 0.2 1"/></rect>')
            for k in range(3):
                bx = tx + 8 + k * 7
                b.append(f'<circle cx="{bx}" cy="{ty+th-10}" r="{1.5+k*.6}" fill="#fff" opacity="0">'
                         f'<animate attributeName="cy" values="{ty+th-10};{ty+42}" dur="{1.8+k*.5:.1f}s" begin="{1.5+i*.25+k*.6:.1f}s" repeatCount="indefinite"/>'
                         f'<animate attributeName="opacity" values="0;.7;0" dur="{1.8+k*.5:.1f}s" begin="{1.5+i*.25+k*.6:.1f}s" repeatCount="indefinite"/></circle>')
            b.append("</g>")
            b.append(f'<path d="M{tx},{ty} L{tx},{ty+th-15} A15,15 0 0 0 {tx+tw},{ty+th-15} L{tx+tw},{ty}" fill="none" stroke="{P["ink2"]}" stroke-width="2"/>')
            b.append(rr(tx - 4, ty - 3, tw + 8, 6, 2, P["ink2"]))
            for gy in (ty + 30, ty + 52, ty + 74):
                b.append(line(tx + tw - 8, gy, tx + tw, gy, P["ink3"], 1))
            b.append(self.T(doc, self.cond, name.upper(), x + 48, 78, 14, P["tiletext"], tracking=.5))
            b.append(self.T(doc, self.type, year, x + 48, 100, 12, c))
            b.append(self.T(doc, self.type, what, x + 48, 120, 12, P["ink2"]))
            b.append(self.T(doc, self.mono, f"sample #{i+1:02d}", x + 48, 142, 10, P["ink3"]))
        return svg(W, H, "".join(b), defs_extra="".join(defs), doc=doc)

    # ----------------------------------------------------------------- stack
    def stack(self):
        doc = Doc(); H = 214; b = [rr(1, 1, W - 2, H - 2, 6, P["paper"], P["hair"], 1)]
        b.append(self.T(doc, self.cond, "REAGENTS ON HAND · PERIODIC TABLE OF THE STACK", 20, 30, 13, P["ink3"], tracking=1.5))
        tw, th, gap = 76, 66, 8; per_row = 9
        for i, (sym, name, group, real) in enumerate(C.STACK):
            r, c = divmod(i, per_row); x = 20 + c * (tw + gap); y = 44 + r * (th + gap)
            col = GROUP[group]
            b.append(rr(x, y, tw, th, 4, P["tile"], col if real else P["ink3"], 1.5 if real else 1.2, "" if real else 'stroke-dasharray="4 3"'))
            b.append(rr(x, y, tw, 4, 0, col))
            b.append(self.T(doc, self.condm, str(i + 1), x + 6, y + 18, 9, P["ink2"]))
            b.append(self.T(doc, self.cond, sym, x + tw / 2, y + 44, 26, P["tiletext"], anchor="middle"))
            b.append(self.T(doc, self.condm, name, x + tw / 2, y + 60, 9.5, col, anchor="middle"))
            if not real:
                b.append(self.T(doc, self.condm, "*", x + tw - 8, y + 18, 11, P["ink2"], anchor="end"))
        y = 44 + 2 * (th + gap) + 14
        x = 20
        for g, col in GROUP.items():
            b.append(rr(x, y - 9, 10, 10, 2, col)); m, w = self.TW(doc, self.condm, g.upper(), x + 16, y, 10, P["ink2"], tracking=1); b.append(m); x += w + 40
        b.append(self.T(doc, self.type, "* not on the periodic table (yet)", W - 20, y, 11, P["ink3"], anchor="end"))
        return svg(W, H, "".join(b), doc=doc)

    # ----------------------------------------------------------------- stats
    def _frame(self, doc, title, sub):
        return [rr(1, 1, STAT_W - 2, STAT_H - 2, 6, P["paper"], P["hair"], 1),
                self.T(doc, self.condx, title, 22, 34, 14, P["amber"], tracking=2.5),
                self.T(doc, self.type, sub, STAT_W - 22, 34, 11, P["ink3"], anchor="end"),
                line(22, 46, STAT_W - 22, 46, P["hair"], 1)]

    def stats_card(self, data=None):
        doc = Doc(); S = data or C.STATS_SAMPLE; b = self._frame(doc, "LAB REPORT", f"subject: {C.HANDLE}")
        rows = [("repositories", S["repos"]), ("contributions / yr", S["contributions"]), ("hackathons", S["hackathons"]),
                ("stars", S["stars"]), ("pull requests", S["prs"]), ("followers", S["followers"])]
        for i, (k, v) in enumerate(rows):
            x = 22 + (i % 3) * 152; y = 96 + (i // 3) * 64
            b.append(self.T(doc, self.cond, str(v), x, y, 36, P["acid"] if i == 1 else P["tiletext"]))
            b.append(self.T(doc, self.type, k, x, y + 18, 11, P["ink2"]))
        return svg(STAT_W, STAT_H, "".join(b), doc=doc)

    def langs_card(self, langs=None):
        doc = Doc(); b = self._frame(doc, "COMPOSITION ANALYSIS", "by bytes, public repos")
        cols = [P["acid"], P["green"], P["blue"], P["amber"], P["ink3"]]
        for i, ((l, pct), c) in enumerate(zip(langs or C.LANGS_SAMPLE, cols)):
            y = 68 + i * 25
            b.append(self.T(doc, self.type, l, 22, y + 4, 12, P["ink2"]))
            b.append(rr(130, y - 5, 290, 9, 2, P["hair2"]))
            b.append(f'<rect x="130" y="{y-5}" width="0" height="9" rx="2" fill="{c}"><animate attributeName="width" from="0" to="{290*pct/100:.0f}" begin="{.2+i*.12:.2f}s" dur=".9s" fill="freeze"/></rect>')
            b.append(self.T(doc, self.cond, f"{pct}%", STAT_W - 22, y + 4, 14, c, anchor="end"))
        return svg(STAT_W, STAT_H, "".join(b), doc=doc)

    def activity_card(self, vals=None):
        doc = Doc(); b = self._frame(doc, "REACTION RATE", "contributions per week · 52 weeks")
        vals = vals or sample_activity(); x0, x1, y0, y1 = 22, STAT_W - 22, 66, 164
        vmax = max(max(vals), 1)
        pts = [(x0 + (x1 - x0) * i / (len(vals) - 1), y1 - (y1 - y0) * v / vmax) for i, v in enumerate(vals)]
        path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        defs = GLOW + f'<linearGradient id="ag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["acid"]}" stop-opacity=".35"/><stop offset="1" stop-color="{P["acid"]}" stop-opacity="0"/></linearGradient>'
        for gy in (y0, (y0 + y1) / 2, y1):
            b.append(line(x0, gy, x1, gy, P["hair2"], 1))
        b.append(f'<path d="{path} L{x1},{y1} L{x0},{y1} Z" fill="url(#ag)"/>')
        b.append(f'<path d="{path}" fill="none" stroke="{P["acid"]}" stroke-width="2" filter="url(#glow)" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" dur="1.8s" fill="freeze"/></path>')
        b.append(self.T(doc, self.mono, "52 weeks ago", x0, 182, 10, P["ink3"]))
        b.append(self.T(doc, self.mono, "now", x1, 182, 10, P["ink3"], anchor="end"))
        return svg(STAT_W, STAT_H, "".join(b), defs_extra=defs, doc=doc)

    # ---------------------------------------------------------------- button
    def button(self, kind, label):
        doc = Doc(); txt = {"email": "EMAIL", "linkedin": "LINKEDIN", "main": "MAIN LAB  »"}[kind]
        w = int(self.condx.measure(txt, 14, 2) + 52); H = 42
        b = [rr(1, 1, w - 2, H - 2, 4, P["tile"], P["border"], 2), rr(1, 1, w - 2, 5, 0, P["border"]),
             self.T(doc, self.condx, txt, w / 2, 27, 14, P["tiletext"], tracking=2, anchor="middle")]
        return svg(w, H, "".join(b), doc=doc)

    def footer(self):
        doc = Doc(); H = 84
        b = [line(0, 10, W, 10, P["hair"], 1),
             self.T(doc, self.type, "all experiments performed on the fun account  ·  main lab: github.com/Sagar-Dalwala", W / 2, 44, 13, P["ink2"], anchor="middle"),
             self.T(doc, self.mono, f"© 2026 {C.NAME.lower()}  ·  all drawings original", W / 2, 66, 10, P["ink3"], anchor="middle")]
        return svg(W, H, "".join(b), doc=doc)

    # --------------------------------------------------------------- widgets
    def typing_url(self):
        from urllib.parse import quote
        return ("https://readme-typing-svg.demolab.com/?font=Special+Elite&size=17&pause=1300&color=8FF0A4"
                f"&center=true&vCenter=true&width=560&height=38&lines={quote(';'.join(C.TYPING_LINES), safe=';')}")

    def streak_url(self):
        return (f"https://streak-stats.demolab.com/?user={C.STATS_USER}&hide_border=false&border=1e3a2f&border_radius=6"
                "&background=0f1f1a&ring=8ff0a4&fire=f9c74f&currStreakNum=eafff0&sideNums=eafff0"
                "&currStreakLabel=8ff0a4&sideLabels=9fb8aa&dates=6b8577&stroke=1e3a2f")

    def snake_css(self):
        return ":root{--cb:#1b1f230a;--cs:#f9c74f;--ce:#161b22;--c0:#161b22;--c1:#0b3b2e;--c2:#146c43;--c3:#1f9d55;--c4:#8ff0a4}"

    def snake_colors(self):
        return "color_snake=#f9c74f&color_dots=#161b22,#0b3b2e,#146c43,#1f9d55,#8ff0a4"

    # ----------------------------------------------------------------- build
    def build(self):
        self.out("hero.svg", self.hero())
        for i, t in enumerate(["about", "featured", "wins", "stack", "stats", "contact"], 1):
            self.out(f"sec-{t}.svg", self.section(i, t))
        self.out("about.svg", self.about())
        for i, p in enumerate(C.PROJECTS, 1):
            self.out(f"card-{i}.svg", self.card(i, p))
        self.out("wins.svg", self.wins())
        self.out("stack.svg", self.stack())
        self.out("stats.svg", self.stats_card())
        self.out("langs.svg", self.langs_card())
        self.out("activity.svg", self.activity_card())
        for k in ("email", "linkedin", "main"):
            self.out(f"btn-{k}.svg", self.button(k, k))
        self.out("footer.svg", self.footer())
        return self.assets

    def readme(self, asset_prefix="assets"):
        a = lambda n: f"{asset_prefix}/{n}"
        P_ = C.PROJECTS
        def card_link(i, p):
            return f'  <a href="{p[3]}"><img src="{a(f"card-{i}.svg")}" width="49%" alt="{esc(p[2])}"></a>'
        cards = "\n".join(f'<p align="center">\n{card_link(i, P_[i-1])}\n{card_link(i+1, P_[i])}\n</p>' for i in (1, 3))
        snake = f"https://raw.githubusercontent.com/{C.HANDLE}/{C.HANDLE}/output/github-contribution-grid-snake-dark.svg"
        return f"""<!-- Generated by .github/scripts/build.py — edit content.py and re-run, or edit this file directly (assets stay the same). -->
<p align="center">
  <img src="{a('hero.svg')}" width="100%" alt="S · Ag · Ar — {esc(C.TAGLINE)}">
</p>
<p align="center">
  <img src="{self.typing_url()}" alt="{esc(' · '.join(C.TYPING_LINES))}">
</p>

<img src="{a('sec-about.svg')}" width="100%" alt="Exhibit 01 · Subject">

<p align="center"><img src="{a('about.svg')}" width="100%" alt="{esc('; '.join(k + ': ' + v for k, v in C.ABOUT))}"></p>

<img src="{a('sec-featured.svg')}" width="100%" alt="Exhibit 02 · Experiments">

{cards}

<img src="{a('sec-wins.svg')}" width="100%" alt="Exhibit 03 · Lab results">

<p align="center"><img src="{a('wins.svg')}" width="100%" alt="{esc(' · '.join(w[0] + ' ' + w[1] for w in C.WINS))}"></p>

<img src="{a('sec-stack.svg')}" width="100%" alt="Exhibit 04 · Reagents">

<p align="center"><img src="{a('stack.svg')}" width="100%" alt="Stack"></p>

<img src="{a('sec-stats.svg')}" width="100%" alt="Exhibit 05 · Lab report">

<p align="center">
  <img src="{a('stats.svg')}" width="49%" alt="GitHub stats">
  <!-- streak card is live from streak-stats.demolab.com — delete the next line to hide it -->
  <img src="{self.streak_url()}" width="49%" alt="Contribution streak">
</p>
<p align="center">
  <img src="{a('langs.svg')}" width="49%" alt="Top languages">
  <img src="{a('activity.svg')}" width="49%" alt="Contribution activity">
</p>
<p align="center">
  <img src="{snake}" width="100%" alt="Contribution snake">
</p>

<img src="{a('sec-contact.svg')}" width="100%" alt="Exhibit 06 · Contact">

<p align="center">
  <a href="mailto:{C.EMAIL}"><img src="{a('btn-email.svg')}" height="42" alt="Email"></a>
  <a href="{C.LINKEDIN}"><img src="{a('btn-linkedin.svg')}" height="42" alt="LinkedIn"></a>
  <a href="{C.MAIN_ACCOUNT}"><img src="{a('btn-main.svg')}" height="42" alt="Main account: Sagar-Dalwala"></a>
</p>

<p align="center"><img src="{a('footer.svg')}" width="100%" alt="© 2026 {C.NAME}"></p>
"""


Theme = Lab
