const cfg = $('Load Config').first().json;
const staticData = $getWorkflowStaticData('global');
const audit = staticData.audit;
let inventory = audit.urlInventory || [];
const seen = new Set(inventory.map(r => r.current_url));
const base = cfg.baseUrl.replace(/\/$/, '');
const roots = [
  { url: base + '/', language: 'fa', content_type: 'language_root' },
  { url: base + '/en/', language: 'en', content_type: 'language_root' },
  { url: base + '/arabic/', language: 'ar', content_type: 'language_root' },
];
function normUrl(u) {
  return String(u || '').replace(/\/$/, '') || u;
}
function isFormLike(row) {
  const u = decodeURIComponent(row.current_url || '');
  const l = u.toLowerCase();
  if (/\.(css|js|map|png|jpe?g|gif|svg|webp|woff2?|ttf|eot)(\?|$)/i.test(l)) return false;
  return (
    u.includes('همکاری') ||
    l.includes('collaboration') ||
    l.includes('calculator') ||
    u.includes('ماشین') ||
    u.includes('محاسبه') ||
    u.includes('تماس') ||
    l.includes('contact')
  );
}
function isProductLike(row) {
  const u = decodeURIComponent(row.current_url || '');
  const l = u.toLowerCase();
  return (
    u.includes('محصولات') ||
    u.includes('کیسه') ||
    u.includes('ساکشن') ||
    (l.includes('/en/') && l.includes('product'))
  );
}
function isDownloadLike(row) {
  const u = decodeURIComponent(row.current_url || '');
  const l = u.toLowerCase();
  return (
    row.content_type === '_downloadcenter' ||
    l.includes('_downloadcenter') ||
    l.includes('download') ||
    u.includes('کاتالوگ') ||
    l.includes('.pdf')
  );
}
if (cfg.includeLanguageRoots) {
  for (const r of roots) {
    const existing = inventory.find(row => normUrl(row.current_url) === normUrl(r.url));
    if (existing) {
      existing.language = r.language;
      existing.content_type = 'language_root';
      existing.seo_importance = 'critical';
      continue;
    }
    inventory.push({
      current_url: r.url,
      language: r.language,
      content_type: r.content_type,
      sitemap_source: 'language_root',
      lastmod: '',
      http_status: '',
      indexed_candidate: 'yes',
      seo_importance: 'critical',
      target_url: r.url,
      migration_action: 'PRESERVE',
      redirect_required: 'review',
      redirect_target: '',
      notes: 'Language root ensured for crawl',
      confidence: 'high',
      human_review_required: 'yes',
      discovery_method: 'language_root',
    });
    seen.add(r.url);
  }
}
audit.urlInventory = inventory;
audit.pageAudits = [];
audit.forms = [];
audit.schemaRecords = [];
audit.linkChecks = [];

function score(row) {
  const u = decodeURIComponent(row.current_url || '');
  const l = u.toLowerCase();
  if (row.content_type === 'language_root' || row.current_url === base + '/') return 0;
  if (isFormLike(row)) return 0;
  if (row.language === 'en' || row.language === 'ar') return 1;
  if (l.includes('/en/') || l.includes('/arabic/')) return 1;
  if (isProductLike(row)) return 1;
  if (isDownloadLike(row)) return 2;
  if (row.content_type === 'page' || row.content_type === 'lang_discovered') return 3;
  return 8;
}

const rootUrlSet = new Set(roots.map(r => normUrl(r.url)));
// Guarantee FA/EN/AR roots lead the crawl even when sitemap already listed them as page/post.
const rootRows = cfg.includeLanguageRoots ? roots.map(r => {
  const hit = inventory.find(row => normUrl(row.current_url) === normUrl(r.url));
  if (hit) {
    hit.language = r.language;
    hit.content_type = 'language_root';
    hit.seo_importance = 'critical';
    return hit;
  }
  return {
    current_url: r.url,
    language: r.language,
    content_type: 'language_root',
    sitemap_source: 'language_root',
    lastmod: '',
    http_status: '',
    indexed_candidate: 'yes',
    seo_importance: 'critical',
    target_url: r.url,
    migration_action: 'PRESERVE',
    redirect_required: 'review',
    redirect_target: '',
    notes: 'Language root ensured for crawl',
    confidence: 'high',
    human_review_required: 'yes',
    discovery_method: 'language_root',
  };
}) : [];
const forms = [];
const products = [];
const downloads = [];
const rest = [];
for (const row of inventory) {
  if (rootUrlSet.has(normUrl(row.current_url))) continue;
  if (isFormLike(row)) forms.push(row);
  else if (isDownloadLike(row)) downloads.push(row);
  else if (isProductLike(row)) products.push(row);
  else rest.push(row);
}
const seenForce = new Set();
const forceUnique = [];
// Force-include early: language roots, form-like pages, FA products, downloads.
for (const r of rootRows.concat(forms, products, downloads)) {
  if (seenForce.has(r.current_url)) continue;
  seenForce.add(r.current_url);
  forceUnique.push(r);
}
const crawlable = forceUnique.concat(
  rest
    .filter(r => !seenForce.has(r.current_url))
    .filter(r => !String(r.current_url).includes('/wp-content/uploads/'))
    .filter(r => r.content_type !== 'jet-menu')
    .sort((a, b) => score(a) - score(b) || String(a.current_url).localeCompare(String(b.current_url)))
).filter(r => !String(r.current_url).includes('/wp-content/uploads/'))
  .filter(r => r.content_type !== 'jet-menu');

const max = Number(cfg.maxCrawlUrls || 0);
const selected = max > 0 ? crawlable.slice(0, max) : crawlable;
audit.crawlSelectedCount = selected.length;
audit.inventoryCount = inventory.length;
return selected.map(row => ({
  json: {
    ...cfg,
    crawlUrl: row.current_url,
    content_type: row.content_type,
    language: row.language,
  },
}));
