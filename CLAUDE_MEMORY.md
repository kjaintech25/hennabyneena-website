# Henna by Neena Jain Website — Memory
Updated: 2026-07-19 | Rebrand, multi-page split, and mobile fixes shipped (commit f08e44a)

## Stack
- Frontend: Static HTML/CSS/JS, no build step, no framework
- Backend: None
- Deploy: Not yet hosted — KSCRUM-165 still open

## Status
Multi-page site (index/faq/stain-progression) with rebrand, real contact
info, and mobile fixes complete, pushed to feat/ui-polish-pass; not live yet.

## Next Steps
1. KSCRUM-165: buy domain + host (Vercel/Netlify)
2. KSCRUM-163: add real stain-progression photos once Neena sends them
3. KSCRUM-164: Instagram feed — Basic Display API is dead, needs embed widget

## Key Decisions
- Real name is "Henna by Neena Jain" (was just "Henna by Neena")
- Contact info confirmed via her real Google Business Profile: 825 River
  Song Place, Cary, NC 27519 | (919) 457-2824 | 5.0★, 184 reviews
- Reviews are real but only 3 of 10-15 — Google gates the rest behind sign-in

## Critical Paths
- index.html/styles.css/script.js: shared core, homepage
- faq.html, stain-progression.html: split off homepage (KSCRUM-170)
- Repo: github.com/kjaintech25/hennabyneena-website, branch feat/ui-polish-pass
- Jira: KSCRUM board, parent epic KSCRUM-1

## Dead Ends (Don't Retry)
- Instagram Basic Display API — dead since end of 2024
- Scraping >3 Google reviews via browser — gated behind sign-in
