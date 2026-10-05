const cfg = $('Load Config').first().json;
const body = String(items[0].json.data || items[0].json.body || '');
const locs = [...body.matchAll(/<loc>(.*?)<\/loc>/gi)].map(m => m[1].trim());
const staticData = $getWorkflowStaticData('global');
staticData.audit.childSitemaps = locs;
if (!locs.length) staticData.audit.errors.push({ stage: 'sitemap_index', message: 'No child sitemap locs found' });
return locs.map(url => ({ json: { ...cfg, sitemapUrl: url } }));
