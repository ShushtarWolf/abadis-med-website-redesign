const cfg = $('Load Config').first().json;
const staticData = $getWorkflowStaticData('global');
const pages = staticData.audit.pageAudits || [];
const seen = new Set();
const links = [];
for (const p of pages) {
  for (const l of (p.internal_links || [])) {
    const href = (l.href || '').split('?')[0];
    if (!href || seen.has(href)) continue;
    if (href.includes('/wp-admin') || href.includes('/wp-json')) continue;
    seen.add(href);
    links.push(href);
  }
}
const maxRaw = cfg.maxBrokenLinkChecks;
const max = maxRaw === undefined || maxRaw === null || maxRaw === '' ? 40 : Number(maxRaw);
const selected = max > 0 ? links.slice(0, max) : [];
staticData.audit.linkCheckQueueSize = selected.length;
staticData.audit.linkCheckUniverse = links.length;
if (!selected.length) return [{ json: { ...cfg, linkUrl: cfg.baseUrl, skip: true } }];
return selected.map(linkUrl => ({ json: { ...cfg, linkUrl, skip: false } }));
