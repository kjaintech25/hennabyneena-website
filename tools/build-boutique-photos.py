#!/usr/bin/env python3
"""Convert Neena's boutique photos into the WebP files the carousels use.

    python3 tools/build-boutique-photos.py

Reads  ../Boutique Photos/<set>/**
Writes Real Images/Boutique/photos/<slug>/<slug>-NN.webp   (carousel rails)
       Real Images/Boutique/tiles/<slug>.webp              (category tiles)
       boutique-data.js  (sizes + counts, same shape as gallery-data.js)

The carousels reuse the gallery machinery in script.js, so boutique-data.js
deliberately declares `galleryData` — boutique.html loads this file and
gallery.html loads gallery-data.js, never both, so there's no clash.

Rail filenames are NUMBERED and renumber whenever a set changes. Tile
filenames are named after the category and are STABLE, which is why the
tiles are built here from named sources rather than pointed at a rail file.

Requires Pillow:  python3 -m pip install pillow
"""
import os
from PIL import Image, ImageOps, ImageColor

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SRC = os.path.join(os.path.dirname(SITE), "Boutique Photos")
DST = os.path.join(SITE, "Real Images", "Boutique", "photos")
TILE_DST = os.path.join(SITE, "Real Images", "Boutique", "tiles")

MAX_EDGE = 1200
QUALITY = 78
EXTS = (".jpg", ".jpeg", ".png", ".heic", ".webp")

# Tiles render in a 3/4 box and the three headline cards in a 4/3 one — see
# .boutique-tile-media and .service-card-media in styles.css. Building each at
# its own ratio means the browser crops nothing, so the crop chosen here is the
# crop that ships. ⚠️ These two ratios are NOT interchangeable: a 3/4 portrait
# dropped into the 4/3 card is centre-cropped hard enough to behead a model.
TILE_SIZE = (640, 853)
COVER_SIZE = (900, 675)

# --color-surface in styles.css. .boutique-tile-media sits on the cream page
# background, so a tile letterboxed onto this colour has no visible edge.
TILE_BG = ImageColor.getrgb("#faf7f1")
# Breathing room around a letterboxed tile, as a fraction of the box. Kept
# small: the landscape jewellery shots already lose height to the 3/4 box, and
# every extra point of margin shrinks the piece further.
TILE_MARGIN = 0.04

# Source folder -> carousel slug. ORDER lists the filenames that should come
# first; anything not named falls in afterwards in filename order.
#
# Party & Bridal mixes glossy model shots with mannequin and showroom shots, so
# the models lead and the stock shots follow — otherwise the two styles
# alternate and the strip looks accidental. Sarees is ordered the same way:
# models, then draped-fabric detail, then mannequins, with the two
# packaged-stock frames last since they read as inventory rather than product.
# Suits is nearly all model shots, with three composite/mannequin frames pushed
# to the end. Blouses is uniformly flat-lay, which is how blouses are actually
# sold, so it needs no reordering. Accessories is fully enumerated because most
# of that folder is excluded — see EXCLUDE.
SETS = [
    ("Party and Bridal Wear", "partywear-bridal", [
        "IMG-20260205-WA0028.jpg", "IMG-20260526-WA0005.jpg", "IMG-20260617-WA0000.jpg",
        "IMG-20260621-WA0079.jpg", "IMG-20260624-WA0000.jpg", "IMG-20260207-WA0041.jpg",
        "IMG-20260207-WA0053.jpg",
    ]),
    ("Sarees", "sarees-rail", [
        # models
        "IMG-20220623-WA0029.jpg", "IMG-20251002-WA0003.jpg", "IMG-20251012-WA0015.jpg",
        "IMG-20211012-WA0019.jpg", "IMG-20220623-WA0046.jpg", "IMG-20220623-WA0042.jpg",
        "IMG-20220525-WA0003.jpg", "IMG-20220623-WA0044.jpg",
        # draped-fabric detail
        "IMG-20241213-WA0010.jpg", "IMG-20241213-WA0013.jpg", "IMG-20241210-WA0019.jpg",
        "IMG-20260226-WA0042.jpg", "IMG-20241214-WA0016.jpg", "IMG-20210614-WA0076.jpg",
        "IMG-20210614-WA0080.jpg",
        # mannequin
        "IMG-20260501-WA0007.jpg", "IMG-20260506-WA0021.jpg",
        # packaged stock, last
        "IMG-20230302-WA0006.jpg", "IMG-20230302-WA0011.jpg",
    ]),
    ("Suits and Dresses", "suits-dresses", [
        "IMG-20250917-WA0000.jpg", "IMG-20250921-WA0038.jpg", "IMG-20250921-WA0042.jpg",
        "IMG-20250921-WA0048.jpg", "IMG-20251106-WA0000.jpg",
        "IMG-20251120-WA0005.jpg", "IMG-20251120-WA0006.jpg", "IMG-20260319-WA0002.jpg",
        "IMG-20260319-WA0003.jpg", "IMG-20260319-WA0004.jpg", "IMG-20260617-WA0001.jpg",
        "IMG-20260624-WA0002.jpg", "IMG-20260624-WA0003.jpg", "IMG-20260702-WA0006.jpg",
        "IMG-20260805-WA0002.jpg", "IMG-20251029-WA0010.jpg", "IMG-20260617-WA0002.jpg",
    ]),
    # ⚠️ SETS order must match the rail order in boutique.html — Jewelry sits
    # between Suits & Dresses and Blouses on the page (Kush, 2026-08-31).
    ("Jewelry", "jewelry-rail", []),
    # An empty ORDER just means "no manual ordering"; filename order is used.
    # An empty SET (no photos found) writes an empty list to boutique-data.js
    # and script.js hides that rail, so the page never shows a headed carousel
    # with nothing in it.
    ("Blouses", "blouses-rail", []),
    ("Accessories", "accessories-rail", [
        "IMG-20220603-WA0020.jpg", "IMG-20220603-WA0021.jpg", "IMG-20260817-WA0045.jpg",
        "IMG-20260818-WA0018.jpg", "IMG-20260818-WA0016.jpg",
        "IMG-20260818-WA0071.jpg", "IMG-20260818-WA0044.jpg", "IMG-20260818-WA0048.jpg",
    ]),
]

# Filenames that are never published, by basename.
#
# 🔴 THESE ARE THE SUPPLIER'S CATALOGUE PHOTOS. 13 of the 16 accessory shots
# carry an "SJNX" badge AND a printed product code ("SJNX-CODE-R-365"). Where
# the code sits on the backdrop it can be cropped away (see CROPS); where the
# supplier stamped a badge onto the JEWELLERY ITSELF there is no crop that
# removes it, so the photo is excluded rather than shipped watermarked. Nothing
# else on this site carries another business's branding — VERIFIED 2026-08-26
# across all 39 previously-live garment photos.
EXCLUDE = {
    # Pulled by Kush 2026-08-31, on look rather than on any mark:
    "IMG-20250510-WA0060.jpg",   # group shot of five guests — an event photo, not a piece
    # ⚠️ THIS FILE IS IN TWO SOURCE FOLDERS (Party and Bridal Wear AND Suits and
    # Dresses, byte-identical) so it was showing TWICE on the page. EXCLUDE is
    # matched on basename, which is what makes one entry remove both.
    "IMG-20250929-WA0089.jpg",   # cream/gold lehenga
    # Sarees — vendor "f" logo top-left plus code 88125 bottom-right.
    "IMG-20250929-WA0025.jpg",
    # Jewelry — 🔴 A THIRD KIND OF MARK, AND THE ONE WITH MONEY ATTACHED: several of
    # these carry a PRICE burned into the frame ("350", "650", "Pachi Kundan 260").
    # They come from a supplier's WhatsApp catalogue, so the number is very likely
    # the WHOLESALE price — publishing it would show customers what Neena pays. The
    # ones below could not be cropped clear; the rest are handled in CROPS.
    "IMG-20250717-WA0012.jpg",   # "No. 21470" on the backdrop INSIDE the necklace arc
    "IMG-20250717-WA0027.jpg",   # "No. 21470", same frame, different colourway
    "IMG-20260817-WA0080.jpg",   # SJNX code diagonal across the piece + badge on it
    "IMG-20260817-WA0082.jpg",   # SJNX code diagonal across the piece + corner badge
    # Jewelry — excluded on QUALITY, not on any mark. Both are multi-panel contact
    # sheets (6-9 products in one frame). Every other photo on this site is a single
    # piece or a model shot; a grid of thumbnails in a carousel reads as a screenshot.
    "IMG-20240621-WA0007.jpg",
    "IMG-20240622-WA0037.jpg",
    # Accessories — badge stamped on the piece itself, uncroppable.
    "IMG-20260817-WA0046.jpg",   # SJNX-CODE-200, badge on the bracelet
    "IMG-20260817-WA0083.jpg",   # SJNX-CODE-C-70, two badges on the kada
    "IMG-20260818-WA0024(1).jpg",  # SJNX-CODE-NT-90, badge on the ring
    "IMG-20260818-WA0027.jpg",   # SJNX-CODE-S-105, badge on the ring
    "IMG-20260818-WA0037.jpg",   # SJNX-CODE-B-85, badge on the pendant
    # 🔴 WA0043 IS THE ONE FRAME WHERE "crop to the clean piece" DOES NOT WORK,
    # and the reason is geometric, not aesthetic — MEASURED 2026-08-31, don't
    # re-derive it. The left earring carries a badge ON the piece, so only the
    # right one is publishable. But (a) the two earrings physically OVERLAP, so
    # any box holding the right one also holds a slice of the left one's stone,
    # and (b) the corner badge occupies x>=0.835, y<=0.14, which is exactly the
    # headroom the right earring's flower cluster needs. Clearing the badge
    # means top>=0.15, which beheads the cluster. There is no box that is both
    # clean and whole.
    "IMG-20260818-WA0043.jpg",   # SJNX-CODE-RB-140, no clean whole-piece crop exists
    "IMG-20260818-WA0065.jpg",   # SJNX-CODE-NT-90 over the model, badge on the ring
    "IMG-20260818-WA0084.jpg",   # SJNX-CODE-D-230, badge on the bangle
}

# basename -> (left, top, right, bottom) as fractions of the source image.
# Applied before the resize, so the published WebP has never contained the
# cropped-away region. Each of these removes a supplier code that sits on the
# backdrop rather than on the piece.
CROPS = {
    # 🔴 THESE ARE RAIL CROPS AND THEY ONLY HAVE ONE JOB: CLEAR THE WATERMARK.
    # They used to be tuned to also fill a 3/4 TILE, which is a different shape,
    # and the rail inherited that tighter box — four accessory slides were
    # showing half a piece. Tile framing now lives in TILE_FILL below; keep
    # these as loose as the watermark allows. (Kush, 2026-08-31.)
    "IMG-20260817-WA0045.jpg": (0.00, 0.52, 0.47, 1.00),  # bottom-left pair, both whole
    "IMG-20260818-WA0016.jpg": (0.48, 0.16, 1.00, 0.97),  # keep the right-hand earring
    "IMG-20260818-WA0018.jpg": (0.06, 0.115, 0.94, 1.00),  # drop code above, badge right
    # ⚠️ WA0048 CANNOT SHOW BOTH EARRINGS — the supplier stamped a badge onto
    # one of them — so it crops to the ONE clean earring. A whole earring beats
    # two halves; Kush's call, 2026-08-31. (WA0043 got the same instruction and
    # FAILED it — see EXCLUDE for why that frame has no clean crop at all.)
    "IMG-20260818-WA0044.jpg": (0.13, 0.14, 1.00, 1.00),  # drop the "940" scale display
    "IMG-20260818-WA0048.jpg": (0.10, 0.27, 0.44, 0.82),  # lower-left earring only
    "IMG-20260818-WA0071.jpg": (0.12, 0.30, 0.76, 1.00),  # centre the ring in a 3/4 box
    # Jewelry. Mostly a price in the bottom-right corner, sometimes with a
    # "Shot on OnePlus" camera watermark bottom-left — one crop clears both.
    "IMG-20240120-WA0013.jpg": (0.00, 0.00, 1.00, 0.92),  # "350"
    "IMG-20240621-WA0001.jpg": (0.00, 0.00, 1.00, 0.91),  # "650"
    "IMG-20240621-WA0003.jpg": (0.00, 0.00, 1.00, 0.92),  # "650"
    "IMG-20240621-WA0013.jpg": (0.00, 0.00, 1.00, 0.78),  # "390"
    "IMG-20240621-WA0014.jpg": (0.00, 0.00, 1.00, 0.83),  # "360"
    "IMG-20240621-WA0028.jpg": (0.00, 0.00, 1.00, 0.92),  # "Pachi Kundan 260"
    "IMG-20240622-WA0025.jpg": (0.00, 0.00, 0.70, 0.90),  # "B 290" + "S 400" + OnePlus
    "IMG-20240622-WA0027.jpg": (0.00, 0.00, 1.00, 0.91),  # "285" + OnePlus
    "IMG-20240622-WA0035.jpg": (0.00, 0.00, 1.00, 0.88),  # "410" + OnePlus — 0.92 left the "410" visible
    "IMG-20250929-WA0103.jpg": (0.00, 0.13, 1.00, 1.00),  # style code "AN70720869", top
    "IMG-20260817-WA0076.jpg": (0.00, 0.20, 1.00, 1.00),  # "SJNX-CODE-310", top
}

# Category tile slug -> (source folder, basename). One representative photo per
# category Neena carries; the slug matches the `src` in script.js's
# boutiqueItems. CROPS above applies here too.
#
# ⚠️ TWO CATEGORIES HAVE NO PHOTO AND ARE NOT IN THIS MAP: "Ring Bracelets"
# (the only two shots are badged on the piece) and "Anklets" (no photo exists
# in any folder). Their tiles are removed from boutiqueItems rather than left
# as artwork among real photos — add the source here and the tile back to
# script.js when Neena sends one.
TILES = {
    "lehengas":      ("Party and Bridal Wear", "IMG-20260526-WA0005.jpg"),
    "sarees":        ("Sarees", "IMG-20251002-WA0003.jpg"),  # 799x1066 — exactly 3/4
    "dresses":       ("Suits and Dresses", "IMG-20251120-WA0006.jpg"),
    "indo-western":  ("Suits and Dresses", "IMG-20260319-WA0003.jpg"),
    "partywear":     ("Party and Bridal Wear", "IMG-20260617-WA0000.jpg"),
    "blouses":       ("Blouses", "Screenshot_20260808_221023_WhatsApp.jpg"),
    "dupattas":      ("Suits and Dresses", "IMG-20250921-WA0038.jpg"),
    "gold-plated":   ("Accessories", "IMG-20260818-WA0018.jpg"),
    "semi-precious": ("Accessories", "IMG-20260818-WA0016.jpg"),
    "oxidized":      ("Accessories", "IMG-20220603-WA0020.jpg"),
    "earrings":      ("Accessories", "IMG-20260817-WA0045.jpg"),
    "rings":         ("Accessories", "IMG-20260818-WA0071.jpg"),
    "bangles-kadas": ("Accessories", "IMG-20260818-WA0044.jpg"),
}

# 🔴 TILES IN THIS SET ARE FITTED INSIDE THE 3/4 BOX, NOT CROPPED TO FILL IT.
# Everything else is a full-length model shot that fills a portrait box
# happily. These four are wide or square jewellery shots, so ImageOps.fit was
# slicing the sides off — the oxidized pair lost an earring edge, the kadas
# lost their top and bottom. Widening the crop is NOT available: every one of
# them has a supplier code or price hard against the frame (see CROPS), which
# is why they were tight in the first place.
#
# So they letterbox onto TILE_BG instead. The whole piece is visible, centred,
# with breathing room, and the cream matches the page so the tile reads as a
# product card rather than a photo with bars. Kush picked this over a blurred
# fill, 2026-08-31.
TILE_FILL = {"oxidized", "gold-plated", "bangles-kadas", "earrings"}

# The three headline cards at the top of boutique.html. Separate map because
# the card box is LANDSCAPE, so these are chosen from the few sources that are
# wider than tall — a full-length model shot cannot fill a 4/3 box without
# cropping to a midriff.
COVERS = {
    "cover-clothing":    ("Sarees", "IMG-20241213-WA0010.jpg"),
    "cover-jewelry":     ("Accessories", "IMG-20260818-WA0016.jpg"),
    "cover-accessories": ("Accessories", "IMG-20220603-WA0021.jpg"),
}

# Covers need their own crops: the CROPS entries above are tuned to fill a
# PORTRAIT tile and several of them come out portrait, which is the wrong shape
# here. A cover crop wins over the CROPS entry for the same file.
COVER_CROPS = {
    # Wide crop of the right-hand earring. Starting at 0.30 down clears both the
    # printed code (upper band) and the corner badge.
    "IMG-20260818-WA0016.jpg": (0.35, 0.30, 1.00, 0.80),
}


def find_all(src_dir):
    """basename -> absolute path, recursing (the folders are doubly nested)."""
    found = {}
    for root, _dirs, names in os.walk(os.path.join(SRC, src_dir)):
        for n in names:
            if n.lower().endswith(EXTS) and n not in EXCLUDE:
                found[n] = os.path.join(root, n)
    return found


def load(path, crops=CROPS):
    """Open, fix EXIF rotation, and apply this file's crop if it has one."""
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    box = crops.get(os.path.basename(path))
    if box:
        w, h = im.size
        left, top, right, bottom = box
        im = im.crop((int(left * w), int(top * h), int(right * w), int(bottom * h)))
    return im


def contain_fill(im, size, margin=TILE_MARGIN, bg=TILE_BG):
    """Fit the WHOLE image inside `size`, centred, on a flat background.

    The counterpart to ImageOps.fit: that one crops to fill and can cut the
    subject, this one shrinks to fit and pads. Used for TILE_FILL — see the
    comment on that set for why those four cannot simply be cropped wider.
    """
    canvas = Image.new("RGB", size, bg)
    inner = (round(size[0] * (1 - 2 * margin)), round(size[1] * (1 - 2 * margin)))
    fitted = im.copy()
    fitted.thumbnail(inner, Image.LANCZOS)
    canvas.paste(fitted, ((size[0] - fitted.width) // 2,
                          (size[1] - fitted.height) // 2))
    return canvas


def clear_webp(directory):
    os.makedirs(directory, exist_ok=True)
    for stale in os.listdir(directory):
        if stale.endswith(".webp"):
            os.remove(os.path.join(directory, stale))


def build_rails():
    manifest = {}
    total = 0
    for src_dir, slug, order in SETS:
        found = find_all(src_dir)
        named = [found[n] for n in order if n in found]
        rest = [found[n] for n in sorted(found) if n not in set(order)]
        files = named + rest

        missing = [n for n in order if n not in found]
        if missing:
            print(f"  ! {slug}: {len(missing)} name(s) in ORDER not found: {missing[:3]}")

        out_dir = os.path.join(DST, slug)
        clear_webp(out_dir)

        dims = []
        for i, path in enumerate(files, 1):
            im = load(path)
            w, h = im.size
            scale = MAX_EDGE / max(w, h)
            if scale < 1:
                im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
            im.save(os.path.join(out_dir, f"{slug}-{i:02d}.webp"), "WEBP",
                    quality=QUALITY, method=6)
            dims.append(list(im.size))

        manifest[slug] = dims
        total += len(files)
        note = "" if files else "   (no photos yet — rail stays hidden)"
        print(f"{slug:18} {len(files):>3} photos{note}")
    return manifest, total


def build_fixed(mapping, label, size, crops=CROPS, fill=frozenset()):
    """Build the stable-named images (tiles, covers) into TILE_DST.

    `fill` names the slugs that letterbox instead of crop-to-fill.
    """
    built = 0
    for slug, (src_dir, basename) in sorted(mapping.items()):
        found = find_all(src_dir)
        path = found.get(basename)
        if not path:
            print(f"  ! {label} {slug}: source not found — {src_dir}/{basename}")
            continue
        src = load(path, crops)
        im = (contain_fill(src, size) if slug in fill
              else ImageOps.fit(src, size, Image.LANCZOS))
        im.save(os.path.join(TILE_DST, f"{slug}.webp"), "WEBP",
                quality=QUALITY, method=6)
        built += 1
    print(f"{label:18} {built:>3} images  ({size[0]}x{size[1]})")
    return built


def main():
    manifest, total = build_rails()

    clear_webp(TILE_DST)
    build_fixed(TILES, "tiles", TILE_SIZE, fill=TILE_FILL)
    build_fixed(COVERS, "covers", COVER_SIZE, {**CROPS, **COVER_CROPS})

    lines = [
        "// GENERATED by tools/build-boutique-photos.py — do not edit by hand.",
        "// Declares galleryData so boutique.html can reuse the gallery carousel",
        "// code in script.js. Only ever loaded on boutique.html.",
        "const galleryData = {",
    ]
    for _s, slug, _o in SETS:
        pairs = ", ".join(f"[{w},{h}]" for w, h in manifest[slug])
        lines.append(f'  "{slug}": [{pairs}],')
    lines.append("};")
    with open(os.path.join(SITE, "boutique-data.js"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\ntotal {total} rail photos -> wrote boutique-data.js")


if __name__ == "__main__":
    main()
