# Henna by Neena Jain Website — Memory
Updated: 2026-08-31 | LIVE at https://hennabyneenajain.com. Static site, 5 pages. Gallery 7 carousels/108 photos · Boutique 6 rails/84 + 13 tiles.

## Stack
- Static HTML/CSS/JS. No framework, no build step, no backend.
- **Deploy: GitHub Pages, auto-builds from `main`.** A push IS the production deploy. Netlify was dropped 2026-08-05.
- DNS at Cloudflare, **proxy must stay OFF (grey cloud)** or GH Pages can't issue the TLS cert. `CNAME` at repo root holds the bare domain; re-adding the domain in GH Settings→Pages rewrites that file, so `git pull` after.
- Repo: github.com/kjaintech25/hennabyneena-website, `main` only. Jira: KSCRUM-172. Board: `freelance` (FRL).

## Workflow
- **Commit and push straight to `main`.** No branches, no PRs (Kush, 2026-07-21).
- Kush prefers **tight, compact spacing** — default to the smaller end when adding sections.
- **Build tooling lives in `tools/` IN THE REPO**, never a scratchpad (one script was lost that way).
- **Don't start a dev server** (see `~/CLAUDE.md` — 8GB machine). Verify statically, or point the browser at the live URL.

## Status
Site is live and done. Open: **Kush-only** — update the website URL on Neena's Google Business Profile, Instagram and Facebook. Never confirmed; not checkable from here.
(HTTPS enforced ✅ VERIFIED 2026-08-18. Instagram feed ❌ cancelled 2026-08-05, section removed.)

## Key Decisions
- Name is "Henna by Neena Jain". Contact from her Google Business Profile: 825 River Song Place, Cary NC 27519 · (919) 457-2824 · 5.0★/184.
- Pages: `index.html` (hero → trust bar → about → services → reviews) · `gallery.html` · `boutique.html` · `faq.html` (**stain progression FIRST**, then accordion) · `book.html` (nav label "Book Now").
- **boutique.html** = Neena's home clothing/jewelry business. Story → 3 headline cards → 6 rails (Partywear & Bridal 7 · Sarees 19 · Suits & Dresses 17 · **Jewelry** 21 · Blouses 12 · Accessories 8) → 4 filter bubbles + 13 type tiles → CTA. VERIFIED 2026-08-31.
- 🔴 **SUPPLIER WATERMARKS ARE A STANDING CONSTRAINT.** Most accessory/jewelry sources carry a wholesaler "SJNX" badge, a product code, or a **price** (likely wholesale — publishing it shows customers what Neena pays). A mark on the BACKDROP crops away (`CROPS`); a mark ON THE PIECE does not (`EXCLUDE`). No garment photo has any branding. **Rights position is UNRULED** — Kush asked 2026-08-26, no answer.
- Reviews carousel = 13 real Google reviews from an export Kush provided.

## Critical Paths
- `index.html` / `styles.css` / `script.js` — shared core. `--section-padding-mobile|desktop` (20px/32px in `:root`) drive nearly all section spacing sitewide; tune those two, not individual sections.
- `tools/build-gallery.py` → gallery WebPs + the 3 homepage cards + `gallery-data.js`.
- `tools/build-boutique-photos.py` → boutique rails + tiles + covers + `boutique-data.js`. Maps: `SETS` `EXCLUDE` `CROPS` `TILES`/`COVERS` `TILE_FILL`.
- `tools/verify-boutique.mjs` → runs the REAL `script.js` under `node:vm` and prints what it built. **Use it instead of a browser.**
- `tools/set-domain.py https://new.com` → rewrites all 25 absolute URLs.
- 🔴 **COUNTS ARE GENERATED, NOT IN `script.js`** (since 2026-08-18). Rerun the build script; `script.js` needs no edit. Any instruction to "update the `count` values in script.js" is STALE.
- 🔴 **RAIL FILENAMES ARE NUMBERED AND RENUMBER; TILE/CARD FILENAMES ARE SLUG-NAMED AND STABLE.** Never point a tile or a homepage card at `<slug>-NN.webp` — the next rebuild moves it. That defect hit the homepage cards FOUR times; fixed at the root 2026-08-26 by building cards from NAMED sources into `Gallery/cards/`.
- 🔴 **BOX RATIOS DIFFER AND BOTH USE `object-fit: cover`:** `.boutique-tile-media` 3/4, `.service-card-media` 4/3. Build each image at its own ratio (`TILE_SIZE`/`COVER_SIZE`) or a full-length model gets cropped to a midriff.
- Gallery images load on demand (`data-src` + 600px proximity, 3 back/6 ahead). Loading all cost ~385MB of decoded bitmap. Carousels with <8 photos repeat their images — Swiper's loop freezes below ~2x visible slides.

## Dead Ends / Gotchas (Don't Retry)
- ✅ **CAROUSEL SLIDES CROP NOTHING — VERIFIED 2026-08-31.** `.portfolio-swiper .swiper-slide img` is `object-fit: contain`, fixed height, auto width. **"The carousel is cropping my photo" is ALWAYS about the built WebP, never the CSS** — go to `CROPS` in the build script. Same pointer is commented in `styles.css` and `boutique.html`.
- 🔴 **NEVER TIGHTEN A `CROPS` BOX TO MAKE A TILE LOOK BETTER.** `CROPS` clears the watermark for the RAIL and nothing else; tile framing is `TILE_FILL` (4 jewellery tiles letterboxed whole onto `#faf7f1`, so their cream margin is DELIBERATE — don't "fix" it). Tuning `CROPS` for a tile is what shipped four half-cropped Accessories slides. **The build script now prints three guards every run** (letterbox assertion, tile-framing table, shared-crop warning) — read its output, the reasoning is in its comments.
- ⚠️ **`EXCLUDE` matches on BASENAME, so it removes the file from EVERY set.** One photo was byte-identical in two source folders and live twice on the page; one entry removed both. Check before excluding something you only meant to pull from one rail.
- 🔴 **THE PREVIEW BROWSER DOES NOT ADVANCE CSS TRANSITIONS**, and `getComputedStyle` reads the START value forever mid-transition (rAF doesn't fire either). Cost a wrong diagnosis and a full accordion rewrite that had to be reverted. **Inject `* { transition: none !important }` before measuring.** The grid `0fr→1fr` technique is FINE — don't "fix" it again.
- ⚠️ **The preview browser cannot scroll** (`scrollY` stays 0), so below-the-fold behaviour can't be screenshotted. Layout numbers from it are trustworthy; scroll-dependent behaviour is not. It also serves stale CSS/JS — cache-bust with `?v=` while verifying.
- 🔴 **NO GLOBAL `box-sizing: border-box` RESET IN THIS STYLESHEET.** Percentage widths resolve against the CONTENT box, so padding/border add on top — a `calc(33.333% - 12px)` flex-basis silently became 2-across. Scope `border-box` to the component; don't add a global reset this late.
- **Three separate things silently break `position: sticky`/`fixed` here:** `overflow-x: hidden` on `html`/`body` (use `clip`), any leftover `transform` on an ancestor (keep entrance animations opacity-only), and a multi-row grid item without `align-self: start`.
- Native `img loading="lazy"` inside a Swiper slide never fires — Swiper's transforms confuse the "near viewport" heuristic (confirmed on the live deploy). Swiper already manages what renders.
- The hero scroll chevron was reported off-centre more than once; measured centred at 375/1440/1920 on local AND live. Don't re-investigate without new evidence — get the reporter's browser/OS first.
