#!/usr/bin/env python3
"""Generate ornamental mandala artwork as SVG.

Standalone and dependency-free (Python standard library only), so it can be
vendored into any project by copying this one file.

Henna site — regenerate the boutique placeholders exactly as shipped:

    python3 tools/build-boutique-placeholders.py

Any other project — point it at a palette and ask for N designs:

    python3 mandala.py --out ./art --count 12 --palette palettes/royal-jade.json

Palette files may use either the Junoon content-studio schema
({"colors": {"primary","dark","light","accent", ...}}) or a flat
{"bg0","bg1","ink","accent"}. Or skip the file and pass --colors directly.

Output is SVG: a few KB each, scales to any size without going soft, and the
colours can be find-replaced afterwards without regenerating.
"""
import argparse
import json
import math
import os
import random
import sys

# --------------------------------------------------------------- geometry ---

# Canvas defaults. CY sits slightly above centre so the composition reads as
# centred once a caption sits underneath it.
DEF_W, DEF_H = 300, 400
CY_RATIO = 0.49

_scale = 1.0


def S(v):
    """Scale a length. Returns the value untouched at 1.0 so the default canvas
    reproduces byte-identical output to what the henna site already ships."""
    return v if _scale == 1.0 else v * _scale


def petal(length, width, taper=0.35):
    """Teardrop pointing up from the origin."""
    return (f"M0 0 C{width} {-length * taper}, {width} {-length * 0.74}, 0 {-length} "
            f"C{-width} {-length * 0.74}, {-width} {-length * taper}, 0 0 Z")


def leaf(length, width):
    """Pointed leaf — flatter shoulders than a teardrop."""
    return (f"M0 0 C{width} {-length * 0.3}, {width} {-length * 0.7}, 0 {-length} "
            f"C{-width} {-length * 0.7}, {-width} {-length * 0.3}, 0 0 Z")


SHAPES = {"petal": petal, "leaf": leaf}


def ring_petals(cx, cy, n, inner, length, width, stroke, fill="none", sw=1.6,
                op=1.0, shape=petal, phase=0.0):
    out = []
    d = shape(length, width)
    for i in range(n):
        a = 360.0 * i / n + phase
        out.append(
            f'      <g transform="rotate({a:.2f} {cx} {cy})">'
            f'<g transform="translate({cx} {cy - inner})">'
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'opacity="{op}"/></g></g>')
    return "\n".join(out)


def ring_dots(cx, cy, n, radius, r, fill, op=1.0, phase=0.0):
    out = []
    for i in range(n):
        a = math.radians(360.0 * i / n + phase)
        x = cx + radius * math.sin(a)
        y = cy - radius * math.cos(a)
        out.append(f'      <circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" '
                   f'fill="{fill}" opacity="{op}"/>')
    return "\n".join(out)


def ring_scallops(cx, cy, n, radius, depth, stroke, sw=1.4, op=1.0):
    """Scalloped arc border — the lace edge common in mehndi cuffs."""
    out = []
    step = 360.0 / n
    for i in range(n):
        a0, a1 = math.radians(step * i), math.radians(step * (i + 1))
        x0, y0 = cx + radius * math.sin(a0), cy - radius * math.cos(a0)
        x1, y1 = cx + radius * math.sin(a1), cy - radius * math.cos(a1)
        out.append(f'      <path d="M{x0:.2f} {y0:.2f} A{depth} {depth} 0 0 1 {x1:.2f} {y1:.2f}" '
                   f'fill="none" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')
    return "\n".join(out)


def circle(cx, cy, r, stroke, sw=1.2, op=1.0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}" opacity="{op}"{d}/>')


def corner_paisley(w, h, accent, op=0.35):
    d = ("M0 0 C14 -4, 24 6, 20 18 C17 27, 7 30, 2 25 C-2 21, 0 14, 5 13 "
         "C9 12, 12 15, 11 18")
    return "\n".join([
        f'    <g opacity="{op}" fill="none" stroke="{accent}" stroke-width="1.5">',
        f'      <g transform="translate(34 34) rotate(0)"><path d="{d}"/></g>',
        f'      <g transform="translate({w - 34} 34) rotate(90)"><path d="{d}"/></g>',
        f'      <g transform="translate({w - 34} {h - 34}) rotate(180)"><path d="{d}"/></g>',
        f'      <g transform="translate(34 {h - 34}) rotate(270)"><path d="{d}"/></g>',
        '    </g>',
    ])


# ----------------------------------------------------------------- colour ---

def _hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c))):02x}" for c in rgb)


def mix(a, b, t):
    """Blend hex colour a toward b by t (0..1)."""
    ra, rb = _hex_to_rgb(a), _hex_to_rgb(b)
    return _rgb_to_hex(tuple(ra[i] + (rb[i] - ra[i]) * t for i in range(3)))


def tones_from_palette(colors):
    """Derive three background/ink pairings from a project palette.

    Expects at least `light`, `dark` and `accent`; `primary` falls back to
    `dark` when absent. Three tones give a grid visual rhythm instead of N
    identical tiles.
    """
    light = colors.get("light") or "#faf7f1"
    dark = colors.get("dark") or "#181614"
    accent = colors.get("accent") or colors.get("primary") or dark
    primary = colors.get("primary") or dark
    return {
        "light": {"bg0": light,               "bg1": mix(light, dark, 0.10),
                  "ink": dark,                "accent": accent},
        "warm":  {"bg0": mix(light, dark, 0.06), "bg1": mix(light, dark, 0.20),
                  "ink": primary,            "accent": dark},
        "deep":  {"bg0": mix(light, accent, 0.10), "bg1": mix(light, dark, 0.26),
                  "ink": dark,               "accent": primary},
    }


# The henna site's palette, kept literal so --preset henna reproduces the
# shipped artwork exactly rather than approximately.
HENNA_TONES = {
    "light": {"bg0": "#faf7f1", "bg1": "#f0e7d6", "ink": "#5c1a0d", "accent": "#d89947"},
    "warm":  {"bg0": "#f0e7d6", "bg1": "#e8dac3", "ink": "#9E4624", "accent": "#5c1a0d"},
    "deep":  {"bg0": "#f6ede0", "bg1": "#e3d0b4", "ink": "#5c1a0d", "accent": "#9E4624"},
}


# ------------------------------------------------------------------ build ---

def design(outer_n, outer_r, outer_len, mid_n, mid_r, mid_len,
           inner_n, inner_len, scallop_n=0, scallop_r=0, dots_n=0, dots_r=0,
           shape=petal):
    """A stack of layers, outermost first."""
    layers = []
    if scallop_n:
        layers.append(lambda cx, cy, i, a: ring_scallops(
            cx, cy, scallop_n, S(scallop_r), 12, a, 1.3, 0.65))
    if dots_n:
        layers.append(lambda cx, cy, i, a: ring_dots(
            cx, cy, dots_n, S(dots_r), 2.4, a, 0.85))
    layers += [
        lambda cx, cy, i, a: ring_petals(cx, cy, outer_n, S(outer_r), S(outer_len),
                                         S(outer_len * 0.30), i, "none", 1.5, 0.9, shape),
        lambda cx, cy, i, a: circle(cx, cy, S(outer_r), a, 1.1, 0.55),
        lambda cx, cy, i, a: ring_petals(cx, cy, mid_n, S(mid_r), S(mid_len),
                                         S(mid_len * 0.36), a, "none", 1.6, 0.95),
        lambda cx, cy, i, a: circle(cx, cy, S(mid_r), i, 1.1, 0.5, "3 5"),
        lambda cx, cy, i, a: ring_petals(cx, cy, inner_n, S(8), S(inner_len),
                                         S(inner_len * 0.42), i, a, 1.4, 0.9),
        lambda cx, cy, i, a: circle(cx, cy, S(9), i, 1.6, 1.0),
        lambda cx, cy, i, a: f'      <circle cx="{cx}" cy="{cy}" r="{S(4.5)}" fill="{a}"/>',
    ]
    return layers


def build(spec, tone, w=DEF_W, h=DEF_H):
    ink, accent = tone["ink"], tone["accent"]
    # Kept as floats deliberately — they land in the SVG as "150.0", which is
    # what the henna site already ships. Rounding them to ints here would
    # rewrite all 18 live files for no visual gain.
    cx, cy = w / 2, h * CY_RATIO
    body = "\n".join(layer(cx, cy, ink, accent) for layer in spec)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.55" y2="1">
      <stop offset="0" stop-color="{tone['bg0']}"/>
      <stop offset="1" stop-color="{tone['bg1']}"/>
    </linearGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.4" fill="{ink}" opacity="0.09"/>
    </pattern>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" fill="url(#dots)"/>
  <rect x="13" y="13" width="{w - 26}" height="{h - 26}" rx="10" fill="none"
        stroke="{accent}" stroke-width="1.1" opacity="0.38"/>
{corner_paisley(w, h, accent)}
  <g stroke-linecap="round" stroke-linejoin="round">
{body}
  </g>
</svg>
'''


# ---------------------------------------------------------------- presets ---

# The 18 designs shipping on hennabyneenajain.com/boutique.html. Explicit rather
# than generated so the live artwork can be rebuilt bit-for-bit.
HENNA_SPECS = [
    ("saree-01",   design(16, 96, 30, 10, 62, 30, 8, 30, scallop_n=24, scallop_r=112), "light"),
    ("saree-02",   design(12, 92, 34, 8, 58, 32, 6, 28, dots_n=18, dots_r=110), "warm"),
    ("saree-03",   design(20, 98, 26, 12, 64, 28, 10, 26, scallop_n=20, scallop_r=114, shape=leaf), "deep"),
    ("lehenga-01", design(14, 94, 32, 10, 60, 30, 8, 28, dots_n=14, dots_r=112), "warm"),
    ("lehenga-02", design(18, 96, 28, 12, 62, 26, 6, 30, scallop_n=18, scallop_r=113), "light"),
    ("anarkali",   design(12, 90, 36, 8, 56, 34, 8, 26, scallop_n=24, scallop_r=110, shape=leaf), "light"),
    ("salwar",     design(16, 94, 30, 10, 60, 28, 10, 24, dots_n=16, dots_r=112), "deep"),
    ("kurti",      design(10, 88, 38, 8, 54, 32, 6, 28, scallop_n=20, scallop_r=108), "light"),
    ("necklace",   design(18, 96, 28, 12, 62, 28, 8, 30, dots_n=24, dots_r=113), "warm"),
    ("jhumka",     design(14, 92, 32, 10, 58, 30, 10, 26, scallop_n=22, scallop_r=110, shape=leaf), "light"),
    ("bangles",    design(20, 98, 26, 14, 64, 26, 8, 28, scallop_n=28, scallop_r=114), "deep"),
    ("tikka",      design(12, 90, 34, 8, 56, 32, 6, 30, dots_n=12, dots_r=110), "warm"),
    ("dupatta",    design(16, 94, 30, 10, 60, 30, 8, 26, scallop_n=20, scallop_r=112, shape=leaf), "light"),
    ("potli",      design(14, 92, 32, 12, 58, 28, 10, 28, dots_n=20, dots_r=111), "deep"),
    ("bindi",      design(18, 96, 28, 10, 62, 30, 6, 26, scallop_n=24, scallop_r=113), "warm"),
    ("cover-clothing",    design(24, 100, 30, 16, 66, 30, 12, 30, scallop_n=32, scallop_r=116), "light"),
    ("cover-jewelry",     design(20, 100, 32, 14, 66, 32, 10, 32, dots_n=28, dots_r=116), "warm"),
    ("cover-accessories", design(24, 100, 28, 16, 66, 28, 12, 28, scallop_n=28, scallop_r=116, shape=leaf), "deep"),
]

PRESETS = {
    "henna": {
        "tones": HENNA_TONES,
        "specs": HENNA_SPECS,
        "out": os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "Real Images", "Boutique", "placeholders"),
        "help": "the 18 boutique placeholders on hennabyneenajain.com",
    },
}


# ------------------------------------------------------------- generation ---

OUTER_N = [10, 12, 14, 16, 18, 20, 24]
MID_N = [8, 10, 12, 14, 16]
INNER_N = [6, 8, 10, 12]


def random_specs(count, seed, tone_names):
    """Deterministic for a given seed — same seed, same artwork."""
    rng = random.Random(seed)
    specs = []
    for i in range(count):
        border = rng.choice(["scallop", "dots", "none"])
        kw = {"shape": SHAPES[rng.choice(["petal", "leaf"])]}
        if border == "scallop":
            kw.update(scallop_n=rng.choice([18, 20, 22, 24, 28, 32]),
                      scallop_r=rng.choice([108, 110, 112, 113, 114, 116]))
        elif border == "dots":
            kw.update(dots_n=rng.choice([12, 14, 16, 18, 20, 24, 28]),
                      dots_r=rng.choice([110, 111, 112, 113, 116]))
        spec = design(rng.choice(OUTER_N), rng.choice([88, 90, 92, 94, 96, 98, 100]),
                      rng.choice([26, 28, 30, 32, 34, 36, 38]),
                      rng.choice(MID_N), rng.choice([54, 56, 58, 60, 62, 64, 66]),
                      rng.choice([26, 28, 30, 32, 34]),
                      rng.choice(INNER_N), rng.choice([24, 26, 28, 30, 32]), **kw)
        specs.append((None, spec, tone_names[i % len(tone_names)]))
    return specs


def main():
    ap = argparse.ArgumentParser(
        description="Generate ornamental mandala SVGs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="examples:\n"
               "  %(prog)s\n"
               "  %(prog)s --out ./art --count 12 --palette palettes/royal-jade.json\n"
               "  %(prog)s --out ./art --count 6 --colors light=#F2F0E4,dark=#0A2E1F,accent=#E8B870\n"
               "  %(prog)s --out ./bg --count 8 --size 1080x1350 --prefix slide\n")
    ap.add_argument("--preset", choices=sorted(PRESETS),
                    help="a built-in design set (default: henna, when no other options given)")
    ap.add_argument("--out", help="output directory")
    ap.add_argument("--count", type=int, help="how many designs to generate")
    ap.add_argument("--palette", help="palette JSON (Junoon content-studio schema or flat)")
    ap.add_argument("--colors", help="inline palette, e.g. light=#fff,dark=#111,accent=#d89947")
    ap.add_argument("--size", default=f"{DEF_W}x{DEF_H}", help="canvas WxH (default 300x400)")
    ap.add_argument("--prefix", default="mandala", help="output filename prefix")
    ap.add_argument("--seed", type=int, default=7, help="same seed reproduces the same artwork")
    ap.add_argument("--names", help="comma-separated filenames, used instead of prefix-NN")
    ap.add_argument("--list-presets", action="store_true")
    args = ap.parse_args()

    if args.list_presets:
        for k, v in sorted(PRESETS.items()):
            print(f"{k:8} {v['help']}")
        return 0

    # No arguments at all → rebuild the henna site's artwork, the original job.
    preset = args.preset or (None if (args.count or args.palette or args.colors) else "henna")

    try:
        w, h = (int(x) for x in args.size.lower().split("x"))
    except ValueError:
        ap.error(f"--size expects WxH, got {args.size!r}")

    global _scale
    _scale = min(w / DEF_W, h / DEF_H)

    if preset:
        p = PRESETS[preset]
        tones, specs = p["tones"], p["specs"]
        out = args.out or p["out"]
        if args.count:
            specs = specs[:args.count]
    else:
        colors = {}
        if args.palette:
            with open(args.palette) as f:
                data = json.load(f)
            colors = data.get("colors", data)
        if args.colors:
            for pair in args.colors.split(","):
                if "=" not in pair:
                    ap.error(f"--colors expects key=#hex pairs, got {pair!r}")
                k, v = pair.split("=", 1)
                colors[k.strip()] = v.strip()
        if not colors:
            ap.error("need --palette or --colors (or use --preset)")
        # A flat {bg0,bg1,ink,accent} palette is used as a single tone as-is.
        if {"ink", "accent"} <= set(colors):
            tones = {"flat": {"bg0": colors.get("bg0", "#faf7f1"),
                              "bg1": colors.get("bg1", colors.get("bg0", "#f0e7d6")),
                              "ink": colors["ink"], "accent": colors["accent"]}}
        else:
            tones = tones_from_palette(colors)
        if not args.out:
            ap.error("--out is required when not using a preset")
        out = args.out
        specs = random_specs(args.count or 6, args.seed, list(tones))

    names = args.names.split(",") if args.names else None
    os.makedirs(out, exist_ok=True)
    written = []
    for i, (name, spec, tone_name) in enumerate(specs):
        fn = (names[i].strip() if names and i < len(names)
              else name or f"{args.prefix}-{i + 1:02d}")
        fn = fn if fn.endswith(".svg") else fn + ".svg"
        with open(os.path.join(out, fn), "w") as f:
            f.write(build(spec, tones[tone_name], w, h))
        written.append(fn)

    print(f"wrote {len(written)} mandala{'s' if len(written) != 1 else ''} "
          f"({w}x{h}) to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
