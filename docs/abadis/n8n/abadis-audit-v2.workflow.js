import { workflow, node, trigger, splitInBatches, nextBatch, ifElse, expr, newCredential } from '@n8n/workflow-sdk';

const start = trigger({
  type: 'n8n-nodes-base.manualTrigger',
  version: 1,
  config: { name: 'Manual Start', position: [0, 0] },
});

const config = node({
  type: 'n8n-nodes-base.set',
  version: 3.4,
  config: {
    name: 'Load Config',
    position: [220, 0],
    parameters: {
      mode: 'manual',
      includeOtherFields: false,
      assignments: {
        assignments: [
          { id: '1', name: 'baseUrl', type: 'string', value: 'https://abadis-med.com' },
          { id: '2', name: 'maxCrawlUrls', type: 'number', value: 15 },
          { id: '3', name: 'requestDelayMs', type: 'number', value: 800 },
          { id: '4', name: 'userAgent', type: 'string', value: 'AbadisAuditBot/1.0 (+migration-audit)' },
          { id: '5', name: 'runAi', type: 'boolean', value: true },
          { id: '6', name: 'includeLanguageRoots', type: 'boolean', value: true },
          { id: '7', name: 'wpPerPage', type: 'number', value: 50 },
          { id: '8', name: 'maxBrokenLinkChecks', type: 'number', value: 20 },
          { id: '9', name: 'wpMaxPagesPerEndpoint', type: 'number', value: 3 },
        ],
      },
    },
  },
});

const initAudit = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Clear audit state',
    position: [440, 0],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst staticData = $getWorkflowStaticData('global');\nstaticData.audit = {\n  config: cfg,\n  fetchedAt: new Date().toISOString(),\n  robotsTxt: '',\n  childSitemaps: [],\n  urlInventory: [],\n  mediaFromSitemaps: [],\n  pageAudits: [],\n  wpContent: { endpoints: [], items: [], totals: {} },\n  enArDiscovery: { seeds: [], addedUrls: [] },\n  linkChecks: [],\n  forms: [],\n  schemaRecords: [],\n  technology: {},\n  relationships: [],\n  orphans: [],\n  errors: [],\n};\nreturn [{ json: { ...cfg, auditCleared: true } }];\n" },
  },
});

const fetchRobots = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch robots.txt',
    position: [660, 0],
    parameters: {
      method: 'GET',
      url: expr('={{ $json.baseUrl }}/robots.txt'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: { parameters: [{ name: 'User-Agent', value: expr('={{ $json.userAgent }}') }] },
      options: { timeout: 45000, response: { response: { fullResponse: true, neverError: true, responseFormat: 'text' } } },
    },
    onError: 'continueRegularOutput',
  },
});

const storeRobots = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Store robots',
    position: [880, 0],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst body = String(items[0].json.data || items[0].json.body || '');\nconst staticData = $getWorkflowStaticData('global');\nstaticData.audit.robotsTxt = body;\nreturn [{ json: { ...cfg, robotsTxt: body, robotsStatus: items[0].json.statusCode || null } }];\n" },
  },
});

const fetchSitemapIndex = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch sitemap index',
    position: [1100, 0],
    parameters: {
      method: 'GET',
      url: expr('={{ $json.baseUrl }}/sitemap_index.xml'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: { parameters: [{ name: 'User-Agent', value: expr('={{ $json.userAgent }}') }] },
      options: { timeout: 60000, response: { response: { fullResponse: true, neverError: true, responseFormat: 'text' } } },
    },
    onError: 'continueRegularOutput',
  },
});

const parseSitemapIndex = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Parse child sitemaps',
    position: [1320, 0],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst body = String(items[0].json.data || items[0].json.body || '');\nconst locs = [...body.matchAll(/<loc>(.*?)<\\/loc>/gi)].map(m => m[1].trim());\nconst staticData = $getWorkflowStaticData('global');\nstaticData.audit.childSitemaps = locs;\nif (!locs.length) staticData.audit.errors.push({ stage: 'sitemap_index', message: 'No child sitemap locs found' });\nreturn locs.map(url => ({ json: { ...cfg, sitemapUrl: url } }));\n" },
  },
});

const sitemapBatch = splitInBatches({
  version: 3,
  config: { name: 'Batch child sitemaps', position: [1540, 0], parameters: { batchSize: 1 } },
});

const fetchChildSitemap = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch child sitemap',
    position: [1760, -120],
    parameters: {
      method: 'GET',
      url: expr('={{ $json.sitemapUrl }}'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: { parameters: [{ name: 'User-Agent', value: expr('={{ $json.userAgent }}') }] },
      options: { timeout: 90000, response: { response: { fullResponse: true, neverError: true, responseFormat: 'text' } } },
    },
    onError: 'continueRegularOutput',
    retryOnFail: true,
    maxTries: 3,
    waitBetweenTries: 1000,
  },
});

const extractSitemapUrls = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Extract sitemap URLs',
    position: [1980, -120],
    parameters: { mode: 'runOnceForEachItem', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst sitemapUrl = $('Batch child sitemaps').item.json.sitemapUrl || $json.sitemapUrl;\nconst body = String($json.data || $json.body || '');\nconst status = $json.statusCode || $json.status || null;\nconst locs = [...body.matchAll(/<loc>(.*?)<\\/loc>/gi)].map(m => m[1].trim());\nconst images = [...body.matchAll(/<image:loc>(.*?)<\\/image:loc>/gi)].map(m => m[1].trim());\nconst lastmods = [...body.matchAll(/<lastmod>(.*?)<\\/lastmod>/gi)].map(m => m[1].trim());\nconst name = String(sitemapUrl).split('/').pop() || 'unknown-sitemap.xml';\nconst type = name.replace('-sitemap.xml', '').replace('.xml', '');\nconst staticData = $getWorkflowStaticData('global');\nconst inv = staticData.audit.urlInventory;\nconst seen = new Set(inv.map(r => r.current_url));\nfor (let i = 0; i < locs.length; i++) {\n  const url = locs[i];\n  if (seen.has(url)) continue;\n  seen.add(url);\n  let language = 'fa';\n  const lower = url.toLowerCase();\n  if (lower.includes('/arabic/')) language = 'ar';\n  else if (lower.includes('/en/')) language = 'en';\n  inv.push({\n    current_url: url,\n    language,\n    content_type: type,\n    sitemap_source: name,\n    lastmod: lastmods[i] || '',\n    http_status: '',\n    indexed_candidate: type === 'jet-menu' ? 'review' : 'yes',\n    seo_importance: ['page', '_downloadcenter'].includes(type) ? 'high' : 'medium',\n    target_url: url,\n    migration_action: ['page', 'post', '_downloadcenter'].includes(type) ? 'PRESERVE' : 'REVIEW',\n    redirect_required: 'no',\n    redirect_target: '',\n    notes: 'FACT: discovered via sitemap',\n    confidence: 'medium',\n    human_review_required: ['author', 'post_tag', 'jet-menu', '_customers', '_franchise', '_citynmg'].includes(type) ? 'yes' : 'no',\n    discovery_method: 'sitemap',\n  });\n}\nfor (const img of images) {\n  staticData.audit.mediaFromSitemaps.push({ url: img, source_sitemap: name, kind: 'sitemap_image' });\n}\nif (status && status >= 400) staticData.audit.errors.push({ stage: 'child_sitemap', sitemapUrl, status });\nreturn { json: { ...cfg, sitemapUrl, status, locCount: locs.length, imageCount: images.length } };\n" },
  },
});

const waitSitemap = node({
  type: 'n8n-nodes-base.wait',
  version: 1.1,
  config: {
    name: 'Throttle sitemaps',
    position: [2200, -120],
    parameters: { resume: 'timeInterval', amount: 1, unit: 'seconds' },
  },
});

const fetchWpRoot = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch wp-json root',
    position: [1760, 160],
    parameters: {
      method: 'GET',
      url: expr("={{ $('Load Config').first().json.baseUrl }}/wp-json/"),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: { parameters: [{ name: 'User-Agent', value: expr("={{ $('Load Config').first().json.userAgent }}") }] },
      options: { timeout: 90000, response: { response: { fullResponse: true, neverError: true, responseFormat: 'json' } } },
    },
    onError: 'continueRegularOutput',
  },
});

const fetchWpTypes = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch WP types',
    position: [1980, 160],
    parameters: {
      method: 'GET',
      url: expr("={{ $('Load Config').first().json.baseUrl }}/wp-json/wp/v2/types"),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: { parameters: [{ name: 'User-Agent', value: expr("={{ $('Load Config').first().json.userAgent }}") }] },
      options: { timeout: 90000, response: { response: { fullResponse: true, neverError: true, responseFormat: 'json' } } },
    },
    onError: 'continueRegularOutput',
  },
});

const fetchWpTaxonomies = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch WP taxonomies',
    position: [2200, 160],
    parameters: {
      method: 'GET',
      url: expr("={{ $('Load Config').first().json.baseUrl }}/wp-json/wp/v2/taxonomies"),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: { parameters: [{ name: 'User-Agent', value: expr("={{ $('Load Config').first().json.userAgent }}") }] },
      options: { timeout: 90000, response: { response: { fullResponse: true, neverError: true, responseFormat: 'json' } } },
    },
    onError: 'continueRegularOutput',
  },
});

const buildWpEndpoints = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Build WP endpoints',
    position: [2420, 160],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst typesRaw = $('Fetch WP types').first().json;\nconst taxRaw = $('Fetch WP taxonomies').first().json;\nconst types = typesRaw.body || typesRaw.data || typesRaw;\nconst taxonomies = taxRaw.body || taxRaw.data || taxRaw;\nconst staticData = $getWorkflowStaticData('global');\nstaticData.audit.wpContent.types = types;\nstaticData.audit.wpContent.taxonomies = taxonomies;\nconst skip = new Set([\n  'wp_block', 'wp_template', 'wp_template_part', 'wp_global_styles',\n  'wp_navigation', 'wp_font_family', 'wp_font_face', 'jet-engine', 'nav_menu_item',\n]);\nconst endpoints = [];\nfor (const [key, meta] of Object.entries(types || {})) {\n  if (skip.has(key)) continue;\n  const rest = meta.rest_base;\n  if (!rest || String(rest).includes('(?P')) continue;\n  endpoints.push({ kind: 'type', key, rest_base: rest, path: '/wp-json/wp/v2/' + rest });\n}\nfor (const [key, meta] of Object.entries(taxonomies || {})) {\n  if (key === 'nav_menu' || key === 'wp_pattern_category') continue;\n  const rest = meta.rest_base;\n  if (!rest) continue;\n  endpoints.push({ kind: 'taxonomy', key, rest_base: rest, path: '/wp-json/wp/v2/' + rest });\n}\nstaticData.audit.wpContent.endpoints = endpoints;\nconst perPage = cfg.wpPerPage || 50;\nreturn endpoints.map(ep => ({\n  json: {\n    ...cfg,\n    ...ep,\n    endpointUrl: cfg.baseUrl.replace(/\\/$/, '') + ep.path + '?per_page=' + perPage,\n  },\n}));\n" },
  },
});

const wpBatch = splitInBatches({
  version: 3,
  config: { name: 'Batch WP endpoints', position: [2640, 160], parameters: { batchSize: 1 } },
});

const fetchWpEndpoint = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch WP endpoint pages',
    position: [2860, 80],
    parameters: {
      method: 'GET',
      url: expr('={{ $json.endpointUrl }}'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: { parameters: [{ name: 'User-Agent', value: expr('={{ $json.userAgent }}') }] },
      sendQuery: true,
      queryParameters: { parameters: [{ name: 'page', value: '1' }] },
      options: {
        timeout: 120000,
        response: { response: { fullResponse: true, neverError: true, responseFormat: 'json' } },
        pagination: {
          pagination: {
            paginationMode: 'updateAParameterInEachRequest',
            parameters: { parameters: [{ type: 'qs', name: 'page', value: '={{ $pageCount + 1 }}' }] },
            paginationCompleteWhen: 'other',
            completeExpression: '={{ Number($response.headers["x-wp-totalpages"] || $response.headers["X-WP-TotalPages"] || 1) <= $pageCount + 1 }}',
            limitPagesFetched: true,
            maxRequests: expr('={{ Number($json.wpMaxPagesPerEndpoint || 3) }}'),
            requestInterval: 800,
          },
        },
      },
    },
    onError: 'continueRegularOutput',
    retryOnFail: true,
    maxTries: 3,
    waitBetweenTries: 1000,
  },
});

const storeWpPage = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Store WP content page',
    position: [3080, 80],
    parameters: { mode: 'runOnceForEachItem', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst meta = $('Batch WP endpoints').item.json;\nconst status = $json.statusCode || null;\nconst headers = $json.headers || {};\nconst total = headers['x-wp-total'] || headers['X-WP-Total'] || null;\nconst totalPages = headers['x-wp-totalpages'] || headers['X-WP-TotalPages'] || null;\nlet body = $json.body !== undefined ? $json.body : $json.data;\nif (typeof body === 'string') {\n  try { body = JSON.parse(body); } catch (e) { body = []; }\n}\nif (!Array.isArray(body)) body = body ? [body] : [];\nconst staticData = $getWorkflowStaticData('global');\nconst key = meta.key || meta.rest_base;\nstaticData.audit.wpContent.totals[key] = {\n  total: total ? Number(total) : body.length,\n  totalPages: totalPages ? Number(totalPages) : null,\n  kind: meta.kind,\n};\nfor (const item of body) {\n  const title = item.title && item.title.rendered ? item.title.rendered : (item.name || item.slug || '');\n  const contentLen = item.content && item.content.rendered ? String(item.content.rendered).length : 0;\n  const yoast = item.yoast_head_json || null;\n  staticData.audit.wpContent.items.push({\n    id: item.id,\n    type_key: key,\n    rest_base: meta.rest_base,\n    kind: meta.kind,\n    link: item.link || null,\n    slug: item.slug || null,\n    title,\n    status: item.status || null,\n    template: item.template || null,\n    parent: item.parent ?? null,\n    modified: item.modified || null,\n    featured_media: item.featured_media ?? null,\n    content_length: contentLen,\n    acf_public: item.acf === undefined ? null : item.acf,\n    yoast_robots: yoast && yoast.robots ? yoast.robots : null,\n    yoast_title: yoast && yoast.title ? yoast.title : null,\n    mime_type: item.mime_type || null,\n    source_url: item.source_url || null,\n  });\n}\nif (status && status >= 400) {\n  staticData.audit.errors.push({ stage: 'wp_rest', endpoint: meta.path, status });\n}\nreturn { json: { ...cfg, rest_base: meta.rest_base, status, stored: body.length, total, totalPages } };\n" },
  },
});

const enArSeed = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Seed EN AR roots',
    position: [2860, 280],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst base = cfg.baseUrl.replace(/\\/$/, '');\nconst seeds = [\n  { crawlUrl: base + '/en/', language: 'en', role: 'language_root' },\n  { crawlUrl: base + '/arabic/', language: 'ar', role: 'language_root' },\n];\nconst staticData = $getWorkflowStaticData('global');\nstaticData.audit.enArDiscovery.seeds = seeds.map(s => s.crawlUrl);\nreturn seeds.map(s => ({ json: { ...cfg, ...s } }));\n" },
  },
});

const enArBatch = splitInBatches({
  version: 3,
  config: { name: 'Batch EN AR seeds', position: [3080, 280], parameters: { batchSize: 1 } },
});

const fetchEnAr = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch EN AR root',
    position: [3300, 200],
    parameters: {
      method: 'GET',
      url: expr('={{ $json.crawlUrl }}'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: { parameters: [{ name: 'User-Agent', value: expr('={{ $json.userAgent }}') }] },
      options: {
        timeout: 90000,
        redirect: { redirect: { followRedirects: true, maxRedirects: 5 } },
        response: { response: { fullResponse: true, neverError: true, responseFormat: 'text' } },
      },
    },
    onError: 'continueRegularOutput',
  },
});

const extractEnAr = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Extract EN AR links',
    position: [3520, 200],
    parameters: { mode: 'runOnceForEachItem', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst seed = $('Batch EN AR seeds').item.json;\nconst html = String($json.data || $json.body || '');\nconst baseHost = 'abadis-med.com';\nconst staticData = $getWorkflowStaticData('global');\nconst inv = staticData.audit.urlInventory;\nconst seen = new Set(inv.map(r => r.current_url));\nconst added = [];\nconst re = /href=[\"']([^\"']+)[\"']/gi;\nlet m;\nwhile ((m = re.exec(html))) {\n  let href = m[1];\n  if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('javascript:')) continue;\n  if (href.startsWith('//')) href = 'https:' + href;\n  if (href.startsWith('/')) href = cfg.baseUrl.replace(/\\/$/, '') + href;\n  if (!href.includes(baseHost)) continue;\n  const lower = href.toLowerCase();\n  const isEn = lower.includes('/en/');\n  const isAr = lower.includes('/arabic/');\n  if (!isEn && !isAr) continue;\n  const clean = href.split('#')[0].split('?')[0];\n  if (seen.has(clean)) continue;\n  seen.add(clean);\n  const language = isAr ? 'ar' : 'en';\n  inv.push({\n    current_url: clean,\n    language,\n    content_type: 'lang_discovered',\n    sitemap_source: 'EN_AR_LINK_DISCOVERY',\n    lastmod: '',\n    http_status: '',\n    indexed_candidate: 'yes',\n    seo_importance: 'high',\n    target_url: clean,\n    migration_action: 'PRESERVE',\n    redirect_required: 'review',\n    redirect_target: '',\n    notes: 'FACT: discovered via same-host link from language root HTML; not assumed present in sitemap',\n    confidence: 'medium',\n    human_review_required: 'yes',\n    discovery_method: 'en_ar_link_discovery',\n    discovered_from: seed.crawlUrl,\n  });\n  added.push(clean);\n}\nstaticData.audit.enArDiscovery.addedUrls.push(...added);\nif (!seen.has(seed.crawlUrl)) {\n  inv.push({\n    current_url: seed.crawlUrl,\n    language: seed.language,\n    content_type: 'language_root',\n    sitemap_source: 'NOT_IN_SITEMAP_OR_ADDED',\n    lastmod: '',\n    http_status: String($json.statusCode || ''),\n    indexed_candidate: 'yes',\n    seo_importance: 'critical',\n    target_url: seed.crawlUrl,\n    migration_action: 'PRESERVE',\n    redirect_required: 'review',\n    redirect_target: '',\n    notes: 'FACT: language root fetched for deep discovery',\n    confidence: 'high',\n    human_review_required: 'yes',\n    discovery_method: 'language_root_seed',\n  });\n}\nreturn { json: { ...cfg, seed: seed.crawlUrl, addedCount: added.length, status: $json.statusCode || null } };\n" },
  },
});

const waitEnAr = node({
  type: 'n8n-nodes-base.wait',
  version: 1.1,
  config: {
    name: 'Throttle EN AR',
    position: [3740, 200],
    parameters: { resume: 'timeInterval', amount: 1, unit: 'seconds' },
  },
});

const buildCrawl = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Build crawl list',
    position: [3300, 400],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst staticData = $getWorkflowStaticData('global');\nconst audit = staticData.audit;\nlet inventory = audit.urlInventory || [];\nconst seen = new Set(inventory.map(r => r.current_url));\nconst base = cfg.baseUrl.replace(/\\/$/, '');\nconst roots = [\n  { url: base + '/', language: 'fa', content_type: 'language_root' },\n  { url: base + '/en/', language: 'en', content_type: 'language_root' },\n  { url: base + '/arabic/', language: 'ar', content_type: 'language_root' },\n];\nif (cfg.includeLanguageRoots) {\n  for (const r of roots) {\n    if (seen.has(r.url)) continue;\n    inventory.push({\n      current_url: r.url,\n      language: r.language,\n      content_type: r.content_type,\n      sitemap_source: 'language_root',\n      lastmod: '',\n      http_status: '',\n      indexed_candidate: 'yes',\n      seo_importance: 'critical',\n      target_url: r.url,\n      migration_action: 'PRESERVE',\n      redirect_required: 'review',\n      redirect_target: '',\n      notes: 'Language root ensured for crawl',\n      confidence: 'high',\n      human_review_required: 'yes',\n      discovery_method: 'language_root',\n    });\n    seen.add(r.url);\n  }\n}\naudit.urlInventory = inventory;\naudit.pageAudits = [];\naudit.forms = [];\naudit.schemaRecords = [];\naudit.linkChecks = [];\n\nfunction score(row) {\n  const u = decodeURIComponent(row.current_url || '');\n  const l = u.toLowerCase();\n  if (row.content_type === 'language_root' || row.current_url === base + '/') return 0;\n  if (row.language === 'en' || row.language === 'ar') return 1;\n  if (l.includes('/en/') || l.includes('/arabic/')) return 1;\n  if (l.includes('/en/') && (l.includes('product') || l.includes('suction'))) return 1;\n  if (u.includes('\u0645\u062d\u0635\u0648\u0644\u0627\u062a') || u.includes('\u06a9\u06cc\u0633\u0647') || u.includes('\u0633\u0627\u06a9\u0634\u0646')) return 1;\n  if (l.includes('_downloadcenter') || u.includes('\u06a9\u0627\u062a\u0627\u0644\u0648\u06af') || l.includes('download') || l.includes('.pdf')) return 2;\n  if (row.content_type === '_downloadcenter') return 2;\n  if (row.content_type === 'page' || row.content_type === 'lang_discovered') return 3;\n  return 8;\n}\n\nconst forced = [];\nconst rest = [];\nfor (const row of inventory) {\n  const u = decodeURIComponent(row.current_url || '');\n  const l = u.toLowerCase();\n  if (row.content_type === 'language_root') forced.push(row);\n  else if (u.includes('\u0645\u062d\u0635\u0648\u0644\u0627\u062a') || u.includes('\u06a9\u06cc\u0633\u0647') || u.includes('\u0633\u0627\u06a9\u0634\u0646') || (l.includes('/en/') && l.includes('product'))) forced.push(row);\n  else if (row.content_type === '_downloadcenter' || l.includes('download') || u.includes('\u06a9\u0627\u062a\u0627\u0644\u0648\u06af')) forced.push(row);\n  else rest.push(row);\n}\nconst seenForce = new Set();\nconst forceUnique = [];\nfor (const r of forced) {\n  if (seenForce.has(r.current_url)) continue;\n  seenForce.add(r.current_url);\n  forceUnique.push(r);\n}\nconst crawlable = forceUnique.concat(\n  rest\n    .filter(r => !seenForce.has(r.current_url))\n    .filter(r => !String(r.current_url).includes('/wp-content/uploads/'))\n    .filter(r => r.content_type !== 'jet-menu')\n    .sort((a, b) => score(a) - score(b) || String(a.current_url).localeCompare(String(b.current_url)))\n).filter(r => !String(r.current_url).includes('/wp-content/uploads/'))\n  .filter(r => r.content_type !== 'jet-menu');\n\nconst max = Number(cfg.maxCrawlUrls || 0);\nconst selected = max > 0 ? crawlable.slice(0, max) : crawlable;\naudit.crawlSelectedCount = selected.length;\naudit.inventoryCount = inventory.length;\nreturn selected.map(row => ({\n  json: {\n    ...cfg,\n    crawlUrl: row.current_url,\n    content_type: row.content_type,\n    language: row.language,\n  },\n}));\n" },
  },
});

const pageBatch = splitInBatches({
  version: 3,
  config: { name: 'Batch page crawl', position: [3520, 400], parameters: { batchSize: 1 } },
});

const waitPage = node({
  type: 'n8n-nodes-base.wait',
  version: 1.1,
  config: {
    name: 'Throttle pages',
    position: [3740, 320],
    parameters: { resume: 'timeInterval', amount: 1, unit: 'seconds' },
  },
});

const resolveRedirects = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Resolve redirect chain',
    position: [3960, 320],
    parameters: { mode: 'runOnceForEachItem', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst incoming = $json || {};\nlet meta = incoming;\ntry {\n  const batch = $('Batch page crawl').item.json;\n  if (batch && batch.crawlUrl) meta = { ...incoming, ...batch };\n} catch (e) { /* use incoming */ }\nconst startUrl = meta.crawlUrl || incoming.crawlUrl;\nif (!startUrl) {\n  return {\n    json: {\n      ...cfg,\n      crawlUrl: null,\n      redirect_chain: [],\n      finalUrl: null,\n      finalStatus: null,\n      hopCount: 0,\n      error: 'FACT: missing crawlUrl on item',\n    },\n  };\n}\nconst ua = cfg.userAgent || 'AbadisAuditBot/1.0';\nconst hops = [];\nlet url = startUrl;\nlet finalUrl = startUrl;\nlet finalStatus = null;\nconst maxHops = 10;\n\nfor (let i = 0; i < maxHops; i++) {\n  let res;\n  try {\n    res = await this.helpers.httpRequest({\n      method: 'GET',\n      url,\n      headers: { 'User-Agent': ua, Accept: 'text/html,*/*' },\n      returnFullResponse: true,\n      ignoreHttpStatusErrors: true,\n      maxRedirects: 0,\n      timeout: 60000,\n    });\n  } catch (e) {\n    const errRes = e.response || (e.cause && e.cause.response) || null;\n    if (errRes) {\n      res = {\n        statusCode: errRes.statusCode || errRes.status,\n        headers: errRes.headers || {},\n      };\n    } else {\n      hops.push({\n        url,\n        status: null,\n        location: null,\n        error: String(e.message || e),\n        classification: 'FACT',\n      });\n      break;\n    }\n  }\n  const status = res.statusCode || res.status || null;\n  const headers = res.headers || {};\n  const location = headers.location || headers.Location || null;\n  hops.push({\n    url,\n    status,\n    location: location || null,\n    headers_subset: {\n      'cache-control': headers['cache-control'] || null,\n      'content-encoding': headers['content-encoding'] || null,\n      server: headers.server || null,\n      'x-robots-tag': headers['x-robots-tag'] || null,\n      'content-type': headers['content-type'] || null,\n    },\n    classification: 'FACT',\n  });\n  finalUrl = url;\n  finalStatus = status;\n  if (status && [301, 302, 303, 307, 308].includes(Number(status)) && location) {\n    if (location.startsWith('/')) {\n      url = cfg.baseUrl.replace(/\\/$/, '') + location;\n    } else if (location.startsWith('//')) {\n      url = 'https:' + location;\n    } else if (!/^https?:/i.test(location)) {\n      try {\n        url = new URL(location, url).toString();\n      } catch (e2) {\n        url = location;\n      }\n    } else {\n      url = location;\n    }\n    continue;\n  }\n  break;\n}\n\nreturn {\n  json: {\n    ...cfg,\n    crawlUrl: startUrl,\n    content_type: meta.content_type || incoming.content_type || null,\n    language: meta.language || incoming.language || null,\n    redirect_chain: hops,\n    finalUrl,\n    finalStatus,\n    hopCount: hops.length,\n  },\n};\n" },
  },
});

const fetchPage = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch page HTML',
    position: [4180, 320],
    parameters: {
      method: 'GET',
      url: expr("={{ $json.finalUrl || $json.crawlUrl }}"),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: { parameters: [{ name: 'User-Agent', value: expr("={{ $('Load Config').first().json.userAgent }}") }] },
      options: {
        timeout: 90000,
        redirect: { redirect: { followRedirects: true, maxRedirects: 5 } },
        response: { response: { fullResponse: true, neverError: true, responseFormat: 'text' } },
      },
    },
    onError: 'continueRegularOutput',
    retryOnFail: true,
    maxTries: 3,
    waitBetweenTries: 1000,
    alwaysOutputData: true,
  },
});

const analyzePage = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Analyze page SEO',
    position: [4400, 320],
    parameters: { mode: 'runOnceForEachItem', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nlet meta = {};\ntry { meta = $('Resolve redirect chain').item.json || {}; } catch (e) { meta = {}; }\nif (!meta.crawlUrl) {\n  try { meta = { ...meta, ...($('Batch page crawl').item.json || {}) }; } catch (e2) { /* ignore */ }\n}\nconst url = meta.crawlUrl;\nconst final = $json;\nconst html = String(final.data || final.body || '');\nconst finalStatus = final.statusCode || final.status || null;\nconst finalHeaders = final.headers || {};\nconst redirect_chain = Array.isArray(meta.redirect_chain) ? meta.redirect_chain.slice() : [];\nif (redirect_chain.length) {\n  const last = redirect_chain[redirect_chain.length - 1];\n  if (last && Number(last.status) !== Number(finalStatus)) {\n    redirect_chain.push({\n      url: meta.finalUrl || url,\n      status: finalStatus,\n      location: null,\n      note: 'FACT: final followed fetch status after hop walk',\n      headers_subset: {\n        'cache-control': finalHeaders['cache-control'] || null,\n        'content-encoding': finalHeaders['content-encoding'] || null,\n        server: finalHeaders.server || null,\n        'x-robots-tag': finalHeaders['x-robots-tag'] || null,\n        'content-type': finalHeaders['content-type'] || null,\n      },\n      classification: 'FACT',\n    });\n  } else if (last) {\n    last.headers_subset = {\n      ...(last.headers_subset || {}),\n      'cache-control': finalHeaders['cache-control'] || last.headers_subset?.['cache-control'] || null,\n      'content-encoding': finalHeaders['content-encoding'] || last.headers_subset?.['content-encoding'] || null,\n      server: finalHeaders.server || last.headers_subset?.server || null,\n      'content-type': finalHeaders['content-type'] || last.headers_subset?.['content-type'] || null,\n    };\n  }\n}\n\nif (!url) {\n  const staticData = $getWorkflowStaticData('global');\n  staticData.audit.errors.push({ stage: 'analyze_page', message: 'missing crawlUrl on paired item' });\n  return { json: { ...cfg, error: 'missing crawlUrl' } };\n}\n\nconst pick = (re) => { const m = html.match(re); return m ? m[1].trim() : null; };\nconst strip = (s) => String(s || '').replace(/<[^>]+>/g, ' ').replace(/\\s+/g, ' ').trim();\nconst title = pick(/<title[^>]*>([^<]+)<\\/title>/i);\nconst canonical = pick(/rel=[\"']canonical[\"'][^>]*href=[\"']([^\"']+)/i) || pick(/href=[\"']([^\"']+)[\"'][^>]*rel=[\"']canonical/i);\nconst description = pick(/name=[\"']description[\"'][^>]*content=[\"']([^\"']*)/i) || pick(/content=[\"']([^\"']*)[\"'][^>]*name=[\"']description/i);\nconst robots = pick(/name=[\"']robots[\"'][^>]*content=[\"']([^\"']*)/i) || pick(/content=[\"']([^\"']*)[\"'][^>]*name=[\"']robots/i);\nconst lang = pick(/<html[^>]*lang=[\"']([^\"']+)/i);\nconst h1 = [...html.matchAll(/<h1[^>]*>([\\s\\S]*?)<\\/h1>/gi)].map(m => strip(m[1])).filter(Boolean);\nconst h2 = [...html.matchAll(/<h2[^>]*>([\\s\\S]*?)<\\/h2>/gi)].map(m => strip(m[1])).filter(Boolean).slice(0, 40);\nconst h3 = [...html.matchAll(/<h3[^>]*>([\\s\\S]*?)<\\/h3>/gi)].map(m => strip(m[1])).filter(Boolean).slice(0, 40);\nconst hreflang = [];\nfor (const m of html.matchAll(/hreflang=[\"']([^\"']+)[\"'][^>]*href=[\"']([^\"']+)/gi)) hreflang.push({ lang: m[1], href: m[2] });\nfor (const m of html.matchAll(/href=[\"']([^\"']+)[\"'][^>]*hreflang=[\"']([^\"']+)/gi)) hreflang.push({ lang: m[2], href: m[1] });\nconst og = {};\nfor (const key of ['title', 'description', 'url', 'image', 'locale', 'type', 'site_name']) {\n  og[key] = pick(new RegExp('property=[\"\\']og:' + key + '[\"\\'][^>]*content=[\"\\']([^\"\\']*)', 'i'))\n    || pick(new RegExp('content=[\"\\']([^\"\\']*)[\"\\'][^>]*property=[\"\\']og:' + key, 'i'));\n}\nconst twitter = {};\nfor (const key of ['card', 'title', 'description', 'image', 'site']) {\n  twitter[key] = pick(new RegExp('name=[\"\\']twitter:' + key + '[\"\\'][^>]*content=[\"\\']([^\"\\']*)', 'i'))\n    || pick(new RegExp('content=[\"\\']([^\"\\']*)[\"\\'][^>]*name=[\"\\']twitter:' + key, 'i'));\n}\nconst schemaBlocks = [];\nconst schemaTypes = [];\nfor (const m of html.matchAll(/<script[^>]*type=[\"']application\\/ld\\+json[\"'][^>]*>([\\s\\S]*?)<\\/script>/gi)) {\n  const raw = m[1].trim();\n  try {\n    const data = JSON.parse(raw);\n    schemaBlocks.push(data);\n    if (data && data['@graph']) for (const n of data['@graph']) if (n && n['@type']) schemaTypes.push(n['@type']);\n    else if (Array.isArray(data)) for (const n of data) if (n && n['@type']) schemaTypes.push(n['@type']);\n    else if (data && data['@type']) schemaTypes.push(data['@type']);\n  } catch (e) {\n    schemaBlocks.push({ parse_error: true, raw_preview: raw.slice(0, 500) });\n  }\n}\nconst images = [];\nfor (const tag of html.matchAll(/<img\\b[^>]*>/gi)) {\n  const t = tag[0];\n  const src = (t.match(/(?:src|data-src)=[\"']([^\"']+)/i) || [])[1] || '';\n  const altM = t.match(/alt=[\"']([^\"']*)[\"']/i);\n  const loading = (t.match(/loading=[\"']([^\"']+)/i) || [])[1] || '';\n  images.push({ src, alt: altM ? altM[1] : null, missing_alt: !altM || !String(altM[1]).trim(), loading });\n}\nconst abs = (href) => {\n  if (!href) return null;\n  if (href.startsWith('//')) return 'https:' + href;\n  if (href.startsWith('/')) return cfg.baseUrl.replace(/\\/$/, '') + href;\n  return href;\n};\nconst internal_links = [];\nconst external_links = [];\nfor (const m of html.matchAll(/<a\\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>([\\s\\S]*?)<\\/a>/gi)) {\n  const href = m[1];\n  const anchor = strip(m[2]).slice(0, 160);\n  if (!href || href.startsWith('#') || href.startsWith('javascript:')) continue;\n  if (href.startsWith('mailto:') || href.startsWith('tel:')) continue;\n  const full = abs(href);\n  if (!full) continue;\n  if (full.includes('abadis-med.com') || href.startsWith('/')) internal_links.push({ href: full.split('#')[0], anchor });\n  else external_links.push({ href: full, anchor });\n}\nconst forms = [];\nfor (const fm of html.matchAll(/<form\\b([^>]*)>([\\s\\S]*?)<\\/form>/gi)) {\n  const attrs = fm[1];\n  const body = fm[2];\n  const action = ((attrs.match(/action=[\"']([^\"']*)[\"']/i) || [])[1]) || '';\n  const method = ((attrs.match(/method=[\"']([^\"']*)[\"']/i) || [])[1] || 'get').toLowerCase();\n  const fields = [];\n  for (const inp of body.matchAll(/<(input|select|textarea)\\b([^>]*)>/gi)) {\n    const a = inp[2];\n    fields.push({\n      tag: inp[1].toLowerCase(),\n      type: ((a.match(/type=[\"']([^\"']*)[\"']/i) || [])[1]) || '',\n      name: ((a.match(/name=[\"']([^\"']*)[\"']/i) || [])[1]) || '',\n      id: ((a.match(/id=[\"']([^\"']*)[\"']/i) || [])[1]) || '',\n    });\n  }\n  forms.push({ action: abs(action) || action, method, fields, page_url: url });\n}\nconst mailto = [...new Set([...html.matchAll(/mailto:([^\"'?\\s>]+)/gi)].map(m => m[1]))];\nconst tel = [...new Set([...html.matchAll(/tel:([^\"'?\\s>]+)/gi)].map(m => m[1]))];\nconst whatsapp = [...new Set([...html.matchAll(/https?:\\/\\/(?:wa\\.me|api\\.whatsapp\\.com)[^\"'\\s>]*/gi)].map(m => m[0]))];\nconst documents = [...new Set([...html.matchAll(/https?:\\/\\/[^\"'\\s>]+\\.(?:pdf|docx?|xlsx?|pptx?|zip)(?:\\?[^\"'\\s>]*)?/gi)].map(m => m[0]))];\nconst tech = {\n  elementor: /elementor/i.test(html),\n  yoast: /yoast/i.test(html),\n  jet_menu: /jet-menu|jet_menu/i.test(html),\n  jet_engine: /jet-engine|jet_engine/i.test(html),\n  uikit: /\\buk-|uikit/i.test(html),\n  bdthemes: /bdt-|element-pack/i.test(html),\n  dynamic_content_elementor: /dce-|dynamic-content-for-elementor/i.test(html),\n  whatsapp: whatsapp.length > 0 || /whatsapp/i.test(html),\n  forms: forms.length > 0 || /elementor-form|wpcf7/i.test(html),\n};\nconst http_signals = {\n  cache_control: finalHeaders['cache-control'] || null,\n  content_encoding: finalHeaders['content-encoding'] || null,\n  server: finalHeaders.server || null,\n  x_robots_tag: finalHeaders['x-robots-tag'] || null,\n  content_type: finalHeaders['content-type'] || null,\n  content_length: finalHeaders['content-length'] || html.length,\n};\nconst auditRow = {\n  url,\n  language: meta.language,\n  content_type: meta.content_type,\n  final_url: meta.finalUrl || url,\n  http_status: finalStatus,\n  redirect_chain,\n  http_signals,\n  title,\n  canonical,\n  meta_description: description,\n  robots_meta: robots,\n  html_lang: lang,\n  h1,\n  h2,\n  h3,\n  hreflang,\n  og,\n  twitter,\n  schema_types: schemaTypes,\n  schema_blocks: schemaBlocks,\n  images: images.slice(0, 100),\n  img_count: images.length,\n  img_missing_alt: images.filter(i => i.missing_alt).length,\n  internal_links: internal_links.slice(0, 200),\n  external_links: external_links.slice(0, 100),\n  internal_link_count: internal_links.length,\n  external_link_count: external_links.length,\n  forms,\n  mailto,\n  tel,\n  whatsapp,\n  documents,\n  tech_signals: tech,\n  html_bytes: html.length,\n  classification: 'FACT',\n};\nconst staticData = $getWorkflowStaticData('global');\nstaticData.audit.pageAudits.push(auditRow);\nfor (const f of forms) staticData.audit.forms.push(f);\nfor (const block of schemaBlocks) {\n  const types = [];\n  if (block && block['@graph']) for (const n of block['@graph']) if (n && n['@type']) types.push(n['@type']);\n  else if (Array.isArray(block)) for (const n of block) if (n && n['@type']) types.push(n['@type']);\n  else if (block && block['@type']) types.push(block['@type']);\n  staticData.audit.schemaRecords.push({ page_url: url, types, raw: block });\n}\nfor (const k of Object.keys(tech)) {\n  if (!tech[k]) continue;\n  staticData.audit.technology[k] = staticData.audit.technology[k] || { signal: true, pages: [] };\n  if (staticData.audit.technology[k].pages.length < 30) staticData.audit.technology[k].pages.push(url);\n}\nconst inv = staticData.audit.urlInventory || [];\nfor (const row of inv) if (row.current_url === url) row.http_status = String(finalStatus || '');\nreturn { json: { ...cfg, url, http_status: finalStatus, title, internal_link_count: internal_links.length, form_count: forms.length } };\n" },
  },
});

const collectLinks = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Collect internal links',
    position: [3960, 520],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst staticData = $getWorkflowStaticData('global');\nconst pages = staticData.audit.pageAudits || [];\nconst seen = new Set();\nconst links = [];\nfor (const p of pages) {\n  for (const l of (p.internal_links || [])) {\n    const href = (l.href || '').split('?')[0];\n    if (!href || seen.has(href)) continue;\n    if (href.includes('/wp-admin') || href.includes('/wp-json')) continue;\n    seen.add(href);\n    links.push(href);\n  }\n}\nconst max = Number(cfg.maxBrokenLinkChecks || 40);\nconst selected = links.slice(0, max);\nstaticData.audit.linkCheckQueueSize = selected.length;\nstaticData.audit.linkCheckUniverse = links.length;\nif (!selected.length) return [{ json: { ...cfg, linkUrl: cfg.baseUrl, skip: true } }];\nreturn selected.map(linkUrl => ({ json: { ...cfg, linkUrl, skip: false } }));\n" },
  },
});

const linkBatch = splitInBatches({
  version: 3,
  config: { name: 'Batch link checks', position: [4180, 520], parameters: { batchSize: 1 } },
});

const waitLink = node({
  type: 'n8n-nodes-base.wait',
  version: 1.1,
  config: {
    name: 'Throttle links',
    position: [4400, 440],
    parameters: { resume: 'timeInterval', amount: 1, unit: 'seconds' },
  },
});

const checkLink = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Check broken link',
    position: [4620, 440],
    parameters: {
      method: 'HEAD',
      url: expr('={{ $json.skip ? $(\'Load Config\').first().json.baseUrl : $json.linkUrl }}'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: { parameters: [{ name: 'User-Agent', value: expr('={{ $json.userAgent }}') }] },
      options: {
        timeout: 30000,
        redirect: { redirect: { followRedirects: true, maxRedirects: 5 } },
        response: { response: { fullResponse: true, neverError: true, responseFormat: 'text' } },
      },
    },
    onError: 'continueRegularOutput',
    alwaysOutputData: true,
  },
});

const storeLink = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Store link check',
    position: [4840, 440],
    parameters: { mode: 'runOnceForEachItem', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst meta = $('Batch link checks').item.json;\nif (meta.skip) return { json: { ...cfg, skipped: true } };\nconst status = $json.statusCode || $json.status || null;\nconst staticData = $getWorkflowStaticData('global');\nstaticData.audit.linkChecks.push({\n  url: meta.linkUrl,\n  http_status: status,\n  ok: status >= 200 && status < 400,\n  content_type: ($json.headers || {})['content-type'] || null,\n  classification: 'FACT',\n});\nreturn { json: { ...cfg, linkUrl: meta.linkUrl, status } };\n" },
  },
});

const relationships = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Orphans and relationships',
    position: [4620, 620],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst staticData = $getWorkflowStaticData('global');\nconst audit = staticData.audit;\nconst pages = (audit.pageAudits || []).filter(p => p && p.url);\nconst inbound = new Map();\nfor (const p of pages) {\n  for (const l of (p.internal_links || [])) {\n    const href = (l.href || '').split('?')[0];\n    if (!href) continue;\n    if (!inbound.has(href)) inbound.set(href, []);\n    inbound.get(href).push(p.url);\n  }\n}\nconst orphans = [];\nfor (const p of pages) {\n  const refs = inbound.get(p.url) || [];\n  if (refs.length === 0 && p.content_type !== 'language_root') {\n    orphans.push({\n      url: p.url,\n      note: 'INFERENCE: no inbound internal links observed from crawled sample set only',\n      classification: 'INFERENCE',\n    });\n  }\n}\naudit.orphans = orphans;\nconst relationships = [];\nfor (const p of pages) {\n  const u = decodeURIComponent(String(p.url || ''));\n  const productLike = /\u0645\u062d\u0635\u0648\u0644|product|suction|\u06a9\u06cc\u0633\u0647|\u0633\u0627\u06a9\u0634\u0646|\u0641\u06cc\u0644\u062a\u0631|\u0645\u062e\u0632\u0646|canister|filter/i.test(u + ' ' + (p.title || ''));\n  if (productLike) {\n    relationships.push({\n      from: p.url,\n      kind: 'product_like_page',\n      related_documents: p.documents || [],\n      related_internal: (p.internal_links || [])\n        .filter(l => /download|catalog|\u06a9\u0627\u062a\u0627\u0644\u0648\u06af|pdf|\u0645\u062d\u0635\u0648\u0644|product/i.test(String(l.href || '') + String(l.anchor || '')))\n        .slice(0, 10),\n      classification: 'INFERENCE',\n      note: 'INFERENCE: product-like based on URL/title keywords; not a confirmed CPT product record',\n    });\n  }\n}\nconst wpItems = (audit.wpContent && audit.wpContent.items) || [];\nfor (const p of pages) {\n  const pageKey = String(p.url || '').replace(/\\/$/, '');\n  if (!pageKey) continue;\n  const match = wpItems.find(w => w && w.link && String(w.link).replace(/\\/$/, '') === pageKey);\n  if (match) {\n    relationships.push({\n      from: p.url,\n      kind: 'wp_rest_match',\n      wp_type: match.type_key,\n      wp_id: match.id,\n      classification: 'FACT',\n      note: 'FACT: URL matches a public WP REST item link',\n    });\n  }\n}\naudit.relationships = relationships;\nreturn [{ json: { ...cfg, orphanCount: orphans.length, relationshipCount: relationships.length } }];\n" },
  },
});

const normalize = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Normalize evidence',
    position: [4840, 620],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst staticData = $getWorkflowStaticData('global');\nconst audit = staticData.audit;\nconst wpRoot = $('Fetch wp-json root').first().json;\naudit.wp = audit.wp || {};\naudit.wp.namespaces = (wpRoot.body && wpRoot.body.namespaces) || wpRoot.namespaces || [];\naudit.wp.rootStatus = wpRoot.statusCode || null;\nconst evidence = {\n  meta: {\n    generated_at: new Date().toISOString(),\n    domain: cfg.baseUrl,\n    maxCrawlUrls: cfg.maxCrawlUrls,\n    classification_scheme: ['FACT', 'INFERENCE', 'RECOMMENDATION', 'UNKNOWN_HUMAN_REVIEW'],\n    rejected_concept: 'concept-preview/ is REJECTED CONCEPT \u2014 VISUAL REFERENCE ONLY',\n  },\n  discovery: {\n    robotsTxt: audit.robotsTxt,\n    childSitemaps: audit.childSitemaps,\n    inventoryCount: (audit.urlInventory || []).length,\n    crawlSelectedCount: audit.crawlSelectedCount || 0,\n    enArAdded: (audit.enArDiscovery && audit.enArDiscovery.addedUrls) || [],\n  },\n  urlInventory: (audit.urlInventory || []).map(u => ({\n    ...u,\n    url: u.current_url || u.url,\n  })),\n  pageAudits: audit.pageAudits,\n  mediaFromSitemaps: audit.mediaFromSitemaps,\n  wpContent: {\n    totals: audit.wpContent.totals,\n    endpointCount: (audit.wpContent.endpoints || []).length,\n    itemCount: (audit.wpContent.items || []).length,\n    items: audit.wpContent.items,\n    types: audit.wpContent.types,\n    taxonomies: audit.wpContent.taxonomies,\n  },\n  forms: audit.forms,\n  schemaRecords: audit.schemaRecords,\n  technology: audit.technology,\n  linkChecks: audit.linkChecks,\n  orphans: audit.orphans,\n  relationships: audit.relationships,\n  wordpress: audit.wp,\n  errors: audit.errors,\n};\nstaticData.audit.evidence = evidence;\n\nconst summary = {\n  inventoryCount: evidence.discovery.inventoryCount,\n  crawled: evidence.pageAudits.length,\n  childSitemaps: evidence.discovery.childSitemaps,\n  enArDiscoveredCount: evidence.discovery.enArAdded.length,\n  wpTotals: evidence.wpContent.totals,\n  wpItemCount: evidence.wpContent.itemCount,\n  formCount: evidence.forms.length,\n  schemaPageCount: evidence.schemaRecords.length,\n  linkChecks: {\n    checked: evidence.linkChecks.length,\n    broken: evidence.linkChecks.filter(l => !l.ok).length,\n  },\n  orphans: evidence.orphans,\n  relationships_sample: evidence.relationships.slice(0, 30),\n  technology: evidence.technology,\n  samplePages: evidence.pageAudits.map(p => ({\n    url: p.url,\n    status: p.http_status,\n    title: p.title,\n    lang: p.html_lang,\n    canonical: p.canonical,\n    robots: p.robots_meta,\n    h1: p.h1,\n    h2_count: (p.h2 || []).length,\n    hreflang: p.hreflang,\n    og: p.og,\n    twitter: p.twitter,\n    schema_types: p.schema_types,\n    redirect_chain: p.redirect_chain,\n    http_signals: p.http_signals,\n    img_count: p.img_count,\n    missing_alt: p.img_missing_alt,\n    internal_links: p.internal_link_count,\n    external_links: p.external_link_count,\n    forms: (p.forms || []).length,\n    documents: p.documents,\n    mailto: p.mailto,\n    tel: p.tel,\n    whatsapp: p.whatsapp,\n    tech: p.tech_signals,\n  })),\n  errors: evidence.errors,\n};\n\nconst evidenceSummary = [\n  'Abadis Med migration audit EVIDENCE ONLY. Every claim must be labeled FACT, INFERENCE, RECOMMENDATION, or UNKNOWN/HUMAN REVIEW.',\n  'Rejected local concept-preview remains REJECTED CONCEPT \u2014 VISUAL REFERENCE ONLY.',\n  'Cover in the plan: SEO, URLs/redirects, content, WordPress/CPTs, multilingual FA/EN/AR, media, forms/business, product architecture, Nuxt 4, headless WordPress, 3D/GLB, Liara, security, performance, testing, launch, rollback.',\n  'Do not invent URLs, fields, plugins, or business rules not supported by evidence.',\n  'Never recommend DELETE; use REVIEW when uncertain.',\n  JSON.stringify(summary).slice(0, 120000),\n].join('\\n\\n');\n\nreturn [{ json: { ...cfg, evidence, evidenceSummary, runAi: cfg.runAi } }];\n" },
  },
});

const aiGate = ifElse({
  version: 2.2,
  config: {
    name: 'AI enabled?',
    position: [5060, 620],
    parameters: {
      conditions: {
        options: { caseSensitive: true, leftValue: '', typeValidation: 'strict', version: 2 },
        conditions: [{ id: 'c1', leftValue: expr('={{ $json.runAi }}'), rightValue: true, operator: { type: 'boolean', operation: 'true', singleValue: true } }],
        combinator: 'and',
      },
    },
  },
});

const aiDraft = node({
  type: '@n8n/n8n-nodes-langchain.openAi',
  version: 2.3,
  config: {
    name: 'AI Draft Plan',
    position: [5280, 500],
    credentials: { openAiApi: newCredential('OpenAI Gateway') },
    parameters: {
      resource: 'text',
      operation: 'response',
      modelId: { __rl: true, mode: 'id', value: 'gpt-4.1-mini' },
      responses: { values: [
        { type: 'text', role: 'system', content: "You are the Abadis Med migration architect. Produce an evidence-based draft plan for Nuxt 4 + headless WordPress + Tailwind/Nuxt UI + Three.js/GLB + Liara + n8n. EVIDENCE RULES: Use ONLY the provided crawl/WP/export evidence. Do not invent URLs, CPT fields, plugins, forms, media, or business rules. LABELING (required on every major claim): FACT | INFERENCE | RECOMMENDATION | UNKNOWN/HUMAN REVIEW. If evidence is missing, write UNKNOWN/HUMAN REVIEW \u2014 never guess. Never recommend DELETE; use REVIEW. concept-preview/ is REJECTED CONCEPT \u2014 VISUAL REFERENCE ONLY (not approved design). REQUIRED SECTIONS (each with labels): 1) SEO (titles/meta/canonical/robots/hreflang/schema/sitemap gaps) 2) URL inventory & redirect map 3) Content model & page types 4) WordPress/CPTs/JetEngine public REST surface & totals (X-WP-Total) 5) Multilingual architecture FA/EN/AR (lang attributes, discovery vs sitemap, Arabic lang issues) 6) Media & documents (images alt/loading, PDFs, WP media) 7) Forms & business functionality (actions/methods/fields, mailto/tel/WhatsApp) 8) Product architecture & relationships (label INFERENCE clearly) 9) Nuxt 4 frontend architecture 10) Headless WordPress data/API strategy 11) 3D/GLB handling 12) Liara hosting/deploy 13) Security 14) Performance & caching headers observed 15) Testing strategy 16) Launch checklist 17) Rollback plan Cite concrete evidence URLs/counts from the payload when stating FACTS." },
        { type: 'text', role: 'user', content: expr('={{ $json.evidenceSummary }}') },
      ] },
      simplify: true,
      options: { maxTokens: 4500 },
    },
    onError: 'continueRegularOutput',
  },
});

const attachDraft = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Attach draft plan',
    position: [5500, 500],
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: "const base = $('Normalize evidence').first().json;\nconst draft = items[0].json.text || items[0].json.output || items[0].json.content || JSON.stringify(items[0].json);\nreturn [{ json: { ...base, draftPlan: draft, evidenceSummary: base.evidenceSummary + '\\n\\n--- DRAFT PLAN ---\\n' + String(draft).slice(0, 50000) } }];",
    },
  },
});

const aiQa = node({
  type: '@n8n/n8n-nodes-langchain.openAi',
  version: 2.3,
  config: {
    name: 'AI QA Review',
    position: [5720, 500],
    credentials: { openAiApi: newCredential('OpenAI Gateway') },
    parameters: {
      resource: 'text',
      operation: 'response',
      modelId: { __rl: true, mode: 'id', value: 'gpt-4.1-mini' },
      responses: { values: [
        { type: 'text', role: 'system', content: "You are a strict QA reviewer of an Abadis Med migration draft. Return only findings: gaps, unsupported assumptions, contradictions, missing FACT labels, overconfident INFERENCES, and risks for SEO, URLs, multilingual FA/EN/AR, WordPress/CPTs, media, forms, product relationships, Nuxt 4, headless WP, 3D/GLB, Liara, security, performance, testing, launch, rollback. Label each finding FACT / INFERENCE / UNKNOWN/HUMAN REVIEW. Do not invent evidence. Do not rewrite the full plan." },
        { type: 'text', role: 'user', content: expr('={{ $json.evidenceSummary }}') },
      ] },
      simplify: true,
      options: { maxTokens: 3000 },
    },
    onError: 'continueRegularOutput',
  },
});

const attachQa = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Attach QA findings',
    position: [5940, 500],
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: "const base = $('Attach draft plan').first().json;\nconst qa = items[0].json.text || items[0].json.output || items[0].json.content || JSON.stringify(items[0].json);\nreturn [{ json: { ...base, qaFindings: qa, evidenceSummary: base.evidenceSummary + '\\n\\n--- QA FINDINGS ---\\n' + String(qa).slice(0, 40000) } }];",
    },
  },
});

const aiFinal = node({
  type: '@n8n/n8n-nodes-langchain.openAi',
  version: 2.3,
  config: {
    name: 'AI Final Plan',
    position: [6160, 500],
    credentials: { openAiApi: newCredential('OpenAI Gateway') },
    parameters: {
      resource: 'text',
      operation: 'response',
      modelId: { __rl: true, mode: 'id', value: 'gpt-4.1-mini' },
      responses: { values: [
        { type: 'text', role: 'system', content: "Synthesize the final Abadis Med migration master plan from EVIDENCE + DRAFT + QA. Every major statement must be labeled FACT, INFERENCE, RECOMMENDATION, or UNKNOWN/HUMAN REVIEW. No invented data. No DELETE recommendations. Preserve SEO equity, URLs, and media unless evidence forces REVIEW. concept-preview remains REJECTED CONCEPT \u2014 VISUAL REFERENCE ONLY. Deliver complete actionable coverage: SEO, URLs/redirects, content, WordPress/CPTs, multilingual FA/EN/AR, media, forms/business functionality, product architecture, Nuxt 4, headless WordPress, 3D/GLB, Liara, security, performance, testing, launch, and rollback. Include an open HUMAN REVIEW queue list for UNKNOWN items." },
        { type: 'text', role: 'user', content: expr('={{ $json.evidenceSummary }}') },
      ] },
      simplify: true,
      options: { maxTokens: 5000 },
    },
    onError: 'continueRegularOutput',
  },
});

const packExports = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Pack export payloads',
    position: [6380, 620],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: "const cfg = $('Load Config').first().json;\nconst staticData = $getWorkflowStaticData('global');\nconst evidence = staticData.audit.evidence;\n\nconst aiNodes = ['AI Draft Plan', 'AI QA Review', 'AI Final Plan'];\nconst aiOutputs = {};\nfor (const name of aiNodes) {\n  try {\n    const n = $(name).first().json;\n    aiOutputs[name] = n.text || n.output || n.content || n.message?.content || n;\n  } catch (e) {\n    aiOutputs[name] = null;\n  }\n}\ntry {\n  const attached = $('Attach QA findings').first().json;\n  if (attached.draftPlan) aiOutputs['AI Draft Plan'] = attached.draftPlan;\n  if (attached.qaFindings) aiOutputs['AI QA Review'] = attached.qaFindings;\n} catch (e) { /* AI may be skipped */ }\ntry {\n  const final = $('AI Final Plan').first().json;\n  aiOutputs['AI Final Plan'] = final.text || final.output || final.content || final.message?.content || final;\n} catch (e) { /* skipped */ }\n\nconst esc = (v) => {\n  const s = v == null ? '' : String(v);\n  return /[\",\\n\\r]/.test(s) ? '\"' + s.replace(/\"/g, '\"\"') + '\"' : s;\n};\nconst toCsv = (rows, headers) => {\n  const lines = [headers.join(',')];\n  for (const r of rows) lines.push(headers.map(h => esc(r[h] == null ? '' : r[h])).join(','));\n  return lines.join('\\n');\n};\n\nconst inventoryRows = (evidence.urlInventory || []).map(u => ({\n  url: u.current_url || u.url || '',\n  source: u.sitemap_source || u.source || u.discovery_method || '',\n  language: u.language || '',\n  content_type: u.content_type || '',\n  classification: u.classification || 'FACT',\n  lastmod: u.lastmod || '',\n  notes: u.notes || '',\n}));\nconst pageRows = (evidence.pageAudits || []).map(p => ({\n  url: p.url,\n  final_url: p.final_url || '',\n  http_status: p.http_status,\n  title: p.title,\n  meta_description: p.meta_description,\n  canonical: p.canonical,\n  robots_meta: p.robots_meta,\n  html_lang: p.html_lang,\n  h1: (p.h1 || []).join(' | '),\n  h2: (p.h2 || []).join(' | '),\n  h3: (p.h3 || []).join(' | '),\n  og_title: p.og?.title || '',\n  og_description: p.og?.description || '',\n  og_image: p.og?.image || '',\n  twitter_card: p.twitter?.card || '',\n  hreflang: JSON.stringify(p.hreflang || []),\n  schema_types: (p.schema_types || []).join('|'),\n  redirect_chain: JSON.stringify(p.redirect_chain || []),\n  internal_links: p.internal_link_count,\n  external_links: p.external_link_count,\n  forms: (p.forms || []).length,\n  documents: (p.documents || []).join('|'),\n  mailto: (p.mailto || []).join('|'),\n  tel: (p.tel || []).join('|'),\n  whatsapp: (p.whatsapp || []).join('|'),\n  img_count: p.img_count,\n  img_missing_alt: p.img_missing_alt,\n  cache_control: p.http_signals?.cache_control || '',\n  content_encoding: p.http_signals?.content_encoding || '',\n  server: p.http_signals?.server || '',\n  tech: JSON.stringify(p.tech_signals || {}),\n  classification: 'FACT',\n}));\nconst mediaRows = [];\nfor (const m of (evidence.mediaFromSitemaps || [])) {\n  mediaRows.push({\n    source: 'sitemap',\n    url: m.loc || m.url || m.current_url || String(m),\n    alt: '',\n    loading: '',\n    page_url: '',\n    classification: 'FACT',\n  });\n}\nfor (const p of (evidence.pageAudits || [])) {\n  for (const img of (p.images || [])) {\n    mediaRows.push({\n      source: 'page_img',\n      url: img.src,\n      alt: img.alt || '',\n      loading: img.loading || '',\n      page_url: p.url,\n      classification: 'FACT',\n    });\n  }\n  for (const d of (p.documents || [])) {\n    mediaRows.push({ source: 'document', url: d, alt: '', loading: '', page_url: p.url, classification: 'FACT' });\n  }\n}\nfor (const w of (evidence.wpContent?.items || []).filter(i => i.mime_type || i.source_url)) {\n  mediaRows.push({\n    source: 'wp_media',\n    url: w.source_url || w.link || '',\n    alt: w.title || '',\n    loading: '',\n    page_url: w.link || '',\n    classification: 'FACT',\n  });\n}\nconst linkRows = [];\nfor (const p of (evidence.pageAudits || [])) {\n  for (const l of (p.internal_links || [])) {\n    linkRows.push({ page_url: p.url, href: l.href, anchor: l.anchor, rel: l.rel || '', kind: 'internal', http_status: '', classification: 'FACT' });\n  }\n  for (const l of (p.external_links || [])) {\n    linkRows.push({ page_url: p.url, href: l.href, anchor: l.anchor, rel: l.rel || '', kind: 'external', http_status: '', classification: 'FACT' });\n  }\n}\nfor (const c of (evidence.linkChecks || [])) {\n  linkRows.push({\n    page_url: '',\n    href: c.url,\n    anchor: '',\n    rel: '',\n    kind: c.ok ? 'broken_check_ok' : 'broken_check_fail',\n    http_status: c.http_status,\n    classification: 'FACT',\n  });\n}\nconst formRows = (evidence.forms || []).map(f => ({\n  page_url: f.page_url,\n  action: f.action,\n  method: f.method,\n  fields: JSON.stringify(f.fields || []),\n  classification: 'FACT',\n}));\nconst schemaRows = (evidence.schemaRecords || []).map(s => ({\n  page_url: s.page_url,\n  schema_types: (s.types || []).join('|'),\n  json_ld: JSON.stringify(s.raw || s.schema || s),\n  classification: 'FACT',\n}));\nconst wpRows = (evidence.wpContent?.items || []).map(w => ({\n  type_key: w.type_key,\n  id: w.id,\n  slug: w.slug,\n  status: w.status,\n  link: w.link,\n  title: typeof w.title === 'string' ? w.title : (w.title?.rendered || ''),\n  modified: w.modified || '',\n  total_hint: JSON.stringify(evidence.wpContent?.totals?.[w.type_key] || {}),\n  classification: 'FACT',\n}));\nconst techRows = [];\nfor (const [k, v] of Object.entries(evidence.technology || {})) {\n  techRows.push({\n    key: k,\n    value: typeof v === 'object' ? JSON.stringify(v) : String(v),\n    page_url: '',\n    classification: 'FACT',\n  });\n}\nfor (const p of (evidence.pageAudits || [])) {\n  for (const [k, v] of Object.entries(p.tech_signals || {})) {\n    if (!v) continue;\n    techRows.push({ key: k, value: String(v), page_url: p.url, classification: 'FACT' });\n  }\n}\nconst orphanRows = (evidence.orphans || []).map(o => ({\n  url: o.url,\n  note: o.note,\n  classification: o.classification || 'INFERENCE',\n}));\nconst relRows = (evidence.relationships || []).map(r => ({\n  from: r.from,\n  kind: r.kind,\n  related: JSON.stringify(r.related_documents || r.related_internal || { wp_type: r.wp_type, wp_id: r.wp_id } || ''),\n  note: r.note,\n  classification: r.classification || 'INFERENCE',\n}));\n\nconst masterPlan = {\n  meta: evidence.meta,\n  evidence_summary: {\n    inventoryCount: (evidence.urlInventory || []).length,\n    crawled: (evidence.pageAudits || []).length,\n    wpTotals: evidence.wpContent?.totals,\n    forms: (evidence.forms || []).length,\n    linkChecks: (evidence.linkChecks || []).length,\n    orphans: (evidence.orphans || []).length,\n    relationships: (evidence.relationships || []).length,\n  },\n  ai: aiOutputs,\n  labeling_required: ['FACT', 'INFERENCE', 'RECOMMENDATION', 'UNKNOWN_HUMAN_REVIEW'],\n  rejected_concept: 'concept-preview/ REJECTED CONCEPT \u2014 VISUAL REFERENCE ONLY',\n};\n\nconst exportMap = {\n  'URL-INVENTORY.csv': toCsv(inventoryRows, ['url', 'source', 'language', 'content_type', 'classification', 'lastmod', 'notes']),\n  'PAGE-AUDIT.csv': toCsv(pageRows, [\n    'url', 'final_url', 'http_status', 'title', 'meta_description', 'canonical', 'robots_meta', 'html_lang',\n    'h1', 'h2', 'h3', 'og_title', 'og_description', 'og_image', 'twitter_card', 'hreflang',\n    'schema_types', 'redirect_chain', 'internal_links', 'external_links', 'forms', 'documents',\n    'mailto', 'tel', 'whatsapp', 'img_count', 'img_missing_alt', 'cache_control', 'content_encoding',\n    'server', 'tech', 'classification',\n  ]),\n  'MEDIA.csv': toCsv(mediaRows, ['source', 'url', 'alt', 'loading', 'page_url', 'classification']),\n  'LINKS.csv': toCsv(linkRows, ['page_url', 'href', 'anchor', 'rel', 'kind', 'http_status', 'classification']),\n  'FORMS.csv': toCsv(formRows, ['page_url', 'action', 'method', 'fields', 'classification']),\n  'SCHEMA.csv': toCsv(schemaRows, ['page_url', 'schema_types', 'json_ld', 'classification']),\n  'WP-CONTENT.csv': toCsv(wpRows, ['type_key', 'id', 'slug', 'status', 'link', 'title', 'modified', 'total_hint', 'classification']),\n  'TECHNOLOGY.csv': toCsv(techRows, ['key', 'value', 'page_url', 'classification']),\n  'ORPHANS.csv': toCsv(orphanRows, ['url', 'note', 'classification']),\n  'RELATIONSHIPS.csv': toCsv(relRows, ['from', 'kind', 'related', 'note', 'classification']),\n  'ABADIS-AUDIT.json': JSON.stringify(evidence, null, 2),\n  'MASTER-PLAN.json': JSON.stringify(masterPlan, null, 2),\n};\n\nconst items = Object.entries(exportMap).map(([fileName, content]) => ({\n  json: {\n    fileName,\n    mimeType: fileName.endsWith('.json') ? 'application/json' : 'text/csv',\n    content,\n    exportKeys: Object.keys(exportMap),\n    aiKeys: Object.keys(aiOutputs).filter(k => aiOutputs[k]),\n    inventoryCount: inventoryRows.length,\n    pageCount: pageRows.length,\n    mediaCount: mediaRows.length,\n    linkCount: linkRows.length,\n    formCount: formRows.length,\n    schemaCount: schemaRows.length,\n    wpCount: wpRows.length,\n    techCount: techRows.length,\n  },\n}));\nreturn items;\n" },
  },
});

const exportFiles = node({
  type: 'n8n-nodes-base.convertToFile',
  version: 1.1,
  config: {
    name: 'Convert exports to files',
    position: [6600, 620],
    parameters: {
      operation: 'toText',
      sourceProperty: 'content',
      binaryPropertyName: 'data',
      options: { fileName: expr('={{ $json.fileName }}'), mimeType: expr('={{ $json.mimeType }}') },
    },
  },
});

export default workflow('abadis-website-audit-v2', 'Abadis Website Audit v2')
  .add(start)
  .to(config)
  .to(initAudit)
  .to(fetchRobots)
  .to(storeRobots)
  .to(fetchSitemapIndex)
  .to(parseSitemapIndex)
  .to(sitemapBatch.onEachBatch(fetchChildSitemap.to(extractSitemapUrls).to(waitSitemap).to(nextBatch(sitemapBatch))).onDone(fetchWpRoot))
  .to(fetchWpTypes)
  .to(fetchWpTaxonomies)
  .to(buildWpEndpoints)
  .to(wpBatch.onEachBatch(fetchWpEndpoint.to(storeWpPage).to(nextBatch(wpBatch))).onDone(enArSeed))
  .to(enArBatch.onEachBatch(fetchEnAr.to(extractEnAr).to(waitEnAr).to(nextBatch(enArBatch))).onDone(buildCrawl))
  .to(pageBatch.onEachBatch(waitPage.to(resolveRedirects).to(fetchPage).to(analyzePage).to(nextBatch(pageBatch))).onDone(collectLinks))
  .to(linkBatch.onEachBatch(waitLink.to(checkLink).to(storeLink).to(nextBatch(linkBatch))).onDone(relationships))
  .to(normalize)
  .to(aiGate.onTrue(aiDraft.to(attachDraft).to(aiQa).to(attachQa).to(aiFinal.to(packExports.to(exportFiles)))).onFalse(packExports.to(exportFiles)))
  .group('Load configuration', [config, initAudit], { description: 'Sets audit config and clears prior run state every execution' })
  .group('Discover site maps', [fetchRobots, storeRobots, fetchSitemapIndex, parseSitemapIndex], { description: 'Loads robots and parses the sitemap index into child sitemap URLs' })
  .group('AI plan stages', [aiDraft, attachDraft, aiQa, attachQa, aiFinal], { description: 'Draft, QA, and final evidence-based migration plan via Gateway OpenAI' });
