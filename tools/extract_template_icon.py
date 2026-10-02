"""Extract labeled icons from the public Snowflake 2026 template as PNG.

Finds the vector icon placed directly above a label on an icon slide, converts
its DrawingML custom geometry (with group transforms) to SVG, and rasterizes it
in Snowflake Blue on a transparent background.
"""
import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, "/tmp/parte-icon-render-deps")
import resvg_py

NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
A = "{%s}" % NS["a"]
P = "{%s}" % NS["p"]
SLIDES = Path("/tmp/sfpotx/ppt/slides")
BLUE = "#29B5E8"


def xfrm(el):
    x = el.find("./p:spPr/a:xfrm", NS) if el.tag == P + "sp" else el.find("./p:grpSpPr/a:xfrm", NS)
    off, ext = x.find("a:off", NS), x.find("a:ext", NS)
    d = dict(x=int(off.get("x")), y=int(off.get("y")), w=int(ext.get("cx")), h=int(ext.get("cy")),
             rot=int(x.get("rot", 0)) / 60000, flipH=x.get("flipH") == "1", flipV=x.get("flipV") == "1")
    co, ce = x.find("a:chOff", NS), x.find("a:chExt", NS)
    if co is not None:
        d.update(cx=int(co.get("x")), cy=int(co.get("y")), cw=int(ce.get("cx")) or 1, ch=int(ce.get("cy")) or 1)
    return d


def text(el):
    return " ".join(t.text for t in el.iter(A + "t") if t.text).strip()


def group_matrix(g):
    """SVG transform mapping child coordinates of a group into its parent."""
    sx, sy = g["w"] / g["cw"], g["h"] / g["ch"]
    return f"translate({g['x']} {g['y']}) scale({sx} {sy}) translate({-g['cx']} {-g['cy']})"


def shape_svg(sp):
    t = xfrm(sp)
    out = []
    geom = sp.find("./p:spPr/a:custGeom", NS)
    if geom is None:
        return ""
    no_fill = sp.find("./p:spPr/a:noFill", NS) is not None
    ln = sp.find("./p:spPr/a:ln", NS)
    stroke = ln is not None and ln.find("a:noFill", NS) is None and ln.find("a:solidFill", NS) is not None
    stroke_w = int(ln.get("w", 12700)) if ln is not None else 0
    for path in geom.find("a:pathLst", NS):
        pw, ph = int(path.get("w", t["w"] or 1)) or 1, int(path.get("h", t["h"] or 1)) or 1
        d, cur, start = [], (0, 0), (0, 0)
        for cmd in path:
            tag = cmd.tag[len(A):]
            pts = [(int(p.get("x")), int(p.get("y"))) for p in cmd.findall("a:pt", NS)]
            if tag == "moveTo":
                cur = start = pts[0]
                d.append("M %d %d" % pts[0])
            elif tag == "lnTo":
                cur = pts[0]
                d.append("L %d %d" % pts[0])
            elif tag == "cubicBezTo":
                cur = pts[2]
                d.append("C " + " ".join("%d %d" % q for q in pts))
            elif tag == "quadBezTo":
                cur = pts[1]
                d.append("Q " + " ".join("%d %d" % q for q in pts))
            elif tag == "arcTo":
                wr, hr = int(cmd.get("wR")), int(cmd.get("hR"))
                st, sw = int(cmd.get("stAng")) / 60000, int(cmd.get("swAng")) / 60000
                a0 = math.radians(st)
                cx, cy = cur[0] - wr * math.cos(a0), cur[1] - hr * math.sin(a0)
                a1 = math.radians(st + sw)
                end = (cx + wr * math.cos(a1), cy + hr * math.sin(a1))
                large = 1 if abs(sw) > 180 else 0
                sweep = 1 if sw > 0 else 0
                d.append("A %d %d 0 %d %d %f %f" % (wr, hr, large, sweep, end[0], end[1]))
                cur = end
            elif tag == "close":
                d.append("Z")
                cur = start
        sx, sy = t["w"] / pw, t["h"] / ph
        tr = f"translate({t['x']} {t['y']}) scale({sx} {sy})"
        if t["flipH"] or t["flipV"] or t["rot"]:
            cxm, cym = t["x"] + t["w"] / 2, t["y"] + t["h"] / 2
            tr = (f"rotate({t['rot']} {cxm} {cym}) translate({cxm} {cym}) "
                  f"scale({-1 if t['flipH'] else 1} {-1 if t['flipV'] else 1}) translate({-cxm} {-cym}) " + tr)
        fill = "none" if no_fill or path.get("fill") == "none" else BLUE
        sattr = f' stroke="{BLUE}" stroke-width="{stroke_w / max(sx, 1e-9)}"' if stroke else ""
        out.append(f'<path transform="{tr}" d="{" ".join(d)}" fill="{fill}" fill-rule="evenodd"{sattr}/>')
    return "".join(out)


def node_svg(el):
    if el.tag == P + "sp":
        return shape_svg(el)
    g = xfrm(el)
    inner = "".join(node_svg(c) for c in el if c.tag in (P + "sp", P + "grpSp"))
    return f'<g transform="{group_matrix(g)}">{inner}</g>'


def find_icon(slide, label):
    tree = ET.parse(SLIDES / slide).getroot().find(".//p:cSld/p:spTree", NS)
    items = [el for el in tree if el.tag in (P + "sp", P + "grpSp")]
    lab = next(el for el in items if text(el) == label)
    lx = xfrm(lab)
    lcx = lx["x"] + lx["w"] / 2
    best = None
    for el in items:
        if text(el) or el is lab:
            continue
        g = xfrm(el)
        gcx, gb = g["x"] + g["w"] / 2, g["y"] + g["h"]
        if abs(gcx - lcx) < 20 * 12700 and 0 <= lx["y"] - gb < 25 * 12700:
            dist = abs(gcx - lcx) + (lx["y"] - gb)
            if best is None or dist < best[0]:
                best = (dist, el, g)
    if best is None:
        raise SystemExit(f"no icon above {label!r} on {slide}")
    return best[1], best[2]


def render(slide, label, out_png, size=512):
    el, g = find_icon(slide, label)
    body = node_svg(el)
    pad = max(g["w"], g["h"]) * 0.04
    vb = (g["x"] - pad, g["y"] - pad, g["w"] + 2 * pad, g["h"] + 2 * pad)
    side = max(vb[2], vb[3])
    vx, vy = vb[0] - (side - vb[2]) / 2, vb[1] - (side - vb[3]) / 2
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx} {vy} {side} {side}" '
           f'width="{size}" height="{size}">{body}</svg>')
    Path(out_png).write_bytes(resvg_py.svg_to_bytes(svg_string=svg, width=size))
    return el.find(".//p:cNvPr", NS).get("id")


if __name__ == "__main__":
    jobs = json.loads(sys.argv[1])
    for slide, label, out in jobs:
        print(label, "-> shape", render(slide, label, out), out)
