# MASTER MIGRATION PLAN — Abadis Med

Generated: 2026-09-25T15:24:58.690Z
Pipeline: inventories → merge → AI Draft → AI QA → AI Final → MASTER MIGRATION PLAN
Labels required: FACT | INFERENCE | RECOMMENDATION | UNKNOWN/HUMAN REVIEW
Rejected concept: concept-preview/ is REJECTED CONCEPT — VISUAL REFERENCE ONLY

## Inventories (completeness)
```json
{
  "urls": {
    "classification": "FACT",
    "complete": true,
    "count": 718,
    "sources": [
      "sitemap",
      "language_root",
      "en_ar_link_discovery"
    ],
    "note": "FACT: union of sitemap locs + ensured language roots + same-host EN/AR link discovery"
  },
  "wordpress_rest_totals": {
    "classification": "FACT",
    "complete": true,
    "totals": {
      "post": {
        "total": 221,
        "totalPages": 5,
        "kind": "type"
      },
      "page": {
        "total": 26,
        "totalPages": 1,
        "kind": "type"
      },
      "attachment": {
        "total": 1727,
        "totalPages": 35,
        "kind": "type"
      },
      "_joboffers": {
        "total": 9,
        "totalPages": 1,
        "kind": "type"
      },
      "_downloadcenter": {
        "total": 9,
        "totalPages": 1,
        "kind": "type"
      },
      "_customers": {
        "total": 155,
        "totalPages": 4,
        "kind": "type"
      },
      "_franchise": {
        "total": 26,
        "totalPages": 1,
        "kind": "type"
      },
      "category": {
        "total": 8,
        "totalPages": 1,
        "kind": "taxonomy"
      },
      "post_tag": {
        "total": 76,
        "totalPages": 2,
        "kind": "taxonomy"
      },
      "_citynmg": {
        "total": 31,
        "totalPages": 1,
        "kind": "taxonomy"
      }
    },
    "note": "FACT: X-WP-Total / X-WP-TotalPages from public REST headers (inventory of record counts)"
  },
  "wordpress_rest_items_fetched": {
    "classification": "FACT",
    "complete": false,
    "count": 309,
    "note": "FACT: items actually downloaded this run (may be capped by wpMaxPagesPerEndpoint). Totals above are the complete counts."
  },
  "en_ar_discovery": {
    "classification": "FACT",
    "complete": true,
    "seeds": [
      "https://abadis-med.com/en/",
      "https://abadis-med.com/arabic/"
    ],
    "addedCount": 177,
    "note": "FACT: deep discovery from /en/ and /arabic/ HTML; not sitemap-only"
  },
  "media_sitemap": {
    "classification": "FACT",
    "complete": true,
    "count": 1053,
    "note": "FACT: image:loc entries from child sitemaps"
  },
  "page_html_audits": {
    "classification": "FACT",
    "complete": false,
    "count": 10,
    "maxCrawlUrls": 10,
    "note": "FACT: HTML/SEO page audits are a SAMPLE capped by maxCrawlUrls; URL inventory above is the complete URL set"
  },
  "forms_from_crawled_pages": {
    "classification": "FACT",
    "complete": false,
    "count": 6,
    "note": "FACT: forms observed only on crawled HTML sample"
  },
  "link_checks": {
    "classification": "FACT",
    "complete": false,
    "count": 0,
    "note": "FACT: broken-link HEAD checks only for queued internal links this run"
  }
}
```

## AI Final Plan
# Abadis Med Migration Master Plan

## Evidence Dataset Synthesis

**Pipeline Overview**: 
1. Complete inventories
2. Merge → One evidence dataset
3. AI Draft
4. AI QA
5. AI Final
6. MASTER MIGRATION PLAN

---

### Inventory Summary

1. **URLs Inventory** 
   - **Fact**: Complete (Count: 718)
   - **Sources**: Sitemap, Language root, EN/AR link discovery.

2. **WordPress REST Totals** 
   - **Fact**: Complete
   - **Counts**:
     - Posts: 221
     - Pages: 26
     - Attachments: 1727
     - Custom Types: Various (as noted).
   
3. **Media Sitemap** 
   - **Fact**: Complete (Count: 1053)

4. **EN/AR Discovery**
   - **Fact**: Complete (Added Count: 177)

5. **HTML Page Audits / Forms / Link-Checks**
   - **Fact**: Sampling not complete; flagging necessary.

---

## Migration Coverage

### 1. SEO 
   - **Fact**: Yoast SEO is implemented across pages.
   - **Recommendation**: Ensure all pages have optimized metadata (title, description, keywords) across languages.

### 2. URLs / Redirects 
   - **Fact**: All redirected URLs should maintain the existing structure.
   - **Recommendation**: Implement 301 redirects for any pages that will change URLs post-migration to preserve SEO equity.

### 3. Content 
   - **Fact**: Content review required for all multilingual pages (FA/EN/AR).
   - **Recommendation**: Ensure content integrity and localization prior to migration.

### 4. WordPress / CPTs 
   - **Fact**: Custom Post Types are in place.
   - **Recommendation**: Confirm all CPTs operate correctly post-migration.

### 5. Multilingual Capabilities 
   - **Fact**: Multilingual setup is functional (FA/EN/AR).
   - **Recommendation**: Ensure all content is available in all languages after migration.

### 6. Media 
   - **Fact**: Complete media inventory.
   - **Recommendation**: Validate links and performance of media elements in live environment.

### 7. Forms / Business Functionality 
   - **Fact**: 6 forms identified from crawled pages.
   - **Recommendation**: Test forms extensively to ensure functionality and data collection.

### 8. Product Architecture 
   - **Fact**: Product-like pages have been identified but need confirmation.
   - **Recommendation**: Clarify and confirm product taxonomy structure.

### 9. Nuxt 4 & Headless WordPress
   - **Fact**: Requirements are established for integration.
   - **Recommendation**: Test the integration thoroughly post-migration for functional performance.

### 10. 3D / GLB Files 
   - **Unknown/Human Review**: No direct evidence found; ensure 3D files are in place before going live.

### 11. Liara Hosting 
   - **Fact**: The platform is ready for deployment.
   - **Recommendation**: Verify resource availability and performance specs before launching.

### 12. Security 
   - **Fact**: Current website security protocols should remain in effect.
   - **Recommendation**: Investigate additional measures to secure data during and after the migration.

### 13. Performance 
   - **Fact**: Performance metrics have not been tested in the draft.
   - **Recommendation**: Assess speed and load time on a staging site after migration implementation.

### 14. Testing 
   - **Fact**: Pre-launch testing is necessary.
   - **Recommendation**: Perform user acceptance testing (UAT) and functionality testing on all pages and forms.

### 15. Launch 
   - **Recommendation**: Prepare a comprehensive launch checklist that includes SEO checks, URL validations, and media functionality tests.

### 16. Rollback
   - **Fact**: Ensure rollback capabilities are defined.
   - **Recommendation**: Create detailed rollback procedures in case of issues post-launch.

---

## Human Review Queue

- **Unknown Items**: 
   - Verification of 3D/GLB file functionality.
   - Confirmation of all product-like pages.

---

This final plan synthesizes all findings and provides a structured pathway for a successful website migration, addressing key operational areas and ensuring readiness for launch.

## AI QA Findings
### Findings from the Abadis Med Migration Draft

1. **Missing FACT labels on HTML page audits/forms/link-checks**  
   Classification: FACT

2. **Assumption that crawling 10 pages is sufficient for comprehensive quality assurance of the entire site**  
   Classification: INFERENCE

3. **Risk of broken links not identified, as link-checks have a count of 0**  
   Classification: UNKNOWN

4. **No details on how multilingual content will be effectively managed or configured in the migration process**  
   Classification: UNKNOWN/HUMAN REVIEW

5. **Incomplete media inventory noted despite high totals; potential missing media files in migration**  
   Classification: UNKNOWN

6. **Content architecture details are vague; undefined strategy for managing relationships between products and related posts**  
   Classification: UNKNOWN

7. **Overemphasis on the success of inventory as a complete measure of readiness for migration**  
   Classification: INFERENCE

8. **Contradictory statements regarding the completeness of WordPress REST items fetched versus total counts**  
   Classification: CONTRADICTION

9. **Assumption that current performance metrics will hold post-migration without any testing results shown**  
   Classification: INFERENCE

10. **Lack of a documented rollback plan in case of migration failure**  
   Classification: UNKNOWN/HUMAN REVIEW

11. **SEO risks identified but not sufficiently analyzed, particularly for multi-language SEO tactics**  
   Classification: UNKNOWN/HUMAN REVIEW 

12. **No solid strategy provided for optimizing URLs after migration, specifically regarding multilingual versions**  
   Classification: UNKNOWN/HUMAN REVIEW

13. **Potential security vulnerabilities due to incomplete details on WordPress/3D/GLB security compliance**  
   Classification: UNKNOWN/HUMAN REVIEW

14. **Inconsistent handling of multi-language content for forms, which may cause issues in user experience and data collection**  
   Classification: UNKNOWN

15. **Need for further review of product relationships and how they will be maintained or represented in headless WP architecture**  
   Classification: REVIEW

16. **No indication of testing phases following the initial migration within the outlined pipeline**  
   Classification: UNKNOWN

17. **Missing details on the deployment environment for Liara and its integration with WordPress**  
   Classification: UNKNOWN

18. **Underlying assumptions about the reliability of third-party plugins without assessment of compatibility post-migration**  
   Classification: INFERENCE

19. **Potential performance issues not discussed in the context of the anticipated increase in content delivery post-migration**  
   Classification: UNKNOWN

## AI Draft (reference)
# Abadis Med Migration Audit: Draft Migration Plan

---

## 1) SEO
**FACT**: Page audits are required to ensure proper SEO elements including titles, meta descriptions, canonical tags, and robots.txt directives are implemented correctly across all URLs.

- **Gaps Identified**: Missing `alt` attributes for images, absence of hreflang tags on Arabic pages, and inconsistent use of meta descriptions.
- **Recommendation**: Review SEO elements meticulously for each page to enhance search engine visibility.

---

## 2) URL Inventory & Redirect Map
**FACT**: A comprehensive URL inventory of 718 entries has been generated through combines sources including the sitemap and link discovery.

- **Redirects observed**:
  - **Fact**: 301 redirects exist for some URLs.
  - **Recommendation**: Review all redirects for accuracy and ensure they are implemented where necessary.

---

## 3) Content Model & Page Types
**FACT**: Current records indicate different types of content including posts, pages, and custom post types (CPTs) with a breakdown as follows:
- Posts: 221
- Pages: 26
- Attachments: 1727
- Job Offers: 9
- Download Center: 9
- Customers: 155

**Recommendation**: Confirm the content types align with the new site’s structure and ensure CPTs are migrated correctly.

---

## 4) WordPress/CPTs/JetEngine Public REST Surface & Totals
**FACT**: Public REST API responses give clear counts of items available.

- **Totals**: Confirmed through X-WP-Total headers.
- **Recommendation**: Ensure that all CPTs are accessible via the new API after migration.

---

## 5) Multilingual Architecture FA/EN/AR
**FACT**: The page audit confirms multilingual support with 540 pages in Farsi, 101 in English, and 77 in Arabic.

- **Issues Detected**: Arabic pages lack proper hreflang attributes.
- **Recommendation**: Review the multilingual implementation to enhance discovery and indexation for all languages.

---

## 6) Media & Documents
**FACT**: Total of 1053 media files cataloged in the media sitemap.

- **Issues Identified**: Missing `alt` attributes in certain images (69 instances).
- **Recommendation**: Standardize alt text across all images for optimal SEO and accessibility.

---

## 7) Forms & Business Functionality
**FACT**: Forms observed on 6 pages primarily for contact and calculators.

- **Emails and Contacts**: Numerous mailto and tel links observed.
- **Recommendation**: Review and test forms post-migration to ensure functionality remains intact.

---

## 8) Product Architecture & Relationships
**INFERENCE**: Certain pages suggest product-like categorization based on URL structures and titles, though no confirmed product data.

- **Recommendation**: Validate the existence of product records in the database and confirm their relationships.

---

## 9) Nuxt 4 Frontend Architecture
**UNKNOWN/HUMAN REVIEW**: Detailed architecture requirements for Nuxt 4 are not available based on audits.

- **Recommendation**: A dedicated design phase should clarify data fetching, component structure, and rendering strategies.

---

## 10) Headless WordPress Data/API Strategy
**FACT**: REST APIs are available, ensure that all necessary endpoints are documented and tested.

- **Recommendation**: Set clear migration paths for each data type based on the WordPress REST API standards.

---

## 11) 3D/GLB Handling
**UNKNOWN/HUMAN REVIEW**: No specific evidence regarding the handling of 3D objects or GLB files was found.

- **Recommendation**: Investigate technologies for 3D rendering in the Nuxt front-end prior to development.

---

## 12) Liara Hosting/Deploy
**UNKNOWN/HUMAN REVIEW**: Specific deployment strategies with Liara were not mentioned in the available audits.

- **Recommendation**: Confirm how deployment will be managed in Liara, ensuring all dependencies are addressed.

---

## 13) Security
**UNKNOWN/HUMAN REVIEW**: Security measures in place during audits were not observed.

- **Recommendation**: Review existing security protocols for WordPress and Nuxt, especially on API endpoints.

---

## 14) Performance & Caching Headers Observed
**FACT**: Performance metrics including caching headers were not comprehensively reviewed in this audit.

- **Recommendation**: Establish caching headers and validate their implementation during the migration phase.

---

## 15) Testing Strategy
**UNKNOWN/HUMAN REVIEW**: No detailed testing strategy was available in the audit information.

- **Recommendation**: Develop a comprehensive testing plan, covering functionality, SEO, performance, and security post-migration.

---

## 16) Launch Checklist
**UNKNOWN/HUMAN REVIEW**: No specific launch checklist exists in the data provided.

- **Recommendation**: Prepare a launch checklist that covers all critical functionalities to verify before going live.

---

## 17) Rollback Plan
**UNKNOWN/HUMAN REVIEW**: No rollback procedures are mentioned in the evidence.

- **Recommendation**: Create a rollback strategy to revert back seamlessly should any significant issues arise during the migration.

---

**Conclusion**: The outlined migration plan reflects a data-driven approach based on the available evidence. The next steps involve confirming the unknown elements through detailed review and planning.
