# Abadis Med — Migration Risks

Every risk is classified. Do not treat inferences as facts.

| ID | Risk | Class | Impact | Likelihood | Mitigation |
|---|---|---|---|---|---|
| R1 | English/Arabic URLs absent from Yoast sitemaps | FACT | High SEO under-discovery for EN/AR | Observed | Inventory all EN/AR URLs via crawl + Search Console; generate correct multilingual sitemaps in Nuxt |
| R2 | Arabic homepage `lang="fa-IR"`, weak robots/schema | FACT | Wrong language signals, thin SEO | Observed | Fix language metadata; human QA of Arabic templates |
| R3 | No `hreflang` on sampled language roots | FACT | Duplicate/wrong-language ranking risk | Observed | Build reciprocal hreflang map only for verified translation pairs |
| R4 | Content trapped in Elementor JSON | INFERENCE | Incomplete headless content | High | Diff `post_content` vs Elementor data; migrate critical fields to CPT/meta |
| R5 | JetEngine meta not in public REST (`acf: []`) | FACT (public empty) | Missing specs/downloads fields | Medium | Authenticated REST or WP admin export; map fields before Nuxt product pages |
| R6 | Customer/franchise archives indexed | FACT (Yoast robots index on samples) | Thin/doorway-like SEO risk **or** valuable local proof | Medium | HUMAN REVIEW with Search Console before noindex/consolidate |
| R7 | Breaking `/wp-content/uploads` URLs | INFERENCE | Mass 404s, lost PDF/certs | High | Preserve upload URLs at launch |
| R8 | Rejected concept treated as approved design | Process | Wasted build / client rejection | Medium | Label `concept-preview` as REJECTED REFERENCE ONLY |
| R9 | Forms/CRM wiring unknown from public HTML | UNKNOWN | Lost leads after cutover | Medium | Inventory all forms on contact/jobs/download pages manually |
| R10 | 3D GLB too heavy (local AMR source ~60MB) | FACT (local files) | Poor mobile CWV | High | Ship compressed web GLB (`AMR_4894-web.glb` ~450KB class) + poster fallback |
| R11 | www vs non-www inconsistency (`en` canonical on www) | FACT (EN sample) | Duplicate host signals | Medium | Pick one host; 301 the other; align canonicals |
| R12 | Intermittent TLS/HTTP2 failures during audit | FACT (auditor) | Incomplete crawl / flaky CI audits | Medium | HTTP/1.1 + retries in n8n; verify from Liara region |
| R13 | Accidental DELETE of old URLs | Process | SEO/business loss | Medium | Actions limited to PRESERVE/REBUILD/REDIRECT/MERGE/ARCHIVE/REVIEW — never auto-DELETE |
| R14 | Calculator / medical claims without sources | INFERENCE from brief | Legal/trust risk | Medium | Transparent formulas; legal review |
| R15 | Launch without redirect verification | Process | Traffic loss | High | Automated redirect test matrix before DNS cutover |

## Rollback

1. Keep WordPress theme capable of serving the site until Nuxt is proven.  
2. Cutover via reverse proxy/DNS switch that can revert in minutes.  
3. Do not delete Elementor content until Nuxt parity signed off.  
4. Retain redirect map versioned in git.
