# Henna By Neena Website — Handoff Notes

## Vision
Build a polished, premium static landing site for Neena’s henna business that feels high-end but not in-your-face. The site should make it immediately clear that she is an experienced, well-respected artist through subtle credibility signals.

**Do NOT re-add calendar/scheduling UI anywhere — this conversation evolved past that.**

---

## What We Have So Far
- **Working directory:** `~/Desktop/voiding szn 1/Freelance/Henna By Neena/website/`
- **Local brand assets:** `../Real Images/logo.JPG` and `../Real Images/Artist Photo.JPG`
- **Fonts:** Manrope + Playfair Display + Material Symbols Outlined
- **Design language:** warm maroon/amber/champagne palette, compact spacing, subtle credibility signals

---

## Key Requirements (do not override these)

1. **Contact-first flow**
   - Primary CTAs: Call, Text, Email, Instagram
   - Display phone as `(919) 032-0123`
   - Links should use `+19190320123` format (or `+191****0123` if you want to partially redact)

2. **Meet Neena section placement**
   - The original **About / Meet Neena** section is the canonical one. It already contains:
     - Portrait image (`../Real Images/Artist Photo.JPG`)
     - Quote: “I believe henna is a conversation between the skin and the soul...”
     - Bio paragraphs
     - Stats: 25+ Years, 500+ Brides, 4.9 Rating
   - **Move this exact section up** to sit directly after the trust bar (right after `trust-bar`)
   - Do NOT blow up the image, do NOT duplicate the section, do NOT create a new `.meet` section
   - Keep the image’s original aspect ratio — no scaling/gross upscaling

3. **Hero adjustments**
   - Shrink hero vertically
   - Center/streamline content
   - Reduce hero bottom padding and internal line spacing

4. **Trust bar (already added)**
   - Trust items: 25+ Years Experience, 500+ Brides, 4.9 Rating, 100% Organic Henna
   - Very subtle maroon tint, small type, not loud

5. **Film grain + page load fade-in (preferred direction)**
   - Film grain: extremely subtle CSS overlay across entire page, opacity ≤ 0.05
   - Page load fade-in: gentle, ~0.75s ease, no flash of unstyled content (`html { scroll-behavior: smooth; }`)

6. **What we DO NOT want**
   - No “Book Now” / “Book a Consultation” loud CTAs in the nav or hero
   - No calendar UI
   - No aggressive self-promotion
   - No duplicate sections
   - No blown-up/distorted images

---

## What Went Wrong (avoid these mistakes)

1. **Accidental duplication**
   - Instead of moving the existing About section, I created a brand new `.meet` section alongside it. This left two “Meet Neena” blocks on the page.

2. **Orphaned HTML**
   - The `mobile-quick-bar` got detached from its opening `<div>` and left raw `<a>` tags floating near the top of the body. The `index.html` is now structurally broken.

3. **Over-editing**
   - I kept patching after the user said stop. Reverts should have happened immediately on request.

4. **Bad write_file call**
   - A `write_file` to `index.html` was truncated, replacing most of the file with partial content. This made the file much smaller (1.4 KB vs expected ~25+ KB). **If this file is smaller than it should be, assume it is corrupted.**

---

## Current File States (as of last action)

| File | Size | Status |
|---|---|---|
| `index.html` | ~1.4 KB | **Likely broken/truncated.** Needs full rebuild. |
| `styles.css` | ~32 KB | Has hero shrink, trust bar, fade-in keyframes, some grain logic. May have orphaned `.meet` selectors. |
| `script.js` | ~2 KB | Has Swiper init for portfolio + reviews. |

---

## Recommended Approach for Next Model

### Step 1: Decide source of truth
- If you have access to a truly clean prior version of this project, use that as the baseline.
- If not, reconstruct `index.html` from the full content captured in conversation history (we have the complete correct About section text and layout from prior reads).

### Step 2: Reconstruct `index.html`
Restore the canonical structure in this order:
1. `<head>` with meta, fonts, Material Symbols, favicon (`../Real Images/logo.JPG`), stylesheet
2. `<nav>` without “Book Now”
3. `<header class="hero">`: shrunk, centered, with meta chip below headline
4. `<section class="trust-bar">` with 4 items
5. `<section class="about">` — the **existing, proper** Meet Neena section (move it up, do not duplicate)

### Step 3: Fix orphaned markup
- Ensure `mobile-quick-bar` has a proper opening `<div class="mobile-quick-bar">` immediately before the button group, and a closing `</div>` after it.
- Make sure no stray tags sit in the wrong place in the body.

### Step 4: Wire Swiper.js properly (once structure is sound)
- Include Swiper CSS + JS via CDN at the bottom
- Update `.carousel-track` wrappers for portfolio to use `class="swiper portfolio-swiper"` with `swiper-wrapper`/`swiper-slide`
- Keep `loop: true` so looping feels circular
- Add dots + arrow navigation

### Step 5: Polish
- Add the film-grain overlay as a fixed pseudo-element or dedicated div with `pointer-events: none`
- Ensure page load fade-in is gentle and doesn’t flash unstyled content
- Verify responsive behavior across mobile/tablet/desktop

---

## Contact Info (use exactly)
- **Display:** (919) 032-0123
- **Tel link:** `tel:+19190320123`
- **SMS link:** `sms:+19190320123`
- **Email:** `mailto:hello@hennabyneena.com`
- **Instagram:** `https://instagram.com/hennabyneena`

---

## Unresolved from prior session
- True circular seamless loop without any end-snap has proven tricky to hand-code reliably. Swiper.js with `loop: true` is the preferred path.
- Original section-specific promos like “Book Your Ritual” headline in contact section should be replaced with simple “Book Your Ritual” + contact pills — no extra booking UI.

---

*Last good state was before infinite-scroll implementation attempts. All edits after that contributed to broken structure.*
