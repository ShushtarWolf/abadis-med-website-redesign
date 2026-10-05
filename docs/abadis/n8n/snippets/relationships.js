const cfg = $('Load Config').first().json;
const staticData = $getWorkflowStaticData('global');
const audit = staticData.audit;
const pages = (audit.pageAudits || []).filter(p => p && p.url);
const inbound = new Map();
for (const p of pages) {
  for (const l of (p.internal_links || [])) {
    const href = (l.href || '').split('?')[0];
    if (!href) continue;
    if (!inbound.has(href)) inbound.set(href, []);
    inbound.get(href).push(p.url);
  }
}
const orphans = [];
for (const p of pages) {
  const refs = inbound.get(p.url) || [];
  if (refs.length === 0 && p.content_type !== 'language_root') {
    orphans.push({
      url: p.url,
      note: 'INFERENCE: no inbound internal links observed from crawled sample set only',
      classification: 'INFERENCE',
    });
  }
}
audit.orphans = orphans;
const relationships = [];
for (const p of pages) {
  const u = decodeURIComponent(String(p.url || ''));
  const productLike = /محصول|product|suction|کیسه|ساکشن|فیلتر|مخزن|canister|filter/i.test(u + ' ' + (p.title || ''));
  if (productLike) {
    relationships.push({
      from: p.url,
      kind: 'product_like_page',
      related_documents: p.documents || [],
      related_internal: (p.internal_links || [])
        .filter(l => /download|catalog|کاتالوگ|pdf|محصول|product/i.test(String(l.href || '') + String(l.anchor || '')))
        .slice(0, 10),
      classification: 'INFERENCE',
      note: 'INFERENCE: product-like based on URL/title keywords; not a confirmed CPT product record',
    });
  }
}
const wpItems = (audit.wpContent && audit.wpContent.items) || [];
for (const p of pages) {
  const pageKey = String(p.url || '').replace(/\/$/, '');
  if (!pageKey) continue;
  const match = wpItems.find(w => w && w.link && String(w.link).replace(/\/$/, '') === pageKey);
  if (match) {
    relationships.push({
      from: p.url,
      kind: 'wp_rest_match',
      wp_type: match.type_key,
      wp_id: match.id,
      classification: 'FACT',
      note: 'FACT: URL matches a public WP REST item link',
    });
  }
}
audit.relationships = relationships;
return [{ json: { ...cfg, orphanCount: orphans.length, relationshipCount: relationships.length } }];
