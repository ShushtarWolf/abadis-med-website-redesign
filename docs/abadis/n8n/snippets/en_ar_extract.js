const cfg = $('Load Config').first().json;
const seed = $('Batch EN AR seeds').item.json;
const html = String($json.data || $json.body || '');
const baseHost = 'abadis-med.com';
const staticData = $getWorkflowStaticData('global');
const inv = staticData.audit.urlInventory;
const seen = new Set(inv.map(r => r.current_url));
const added = [];
const re = /href=["']([^"']+)["']/gi;
let m;
while ((m = re.exec(html))) {
  let href = m[1];
  if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('javascript:')) continue;
  if (href.startsWith('//')) href = 'https:' + href;
  if (href.startsWith('/')) href = cfg.baseUrl.replace(/\/$/, '') + href;
  if (!href.includes(baseHost)) continue;
  const lower = href.toLowerCase();
  const isEn = lower.includes('/en/');
  const isAr = lower.includes('/arabic/');
  if (!isEn && !isAr) continue;
  const clean = href.split('#')[0].split('?')[0];
  if (seen.has(clean)) continue;
  seen.add(clean);
  const language = isAr ? 'ar' : 'en';
  inv.push({
    current_url: clean,
    language,
    content_type: 'lang_discovered',
    sitemap_source: 'EN_AR_LINK_DISCOVERY',
    lastmod: '',
    http_status: '',
    indexed_candidate: 'yes',
    seo_importance: 'high',
    target_url: clean,
    migration_action: 'PRESERVE',
    redirect_required: 'review',
    redirect_target: '',
    notes: 'FACT: discovered via same-host link from language root HTML; not assumed present in sitemap',
    confidence: 'medium',
    human_review_required: 'yes',
    discovery_method: 'en_ar_link_discovery',
    discovered_from: seed.crawlUrl,
  });
  added.push(clean);
}
staticData.audit.enArDiscovery.addedUrls.push(...added);
if (!seen.has(seed.crawlUrl)) {
  inv.push({
    current_url: seed.crawlUrl,
    language: seed.language,
    content_type: 'language_root',
    sitemap_source: 'NOT_IN_SITEMAP_OR_ADDED',
    lastmod: '',
    http_status: String($json.statusCode || ''),
    indexed_candidate: 'yes',
    seo_importance: 'critical',
    target_url: seed.crawlUrl,
    migration_action: 'PRESERVE',
    redirect_required: 'review',
    redirect_target: '',
    notes: 'FACT: language root fetched for deep discovery',
    confidence: 'high',
    human_review_required: 'yes',
    discovery_method: 'language_root_seed',
  });
}
return { json: { ...cfg, seed: seed.crawlUrl, addedCount: added.length, status: $json.statusCode || null } };
