# Henna by Neena Jain Website — Memory
Updated: 2026-08-18 | LIVE at https://hennabyneenajain.com. 5 pages incl. Boutique. Gallery = 7 carousels / 108 photos. Boutique = 3 photo rails (39) + 15 type tiles.

## Stack
- Frontend: Static HTML/CSS/JS, no build step, no framework
- Backend: None
- Deploy: **GitHub Pages at https://hennabyneenajain.com**, auto-builds from `main`. Netlify was dropped (2026-08-05) — GH Pages is the permanent home.
- Domain registered at Cloudflare; Cloudflare is DNS-only (4 A records to GitHub's IPs + `www` CNAME). **Proxy must stay OFF (grey cloud)** or GitHub can't issue the TLS cert.
- `CNAME` file at repo root holds the bare domain. Removing/re-adding the domain in GitHub Settings→Pages deletes and recreates that file — `git pull` afterwards or the next push conflicts.

## Workflow
- **Commit and push directly to `main`.** No feature branches, no PRs — Kush asked to drop that workflow (2026-07-21) since this is a solo repo with no CI gating.
- Browser-preview cache is unreliable mid-session (stale CSS/JS survives reloads) — cache-bust with a `?v=` query string on the `<link>`/`<script>` tag when verifying a change, then remove it before committing.
- The browser preview tool itself is flaky this environment: `navigate()` on an already-open tab frequently no-ops silently (check `location.href` after navigating — if it didn't move, open a fresh tab with `tabs_create` instead), and `screenshot` intermittently returns a blank frame even when the page is fine. Don't trust either as the sole source of truth — verify layout/content changes with direct DOM inspection (`getBoundingClientRect`, `getComputedStyle`, real network request logs) and treat screenshots as a secondary sanity check, not primary evidence.
- Kush prefers **tight, compact spacing** over generous/airy whitespace as a general design taste for this site — when adding new sections, default to the smaller end of spacing rather than assuming a template's default padding is fine.

## Status — KSCRUM-172 (parent ticket)
Done: KSCRUM-175 (gallery images), KSCRUM-176 (Google reviews), KSCRUM-187 (FAQ accordion), KSCRUM-188 (stain progression photos).
Open:
1. **KSCRUM-189** Instagram feed — **cancelled** (2026-08-05). The placeholder section was removed from the homepage entirely; Kush didn't want to wait on a third-party widget. Profile links remain in the footer/book page.
2. **KSCRUM-190** Hosting — **done**. Live on GH Pages + hennabyneenajain.com.
3. **Enforce HTTPS — DONE.** VERIFIED 2026-08-18: `curl -o /dev/null -w '%{http_code} %{redirect_url}' http://hennabyneenajain.com` → `301 https://hennabyneenajain.com/`. Re-verify, don't re-derive.
4. STILL OPEN (Kush-only, never confirmed done): update the website URL on Neena's **Google Business Profile, Instagram and Facebook**. HYPOTHESIS — not checkable from here.

## Key Decisions
- Real name is "Henna by Neena Jain" (was just "Henna by Neena")
- Contact info via her real Google Business Profile: 825 River Song Place, Cary, NC 27519 | (919) 457-2824 | 5.0★, 184 reviews
- Reviews carousel has 13 real reviews (sourced from a Google Reviews export Kush provided, not scraping)
- Site structure: index.html (home), gallery.html, faq.html (FAQ + Stain Progression), book.html (all contact/booking info — split out from the homepage Contact section)
- Homepage order: hero → trust bar → about → services (+ "View the Full Gallery" CTA above the cards) → reviews → footer
- Gallery is **7 carousels, 108 photos** — VERIFIED 2026-08-18 from gallery-data.js: Bridal 15 · Feet 15 · Stylish 16 · Party 17 · Event Guest 11 · Family 14 · Jagua 20. **White Henna was dropped**; the earlier "8 carousels / 121 photos incl. White 4" line was stale.
- **boutique.html** (nav tab "Boutique"): Neena's home-based Indian clothing/jewelry business. Order: story write-up (4 paras, 2-column ≥900px) → 3 headline cards → 3 photo rails (Partywear & Bridal 9 · Suits & Dresses 18 · Blouses 12) → 4 filter bubbles (All/Clothing/Jewelry/Accessories) + 15 type tiles → CTA.
- Boutique **Jewelry and Accessories rails exist but are EMPTY and auto-hidden** — script.js hides any `.gallery-collection` whose manifest entry is `[]`. Drop photos in `../Boutique Photos/Jewelry` (or `/Accessories`), rerun `tools/build-boutique-photos.py`, and they appear.
- The 15 boutique type tiles are still **decorative mandala placeholders**, now sitting directly below 39 real garment photos. Kush has been told they will start reading as "images missing" — next candidate for real photos.

## Critical Paths
- index.html/styles.css/script.js: shared core
- book.html: contact/booking page (nav tab is "Book Now", not "Contact")
- faq.html: page order is **Stain Progression carousel first** (right under the intro), then FAQ accordion, then CTA — deliberately reordered from the original FAQ-first layout
- Section rhythm: `--section-padding-mobile`/`--section-padding-desktop` (in `:root`) are 20px/32px and drive nearly all section-to-section spacing sitewide — tune these two variables rather than patching individual section padding when adjusting overall page density
- **Build tooling lives in `tools/` IN THE REPO** — never in a scratchpad. (2026-08-18: `build-gallery.py` was kept in the session scratchpad, got wiped between sessions, and had to be reconstructed from memory. It is committed now; keep it that way.)
  · `tools/build-gallery.py` → gallery WebPs + `gallery-data.js`
  · `tools/build-boutique-photos.py` → boutique rail WebPs + `boutique-data.js`
  · `tools/build-boutique-placeholders.py` → the mandala SVG placeholders
  · `tools/set-domain.py https://new.com` → rewrites all 25 absolute URLs
- 🔴 **COUNTS ARE NO LONGER IN script.js** (changed 2026-08-18). `gallery-data.js` / `boutique-data.js` are GENERATED and carry both the per-photo pixel sizes and the counts. Rerun the build script; script.js needs no edit. Any instruction saying "update the `count` values in script.js" is STALE.
- 🔴 **BUT the 3 homepage service-card image refs are STILL hardcoded and renumbering still moves them.** `index.html` points at `bridal-02.webp`, `party-07.webp`, `jagua-09.webp`. This broke THREE times in one session (jagua-10→11 when photos were added, jagua-16→09 when photos were removed, bridal-05→02 when feet split out). After ANY rebuild, open index.html and confirm each card still shows the photo you expect.
- `tools/set-domain.py https://newdomain.com` rewrites all 25 absolute URLs (canonical, OG, schema, sitemap, robots) if the domain ever changes.
- Gallery images load on demand: `data-src` + a 600px proximity check, 3 slides behind / 6 ahead. Loading all of them at once cost ~385MB of decoded bitmap and made scrolling crawl.
- Carousels with fewer than 8 photos repeat their images (aria-hidden) — Swiper's loop silently freezes below ~2x the visible slides.
- Repo: github.com/kjaintech25/hennabyneena-website, branch `main` only
- Jira: KSCRUM board, parent epic KSCRUM-1 → KSCRUM-172 (this site)

## Dead Ends / Gotchas (Don't Retry)
- 🔴 **THE PREVIEW BROWSER DOES NOT ADVANCE CSS TRANSITIONS, AND `getComputedStyle` LIES MID-TRANSITION.** Symptom: an element's inline style reads `0px` while its computed value sits at `601px` forever; a panel that should expand measures 0. Cause: transitions never tick in this pane (rAF doesn't fire either), so a transitioning property is stuck at its START value. (2026-08-18 — cost a wrong diagnosis, a full rewrite of both FAQ accordions from `0fr→1fr` grid onto `max-height`, and a revert when the real cause surfaced.) **Fix: inject `* { transition: none !important }` before measuring, and read the settled end state.** The grid `0fr→1fr` technique is FINE — do not "fix" it again.
- 🔴 **THIS STYLESHEET HAS NO GLOBAL `box-sizing: border-box` RESET.** Percentage widths resolve against the CONTENT box, so padding + border are added on top. A `flex-basis: calc(33.333% - 12px)` came out ~50px wider than intended per item and silently forced 2-across instead of 3. (2026-08-18.) Scope `box-sizing: border-box` onto the component you're sizing; do NOT add a global reset this late without checking the whole site.
- ⚠️ **The preview browser cannot scroll** — `window.scrollTo` / `scrollIntoView` leave `scrollY` at 0, so anything below the fold can't be screenshotted or interaction-tested. To verify off-screen behaviour, stub `getBoundingClientRect` on the element to simulate its position and call the handler directly. Layout numbers from that pane are still trustworthy; scroll-dependent behaviour is not.
- ⚠️ **macOS/iCloud resurrects `"whatever 2.webp"` copies while a script rewrites files in place.** 28 appeared during one conversion run, untracked and unreferenced. `.gitignore` now carries `* 2.*` / `* 3.*`. If a count looks too high, check for them before believing it.
- Instagram Basic Display API — dead since end of 2024, must use a third-party embed widget
- Scraping >3 Google reviews via browser — gated behind sign-in (resolved instead via a docx export Kush provided)
- `overflow-x: hidden` on `html`/`body` forces `overflow-y` to compute as `auto` per spec, which silently breaks `position: sticky`/`fixed` for all descendants (the "fixed" nav was actually scrolling away with the page for who knows how long before this was caught). Fixed by using `overflow-x: clip` instead.
- A CSS `transform` left on an ancestor after an animation finishes (even a no-op `translateY(0)`, via `animation-fill-mode: both`) creates a new containing block that also breaks `position: sticky`/`fixed` on descendants. Keep entrance animations to opacity-only if anything downstream needs sticky/fixed positioning.
- `position: sticky` on a CSS Grid item that spans multiple rows needs `align-self: start` (not the default `stretch`) to actually stick in this environment — stretch silently no-ops it.
- Native `img loading="lazy"` inside a Swiper carousel is unreliable — Swiper's transform-based slide positioning confuses the browser's "near viewport" heuristic, so images can just never fire their fetch on a normal page visit (confirmed on the live deploy, not a cache artifact). Don't use `loading="lazy"` on images inside `.swiper-slide`; Swiper already manages what's rendered.
- The hero's scroll-down chevron (`.scroll-indicator`) was reported as visually off-center more than once — verified via `getBoundingClientRect` math at 375px/1440px/1920px widths, on both local and the live deploy: it's centered exactly relative to `.hero`'s own box every time. Don't re-investigate this as a CSS bug without new evidence; if it recurs, get the reporter's exact browser/OS first.
