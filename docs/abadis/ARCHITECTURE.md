# Abadis Med — Target Architecture

**Classification:** Architecture statements below are **RECOMMENDATION** unless marked otherwise.  
**Observed current stack (FACT):** WordPress + Elementor + JetEngine + JetMenu + Yoast, public HTML front.

---

## Target high-level

```text
Browser
  ↓
Nuxt 4 (SSR / hybrid)  ← Tailwind CSS, Nuxt UI where appropriate
  ↓  HTTPS REST (public + authenticated where needed)
WordPress REST API
  ↓
WordPress CMS (content, media, CPTs, editorial SEO fields)

n8n → audits, form pipelines, CRM/notifications, content sync jobs

Nuxt → Three.js → GLB product assets (progressive enhancement)

Hosting: Liara (Nuxt) + WordPress host (existing or Liara/other) + media CDN strategy
```

---

## Frontend (Nuxt 4)

- **Runtime:** Nuxt 4 with Vue 3, SSR for SEO-critical routes.
- **Styling:** Tailwind CSS; Nuxt UI for accessible primitives only where it fits the eventual approved design system.
- **i18n:** Explicit route prefixes matching current roots: `fa` → `/`, `en` → `/en/`, `ar` → `/arabic/` (**preserve observed URL structure** — FACT of current IA).
- **SEO:** `useSeoMeta`, canonical, robots, Open Graph, Twitter, `hreflang`, JSON-LD, generated sitemap index.
- **3D:** Client-only product viewers; static poster fallback; never the sole content carrier.
- **Config env (examples, not secrets):**
  - `NUXT_PUBLIC_SITE_URL`
  - `NUXT_PUBLIC_WP_API_BASE` (e.g. `https://abadis-med.com/wp-json`)
  - `NUXT_PUBLIC_MEDIA_BASE` (likely same origin `/wp-content/uploads` initially)
  - `NUXT_PUBLIC_DEFAULT_LOCALE=fa`
  - Server-only: form webhook secrets, WP application password if needed

## WordPress (headless CMS)

- Keep WordPress as system of record for pages, posts, CPTs, media.
- Expose structured fields via REST (native + JetEngine/ACF as available).
- Elementor becomes transitional; new content should prefer structured fields.
- **Do not** expose admin/private JetEngine management routes to the public Nuxt app.
- CORS: allow only Nuxt origins (staging + production).

## Media & URLs

- **FACT:** Large media library (`X-WP-Total: 1727` media on 2026-09-25 sample).
- **RECOMMENDATION:** First release keep `https://abadis-med.com/wp-content/uploads/...` URLs to avoid mass 404s.
- Later: CDN in front of uploads or Liara object storage with redirects.

## Caching

- Nuxt: route rules / ISR or SWR-style revalidation for product & page routes.
- WordPress: page-cache less critical once Nuxt owns HTML; keep object cache for REST.
- CDN: cache public Nuxt HTML + static assets; bypass for form POST and authenticated API.

## n8n

- Reusable **Abadis Website Audit** workflow (this project).
- Future: form → CRM/email, broken-link monitors, sitemap diff alerts, translation QA jobs.

## Liara deployment

- Nuxt app as Liara platform app (Node).
- Env vars in Liara panel (never commit secrets).
- Staging app + production app.
- WordPress may remain on current host initially; document API latency and TLS stability (audit host saw intermittent TLS/HTTP2 errors — FACT of auditor network path, not proof of end-user outage).

## Security boundaries

| Boundary | Rule |
|---|---|
| Public browser | Only public REST + public media |
| Nuxt server | May hold webhook secrets; never ship WP admin credentials to client |
| WordPress admin | Isolated; IP allowlist if possible |
| Forms | Server-side validation + spam protection; forward to n8n |
| Uploads | Remain WP-mediated; no open Nuxt upload to disk without auth |

## Preview / staging / production

1. **Audit/staging Nuxt** reads production WP (read-only) or a WP staging clone.  
2. **SEO staging** uses `noindex` until cutover.  
3. **Cutover:** DNS/Liara + redirect table verification + Search Console sitemap resubmit.  
4. **Rollback:** Point traffic back to WordPress theme rendering; keep WP content untouched during front cutover.
