const cfg = $('Load Config').first().json;
const sitemapUrl = $('Batch child sitemaps').item.json.sitemapUrl || $json.sitemapUrl;
const body = String($json.data || $json.body || '');
const status = $json.statusCode || $json.status || null;
const locs = [...body.matchAll(/<loc>(.*?)<\/loc>/gi)].map(m => m[1].trim());
const images = [...body.matchAll(/<image:loc>(.*?)<\/image:loc>/gi)].map(m => m[1].trim());
const lastmods = [...body.matchAll(/<lastmod>(.*?)<\/lastmod>/gi)].map(m => m[1].trim());
const name = String(sitemapUrl).split('/').pop() || 'unknown-sitemap.xml';
const type = name.replace('-sitemap.xml', '').replace('.xml', '');
const staticData = $getWorkflowStaticData('global');
const inv = staticData.audit.urlInventory;
const seen = new Set(inv.map(r => r.current_url));
for (let i = 0; i < locs.length; i++) {
  const url = locs[i];
  if (seen.has(url)) continue;
  seen.add(url);
  let language = 'fa';
  const lower = url.toLowerCase();
  if (lower.includes('/arabic/')) language = 'ar';
  else if (lower.includes('/en/')) language = 'en';
  inv.push({
    current_url: url,
    language,
    content_type: type,
    sitemap_source: name,
    lastmod: lastmods[i] || '',
    http_status: '',
    indexed_candidate: type === 'jet-menu' ? 'review' : 'yes',
    seo_importance: ['page', '_downloadcenter'].includes(type) ? 'high' : 'medium',
    target_url: url,
    migration_action: ['page', 'post', '_downloadcenter'].includes(type) ? 'PRESERVE' : 'REVIEW',
    redirect_required: 'no',
    redirect_target: '',
    notes: 'FACT: discovered via sitemap',
    confidence: 'medium',
    human_review_required: ['author', 'post_tag', 'jet-menu', '_customers', '_franchise', '_citynmg'].includes(type) ? 'yes' : 'no',
    discovery_method: 'sitemap',
  });
}
for (const img of images) {
  staticData.audit.mediaFromSitemaps.push({ url: img, source_sitemap: name, kind: 'sitemap_image' });
}
if (status && status >= 400) staticData.audit.errors.push({ stage: 'child_sitemap', sitemapUrl, status });
return { json: { ...cfg, sitemapUrl, status, locCount: locs.length, imageCount: images.length } };
