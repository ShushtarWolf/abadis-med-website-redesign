# Abadis — Multilingual URL & Translation-Pair Inventory

**Investigation date:** 2026-09-25  
**Scope:** EN/AR discoverable URLs, FA equivalents, linking mechanism, hreflang, language switcher, gaps.  
**Sources used:** existing audit pack + live public HTTP/REST (read-only).  
**Not modified:** live site, application code, existing audit files.  
**Search Console:** no GSC export or connection found in this project (**S1** remains open).

Classification used below: **FACT** / **INFERENCE** / **Not verified**.

---

## 1. Language architecture

### URL roots (FACT)

| Language | Public root | Primary host observed |
|---|---|---|
| Persian (FA) | `https://abadis-med.com/` | non-www |
| English (EN) | `https://www.abadis-med.com/en/` (also reachable via `https://abadis-med.com/en/` → redirects to www) | **www** |
| Arabic (AR) | `https://abadis-med.com/arabic/` | non-www |

Evidence: live REST `link` fields; product crawl redirects (`abadis-med.com/en/...` → `www.abadis-med.com/en/...`); `docs/abadis/SEO-AUDIT.csv`; `audit-raw/live/api/en_.body`, `arabic_.body`, `home.html`.

### Implementation model (FACT)

FA, EN, and AR are **three separate WordPress frontends/installs** (subdirectory trees), each with its own:

- `wp-json` root (`/wp-json/`, `/en/wp-json/`, `/arabic/wp-json/`)
- `wp-content` / uploads path under that prefix
- independent page/post IDs (e.g. home FA `id=6`, EN `id=1214`, AR `id=266`)

Evidence: REST page payloads and asset URLs in `audit-raw/live/api/en_.body` / `arabic_.body` / `home.html`; live namespace lists (2026-09-25).

### Not WPML / Polylang / TranslatePress (FACT of public API)

Public `namespaces` on all three roots contain **no** `wpml`, `pll`, or translatepress-style routes.

| Install | Notable namespaces |
|---|---|
| FA | `yoast/v1`, `elementor/*`, `jet-engine/v2`, `jet-menu-api/v2`, `jet-reviews-api/v1`, … |
| EN | `yoast/v1`, Elementor/Jet stack, … |
| AR | Elementor/Jet stack; **`yoast/v1` absent** |

### Sitemap discovery asymmetry (FACT)

| Locale | Sitemap index | Notes |
|---|---|---|
| FA | `https://abadis-med.com/sitemap_index.xml` | Present; child locs are Persian paths only (prior audit) |
| EN | `https://www.abadis-med.com/en/sitemap_index.xml` | Present (Yoast); page + post child sitemaps work |
| AR | `https://abadis-med.com/arabic/sitemap_index.xml` | Returns **HTML** (soft failure / not a sitemap); `robots.txt` similarly HTML |

This explains why the FA-centric audit URL map almost entirely misses EN/AR.

### Products (FACT)

Products are **WordPress pages** (often children of a Products page), not a shared multilingual product CPT across locales.

---

## 2. URL inventory

### Counts (live REST / sitemaps, 2026-09-25)

| Language | Pages (REST) | Posts (REST / sitemap) | In FA Yoast child sitemaps? |
|---|---:|---:|---|
| FA | 26 | 221 (prior audit `X-WP-Total`) | Yes (FA URLs) |
| EN | 31 | 84 (`en/post-sitemap.xml`) | No |
| AR | 19 | 28 | No |

### Core page / product pairs (semantic)

Confidence = editorial/nav equivalence strength. **Possible Translation URL** is hypothesized from nav/role, **not** from a WP translation ID.

| Language | URL | Content Type | Title | Possible Translation URL | Confidence | Evidence |
|---|---|---|---|---|---|---|
| FA | `https://abadis-med.com/` | page / home | صفحه اصلی | EN `/en/`; AR `/arabic/` | high | REST pages; switcher links |
| EN | `https://www.abadis-med.com/en/` | page / home | Home | FA `/`; AR `/arabic/` | high | REST; EN page-sitemap |
| AR | `https://abadis-med.com/arabic/` | page / home | صفحه اصلی | FA `/`; EN `/en/` | high | REST; AR HTML |
| FA | `…/درباره-ما/` | page | درباره ما | EN `…/en/about-us/`; AR `…/arabic/من-نحن/` | high | REST + menus |
| EN | `…/en/about-us/` | page | About us | FA/AR above | high | REST; EN sitemap |
| AR | `…/arabic/من-نحن/` | page | من نحن | FA/EN above | high | REST; AR menu |
| FA | `…/محصولات/` | page | محصولات | EN `…/en/products/`; AR `…/arabic/منتجات/` | high | REST + menus |
| EN | `…/en/products/` | page | Products | FA/AR above | high | REST |
| AR | `…/arabic/منتجات/` | page | منتجات | FA/EN above | high | REST |
| FA | `…/محصولات/کیسه-ساکشن/` | product page | کیسه ساکشن | EN `…/en/products/suction-bag/`; AR `…/arabic/كيس-الشفط/` | high | REST; HTTP 200; menus |
| EN | `…/en/products/suction-bag/` | product page | Suction Bag | FA/AR above | high | REST; EN sitemap; live 200 |
| AR | `…/arabic/كيس-الشفط/` | product page | كيس الشفط | FA/EN above | high | REST; live 200 |
| FA | `…/محصولات/پایه/` | product page | پایه و نگهدارنده ها | EN `…/en/products/base-and-holder/`; AR `…/arabic/تثبیت/` | high | REST + menus |
| EN | `…/en/products/base-and-holder/` | product page | Base and Holder | FA/AR above | high | REST |
| AR | `…/arabic/تثبیت/` | product page | تثبیت | FA/EN above | medium–high | REST + AR menu label |
| FA | `…/محصولات/فیلترها/` | product page | فیلترها | EN `…/en/products/filters/`; AR `…/arabic/الفلتر/` | high | REST + menus |
| EN | `…/en/products/filters/` | product page | Filters | FA/AR above | high | REST |
| AR | `…/arabic/الفلتر/` | product page | الفلتر | FA/EN above | high | REST |
| FA | `…/محصولات/مخزن/` | product page | مخزن | EN `…/en/products/canisters/`; AR `…/arabic/خزانات/` | high | REST + menus |
| EN | `…/en/products/canisters/` | product page | Canisters | FA/AR above | high | REST |
| AR | `…/arabic/خزانات/` | product page | خزانات | FA/EN above | high | REST |
| FA | `…/محصولات/اتصالات/` | product page | اتصالات | EN `…/en/products/connections/`; AR `…/arabic/الوصلات/` | high | REST + menus |
| EN | `…/en/products/connections/` | product page | Connections | FA/AR above | high | REST |
| AR | `…/arabic/الوصلات/` | product page | الوصلات | FA/EN above | high | REST |
| FA | `…/محصولات/سایر-محصولات/` | product page | سایر محصولات | EN `…/en/products/other-products/`; AR `…/arabic/منتجات-اخری/` | high | REST + menus |
| EN | `…/en/products/other-products/` | product page | Other Products | FA/AR above | high | REST |
| AR | `…/arabic/منتجات-اخری/` | product page | منتجات اخری | FA/EN above | high | REST |
| FA | `…/محصولات/ساکشن-تیوب/` | product page | ساکشن تیوب | EN `…/en/suction-tube/` (not under `/products/`); AR `…/arabic/أنبوب-الشفط/` | medium–high | REST; path shape differs on EN |
| EN | `…/en/suction-tube/` | product page | Suction Tube | FA/AR above | medium–high | REST; EN sitemap |
| AR | `…/arabic/أنبوب-الشفط/` | product page | أنبوب الشفط | FA/EN above | high | REST |
| FA | `…/محاسبه-گر/` | page / tool | محاسبه گر | EN `…/en/calculator/`; AR `…/arabic/الحوسبة/` (+ also AR `…/الحاسبة/`) | medium | REST; AR has **two** calculator-like pages |
| EN | `…/en/calculator/` | page / tool | calculator | FA/AR above | medium | REST; also EN `reservoir-calculator` |
| AR | `…/arabic/الحوسبة/` | page / tool | الحوسبة | FA `محاسبه-گر` | medium | REST; live 200 |
| AR | `…/arabic/الحاسبة/` | page / tool | الحاسبة | unclear vs `الحوسبة` | low | REST only; relationship **Not verified** |
| FA | `…/ارتباط-با-ما/` | page | ارتباط با ما | EN `…/en/contact-us/`; AR `…/arabic/اتصل-بنا/` | high | REST |
| EN | `…/en/contact-us/` | page | Contact Us | FA/AR | high | REST |
| AR | `…/arabic/اتصل-بنا/` | page | اتصل بنا | FA/EN | high | REST |
| FA | `…/پرسش-های-متداول/` | page | پرسش های متداول | EN `…/en/faqs/`; AR `…/arabic/پرسش-های-متداول/` (Persian slug on AR) | high | REST |
| EN | `…/en/faqs/` | page | FAQs | FA/AR | high | REST |
| AR | `…/arabic/پرسش-های-متداول/` | page | پرسش های متداول | FA/EN | high | REST (slug not Arabic) |
| FA | `…/راهنمای-نصب/` | page | راهنمای نصب | EN `…/en/installation-manual/`; AR `…/arabic/دليل-التركيب/` | high | REST |
| EN | `…/en/installation-manual/` | page | Installation Manual | FA/AR | high | REST |
| AR | `…/arabic/دليل-التركيب/` | page | دليل التركيب | FA/EN | high | REST |
| FA | `…/لیست-نمایندگان/` | page | لیست نمایندگان | EN `…/en/representatives/`; AR `…/arabic/قائمة-الممثلين/` | high | REST |
| EN | `…/en/representatives/` | page | Representatives | FA/AR | medium–high | REST; also EN `representatives-3` |
| AR | `…/arabic/قائمة-الممثلين/` | page | قائمة الممثلين | FA/EN | high | REST |
| FA | `…/کاتالوگ/` (title مرکز دانلود) | page | مرکز دانلود | EN `…/en/center-download/`; AR `…/arabic/مركز-التنزيل/` | high | REST titles/links |
| EN | `…/en/center-download/` | page | Download Center | FA/AR | high | REST |
| AR | `…/arabic/مركز-التنزيل/` | page | مركز التنزيل | FA/EN | high | REST |
| FA | `…/آخرین-اخبار/` | page | آخرین اخبار | EN `…/en/latest-news/`; AR `…/arabic/الاخبار/` | high | REST |
| EN | `…/en/latest-news/` | page | News | FA/AR | high | REST |
| AR | `…/arabic/الاخبار/` | page | الاخبار | FA/EN | high | REST |
| FA | `…/مقالات/` | page | مقالات | EN `…/en/blog/` (also EN `articles`) | medium | REST; dual EN surfaces |
| EN | `…/en/blog/` | page | Blog | FA `مقالات` | medium | REST |
| FA | `…/مسئولیت-اجتماعی/` | page | مسئولیت اجتماعی | EN `…/en/csr/` | medium–high | REST |
| EN | `…/en/csr/` | page | CSR | FA above | medium–high | REST |
| FA | `…/توسعه-پایدار/` | page | توسعه پایدار | EN `…/en/sdgs/` | medium | REST; naming differs |
| EN | `…/en/sdgs/` | page | SDG’s | FA above | medium | REST |
| FA | `…/مشتریان-ما/` | page | مشتریان ما | EN `…/en/our-customers/` | medium–high | REST |
| EN | `…/en/our-customers/` | page | Our customers | FA above | medium–high | REST |
| FA | `…/فرصت-های-همکاری/` | page | فرصت های همکاری | EN `…/en/collaboration-opportunities/` | medium–high | REST |
| EN | `…/en/collaboration-opportunities/` | page | Collaboration opportunities | FA above | medium–high | REST |
| FA | `…/موقعیت-های-شغلی/` | page | موقعیت های شغلی | — | — | REST; **no EN/AR page found** |
| FA | `…/تجارب-ما/` | page | تجارب ما | — | — | REST; **no EN/AR page found** |
| EN | `…/en/products/oral-hygiene/` (nav link historically) | — | — | — | — | Live follow → **`/en/products/other-products/`** (200); not a distinct page in REST |
| EN | utility/odd pages: `فوتر`, `a1-2`, `دیگر-محصولات-2`, `catalogue`, `canister-installation`, `user-manuals`, `reservoir-calculator`, `representatives-3` | page | various | mostly unmatched / internal | low | EN REST + page-sitemap |
| AR | `…/arabic/برگه-نمونه/` | page | برگه نمونه | — | — | REST sample page |

### Posts (summary, not full pair table)

| Language | Count | Notes |
|---|---:|---|
| FA | 221 | Dominates content volume (prior audit) |
| EN | 84 | Listed in `en/post-sitemap.xml` |
| AR | 28 | REST list; mostly older event/news items |

**Post-level FA↔EN↔AR ID linking:** **Not verified** / no public translation API. Some topics appear related by title (INFERENCE only), e.g. CE certification / Iran Health reports, but **no machine-verified pair map** was built for all posts in this pass.

Full EN page list: `https://www.abadis-med.com/en/page-sitemap.xml` (31 locs).  
Full EN post list: `https://www.abadis-med.com/en/post-sitemap.xml` (84 locs).  
AR pages/posts: live `arabic/wp-json/wp/v2/pages|posts`.

---

## 3. Translation relationships

### How versions are connected (FACT + INFERENCE)

1. **Not** connected by WPML/Polylang translation groups or shared post IDs across locales (FACT: separate installs + different IDs + no multilingual namespaces).
2. Connected **editorially** by parallel navigation/menus and human-maintained equivalent pages (INFERENCE from menu structure + semantic pairs above).
3. Language switcher does **not** compute equivalents; it links to **language home roots** only (FACT — §5).
4. No `hreflang` graph binds pairs (FACT — §4).

### Consistency

| Aspect | Finding |
|---|---|
| Product family pages | Mostly consistent triad FA/EN/AR for core products |
| Path conventions | Inconsistent (EN suction tube outside `/products/`; AR FAQ uses Persian slug) |
| Feature pages | FA-only for jobs + “تجارب ما”; EN has CSR/SDGs; AR lacks CSR/SDGs/customers/jobs |
| Calculators | Messy: FA one page; EN `calculator` + `reservoir-calculator`; AR `الحوسبة` + `الحاسبة` |
| Content volume | FA ≫ EN ≫ AR for posts |

---

## 4. hreflang

| Check | Result | Evidence |
|---|---|---|
| FA/EN/AR homepages (prior audit) | `hreflang` count **0** | `SEO-AUDIT.csv`, `ABADIS-AUDIT.json` |
| FA product `…/محصولات/کیسه-ساکشن/` | no `hreflang` attrs; `html lang=fa-IR`; Yoast present | live HTML 2026-09-25 |
| EN product `…/en/products/suction-bag/` | no `hreflang`; `html lang=en-US`; Yoast present | live HTML |
| AR product `…/arabic/كيس-الشفط/` | no `hreflang`; **`html lang=fa-IR` (wrong)**; Yoast markers absent | live HTML |
| Generation source | None observed for hreflang | — |

**Problems:** missing reciprocal alternates; Arabic language attribute wrong; EN/AR under-discovery from FA sitemap; EN canonical host is www while FA/AR are non-www.

---

## 5. Language switcher

### Behavior (FACT)

Observed on locale **homepages** (`home.html`, `en_.body`, `arabic_.body`):

| From | Control | Target | Notes |
|---|---|---|---|
| FA | “English” / “العربی” buttons | `https://www.abadis-med.com/en/` and `…/arabic/` | `target="_blank"` |
| EN | “Arabic” / “Persian” | `…/arabic/` and `https://www.abadis-med.com/` | roots only; `target="_blank"` |
| AR | “English” / “فارسی” | `…/en` and `https://abadis-med.com/` | roots only; `target="_blank"` |

### How equivalent page is found

**It is not.** The switcher does not map `/محصولات/کیسه-ساکشن/` → `/en/products/suction-bag/`. It always sends users to the **other language’s homepage**.

No JS translation-map evidence was found in these homepage HTML samples. Deep-page switcher behavior beyond homes: **Not fully verified** (homepages confirmed; product-page chrome likely similar via shared header templates — INFERENCE).

---

## 6. Missing / unmatched translations

### FA pages without clear EN/AR page

- `…/موقعیت-های-شغلی/` (jobs)
- `…/تجارب-ما/`
- FA-only JetEngine public archives (`_customers`, `_franchise`, `_joboffers`, `_downloadcenter`, `_citynmg`) — EN has separate `representatives_01` sitemap type; full CPT parity **Not verified**

### EN pages without clear FA/AR equivalent

- Utility/orphan-ish: `فوتر`, `a1-2`, `دیگر-محصولات-2`, `representatives-3`
- `catalogue`, `canister-installation`, `user-manuals`, `reservoir-calculator` (possible FA partial overlaps with installation/calculator — **Not verified**)
- Nav URL `…/en/products/oral-hygiene/` resolves to **other-products** (no distinct EN oral-hygiene page)

### AR gaps vs FA/EN

- No AR pages found for: CSR, SDGs/sustainability, customers, jobs, “تجارب ما”, blog/articles hub equivalent to FA `مقالات` / EN `blog`
- AR FAQ slug remains Persian
- AR sample page `برگه-نمونه`
- AR sitemap/robots effectively missing (HTML responses)

### Product equivalents

Core product set (suction bag, base/holder, filters, canisters, connections, other, suction tube) **does** have EN/AR page equivalents (high confidence).  
Parity of **specs/media inside** those pages: **Not verified** (needs content diff / field export).

### Post corpus

FA 221 vs EN 84 vs AR 28 → large unmatched article sets (FACT counts; pair mapping incomplete).

---

## 7. SEO / migration risks

| Risk | Why it matters | Evidence |
|---|---|---|
| **URLs** | Three installs + different path shapes; EN prefers www | REST links; redirects |
| **Canonical** | www vs non-www split; AR/FA non-www | EN product canonical on www |
| **hreflang** | None → search engines must infer language versions | live HTML; audit JSON |
| **Redirects** | EN non-www→www; oral-hygiene→other-products; unknown historical maps | live follow |
| **Duplicate / near-duplicate** | Parallel product pages without alternates; possible calculator duplicates (AR/EN) | REST inventories |
| **Language switching** | Always drops user on homepage → poor UX + weak internal linking across locales | homepage HTML |
| **Indexed pages** | FA sitemap omits EN/AR; AR has no working sitemap index; EN has its own Yoast sitemaps (may be under-submitted from primary Search Console property) | FA audit; live EN/AR sitemap checks |
| **Arabic `lang`** | `fa-IR` on AR pages mis-signals language | AR home + product HTML |
| **AR SEO plugin gap** | No `yoast/v1` on AR REST root | live AR `wp-json` namespaces |
| **Migration model** | Cannot rely on WP translation IDs; must build an explicit pair table + preserve three URL namespaces | architecture FACT |

---

## 8. Answers to existing open questions

Analysis/recommendation only (does **not** edit `ABADIS-OPEN-QUESTIONS.md`).

### L1 — How product/page language versions relate

**Evidence-backed finding:** Versions are **separate WP page records in separate locale installs**, paired only by editorial/nav convention—not by WPML-style relationships or shared IDs.

**Recommendation for later decision:** Treat L1 as requiring an **explicit migration pairing table** (CSV) maintained by humans from this inventory; Nuxt should implement hreflang from that table, not from WP translation APIs (none found).

Status implication: still needs **joint confirmation** of the pair list, but mechanism is no longer “unknown plugin”—it is **multi-install + manual pairing**.

### C2 — Data model (language portion)

**Evidence-backed finding:** Locale content is not one WP graph with language fields; it is **three content databases/frontends**. Product fields must be modeled **per locale** (or unified in headless WP later) with a cross-locale `translation_group` key invented at migration time.

Remaining open: field schemas, roles, Elementor-only content (still need auth export).

### C3 — REST completeness for products / SEO fields

**Additional evidence:**

- FA & EN expose `yoast/v1`; AR does **not**.
- Pages/media listings work per install.
- Custom field emptiness on public samples (prior audit) still stands.
- Products are pages under each install’s page tree.

**Proposed refinement (not a full close):** Default REST is sufficient to **inventory URLs/titles** per locale; insufficient for unified translation IDs or guaranteed product meta; AR SEO metadata source is weaker.

### S1 — Search Console

**Finding:** No Search Console export, property dump, or API credential/data exists in this repository.

**Answer:** Still **Needs Abadis** to provide GSC data (especially which property covers `/en/` www vs apex, and whether `/arabic/` is indexed).

---

## 9. Remaining unknowns

1. Exact hosting topology (true multisite vs three separate WP installs sharing a server) beyond public URL/`wp-json` evidence.  
2. Full deep-page language-switcher markup on every template (only homes fully inspected).  
3. Complete FA↔EN↔AR **post** pair map.  
4. Whether calculator pages (`الحاسبة` vs `الحوسبة`; EN `reservoir-calculator`) are duplicates or distinct tools.  
5. Content parity of paired product pages (specs, downloads, claims).  
6. EN CPT `representatives_01` vs FA `_franchise` relationship.  
7. IP/geo redirect behavior for real client IPs (Accept-Language alone does **not** redirect — FACT; IP-based routing **Not verified**).  
8. Whether EN Yoast sitemaps are submitted in Google Search Console.  
9. Auth-only meta / Elementor JSON differences across the three installs.  
10. Historical redirect rules between old EN/AR slugs.

---

## Appendix — Method notes

- Existing audit first: `ABADIS-AUDIT.json`, `SEO-AUDIT.csv`, `TECHNOLOGY-PLUGIN-AUDIT.md`, `URL-MIGRATION-MAP.csv`, reconciliation doc, `audit-raw/live/*`.  
- Live reads: REST pages/posts/namespaces; EN Yoast sitemaps; HTTP follows for key URLs; Accept-Language header probes on FA home (no Location redirect).  
- No site modifications. No GSC data available in-project.
