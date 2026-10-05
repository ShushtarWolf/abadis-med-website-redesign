# Human Review Required

Items that **must not** be decided by automation alone.

## Critical

1. **Approved visual direction** — `concept-preview/` is **REJECTED CONCEPT — VISUAL REFERENCE ONLY**. Obtain a new approved design brief before Nuxt UI build.
2. **Search Console / Analytics** — export indexed URLs, top queries, EN/AR coverage, 404s, and compare to sitemap inventory (EN/AR missing from Yoast sitemaps is a FACT).
3. **Multilingual system** — identify the plugin/custom mechanism that powers `/en/` and `/arabic/`; document translation pairing rules.
4. **www vs non-www** — choose canonical host; EN sample canonical used `www.abadis-med.com`.
5. **Customer (`_customers`) & franchise (`_franchise`) indexability** — keep, noindex, or consolidate after business + SEO review.
6. **Job offers** — which `_joboffers` entries are still active.
7. **Download center files** — confirm every PDF/catalog/certificate URL and whether gated by forms.
8. **Forms & CRM** — map contact, quote, recruitment, WhatsApp destinations and any n8n/CRM webhooks (not fully visible on homepages).
9. **Medical / savings calculator claims** — legal and clinical review of formulas and copy.
10. **Product specifications** — manufacturer-confirmed specs only; do not publish CAD-inferred numbers.
11. **JetEngine/ACF private fields** — authenticated export of meta schema.
12. **Elementor-only content** — pages where meaning exists only in Elementor data.
13. **Analytics/tags** — confirm GA/GTM/Clarity/Ads tags (not seen in sampled homepage HTML).
14. **3D asset ownership** — approve web GLBs vs photography fallbacks before launch dependency.
15. **Hosting cutover window** — Liara + WordPress DNS/TLS plan and rollback owner.

## Review workflow

For each item: owner → evidence link → decision → date → update `URL-MIGRATION-MAP.csv` / master plan.
