#!/usr/bin/env python3
"""Generate ornamental placeholder tiles for the boutique page.

Henna-style mandalas built from radial symmetry — original artwork in the site
palette. Deliberately decorative rather than photographic: nothing here claims
to be a specific piece of stock.
"""
import math
import os

OUT = os.path.join(
    "/Users/kushjain/Desktop/voiding szn 1/Freelance/Henna By Neena/website",
    "Real Images", "Boutique", "placeholders")

INK, SIENNA, GOLD = "#5c1a0d", "#9E4624", "#d89947"
SILK, CREAM = "#f0e7d6", "#faf7f1"

TONES = {
    "light": {"bg0": CREAM, "bg1": SILK,      "ink": INK,    "accent": GOLD},
    "warm":  {"bg0": SILK,  "bg1": "#e8dac3", "ink": SIENNA, "accent": INK},
    "deep":  {"bg0": "#f6ede0", "bg1": "#e3d0b4", "ink": INK, "accent": SIENNA},
}

CX, CY = 150.0, 196.0


def petal(length, width, taper=0.35):
    """Teardrop pointing up from the origin."""
    return (f"M0 0 C{width} {-length * taper}, {width} {-length * 0.74}, 0 {-length} "
            f"C{-width} {-length * 0.74}, {-width} {-length * taper}, 0 0 Z")


def leaf(length, width):
    """Pointed leaf with a midrib."""
    return (f"M0 0 C{width} {-length * 0.3}, {width} {-length * 0.7}, 0 {-length} "
            f"C{-width} {-length * 0.7}, {-width} {-length * 0.3}, 0 0 Z")


def ring_petals(n, inner, length, width, stroke, fill="none", sw=1.6,
                op=1.0, shape=petal, phase=0.0):
    out = []
    d = shape(length, width)
    for i in range(n):
        a = 360.0 * i / n + phase
        out.append(
            f'      <g transform="rotate({a:.2f} {CX} {CY})">'
            f'<g transform="translate({CX} {CY - inner})">'
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'opacity="{op}"/></g></g>')
    return "\n".join(out)


def ring_dots(n, radius, r, fill, op=1.0, phase=0.0):
    out = []
    for i in range(n):
        a = math.radians(360.0 * i / n + phase)
        x = CX + radius * math.sin(a)
        y = CY - radius * math.cos(a)
        out.append(f'      <circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" '
                   f'fill="{fill}" opacity="{op}"/>')
    return "\n".join(out)


def ring_scallops(n, radius, depth, stroke, sw=1.4, op=1.0):
    """Scalloped arc border — the lace edge common in mehndi cuffs."""
    out = []
    step = 360.0 / n
    for i in range(n):
        a0 = math.radians(step * i)
        a1 = math.radians(step * (i + 1))
        x0, y0 = CX + radius * math.sin(a0), CY - radius * math.cos(a0)
        x1, y1 = CX + radius * math.sin(a1), CY - radius * math.cos(a1)
        out.append(f'      <path d="M{x0:.2f} {y0:.2f} A{depth} {depth} 0 0 1 {x1:.2f} {y1:.2f}" '
                   f'fill="none" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')
    return "\n".join(out)


def circle(r, stroke, sw=1.2, op=1.0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'      <circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}" opacity="{op}"{d}/>')


def corner_paisley(accent, op=0.35):
    """Small paisley in each corner — fills the frame without crowding."""
    d = ("M0 0 C14 -4, 24 6, 20 18 C17 27, 7 30, 2 25 C-2 21, 0 14, 5 13 "
         "C9 12, 12 15, 11 18")
    return "\n".join([
        f'    <g opacity="{op}" fill="none" stroke="{accent}" stroke-width="1.5">',
        f'      <g transform="translate(34 34) rotate(0)"><path d="{d}"/></g>',
        f'      <g transform="translate(266 34) rotate(90)"><path d="{d}"/></g>',
        f'      <g transform="translate(266 366) rotate(180)"><path d="{d}"/></g>',
        f'      <g transform="translate(34 366) rotate(270)"><path d="{d}"/></g>',
        '    </g>',
    ])


def build(spec, tone):
    t = TONES[tone]
    ink, accent = t["ink"], t["accent"]
    body = "\n".join(layer(ink, accent) for layer in spec)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400" width="300" height="400" role="img">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.55" y2="1">
      <stop offset="0" stop-color="{t['bg0']}"/>
      <stop offset="1" stop-color="{t['bg1']}"/>
    </linearGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.4" fill="{ink}" opacity="0.09"/>
    </pattern>
  </defs>
  <rect width="300" height="400" fill="url(#bg)"/>
  <rect width="300" height="400" fill="url(#dots)"/>
  <rect x="13" y="13" width="274" height="374" rx="10" fill="none"
        stroke="{accent}" stroke-width="1.1" opacity="0.38"/>
{corner_paisley(accent)}
  <g stroke-linecap="round" stroke-linejoin="round">
{body}
  </g>
</svg>
'''


# Each design is a list of layers, outermost first. Petal counts and radii vary
# so no two tiles repeat, while the construction keeps them a family.
def design(outer_n, outer_r, outer_len, mid_n, mid_r, mid_len,
           inner_n, inner_len, scallop_n=0, scallop_r=0, dots_n=0, dots_r=0,
           shape=petal):
    layers = []
    if scallop_n:
        layers.append(lambda i, a, n=scallop_n, r=scallop_r:
                      ring_scallops(n, r, 12, a, 1.3, 0.65))
    if dots_n:
        layers.append(lambda i, a, n=dots_n, r=dots_r:
                      ring_dots(n, r, 2.4, a, 0.85))
    layers += [
        lambda i, a, n=outer_n, r=outer_r, L=outer_len, s=shape:
            ring_petals(n, r, L, L * 0.30, i, "none", 1.5, 0.9, s),
        lambda i, a, r=outer_r: circle(r, a, 1.1, 0.55),
        lambda i, a, n=mid_n, r=mid_r, L=mid_len:
            ring_petals(n, r, L, L * 0.36, a, "none", 1.6, 0.95),
        lambda i, a, r=mid_r: circle(r, i, 1.1, 0.5, "3 5"),
        lambda i, a, n=inner_n, L=inner_len:
            ring_petals(n, 8, L, L * 0.42, i, a, 1.4, 0.9),
        lambda i, a: circle(9, i, 1.6, 1.0),
        lambda i, a: f'      <circle cx="{CX}" cy="{CY}" r="4.5" fill="{a}"/>',
    ]
    return layers


SPECS = [
    # clothing
    ("saree-01",   design(16, 96, 30, 10, 62, 30, 8, 30, scallop_n=24, scallop_r=112), "light"),
    ("saree-02",   design(12, 92, 34, 8, 58, 32, 6, 28, dots_n=18, dots_r=110), "warm"),
    ("saree-03",   design(20, 98, 26, 12, 64, 28, 10, 26, scallop_n=20, scallop_r=114, shape=leaf), "deep"),
    ("lehenga-01", design(14, 94, 32, 10, 60, 30, 8, 28, dots_n=14, dots_r=112), "warm"),
    ("lehenga-02", design(18, 96, 28, 12, 62, 26, 6, 30, scallop_n=18, scallop_r=113), "light"),
    ("anarkali",   design(12, 90, 36, 8, 56, 34, 8, 26, scallop_n=24, scallop_r=110, shape=leaf), "light"),
    ("salwar",     design(16, 94, 30, 10, 60, 28, 10, 24, dots_n=16, dots_r=112), "deep"),
    ("kurti",      design(10, 88, 38, 8, 54, 32, 6, 28, scallop_n=20, scallop_r=108), "light"),
    # jewelry
    ("necklace",   design(18, 96, 28, 12, 62, 28, 8, 30, dots_n=24, dots_r=113), "warm"),
    ("jhumka",     design(14, 92, 32, 10, 58, 30, 10, 26, scallop_n=22, scallop_r=110, shape=leaf), "light"),
    ("bangles",    design(20, 98, 26, 14, 64, 26, 8, 28, scallop_n=28, scallop_r=114), "deep"),
    ("tikka",      design(12, 90, 34, 8, 56, 32, 6, 30, dots_n=12, dots_r=110), "warm"),
    # accessories
    ("dupatta",    design(16, 94, 30, 10, 60, 30, 8, 26, scallop_n=20, scallop_r=112, shape=leaf), "light"),
    ("potli",      design(14, 92, 32, 12, 58, 28, 10, 28, dots_n=20, dots_r=111), "deep"),
    ("bindi",      design(18, 96, 28, 10, 62, 30, 6, 26, scallop_n=24, scallop_r=113), "warm"),
    # headline covers — denser, since they render much larger
    ("cover-clothing",    design(24, 100, 30, 16, 66, 30, 12, 30, scallop_n=32, scallop_r=116), "light"),
    ("cover-jewelry",     design(20, 100, 32, 14, 66, 32, 10, 32, dots_n=28, dots_r=116), "warm"),
    ("cover-accessories", design(24, 100, 28, 16, 66, 28, 12, 28, scallop_n=28, scallop_r=116, shape=leaf), "deep"),
]

os.makedirs(OUT, exist_ok=True)
for name, spec, tone in SPECS:
    open(os.path.join(OUT, name + ".svg"), "w").write(build(spec, tone))
print(f"wrote {len(SPECS)} mandala placeholders")
