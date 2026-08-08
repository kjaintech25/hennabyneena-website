#!/usr/bin/env python3
"""Rebuild the gallery WebP files from the original photos.

Run from anywhere:  python3 tools/build-gallery.py

Reads  ../Updated Images and Text/<folder>/**  (any nesting depth)
Writes Real Images/Gallery/<slug>/<slug>-NN.webp

After running, update the `count` values in script.js to match the totals it
prints, and check that the three homepage service-card references still point
at the photos you expect — renumbering can move them.

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
for slug in ALL_SLUGS:
    out_dir = os.path.join(DST, slug)
    os.makedirs(out_dir, exist_ok=True)

    # Natives keep their order; reassigned photos append.
    files = native[slug] + sorted(incoming[slug], key=lambda x: os.path.basename(x))

    # Clear leftovers from a previous run (including any macOS " 2" copies)
    for stale in os.listdir(out_dir):
        if stale.endswith(".webp"):
            os.remove(os.path.join(out_dir, stale))

    for i, path in enumerate(files, 1):
        im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        im = trim_white(im)
        w, h = im.size
        scale = MAX_EDGE / max(w, h)
        if scale < 1:
            im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        out = os.path.join(out_dir, f"{slug}-{i:02d}.webp")
        im.save(out, "WEBP", quality=QUALITY, method=6)
    total += len(files)
    print(f"{slug:8} {len(files):>3} images")

print(f"\ntotal {total} images -> update the counts in script.js")
