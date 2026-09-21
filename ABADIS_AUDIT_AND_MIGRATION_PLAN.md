# Abadis Med Website Redesign
## Audit, SEO Migration Strategy, and Implementation Plan

**Prepared by:** Manus AI  
**Audit date:** 21 September 2026  
**Audited domain:** [abadis-med.com](https://abadis-med.com/)

## Executive conclusion

The existing Abadis Med website should be **migrated, not replaced by a clean-slate marketing site**. It is a WordPress site with a substantial searchable archive, three language roots, product taxonomy, customer and representative records, downloadable materials, installation content, a savings calculator, certifications, and a large technical/article library. The redesign can substantially improve product presentation and brand quality, but the first release must preserve the existing URL graph and content meaning.

The safest strategy is to build a new Nuxt 4 front end around a **content and URL migration manifest**. Every existing URL should be classified as one of four states: preserve exactly, improve in place, consolidate with a documented 301 redirect, or exclude only after a content and indexation review. The migration should keep the Persian root, the English `/en/` root, and the Arabic `/arabic/` root. It should also retain WordPress media and document paths during the first release wherever practical.

The proposed experience is a premium medical-industrial product showcase. It should lead with the product system, factory credibility, infection-control value, specifications, certifications, and contact paths. Cinematic motion and 3D should support comprehension rather than conceal information. The calculator should become a transparent, validated decision tool rather than an ornamental counter.

## Audit scope and evidence

This first audit examined the live homepage and sitemap index, the Persian, English, and Arabic homepages, all child sitemap endpoints listed by the site, representative core routes, the local editable design brief, and the supplied product assets. The sitemap endpoints were downloaded with bounded requests into the project’s `audit-raw/` directory. The raw URL-record count is summarized below.

| Sitemap | URL records | What it appears to contain |
|---|---:|---|
| `page-sitemap.xml` | 26 | Core pages, utilities, guides, product routes, and page-level media references |
| `post-sitemap.xml` | 207 | Articles, news, historical posts, technical content, and older product-related pages |
| `_customers-sitemap.xml` | 156 | Customer records and customer/location pages |
| `_franchise-sitemap.xml` | 27 | Franchise or representative-related records |
| `_citynmg-sitemap.xml` | 25 | City/location records |
| `post_tag-sitemap.xml` | 63 | Post tag archive URLs |
| `_downloadcenter-sitemap.xml` | 10 | Download-center records |
| `_joboffers-sitemap.xml` | 10 | Job or recruitment records |
| `category-sitemap.xml` | 8 | Category archives |
| `jet-menu-sitemap.xml` | 3 | Menu-builder records |
| `author-sitemap.xml` | 4 | Author archives |
| **Total** | **545** | Raw URL records across 11 child sitemaps |

The sitemap totals are a count of `<url>` records, not a count of every embedded image or document reference. The complete raw sitemap files and collection script are committed with this report so the migration matrix can be extended without repeating the first crawl.

## Existing information architecture

The current site has a recognizable but uneven structure. The Persian home is the default root. English content is primarily grouped under `/en/`, while Arabic content is grouped under `/arabic/`. The English navigation exposes a more explicit product hierarchy than the Persian homepage. It includes `/en/products/` with suction bags, base and holder, filters, canisters, connections, suction tube, and other products. The Arabic navigation has corresponding product categories, but several Arabic pages use Persian or legacy-looking slugs and do not appear to have a clean one-to-one relationship with the English routes.

The principal content areas are:

| Area | Current role | Migration treatment |
|---|---|---|
| Homepage | Brand, company, product value, customer proof, news, calculator CTA, contact, certifications | Preserve root URLs; redesign in place with content parity |
| About | Company story, mission, team, factory credibility | Preserve each language route; rewrite only after source/content sign-off |
| Products | Product taxonomy and product information | Preserve category and detail URLs; give product detail pages the highest design priority |
| Installation | Installation manual and illustrated guidance | Preserve routes and media; make instructions more accessible and searchable |
| Calculator | Savings estimate for water, waste, time, and cost | Preserve route; rebuild as a transparent, validated tool |
| Articles and news | SEO acquisition and company knowledge | Keep article URLs; visually separate news, technical articles, and social responsibility |
| Customers | Trust and proof of adoption | Keep customer records and location relationships; normalize templates |
| Representatives/franchise | Business development and export support | Preserve URLs; expose region and contact data carefully |
| Download center | Catalogs, technical files, certificates, product documents | Preserve file URLs when possible; add stable metadata and document types |
| Careers/job offers | Internal recruiting and employer content | Preserve unless a page is confirmed obsolete and non-indexed |
| Taxonomy/author/menu archives | WordPress-generated discovery surfaces | Audit indexation before preserving, canonicalizing, or noindexing |

## Content and product inventory findings

The homepage currently communicates the following source-of-truth claims and content themes: Abadis is a knowledge-based manufacturer focused on hospital fluids and infectious waste; it produces disposable suction liner bags; it positions its products around infection control, waste management, reduced washing, lower resource consumption, ease of use, and sustainability; it presents factory capacity and customer adoption; and it links to CE, IMED, and ISO documents. These claims must remain available in the new site, subject to a final legal and commercial verification.

The local design brief adds a company history from 1396/2017 through 1405/2026. It describes factory preparation, the first sale in 1397/2018, MIS and BI adoption, COVID-era growth, knowledge-based certification, exports to Iraq and Oman, development of a receiver, antibacterial and porous filters, a flow-stop filter, suction tubing, and a tracheal-tube fixer. It also describes a sustainability program involving 4,000 oak trees in the Zagros region from 1403 to 1408. These details should become a structured company timeline, but they should not overwrite older indexed About content until the two versions are reconciled.

The supplied project assets include a CATPart model, a ZIP copy of the CATPart, a logo Illustrator file, and a one-liter suction-bag PNG. The CAD files are useful evidence that a 3D workflow is possible, but they are not yet web-ready assets. Geometry, material assignments, product variants, dimensions, connector details, and production-approved imagery still need confirmation.

## Multilingual and language-behavior audit

The live site does not currently justify changing language selection behavior. The Persian homepage links to the English and Arabic roots. The English homepage provides English product categories and links back to Persian and Arabic. The Arabic homepage provides Arabic navigation but includes some legacy or mixed-language URL patterns. This is a strong reason to create a language relationship matrix before any route redesign.

The first implementation should use explicit language URLs and avoid server-side IP-based language switching. If the existing site uses location or IP signals in some contexts, the new site should treat them only as a non-blocking suggestion. It must never redirect a crawler or a user away from the requested language URL. A visitor who opens `/en/` should remain on `/en/`; a visitor who opens `/arabic/` should remain on `/arabic/`.

For every translatable page, the migration manifest should record the Persian, English, and Arabic URLs, the canonical URL for each language, the reciprocal `hreflang` set, the translation completeness status, and the fallback policy. Missing translations should not be silently represented as duplicate content from another language. They should either receive a clearly marked localized page or be kept out of the alternate-language relationship until translated.

## SEO preservation requirements

### URL policy

Existing slugs are an asset. The first release should keep them even where they are long, percent-encoded, or inconsistent. A clean new route may be added only when the old route remains live or redirects permanently to the single canonical replacement. The migration must maintain a redirect table with the old URL, new URL, reason, language, status code, and verification result.

Do not use blanket wildcard redirects from WordPress paths to the homepage. Those redirects destroy relevance and make it impossible to distinguish a product, article, guide, customer, or document destination. Redirects should be one-to-one and content-equivalent.

### Metadata policy

For every preserved or migrated URL, capture the current title, description, canonical, indexability, language, H1, heading outline, Open Graph fields, structured data, main image, and important internal links. Improve weak titles and headings only after the original meaning and search intent are recorded. The new site should produce one descriptive H1, a stable title template, a unique meta description, canonical URLs without tracking parameters, and language-appropriate Open Graph data.

### Sitemap and robots policy

During the migration, generate a sitemap index that mirrors the language and content boundaries of the live site. Do not submit a reduced sitemap until all important URL classes have been tested. Keep redirects out of the sitemap. Keep `noindex` archives out of the sitemap. Preserve document URLs even if the document itself remains hosted on the original media path.

Validate `robots.txt`, canonical URLs, `hreflang`, JSON-LD, 301 behavior, trailing slash behavior, uppercase/lowercase behavior, percent-encoded Persian paths, and query-string handling in a staging environment before launch.

### Structured data

Use organization and website schema site-wide. Use breadcrumb schema on content pages. Use product schema only where the page contains stable product identity, image, brand, description, material/specification data, and a valid contact or availability model. Do not invent prices, stock, reviews, ratings, or medical outcomes. Use article schema for genuine articles and news article schema for company news where the dates and authors are accurate.

## Redirect and preservation matrix

The following decisions are recommended before implementation:

| URL family | Decision now | Required verification |
|---|---|---|
| `/`, `/en/`, `/arabic/` | Preserve exactly | Confirm canonical and language alternates |
| Existing product category and detail routes | Preserve exactly at launch | Match each route to a product record and translated equivalent |
| Existing articles and news posts | Preserve exactly | Record indexability, traffic, and content status before redesign |
| Installation and calculator routes | Preserve exactly | Rebuild templates behind the same URLs |
| Download-center and certificate files | Preserve file URLs where practical | Verify downloads, MIME types, access, and document ownership |
| Customer, city, franchise, and representative routes | Preserve unless demonstrably empty | Decide whether archives are indexable or utility-only |
| Author, tag, menu, and generated archives | Do not delete yet | Review Search Console/indexation and internal-link value |
| Duplicate legacy product pages | Consolidate only after evidence | Create explicit one-to-one 301 and update all internal links |
| Obsolete recruitment pages | Preserve or redirect based on indexation and backlinks | Do not return a soft 404 or redirect unrelated pages to home |

A complete redirect CSV should be generated from the final crawl, not manually guessed from the visible navigation. Before launch, run the list against both hostname variants (`abadis-med.com` and `www.abadis-med.com`), HTTP to HTTPS, trailing slash variants, encoded paths, and any legacy aliases discovered in analytics or Search Console.

## Recommended homepage experience

The homepage should become a product-led narrative with a clear information hierarchy. The first viewport should identify Abadis as a medical and industrial manufacturer, show the core suction/waste-management system, and provide two primary actions: **view products** and **request consultation**. The visual system can be cinematic, but the first screen must contain crawlable text, a real H1, a meaningful product image, and accessible controls.

A practical sequence is:

1. A language-specific hero with the product system, one strong value proposition, and product/consultation actions.
2. A concise manufacturer credibility block with knowledge-based status, factory capability, regions served, and verified certifications.
3. A product-system sequence showing the bag, canister, base/holder, filters, connections, and tubing as a coherent workflow rather than as unrelated cards.
4. A scroll-linked product visual or 3D model that exposes parts and use context, with a static poster image fallback.
5. An infection-control and resource-impact section explaining the mechanism in plain language, with a link to the transparent calculator.
6. Factory and process proof through a short, compressed video or image sequence. Motion must not be the only way to access the factory story.
7. Customer and representative proof with accessible text labels and region context.
8. Certifications and technical-download access.
9. Separated content lanes for company news, educational articles, and sustainability projects.
10. A conversion section for consultation, representative requests, sales/export contact, and catalog access.

Avoid repeating the current carousel content several times in the DOM. Use a small number of editorially selected items with server-rendered links. Every decorative image should have an empty alt attribute; every informative image needs a precise localized alt description.

## Recommended product page template

Every important product should share one understandable template. The template should be data-driven, but the data model should remain simple enough for a non-expert owner to edit in Cursor.

The product page should contain a product name, short functional summary, approved hero visual, product family and compatible components, primary applications, infection-control or workflow benefits, materials, dimensions and capacity, connection details, available variants, certifications, packaging or single-use information where applicable, technical specifications, installation instructions, downloads, related products, and a direct request/contact action. The factual sections should be available as HTML, not embedded only in a 3D canvas.

A product page should use stable identifiers and product codes when they exist. It should not publish a specification inferred from a CAD file or image. A content checklist should require manufacturer confirmation before any technical claim, performance number, biocompatibility statement, sterility statement, or medical outcome is published.

## 3D asset workflow recommendation

The existing CATPart should first be converted in a controlled desktop workflow to a lightweight GLB. The source team should remove hidden manufacturing geometry, separate visually meaningful parts, apply production-approved materials, set a consistent origin and scale, create a low-detail mobile mesh, and preserve a high-detail version only for larger screens. The final GLB should be tested on current mobile browsers before it becomes a launch dependency.

The preferred interaction is progressive enhancement. On capable devices, a Three.js or `<model-viewer>` scene can respond to scroll progress and allow controlled rotation. On low-power devices, reduced-motion users, keyboard users, and crawlers, the page should show an optimized poster image plus labeled hotspot cards and a specification diagram. GSAP should be introduced only for a small number of scroll sequences after performance testing; it should not become the application’s routing or content layer.

The 3D acceptance checklist is: correct scale, correct connector geometry, no hidden or misleading product parts, stable lighting, acceptable file weight, usable keyboard/focus behavior, reduced-motion support, no blocked text content, no layout shift, and a static fallback. The product owner must approve the visual model before publication.

## Technical architecture for Nuxt 4

The recommended stack is Nuxt 4, Vue, Tailwind CSS, Nuxt UI where it improves accessible primitives, Bun for local package management, and Vercel-compatible deployment. The architecture should favor a small number of explicit layers:

- **Content layer:** typed content records for products, categories, pages, articles, customers, representatives, downloads, and locales.
- **Route layer:** a route manifest that maps every preserved legacy path to a content record or an explicit redirect.
- **Presentation layer:** shared layouts, language-aware navigation, product sections, article templates, breadcrumbs, and contact CTAs.
- **SEO layer:** one composable for title, description, canonical, language alternates, Open Graph, and JSON-LD.
- **Asset layer:** original WordPress media references during migration, with a later optimization pass for local copies and modern formats.
- **Interaction layer:** isolated calculator, 3D viewer, and motion components that can be disabled or replaced by static fallbacks.

Do not begin with a headless CMS, customer accounts, CRM, AI chatbot, or order system in the public redesign. First make the catalog, content, URLs, SEO, and contact paths reliable. Phase-two APIs can be added behind stable interfaces once product and customer data ownership is clarified.

## Calculator requirements

The calculator is a high-value differentiator and should be rebuilt behind its existing route. Its model must identify inputs, assumptions, units, formulas, source dates, and uncertainty. It should compare the current/traditional process with the disposable-bag workflow and show estimated water, cleaning time, cost, and waste changes in a way a hospital administrator can understand.

The result should be shareable through a stable, non-sensitive report URL or downloadable PDF only if the privacy implications are understood. User inputs should be validated and should not be sent to analytics by default. The page must contain crawlable explanatory content describing what the calculator measures and what it does not measure.

## Phased implementation plan

### Phase 0: freeze and evidence capture

Export the full sitemap and crawl results, preserve a copy of the current HTML and metadata for every important URL, obtain Search Console and analytics data, inventory media and documents, and freeze any URL changes on the old site. Confirm the canonical hostname, redirects, language behavior, forms, calculator behavior, downloads, and contact destinations.

### Phase 1: migration manifest and content model

Create the route manifest and URL classification matrix. Create localized records for products, pages, articles, customers, representatives, and downloads. Mark each field as verified, copied, translated, rewritten, or pending owner approval. Do not delete source content during this phase.

### Phase 2: Nuxt foundation and SEO parity

Implement layouts, typography, language routing, metadata composables, breadcrumbs, redirects, sitemap generation, robots behavior, structured data, and the preserved content templates. Make a staging deployment that can be crawled before the cinematic homepage is complete.

### Phase 3: product showcase and 3D pilot

Build one product family end-to-end. Start with the one-liter suction bag and its related components because the project already contains a one-liter product image and CAD evidence. Compare a static premium presentation, a 360-degree image sequence, `<model-viewer>`, and a Three.js/GLB viewer. Choose the least complex option that meets the visual and technical goals.

### Phase 4: homepage, calculator, and content refinement

Build the product-led homepage, transparent calculator, factory story, certifications, customer proof, and separated news/article/sustainability lanes. Preserve the original text meaning and publish new copy only after commercial and technical review.

### Phase 5: launch validation

Run automated route checks, redirect checks, metadata checks, language-alternate checks, structured-data validation, accessibility audits, performance tests, mobile tests, and manual review of every product and document. Compare the staging URL inventory with the pre-migration manifest. Launch with monitoring and a rollback plan.

### Phase 6: post-launch improvement

Monitor Search Console coverage, crawl errors, rankings, conversions, calculator usage, downloads, and contact requests. Add CRM, chatbot, customer accounts, or ordering only after the public catalog and data governance are stable.

## Definition of done for the first release

The first release is complete when every important pre-launch URL has a verified destination, every redirect is explicit and content-equivalent, the three language roots remain accessible, product and technical content is available without JavaScript, canonical and `hreflang` signals are reciprocal, the sitemap contains only intended canonical URLs, documents and forms work, the calculator exposes its assumptions, and the 3D experience has a static accessible fallback.

The visual redesign should be considered successful only if a hospital buyer can identify the relevant product, understand its application and technical boundaries, find a document or installation guide, verify credibility, and contact the correct sales or export team without needing to decode the animation.

## Immediate next actions

The next implementation task should not be a full-site build. It should be a **content and URL manifest** containing one row per sitemap URL with language, content type, status code, indexability, title, description, canonical, H1, last modified date, primary image, linked documents, proposed Nuxt route, and migration decision. After that manifest is reviewed, build the first product page and the shared SEO/layout foundation.

## References

[1]: https://abadis-med.com/ "Abadis Med Persian homepage"
[2]: https://www.abadis-med.com/en/ "Abadis Med English homepage"
[3]: https://www.abadis-med.com/arabic/ "Abadis Med Arabic homepage"
[4]: https://abadis-med.com/sitemap_index.xml "Abadis Med sitemap index"
[5]: https://abadis-med.com/page-sitemap.xml "Abadis Med page sitemap"
[6]: https://abadis-med.com/post-sitemap.xml "Abadis Med post sitemap"
[7]: https://abadis-med.com/%d8%b1%d8%a7%d9%87%d9%86%d9%85%d8%a7%db%8c-%d9%86%d8%b5%d8%a8/ "Abadis Med Persian installation guide"
[8]: https://abadis-med.com/%d9%85%d8%ad%d8%a7%d8%b3%d8%a8%d9%87-%da%af%d8%b1/ "Abadis Med Persian calculator"
