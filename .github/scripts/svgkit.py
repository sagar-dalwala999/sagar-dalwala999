"""Tiny SVG toolkit: shapes text into glyph outlines (so GitHub renders it identically
everywhere — no font loading inside <img>), with per-glyph handles for animation."""
import io, re, math, random
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.varLib import instancer

import os
FONT_DIR = os.environ.get("README_FONT_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

_face_cache = {}

class Face:
    def __init__(self, file, wght=None, key=None, opsz=None):
        self.key = key or re.sub(r"[^A-Za-z0-9]", "", file.split("/")[-1].split(".")[0]) + (f"w{wght}" if wght else "") + (f"o{opsz}" if opsz else "")
        tt = TTFont(f"{FONT_DIR}/{file}")
        if wght is not None and "fvar" in tt:
            axes = {a.axisTag: a for a in tt["fvar"].axes}
            loc = {"wght": wght}
            if "opsz" in axes:
                loc["opsz"] = opsz if opsz is not None else axes["opsz"].maxValue
            tt = instancer.instantiateVariableFont(tt, loc)
        self.tt = tt
        self.upem = tt["head"].unitsPerEm
        buf = io.BytesIO(); tt.save(buf); data = buf.getvalue()
        self.hb_face = hb.Face(data)
        self.hb_font = hb.Font(self.hb_face)
        self.hb_font.scale = (self.upem, self.upem)
        self.glyph_set = tt.getGlyphSet()
        self.glyph_order = tt.getGlyphOrder()
        self._paths = {}
        self.ascender = tt["hhea"].ascent
        self.descender = tt["hhea"].descent
        self.cap_height = getattr(tt["OS/2"], "sCapHeight", None) or int(self.upem * 0.7)
        self.x_height = getattr(tt["OS/2"], "sxHeight", None) or int(self.upem * 0.5)

    def glyph_path(self, gid):
        """SVG path 'd' for a glyph in font units (y-up, so caller flips)."""
        if gid in self._paths:
            return self._paths[gid]
        name = self.glyph_order[gid]
        pen = SVGPathPen(self.glyph_set)
        self.glyph_set[name].draw(pen)
        d = pen.getCommands()
        # round to 0.1 font units — invisible at any render size, ~40% smaller files
        d = re.sub(r"-?\d+\.\d+", lambda m: (f"{float(m.group()):.1f}").rstrip("0").rstrip("."), d)
        self._paths[gid] = d
        return d

    def shape(self, text, features=None):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(self.hb_font, buf, features or {"kern": True, "liga": True})
        out = []; x = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((info.codepoint, x + pos.x_offset, pos.y_offset, pos.x_advance, info.cluster))
            x += pos.x_advance
        return out, x

    def measure(self, text, size, tracking=0):
        glyphs, adv = self.shape(text)
        return adv * size / self.upem + tracking * max(len(glyphs) - 1, 0)


def face(file, wght=None, opsz=None):
    k = (file, wght, opsz)
    if k not in _face_cache:
        _face_cache[k] = Face(file, wght, opsz=opsz)
    return _face_cache[k]


class Doc:
    """Collects glyph <defs> and emits text as <use> refs; keeps files small."""
    def __init__(self):
        self.defs = {}      # id -> path d
        self.counter = 0

    def uid(self, prefix="e"):
        self.counter += 1
        return f"{prefix}{self.counter}"

    def _glyph_id(self, face, gid):
        gid_key = f"g{face.key}-{gid}"
        if gid_key not in self.defs:
            self.defs[gid_key] = face.glyph_path(gid)
        return gid_key

    def text(self, face, text, x, y, size, fill="#fff", tracking=0, anchor="start",
             per_glyph=False, cls=None, extra="", opacity=None, delay_fn=None, glyph_fn=None, wrap_tag=True):
        """Return SVG markup drawing `text` at baseline y. If per_glyph, each glyph is its own
        <use> wrapped in a <g> (class cls, style from delay_fn(i, ch)); or glyph_fn(i, ch, use_markup)
        returns the full markup for that glyph (use this for SMIL reveals — see reveal())."""
        glyphs, adv = face.shape(text)
        s = size / face.upem
        width = adv * s + tracking * max(len(glyphs) - 1, 0)
        x0 = x - (width if anchor == "end" else width / 2 if anchor == "middle" else 0)
        parts = []
        for i, (gid, gx, gy, gadv, cluster) in enumerate(glyphs):
            d = face.glyph_path(gid)
            if not d:  # space etc.
                continue
            gk = self._glyph_id(face, gid)
            px = x0 + gx * s + tracking * i
            py = y - gy * s
            attrs = f'href="#{gk}" transform="translate({px:.2f} {py:.2f}) scale({s:.5f} {-s:.5f})"'
            if per_glyph:
                if glyph_fn:
                    parts.append(glyph_fn(i, text[cluster], f'<use {attrs}/>'))
                    continue
                st = delay_fn(i, text[cluster]) if delay_fn else ""
                c = f' class="{cls}"' if cls else ""
                stl = f' style="{st}"' if st else ""
                # wrap in <g> so CSS transforms on the glyph don't fight the <use> transform attr
                parts.append(f'<g{c}{stl}><use {attrs}/></g>')
            else:
                parts.append(f'<use {attrs}/>')
        if per_glyph:
            g = f'<g fill="{fill}" {extra}>' + "".join(parts) + "</g>"
        else:
            c = f' class="{cls}"' if cls else ""
            op = f' opacity="{opacity}"' if opacity is not None else ""
            g = f'<g fill="{fill}"{c}{op} {extra}>' + "".join(parts) + "</g>"
        return g, width

    def text_path_d(self, face, text, x, y, size, tracking=0, anchor="start"):
        """Return a single combined path 'd' (absolute coords) — for stroke/draw animations."""
        glyphs, adv = face.shape(text)
        s = size / face.upem
        width = adv * s + tracking * max(len(glyphs) - 1, 0)
        x0 = x - (width if anchor == "end" else width / 2 if anchor == "middle" else 0)
        from fontTools.pens.transformPen import TransformPen
        ds = []
        for i, (gid, gx, gy, gadv, cluster) in enumerate(glyphs):
            name = face.glyph_order[gid]
            pen = SVGPathPen(face.glyph_set)
            tpen = TransformPen(pen, (s, 0, 0, -s, x0 + gx * s + tracking * i, y - gy * s))
            face.glyph_set[name].draw(tpen)
            d = pen.getCommands()
            if d:
                ds.append(d)
        return " ".join(ds), width

    def render_defs(self):
        return "<defs>" + "".join(f'<path id="{k}" d="{d}"/>' for k, d in self.defs.items()) + "</defs>"


def reveal(begin, inner, to=1, frm=0):
    """SMIL opacity reveal — robust inside <img> (CSS steps()/tiny durations are not)."""
    return f'<g opacity="{frm}"><set attributeName="opacity" to="{to}" begin="{begin:.2f}s" fill="freeze"/>{inner}</g>'


def fade(begin, inner, dur=0.35):
    return (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" '
            f'dur="{dur}s" fill="freeze"/>{inner}</g>')


def rise(begin, inner, dy=14, dur=0.7):
    """Fade in while drifting up dy px (SMIL, img-safe)."""
    return (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="{dur}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" begin="{begin:.2f}s" '
            f'dur="{dur}s" fill="freeze" calcMode="spline" keySplines="0.2 0.7 0.2 1"/>{inner}</g>')


def draw_line(x1, y1, x2, y2, stroke, sw=1, begin=0, dur=1.0, extra=""):
    """A line that draws itself from (x1,y1) to (x2,y2)."""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{stroke}" stroke-width="{sw}" {extra}>'
            f'<animate attributeName="x2" from="{x1}" to="{x2}" begin="{begin:.2f}s" dur="{dur}s" fill="freeze" calcMode="spline" keySplines="0.2 0.7 0.2 1"/>'
            f'<animate attributeName="y2" from="{y1}" to="{y2}" begin="{begin:.2f}s" dur="{dur}s" fill="freeze" calcMode="spline" keySplines="0.2 0.7 0.2 1"/></line>')


def svg(width, height, body, defs_extra="", style="", doc=None, bg=None, attrs=""):
    defs = (doc.render_defs() if doc else "")
    extra = f"<defs>{defs_extra}</defs>" if defs_extra else ""
    st = f"<style>{style}</style>" if style else ""
    bgr = f'<rect width="{width}" height="{height}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            f'role="img" {attrs}>{st}{defs}{extra}{bgr}{body}</svg>')


def wobble_path(d, amp=1.2, seed=1):
    """Roughen a path's coordinates slightly (hand-drawn feel) — only for simple absolute paths."""
    rnd = random.Random(seed)
    def rep(m):
        v = float(m.group(0)); return f"{v + rnd.uniform(-amp, amp):.2f}"
    return re.sub(r"-?\d+\.?\d*", rep, d)


def minify(s):
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r">\s+<", "><", s)
    return s.strip()
