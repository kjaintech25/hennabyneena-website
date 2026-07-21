# Henna by Neena Jain Website — Memory
Updated: 2026-07-21 | Real content complete (gallery, reviews, stain progression), deployed to GitHub Pages, layout tightened sitewide

## Stack
- Frontend: Static HTML/CSS/JS, no build step, no framework
- Backend: None
- Deploy: Live on GitHub Pages (`kjaintech25.github.io/hennabyneena-website`), auto-builds from `main`. Final home will be Netlify + a custom domain once Kush buys one (KSCRUM-190) — GH Pages is just the interim preview.

## Workflow
- **Commit and push directly to `main`.** No feature branches, no PRs — Kush asked to drop that workflow (2026-07-21) since this is a solo repo with no CI gating.
- Browser-preview cache is unreliable mid-session (stale CSS/JS survives reloads) — cache-bust with a `?v=` query string on the `<link>`/`<script>` tag when verifying a change, then remove it before committing.
- The browser preview tool itself is flaky this environment: `navigate()` on an already-open tab frequently no-ops silently (check `location.href` after navigating — if it didn't move, open a fresh tab with `tabs_create` instead), and `screenshot` intermittently returns a blank frame even when the page is fine. Don't trust either as the sole source of truth — verify layout/content changes with direct DOM inspection (`getBoundingClientRect`, `getComputedStyle`, real network request logs) and treat screenshots as a secondary sanity check, not primary evidence.
- Kush prefers **tight, compact spacing** over generous/airy whitespace as a general design taste for this site — when adding new sections, default to the smaller end of spacing rather than assuming a template's default padding is fine.

## Status — KSCRUM-172 (parent ticket)
Done: KSCRUM-175 (gallery images), KSCRUM-176 (Google reviews), KSCRUM-187 (FAQ accordion), KSCRUM-188 (stain progression photos).
Open:
1. **KSCRUM-189** Instagram feed — blocked on Kush setting up a widget account (SnapWidget/Elfsight/Behold.so, since Basic Display API is dead) and connecting `@henna.neena.jain`; he's coordinating the login/setup with his mom (Neena, the account owner).
2. **KSCRUM-190** Hosting — Kush is buying a domain and hosting on **Netlify** (decided over Vercel).

## Key Decisions
- Real name is "Henna by Neena Jain" (was just "Henna by Neena")
- Contact info via her real Google Business Profile: 825 River Song Place, Cary, NC 27519 | (919) 457-2824 | 5.0★, 184 reviews
- Reviews carousel has 13 real reviews (sourced from a Google Reviews export Kush provided, not scraping)
- Site structure: index.html (home), gallery.html, faq.html (FAQ + Stain Progression), book.html (all contact/booking info — split out from the homepage Contact section)
- Instagram feed section lives on the homepage under Client Reviews, not on the Gallery page

## Critical Paths
- index.html/styles.css/script.js: shared core
- book.html: contact/booking page (nav tab is "Book Now", not "Contact")
- faq.html: page order is **Stain Progression carousel first** (right under the intro), then FAQ accordion, then CTA — deliberately reordered from the original FAQ-first layout
- Section rhythm: `--section-padding-mobile`/`--section-padding-desktop` (in `:root`) are 20px/32px and drive nearly all section-to-section spacing sitewide — tune these two variables rather than patching individual section padding when adjusting overall page density
- Repo: github.com/kjaintech25/hennabyneena-website, branch `main` only
- Jira: KSCRUM board, parent epic KSCRUM-1 → KSCRUM-172 (this site)

## Dead Ends / Gotchas (Don't Retry)
- Instagram Basic Display API — dead since end of 2024, must use a third-party embed widget
- Scraping >3 Google reviews via browser — gated behind sign-in (resolved instead via a docx export Kush provided)
- `overflow-x: hidden` on `html`/`body` forces `overflow-y` to compute as `auto` per spec, which silently breaks `position: sticky`/`fixed` for all descendants (the "fixed" nav was actually scrolling away with the page for who knows how long before this was caught). Fixed by using `overflow-x: clip` instead.
- A CSS `transform` left on an ancestor after an animation finishes (even a no-op `translateY(0)`, via `animation-fill-mode: both`) creates a new containing block that also breaks `position: sticky`/`fixed` on descendants. Keep entrance animations to opacity-only if anything downstream needs sticky/fixed positioning.
- `position: sticky` on a CSS Grid item that spans multiple rows needs `align-self: start` (not the default `stretch`) to actually stick in this environment — stretch silently no-ops it.
- Native `img loading="lazy"` inside a Swiper carousel is unreliable — Swiper's transform-based slide positioning confuses the browser's "near viewport" heuristic, so images can just never fire their fetch on a normal page visit (confirmed on the live deploy, not a cache artifact). Don't use `loading="lazy"` on images inside `.swiper-slide`; Swiper already manages what's rendered.
- The hero's scroll-down chevron (`.scroll-indicator`) was reported as visually off-center more than once — verified via `getBoundingClientRect` math at 375px/1440px/1920px widths, on both local and the live deploy: it's centered exactly relative to `.hero`'s own box every time. Don't re-investigate this as a CSS bug without new evidence; if it recurs, get the reporter's exact browser/OS first.
