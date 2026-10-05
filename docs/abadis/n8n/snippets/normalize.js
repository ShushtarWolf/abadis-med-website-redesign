const cfg = $('Load Config').first().json;
const staticData = $getWorkflowStaticData('global');
const audit = staticData.audit;
const wpRoot = $('Fetch wp-json root').first().json;
audit.wp = audit.wp || {};
audit.wp.namespaces = (wpRoot.body && wpRoot.body.namespaces) || wpRoot.namespaces || [];
audit.wp.rootStatus = wpRoot.statusCode || null;

const urlInventory = (audit.urlInventory || []).map(u => ({
  ...u,
  url: u.current_url || u.url,
}));
const wpTotals = (audit.wpContent && audit.wpContent.totals) || {};
const wpItems = (audit.wpContent && audit.wpContent.items) || [];
const enArAdded = (audit.enArDiscovery && audit.enArDiscovery.addedUrls) || [];
const mediaFromSitemaps = audit.mediaFromSitemaps || [];
const pageAudits = audit.pageAudits || [];

// --- Complete inventories (counts from discovery; not invented) ---
const inventories = {
  urls: {
    classification: 'FACT',
    complete: true,
    count: urlInventory.length,
    sources: ['sitemap', 'language_root', 'en_ar_link_discovery'],
    note: 'FACT: union of sitemap locs + ensured language roots + same-host EN/AR link discovery',
  },
  wordpress_rest_totals: {
    classification: 'FACT',
    complete: true,
    totals: wpTotals,
    note: 'FACT: X-WP-Total / X-WP-TotalPages from public REST headers (inventory of record counts)',
  },
  wordpress_rest_items_fetched: {
    classification: 'FACT',
    complete: false,
    count: wpItems.length,
    note: 'FACT: items actually downloaded this run (may be capped by wpMaxPagesPerEndpoint). Totals above are the complete counts.',
  },
  en_ar_discovery: {
    classification: 'FACT',
    complete: true,
    seeds: (audit.enArDiscovery && audit.enArDiscovery.seeds) || [],
    addedCount: enArAdded.length,
    note: 'FACT: deep discovery from /en/ and /arabic/ HTML; not sitemap-only',
  },
  media_sitemap: {
    classification: 'FACT',
    complete: true,
    count: mediaFromSitemaps.length,
    note: 'FACT: image:loc entries from child sitemaps',
  },
  page_html_audits: {
    classification: 'FACT',
    complete: false,
    count: pageAudits.length,
    maxCrawlUrls: cfg.maxCrawlUrls,
    note: Number(cfg.maxCrawlUrls) === 0
      ? 'FACT: maxCrawlUrls=0 — attempted full HTML crawl of inventory'
      : 'FACT: HTML/SEO page audits are a SAMPLE capped by maxCrawlUrls; URL inventory above is the complete URL set',
  },
  forms_from_crawled_pages: {
    classification: 'FACT',
    complete: false,
    count: (audit.forms || []).length,
    note: 'FACT: forms observed only on crawled HTML sample',
  },
  link_checks: {
    classification: 'FACT',
    complete: false,
    count: (audit.linkChecks || []).length,
    note: 'FACT: broken-link HEAD checks only for queued internal links this run',
  },
};

// --- ONE merged evidence dataset ---
const evidence = {
  meta: {
    generated_at: new Date().toISOString(),
    domain: cfg.baseUrl,
    maxCrawlUrls: cfg.maxCrawlUrls,
    pipeline: [
      'URL+WP+EN/AR+media inventories',
      'merge → one evidence dataset',
      'AI Draft',
      'AI QA',
      'AI Final',
      'MASTER MIGRATION PLAN',
    ],
    classification_scheme: ['FACT', 'INFERENCE', 'RECOMMENDATION', 'UNKNOWN_HUMAN_REVIEW'],
    rejected_concept: 'concept-preview/ is REJECTED CONCEPT — VISUAL REFERENCE ONLY',
  },
  inventories,
  discovery: {
    robotsTxt: audit.robotsTxt,
    childSitemaps: audit.childSitemaps,
    inventoryCount: urlInventory.length,
    crawlSelectedCount: audit.crawlSelectedCount || 0,
    enArAdded,
  },
  urlInventory,
  pageAudits,
  mediaFromSitemaps,
  wpContent: {
    totals: wpTotals,
    endpointCount: (audit.wpContent.endpoints || []).length,
    itemCount: wpItems.length,
    items: wpItems,
    types: audit.wpContent.types,
    taxonomies: audit.wpContent.taxonomies,
  },
  forms: audit.forms,
  schemaRecords: audit.schemaRecords,
  technology: audit.technology,
  linkChecks: audit.linkChecks,
  orphans: audit.orphans,
  relationships: audit.relationships,
  wordpress: audit.wp,
  errors: audit.errors,
};
staticData.audit.evidence = evidence;

const byLang = { fa: 0, en: 0, ar: 0, other: 0 };
for (const u of urlInventory) {
  const lang = u.language || 'other';
  if (byLang[lang] != null) byLang[lang]++;
  else byLang.other++;
}

const summary = {
  pipeline: evidence.meta.pipeline,
  inventories,
  inventoryCount: urlInventory.length,
  inventoryByLanguage: byLang,
  crawledHtmlSample: pageAudits.length,
  childSitemaps: evidence.discovery.childSitemaps,
  enArDiscoveredCount: enArAdded.length,
  wpTotals,
  wpItemCount: wpItems.length,
  formCount: (audit.forms || []).length,
  schemaPageCount: (audit.schemaRecords || []).length,
  mediaSitemapCount: mediaFromSitemaps.length,
  linkChecks: {
    checked: (audit.linkChecks || []).length,
    broken: (audit.linkChecks || []).filter(l => !l.ok).length,
  },
  orphans: audit.orphans,
  relationships_sample: (audit.relationships || []).slice(0, 30),
  technology: audit.technology,
  urlInventory_sample: urlInventory.slice(0, 80).map(u => ({
    url: u.url,
    language: u.language,
    content_type: u.content_type,
    source: u.sitemap_source || u.discovery_method,
  })),
  samplePages: pageAudits.map(p => ({
    url: p.url,
    status: p.http_status,
    title: p.title,
    lang: p.html_lang,
    canonical: p.canonical,
    robots: p.robots_meta,
    h1: p.h1,
    h2_count: (p.h2 || []).length,
    hreflang: p.hreflang,
    og: p.og,
    twitter: p.twitter,
    schema_types: p.schema_types,
    redirect_chain: p.redirect_chain,
    http_signals: p.http_signals,
    img_count: p.img_count,
    missing_alt: p.img_missing_alt,
    internal_links: p.internal_link_count,
    external_links: p.external_link_count,
    forms: (p.forms || []).length,
    documents: p.documents,
    mailto: p.mailto,
    tel: p.tel,
    whatsapp: p.whatsapp,
    tech: p.tech_signals,
  })),
  errors: evidence.errors,
};

const evidenceSummary = [
  'Abadis Med migration audit — ONE MERGED EVIDENCE DATASET.',
  'Pipeline: complete inventories → merge → AI Draft → AI QA → AI Final → MASTER MIGRATION PLAN.',
  'Label every claim: FACT | INFERENCE | RECOMMENDATION | UNKNOWN/HUMAN REVIEW.',
  'URL inventory + WP REST totals + EN/AR discovery are COMPLETE inventories (FACT). HTML page audits / forms / link-checks may be SAMPLED — see inventories.*.complete flags.',
  'Rejected concept-preview remains REJECTED CONCEPT — VISUAL REFERENCE ONLY.',
  'Cover: SEO, URLs/redirects, content, WordPress/CPTs, multilingual FA/EN/AR, media, forms/business, product architecture, Nuxt 4, headless WordPress, 3D/GLB, Liara, security, performance, testing, launch, rollback.',
  'Do not invent data. Never recommend DELETE; use REVIEW when uncertain.',
  JSON.stringify(summary).slice(0, 60000),
].join('\n\n');

return [{
  json: {
    ...cfg,
    evidence,
    evidenceSummary,
    runAi: cfg.runAi,
    inventoryCount: urlInventory.length,
    inventoriesComplete: {
      urls: inventories.urls.count,
      wpTotalsKeys: Object.keys(wpTotals).length,
      enArAdded: enArAdded.length,
      mediaSitemap: mediaFromSitemaps.length,
      pageSample: pageAudits.length,
    },
  },
}];
