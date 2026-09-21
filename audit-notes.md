# Audit Notes (working)

## Live homepage and language observations
- Source: https://abadis-med.com/ fetched 2026-09-21.
- Primary homepage is Persian and links to explicit English (`https://www.abadis-med.com/en/`) and Arabic (`https://www.abadis-med.com/arabic/`) roots.
- Persian homepage navigation includes About, Installation Guide, Articles, Contact, and language links. It also exposes a calculator, customer logos, team section, news, company/factory information, and CE/IMED/ISO certification documents.
- Homepage states Abadis is a knowledge-based manufacturer focused on hospital fluid and infectious-waste management, disposable suction liner bags, infection control, sustainability, and 5 million annual bag capacity.
- Contact details shown include Tehran office, Shamsabad factory, phone numbers, email `info@abadis-med.com`, and certification documents.
- Homepage content appears WordPress-rendered and includes repeated carousel items, older news, and many image assets.

## Sitemap observations
- Sitemap index: https://abadis-med.com/sitemap_index.xml
- Child sitemaps: post, page, jet-menu, _joboffers, _downloadcenter, _customers, _franchise, category, post_tag, _citynmg, author.
- Page sitemap last modified 2026-09-21; post sitemap last modified 2026-09-15.
- Page sitemap visibly includes calculator, careers/job pages, installation guides, catalog, customers, articles, latest news, and product paths. It also includes image references under pages.
- Post sitemap is large (about 177k characters) and includes old product/article URLs, employment pages, and technical articles. It must be fully inventoried before redirects or consolidation.

## Multilingual observations
- English homepage has a clean product taxonomy: `/en/products/`, `/en/products/suction-bag/`, `/en/products/base-and-holder/`, `/en/products/filters/`, `/en/products/canisters/`, `/en/products/connections/`, `/en/suction-tube/`, `/en/products/other-products/`, plus installation manual, blog, contact, and about pages.
- Arabic homepage has `/arabic/منتجات/` and category routes for suction bag, holder, filter, connections, and other products. It also links to older/odd Persian-slug paths in Arabic contexts, suggesting hreflang/content relationship quality must be checked rather than assumed.
- Arabic content includes legacy-looking zero counters and old 2018–2019 news, while Persian/English pages include newer material. Language completeness and cross-language URL mapping require an inventory.

## Project brief observations
- Source: `/home/ubuntu/projects/abadis-8638c0b0/Abadis_Website_Design_Brief_Editable.docx`, 11 pages.
- The brief describes company history from 1396/2017 through 1405/2026, including factory setup, first sale in 1397/2018, MIS and BI adoption, COVID-era growth, knowledge-based certification, exports to Iraq and Oman, product expansion (receiver, antibacterial filter, flow-stop filter, tubing), sustainable-development planning, and a 1405/2026 tubing product.
- Brand direction in the brief: medical, technology, industrial, premium, minimal, official/international.
- Goals include presenting Abadis as a professional manufacturer, increasing trust among hospitals and foreign representatives, showing economic/health/environmental impact, and turning the site into a quotation/contact tool.
- Proposed homepage structure includes multilingual hero, Abadis introduction, slogan, product showcase, collaboration request, latest news/articles, and statistics.
- The current source assets include a CATPart model, a ZIP of the CATPart, an Abadis logo AI file, and a one-liter bag PNG. These are candidates for asset preparation, not yet web-ready 3D assets.

## Initial conclusions
- Do not replace URLs or content until the complete sitemap and page/post/media inventory is captured.
- Product taxonomy and multilingual roots are high-priority preservation surfaces.
- The migration should retain WordPress URLs and document/media URLs where practical, with an explicit redirect matrix for only true consolidations.
- Interactive 3D should be evaluated after confirming available CAD geometry, materials, dimensions, and production-approved product photography.

## Additional brief findings from pages 6–11
The brief prioritizes the homepage, About, calculator, and product pages for distinctive design. Secondary priorities are sustainability, representatives, social responsibility, latest news, and practical customer/staff pages such as FAQ, installation, contact, download center, and careers. It proposes a dynamic impact counter for estimated water savings, avoided washing cycles, and reduced cleaning time/cost, but explicitly requires transparent formulas and citable sources.

The brief proposes separating company news/events, educational/technical articles, and social-responsibility projects. It also proposes an AI chatbot restricted to product selection guidance, FAQs, installation help, catalogs/technical files, contact requests, and routing to sales/export. Later phases mention CRM/API integration, customer accounts, orders, invoices, discounts, and purchased-product documents; these should remain future scope rather than being silently introduced in the redesign.

The brief’s explicit shortcomings are: no standard H1 on several core pages, missing image alt text, weak/general page titles, irregular heading hierarchy, repetitive sliders, an overloaded homepage, counters that initially show zero, and poor visual separation of news and articles. It also says the existing calculator lacks transparent assumptions, sources, visual comparison, downloadable/shareable reports, and input validation. It warns that important information must not be sacrificed for visual design.
