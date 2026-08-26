#!/usr/bin/env python3
"""Rebuild the gallery WebP files from the original photos.

Run from anywhere:  python3 tools/build-gallery.py

Reads  ../Updated Images and Text/<folder>/**  (any nesting depth)
Writes Real Images/Gallery/<slug>/<slug>-NN.webp   (carousel slides, NUMBERED)
       Real Images/Gallery/cards/<name>.webp       (homepage cards, STABLE names)
       gallery-data.js  (counts + per-photo pixel sizes)

Counts are NOT in script.js — they come from the generated gallery-data.js, so
nothing needs updating by hand after a run.

The carousel files are NUMBERED and renumber whenever photos are added or
removed. The homepage card files are named after the CARD, built from a named
source, and therefore cannot move — see CARDS below.

Requires Pillow:  python3 -m pip install pillow
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SRC = os.path.join(os.path.dirname(SITE), "Updated Images and Text")
DST = os.path.join(SITE, "Real Images", "Gallery")

# Source folder -> carousel slug. Subfolders are walked automatically, so
# "Jagua Henna Carousel/jaguahenna 2/..." is picked up without any change here.
JOBS = [
    ("bridalhenna", "bridal"),
    ("Stylish Henna", "stylish"),
    ("Party Henna", "party"),
    ("Guest Henna", "guest"),
    ("Family Henna", "family"),
    ("Jagua Henna Carousel", "jagua"),
]

MAX_EDGE = 1200
QUALITY = 78

# The three homepage "What I Offer" cards, keyed on the SOURCE filename.
#
# 🔴 THIS MAP EXISTS BECAUSE POINTING index.html AT A NUMBERED SLIDE BROKE FOUR
# TIMES. `<slug>-NN.webp` is rebuilt from scratch on every run, so adding or
# removing ONE photo shifts every file after it — the ref stays valid and
# silently shows a different photograph. Nothing errors and no gate catches it.
# Source basenames never move, so a card built from one cannot drift.
# ⚠️ NEVER point a card in index.html back at a `<slug>-NN.webp` path.
#
# Cards render in a 4/3 box with object-fit: cover (.service-card-media in
# styles.css). Building at that ratio means the browser crops nothing.
# ⚠️ NOT 3/4 — that is the boutique TILE ratio, and a portrait image in the 4/3
# card box is centre-cropped hard enough to behead a model.
CARD_SIZE = (900, 675)
CARDS = {
    "card-bridal":  "InShot_20231029_002952559.jpg",
    "card-stylish": "InShot_20260331_214551241.jpg",
    "card-jagua":   "InShot_20240608_200456795.jpg",
}

# Photos that sit in one source folder but belong in another carousel, keyed by
# filename. Reassigned photos are appended to the end of their destination so
# existing numbering stays stable.
REASSIGN = {
    # Black-blue jagua stain, not henna — matches the other jagua body art
    "InShot_20260607_205546742.jpg": "jagua",
    # Dense hand/forearm work with temple-dome bands, elephants, peacocks
    "InShot_20250607_220257821.jpg": "bridal",
    "InShot_20250704_225931389.jpg": "bridal",
    "InShot_20250709_211206719.jpg": "bridal",
    "InShot_20251208_223228344.jpg": "bridal",
    # Feet have their own carousel. Shots showing hands AND feet together stay
    # in Bridal, since they read as the complete bridal look.
    "InShot_20230626_223439106.jpg": "feet",
    "InShot_20230726_131843543.jpg": "feet",
    "InShot_20230821_182453626.jpg": "feet",
    "InShot_20230903_193402242.jpg": "feet",
    "InShot_20231029_002009496.jpg": "feet",
    "InShot_20231031_235101305.jpg": "feet",
    "InShot_20250527_222231205.jpg": "feet",
    "InShot_20250527_223529548.jpg": "feet",
    "InShot_20250528_220041031.jpg": "feet",
    "InShot_20260615_203242820.jpg": "feet",
    # These five came in from the Stylish folder and are feet, not hands
    "InShot_20221010_095352270.jpg": "feet",
    "InShot_20240526_154906331.jpg": "feet",
    "InShot_20250506_230413023.jpg": "feet",
    "InShot_20250511_212523917.jpg": "feet",
    "InShot_20250527_222335911.jpg": "feet",
}

# Photos Neena pulled from the site — each was a second shot of a design that
# already appears in the same carousel, so the pair read as a duplicate
# (2026-08-08). The originals are still in the source folders, so without this
# skip list a rebuild would put them straight back.
SKIP = {
    "InShot_20260525_200320004.jpg",  # was bridal-10, dupe of bridal-09
    "InShot_20260802_165618832.jpg",  # was guest-07,  dupe of guest-03
    "InShot_20260630_222610801.jpg",  # was family-15, dupe of family-14
    "InShot_20260630_222514276.jpg",  # was stylish-15, dupe of stylish-11
    # Pulled 2026-08-09 — Neena didn't want these on the site regardless of
    # how they were cropped.
    "InShot_20260518_214227975.jpg",  # was party-09
    "InShot_20260802_165535111.jpg",  # was guest-06
    "20210525_163720.jpg",            # was jagua-01
    "20240925_113107.jpg",            # was jagua-03
    "InShot_20231012_214459312.jpg",  # was jagua-09
}

EXTS = (".jpg", ".jpeg", ".png", ".heic", ".webp")

from PIL import Image, ImageOps


def trim_white(im, thresh=245):
    """Some sources are InShot exports with white padding baked in. Crop it."""
    px = im.load()
    w, h = im.size

    def col_white(x):
        return all(all(c > thresh for c in px[x, y]) for y in range(0, h, max(1, h // 60)))

    def row_white(y):
        return all(all(c > thresh for c in px[x, y]) for x in range(0, w, max(1, w // 60)))

    left = 0
    while left < w // 2 and col_white(left):
        left += 1
    right = w - 1
    while right > w // 2 and col_white(right):
        right -= 1
    top = 0
    while top < h // 2 and row_white(top):
        top += 1
    bottom = h - 1
    while bottom > h // 2 and row_white(bottom):
        bottom -= 1

    if (left, top, right, bottom) == (0, 0, w - 1, h - 1):
        return im
    return im.crop((left, top, right + 1, bottom + 1))


# Collections can exist purely as a reassignment destination, with no source
# folder of their own (e.g. "feet", gathered from Bridal and Stylish).
ALL_SLUGS = [slug for _s, slug in JOBS]
for dest in REASSIGN.values():
    if dest not in ALL_SLUGS:
        ALL_SLUGS.append(dest)

native = {slug: [] for slug in ALL_SLUGS}
incoming = {slug: [] for slug in ALL_SLUGS}

for src_dir, slug in JOBS:
    found = []
    for root, _dirs, names in os.walk(os.path.join(SRC, src_dir)):
        for n in names:
            if n.lower().endswith(EXTS):
                found.append(os.path.join(root, n))
    for p in sorted(found, key=lambda x: os.path.basename(x)):
        if os.path.basename(p) in SKIP:
            continue
        dest = REASSIGN.get(os.path.basename(p))
        (incoming[dest] if dest else native[slug]).append(p)

total = 0
manifest = {}
for slug in ALL_SLUGS:
    out_dir = os.path.join(DST, slug)
    os.makedirs(out_dir, exist_ok=True)

    # Natives keep their order; reassigned photos append.
    files = native[slug] + sorted(incoming[slug], key=lambda x: os.path.basename(x))

    # Clear leftovers from a previous run (including any macOS " 2" copies)
    for stale in os.listdir(out_dir):
        if stale.endswith(".webp"):
            os.remove(os.path.join(out_dir, stale))

    dims = []
    for i, path in enumerate(files, 1):
        im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        im = trim_white(im)
        w, h = im.size
        scale = MAX_EDGE / max(w, h)
        if scale < 1:
            im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        out = os.path.join(out_dir, f"{slug}-{i:02d}.webp")
        im.save(out, "WEBP", quality=QUALITY, method=6)
        dims.append(list(im.size))
    manifest[slug] = dims
    total += len(files)
    print(f"{slug:8} {len(files):>3} images")

# Homepage cards. Built from named sources into STABLE filenames, so a rebuild
# can never move them the way it moves the numbered slides above.
card_dir = os.path.join(DST, "cards")
os.makedirs(card_dir, exist_ok=True)
for stale in os.listdir(card_dir):
    if stale.endswith(".webp"):
        os.remove(os.path.join(card_dir, stale))

# Sources live under any of the JOBS folders; basenames are unique across them.
by_name = {}
for _src_dir, _slug in JOBS:
    for root, _dirs, names in os.walk(os.path.join(SRC, _src_dir)):
        for n in names:
            if n.lower().endswith(EXTS):
                by_name.setdefault(n, os.path.join(root, n))

for card, basename in sorted(CARDS.items()):
    path = by_name.get(basename)
    if not path:
        # Loud, not silent: a missing card source means index.html is about to
        # 404 on a live page, which is worse than a build that says so.
        print(f"  ! CARD {card}: source not found — {basename}")
        continue
    im = trim_white(ImageOps.exif_transpose(Image.open(path)).convert("RGB"))
    ImageOps.fit(im, CARD_SIZE, Image.LANCZOS).save(
        os.path.join(card_dir, f"{card}.webp"), "WEBP", quality=QUALITY, method=6)
print(f"cards    {len(CARDS):>3} images  ({CARD_SIZE[0]}x{CARD_SIZE[1]})")

# Every photo's final pixel size, so the page can reserve the right space for a
# slide before its image has loaded. Without this the carousel can't size
# slides to each photo's shape (they load on demand and have no intrinsic size
# until then), which is what forces the crop-to-a-fixed-box behaviour.
lines = [
    "// GENERATED by tools/build-gallery.py — do not edit by hand.",
    "// galleryData[slug] = [[width, height], ...] in slide order.",
    "const galleryData = {",
]
for slug in ALL_SLUGS:
    pairs = ", ".join(f"[{w},{h}]" for w, h in manifest[slug])
    lines.append(f'  "{slug}": [{pairs}],')
lines.append("};")
with open(os.path.join(SITE, "gallery-data.js"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"\ntotal {total} images")
print("wrote gallery-data.js — counts and sizes come from there, "
      "so script.js needs no manual updating")
