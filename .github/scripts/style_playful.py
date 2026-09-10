from base import *
from svgkit import Doc, face, svg, reveal, fade, rise, draw_line
import content as C
import random

from palettes import PALETTES
P = dict(PALETTES["ocean"], page="#0d1117")

def set_palette(d):
    P.update(d)

WOB = ('<filter id="wob" x="-6%" y="-6%" width="112%" height="112%">'
       '<feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="7" result="n"/>'
       '<feDisplacementMap in="SourceGraphic" in2="n" scale="4" xChannelSelector="R" yChannelSelector="G"/></filter>')

def sticker(x, y, w, h, fill, r=14, rot=0, shadow=True, stroke=None, sw=2):
    """Sticker card with a hard offset shadow and a wobbly outline."""
    stroke = stroke or P["stroke"]
    cx, cy = x + w/2, y + h/2
    s = ""
    if shadow:
        s += f'<rect x="{x+5}" y="{y+6}" width="{w}" height="{h}" rx="{r}" fill="{P["shadow"]}" opacity=".9"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" filter="url(#wob)"/>'
    return f'<g transform="rotate({rot} {cx} {cy})">{s}</g>'

def tape(x, y, w=64, h=20, rot=-8, fill="#ffe066"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" opacity=".85" transform="rotate({rot} {x+w/2} {y+h/2})"/>'

def sparkle(cx, cy, r, fill, begin=0, dur=1.8):
    d = f"M{cx},{cy-r} Q{cx},{cy} {cx+r},{cy} Q{cx},{cy} {cx},{cy+r} Q{cx},{cy} {cx-r},{cy} Q{cx},{cy} {cx},{cy-r} Z"
    return (f'<path d="{d}" fill="{fill}"><animate attributeName="opacity" values=".2;1;.2" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="scale" values=".6;1.15;.6" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" additive="sum"/></path>')

def sparkle_at(cx, cy, r, fill, begin=0, dur=1.8):
    # scale about its own centre: translate to origin, scale, translate back
    return f'<g transform="translate({cx} {cy})">{sparkle(0, 0, r, fill, begin, dur)}</g>'

def squiggle(x1, x2, y, amp=4, step=14, stroke="#ff6b6b", sw=3, begin=0.3, dur=0.9):
    pts = []; x = x1; up = True
    d = f"M{x1},{y}"
    while x < x2:
        nx = min(x + step, x2)
        d += f" Q{(x+nx)/2},{y + (-amp if up else amp)} {nx},{y}"
        x = nx; up = not up
    return (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" pathLength="1" '
            f'stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" begin="{begin}s" dur="{dur}s" fill="freeze"/></path>')

def pill(doc, f, txt, x, y, size, fill, ink, pad=10, h=None, rot=0):
    w = f.measure(txt, size) + pad * 2; h = h or size + 12
    cx, cy = x + w/2, y + h/2
    m, _ = doc.text(f, txt, x + pad, y + h/2 + size*0.35, size, fill=ink)
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{P["stroke"]}" stroke-width="1.5"/>{m}</g>', w)

class Playful(Style):
    id, name = "playful", "Playful"
    pal = P

    def __init__(self):
        super().__init__()
        self.disp = face("Caveat.ttf", 700)
        self.hand = face("PatrickHand.ttf")

    # ------------------------------------------------------------------ hero
    def hero(self):
        doc = Doc(); H = 300; b = []
        b.append(sticker(28, 22, 700, 250, P["cream"], r=18, rot=-1.2))
        b.append(tape(40, 10, 80, 22, -12)); b.append(tape(640, 8, 80, 22, 9, P["teal"]))
        b.append(fade(0.2, self.T(doc, self.hand, "hi there, I'm", 70, 96, 26, P["ink2"])))
        m, w = self.TW(doc, self.disp, C.NAME, 66, 172, 86, P["ink"], per_glyph=True,
                       glyph_fn=lambda i, ch, use: rise(0.3 + i*0.04, use, dy=10, dur=0.5))
        b.append(m)
        b.append(squiggle(70, 70 + w, 186, amp=5, stroke=P["coral"], sw=4, begin=0.9))
        b.append(fade(1.2, self.T(doc, self.hand, "full-stack dev  ·  building AI agents & pipelines  ·  India", 70, 226, 21, P["ink2"])))
        p1, w1 = pill(doc, self.hand, "MERN × AI", 560, 60, 16, P["coral"], P["cream"], rot=6)
        p2, w2 = pill(doc, self.hand, "hackathon regular", 545, 104, 15, P["yellow"], P["pill_ink"], rot=-4)
        b.append(fade(1.4, p1)); b.append(fade(1.6, p2))
        # rocket doodle (bobbing) at right, outside the card
        rocket = (f'<g stroke="{P["page_text"]}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round" fill="none">'
                  f'<path d="M0,-38 C14,-22 16,4 10,22 L-10,22 C-16,4 -14,-22 0,-38 Z" fill="{P["cream"]}"/>'
                  f'<circle cx="0" cy="-8" r="6" fill="{P["sky"]}"/>'
                  f'<path d="M-10,10 L-22,26 L-8,22 M10,10 L22,26 L8,22"/>'
                  f'<path d="M-5,22 Q0,44 5,22" fill="{P["coral"]}" stroke="{P["coral"]}">'
                  f'<animate attributeName="d" values="M-5,22 Q0,44 5,22;M-5,22 Q0,56 5,22;M-5,22 Q0,44 5,22" dur=".5s" repeatCount="indefinite"/></path></g>')
        b.append(f'<g transform="translate(790 110) rotate(18)"><g>{rocket}<animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" dur="2.4s" repeatCount="indefinite"/></g></g>')
        for (cx, cy, r, c, bg) in [(760, 200, 9, P["yellow"], 0), (812, 60, 7, P["coral"], .6), (790, 240, 6, P["teal"], 1.1), (12, 120, 7, P["yellow"], .3), (60, 290, 6, P["coral"], .9)]:
            b.append(sparkle_at(cx, cy, r, c, bg))
        return svg(W, H, "".join(b), defs_extra=WOB, doc=doc)

    # --------------------------------------------------------------- section
    def section(self, idx, title):
        doc = Doc(); H = 58
        cols = [P["coral"], P["teal"], P["yellow"], P["lav"], P["sky"], P["peach"]]
        c = cols[(idx - 1) % len(cols)]
        m, w = self.TW(doc, self.disp, title, 2, 38, 36, P["page_text"])
        b = [m, squiggle(4, 4 + w, 48, amp=4, stroke=c, sw=3, begin=0.2), sparkle_at(w + 26, 20, 7, c, 0.2)]
        return svg(W, H, "".join(b), defs_extra=WOB, doc=doc)

    # ------------------------------------------------------------------ card
    def card(self, idx, p):
        title, url, desc, tags, award = p
        doc = Doc(); H = CARD_H + 24
        rot = 0.8 if idx % 2 else -0.8
        b = [sticker(14, 14, CARD_W-34, H-34, P["cream"], r=14, rot=rot)]
        b.append(tape(CARD_W - 86, 6, 56, 16, -10 if idx % 2 else 12, [P["yellow"], P["teal"], P["lav"], P["coral"]][idx % 4]))
        b.append(self.T(doc, self.disp, title, 32, 52, 27, P["ink"]))
        y = 76
        for ln in wrap(self.hand, desc, 14, CARD_W-72)[:2]:
            b.append(self.T(doc, self.hand, ln, 32, y, 14, P["ink2"])); y += 18
        if award:
            b.append(star(38, 114, 7, P["yellow"], extra=f'stroke="{P["stroke"]}" stroke-width="1"'))
            b.append(self.T(doc, self.hand, award, 50, 118, 13, P["coral"]))
        x = 32; pcols = [P["teal"], P["lav"], P["sky"], P["mint"], P["peach"]]
        for i, tg in enumerate(tags):
            m, w = pill(doc, self.hand, tg, x, 126, 11.5, pcols[i % 5], P["pill_ink"], pad=8, h=20); b.append(m); x += w + 6
        return svg(CARD_W, H, "".join(b), defs_extra=WOB, doc=doc)

    # ------------------------------------------------------------------ wins
    def wins(self):
        doc = Doc(); H = 118; b = []
        col = W / 3; cols = [P["yellow"], P["teal"], P["coral"]]
        for i, (name, year, what) in enumerate(C.WINS):
            x = 8 + i * col; cx, cy = x + 24, 50
            # medal: ribbon + circle
            b.append(f'<path d="M{cx-11},{cy+12} L{cx-14},{cy+40} L{cx},{cy+32} L{cx+14},{cy+40} L{cx+11},{cy+12}" fill="{P["lav"]}" stroke="{P["stroke"]}" stroke-width="1.5"/>')
            b.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="{cols[i]}" stroke="{P["stroke"]}" stroke-width="2" filter="url(#wob)"/>')
            b.append(star(cx, cy + 1, 10, P["cream"], extra=f'stroke="{P["stroke"]}" stroke-width="1"'))
            b.append(self.T(doc, self.disp, name, x + 56, 46, 21, P["page_text"]))
            b.append(self.T(doc, self.hand, f"{year}  ·  {what}", x + 56, 70, 13.5, P["muted_on_page"]))
            b.append(sparkle_at(x + 52, 86, 5, cols[i], i * 0.4))
        return svg(W, H, "".join(b), defs_extra=WOB, doc=doc)

    def stack(self):
        return None

    # ----------------------------------------------------------------- stats
    def _frame(self, doc, title, rot):
        return [sticker(12, 12, STAT_W-28, STAT_H-28, P["cream"], r=16, rot=rot * 0.6),
                self.T(doc, self.disp, title, 32, 48, 26, P["ink"]), line(32, 58, STAT_W-32, 58, P["paper_line"], 2, 'stroke-dasharray="6 5" stroke-linecap="round"')]

    def stats_card(self, data=None):
        doc = Doc(); S = data or C.STATS_SAMPLE; b = self._frame(doc, "my github, roughly", -0.8)
        rows = [("repos", S["repos"], P["coral"]), ("contributions", S["contributions"], P["teal"]), ("hackathons", S["hackathons"], P["yellow"]),
                ("stars", S["stars"], P["sky"]), ("pull requests", S["prs"], P["lav"]), ("followers", S["followers"], P["peach"])]
        for i, (k, v, c) in enumerate(rows):
            x = 34 + (i % 3) * 150; y = 104 + (i // 3) * 58
            b.append(f'<circle cx="{x+14}" cy="{y-12}" r="20" fill="{c}" stroke="{P["stroke"]}" stroke-width="1.5"/>')
            b.append(self.T(doc, self.disp, str(v), x + 14, y - 3, 26, P["pill_ink"], anchor="middle"))
            b.append(self.T(doc, self.hand, k, x + 42, y - 6, 14, P["ink2"]))
        return svg(STAT_W, STAT_H, "".join(b), defs_extra=WOB, doc=doc)

    def langs_card(self, langs=None):
        doc = Doc(); b = self._frame(doc, "what I write in", 0.7)
        cols = [P["yellow"], P["sky"], P["teal"], P["coral"], P["lav"]]
        for i, ((l, pct), c) in enumerate(zip(langs or C.LANGS_SAMPLE, cols)):
            y = 78 + i * 22
            b.append(self.T(doc, self.hand, l, 32, y + 5, 14, P["ink2"]))
            b.append(f'<rect x="130" y="{y-6}" width="{300*pct/100:.0f}" height="14" rx="7" fill="{c}" stroke="{P["stroke"]}" stroke-width="1.5" filter="url(#wob)"><animate attributeName="width" from="0" to="{300*pct/100:.0f}" begin="{0.2+i*0.12:.2f}s" dur="0.9s" fill="freeze"/></rect>')
            b.append(self.T(doc, self.hand, f"{pct}%", STAT_W-34, y + 5, 14, P["ink"], anchor="end"))
        return svg(STAT_W, STAT_H, "".join(b), defs_extra=WOB, doc=doc)

    def activity_card(self, vals=None):
        doc = Doc(); b = self._frame(doc, "a year of commits", -0.6)
        vals = vals or sample_activity(); x0, x1, y0, y1 = 32, STAT_W-32, 72, 158
        vmax = max(max(vals), 1)
        pts = [(x0 + (x1-x0)*i/(len(vals)-1), y1 - (y1-y0)*v/vmax) for i, v in enumerate(vals)]
        path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        b.append(f'<path d="{path} L{x1},{y1} L{x0},{y1} Z" fill="{P["teal"]}" opacity=".35"/>')
        b.append(line(x0, y1, x1, y1, P["stroke"], 2, 'stroke-linecap="round"'))
        b.append(f'<path d="{path}" fill="none" stroke="{P["coral"]}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" filter="url(#wob)" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" dur="1.8s" fill="freeze"/></path>')
        b.append(self.T(doc, self.hand, "52 weeks ago", x0, 176, 12, P["ink3"]))
        b.append(self.T(doc, self.hand, "now", x1, 176, 12, P["ink3"], anchor="end"))
        return svg(STAT_W, STAT_H, "".join(b), defs_extra=WOB, doc=doc)

    # ---------------------------------------------------------------- button
    def button(self, kind, label):
        doc = Doc(); txt, col = {"email": ("say hi ✉", P["coral"]), "linkedin": ("linkedin", P["sky"]), "resume": ("resume ↓", P["yellow"])}[kind]
        txt = txt.replace(" ✉", "").replace(" ↓", "")
        w = int(self.hand.measure(txt, 18) + 56); H = 46
        b = [f'<rect x="7" y="8" width="{w-12}" height="{H-14}" rx="17" fill="{P["shadow"]}"/>',
             f'<rect x="3" y="3" width="{w-12}" height="{H-14}" rx="17" fill="{col}" stroke="{P["stroke"]}" stroke-width="2"/>',
             self.T(doc, self.hand, txt, (w-6)/2, 26, 18, P["pill_ink"], anchor="middle")]
        return svg(w, H, "".join(b), doc=doc)

    def footer(self):
        doc = Doc(); H = 76
        b = [squiggle(W/2 - 160, W/2 + 160, 14, amp=4, stroke=P["teal"], sw=3),
             self.T(doc, self.disp, "thanks for scrolling!", W/2, 50, 30, P["page_text"], anchor="middle"),
             self.T(doc, self.hand, f"© 2026 {C.NAME}  ·  made with too much chai", W/2, 70, 13, P["muted_on_page"], anchor="middle"),
             sparkle_at(W/2 + 150, 42, 8, P["yellow"], 0.3), sparkle_at(W/2 - 150, 40, 6, P["coral"], 0.8)]
        return svg(W, H, "".join(b), doc=doc)

    # --------------------------------------------------------------- widgets
    def typing_url(self):
        from urllib.parse import quote
        return (f"https://readme-typing-svg.demolab.com/?font=Caveat&weight=700&size=28&pause=1200&color={P['yellow'][1:].upper()}"
                f"&center=true&vCenter=true&width=520&height=48&lines={quote(';'.join(C.TYPING_LINES), safe=';')}")

    def streak_url(self):
        h = lambda k: P[k][1:]
        return (f"https://streak-stats.demolab.com/?user={C.STATS_USER}&hide_border=false&border={h('stroke')}&border_radius=14"
                f"&background={h('cream')}&ring={h('coral')}&fire={h('coral')}&currStreakNum={h('ink')}&sideNums={h('ink')}"
                f"&currStreakLabel={h('coral')}&sideLabels={h('ink2')}&dates={h('ink3')}&stroke={h('paper_line')}")

    def snake_css(self):
        return ":root{--cb:#1b1f230a;--cs:%s;--ce:#161b22;--c0:#161b22;--c1:#0b4f3f;--c2:#12866a;--c3:#12b886;--c4:#96f2d7}" % P["coral"]

    def md_about(self):
        icons = {"now": "🛠️", "into": "🧠", "edu": "🎓", "base": "📍"}
        return "\n".join(f"- {icons[k]} **{k}** — {v}" for k, v in C.ABOUT)

    def md_stack(self, a):
        return f'<p align="center"><img src="https://skillicons.dev/icons?i={C.SKILLICONS}&perline=8" alt="Stack"></p>'
