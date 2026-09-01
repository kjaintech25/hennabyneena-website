# Memory Archive — Henna by Neena Jain Website

Not auto-loaded. Historical reference only — everything here was true when
written and was moved out of `CLAUDE_MEMORY.md` to keep session-start context
small. Check it against the code before acting on it.

## Archived 2026-08-31
Compressed CLAUDE_MEMORY.md from 82 lines / 17.7KB to 47 lines / 6.9KB.
Most of what follows is now enforced or documented closer to the code — in
`tools/build-boutique-photos.py`, `styles.css` or `boutique.html` — which is
why it no longer needs to load every session.

### Key Decisions
- 🟢 **THE MANDALA TILES ARE GONE (2026-08-26).** 13 of the 15 type tiles now carry a real photo, as do the 3 headline cards. **"Ring Bracelets" and "Anklets" were REMOVED, not faked** — no publishable photo exists for either, and one drawing among twelve photographs reads as a broken image. Restoring one is two lines: a `TILES` entry in the build script + a `boutiqueItems` entry in script.js. Both carry a ⚠️ comment naming the other.
  · The mandala SVGs are NOT deleted — `Real Images/Boutique/placeholders/` still holds all 18 and `isArtwork()` still special-cases that path. Nothing references them; they stay as the fallback.
- ⚠️ **`IMG-20260818-WA0043.jpg` is the proof that "crop to the clean piece" is not always available.** Kush ruled "crop to one clean earring"; that frame COULD NOT comply and is in `EXCLUDE` with the measurement written out. Two overlapping earrings, a badge on one, and a corner badge occupying exactly the headroom the good one needs. Don't retry it — get a new photo.
- ✅ **THE CROP/TILE COUPLING IS NOW GUARDED MECHANICALLY, NOT JUST DOCUMENTED — every run of `build-boutique-photos.py` prints three things.** A written rule binds nobody; these fire whether or not anyone read the comments.
  1. `fill tiles N verified letterboxed onto (250,247,241)` — asserts each `TILE_FILL` tile really has cream corners. **PROVEN by revert/restore 2026-08-31:** dropping `fill=TILE_FILL` from the build call made all four fail loudly; restoring it went green. ⚠️ Compared with a ±4 tolerance because WebP is lossy — an exact match fails on every tile.
  2. `tile framing` table — what crop-to-fill would discard per tile, marking the letterboxed ones. **A TABLE, not a threshold, on purpose:** filled tiles keep 62/68/76/87%, but `blouses` keeps 77% and `rings` 82% and both are fine cropped — no cutoff reproduces the membership, and a tuned one cries wolf every run. Low keep-% + no FILL marker = the shape of the bug.
  3. `⚠️ CROPS boxes shared by a rail and a crop-to-fill tile` — currently `rings` and `semi-precious`. Legitimate today; they are the two places the bug could come back.
- An empty rail auto-hides: script.js hides any `.gallery-collection` whose manifest entry is `[]`, so a set with no photos never shows a headed carousel with nothing in it. Drop photos in `../Boutique Photos/<Set>` (any nesting — os.walk recurses) and rerun `tools/build-boutique-photos.py`.
- 🔴 **RAIL CROPS AND TILE CROPS ARE NOW SEPARATE, AND THE BUG THAT FORCED THE SPLIT IS THE ONE TO REMEMBER.** `CROPS` boxes had been tuned to fill the 3/4 TILE box; the rails reuse the same file, so four Accessories slides were shipping half a piece. `CROPS` now does ONE job — clear the watermark, as loose as possible — and tile framing lives in `TILE_FILL`. **Never re-tighten a `CROPS` box to make a tile look better.** (Kush spotted it 2026-08-31.)
- 🔴 **`TILE_FILL` = the four jewellery tiles that LETTERBOX instead of crop-to-fill** (oxidized, gold-plated, bangles-kadas, earrings). They are wide/square shots in a 3/4 portrait box, and `ImageOps.fit` sliced the sides off; widening `CROPS` was not available because each has a code hard against the frame. They fit whole onto `TILE_BG` (`#faf7f1` = `--color-surface`, so no visible edge on the cream page). Kush chose flat cream over a blurred fill, 2026-08-31.

### Critical Paths
- ✅ **THE HOMEPAGE SERVICE-CARD BUG IS FIXED AT THE ROOT (2026-08-26, FRL-009). THE OLD RULE — "after ANY rebuild, open index.html and confirm each card" — IS RETIRED; do not reinstate it.** `index.html` now points at `Real Images/Gallery/cards/card-{bridal,stylish,jagua}.webp`, built by `build-gallery.py`'s `CARDS` map from NAMED source files. PROVEN by revert/restore: a photo was added to `bridalhenna/` forcing a renumber — `card-bridal.webp` md5 was IDENTICAL before and after, while `bridal-02.webp` md5 CHANGED. The old approach silently swapped the photo; the new one cannot.
  ⚠️ It had bitten FOUR times (jagua-10→11 on an add, jagua-16→09 on a removal, bridal-05→02 when feet split out, party-07 stranded on a renamed card). **Never point a card back at a `<slug>-NN.webp` path.**
  🔴 **CARDS BUILD AT 4/3, BOUTIQUE TILES AT 3/4** — `.service-card-media` vs `.boutique-tile-media`, both `object-fit: cover`. Mixing them centre-crops a full-length model to a midriff.
  · `tools/build-boutique-placeholders.py` → the mandala SVG placeholders

### Dead Ends
- Instagram Basic Display API — dead since end of 2024, must use a third-party embed widget
- Scraping >3 Google reviews via browser — gated behind sign-in (resolved instead via a docx export Kush provided)
- ⚠️ **macOS/iCloud resurrects `"whatever 2.webp"` copies while a script rewrites files in place.** 28 appeared during one conversion run, untracked and unreferenced. `.gitignore` now carries `* 2.*` / `* 3.*`. If a count looks too high, check for them before believing it.
