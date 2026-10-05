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
    position: [240, 0],
    parameters: {
      mode: 'manual',
      includeOtherFields: false,
      assignments: {
        assignments: [
          { id: '1', name: 'baseUrl', type: 'string', value: 'https://abadis-med.com' },
          { id: '2', name: 'maxCrawlUrls', type: 'number', value: 5 },
          { id: '3', name: 'requestDelayMs', type: 'number', value: 800 },
          { id: '4', name: 'userAgent', type: 'string', value: 'AbadisAuditBot/1.0 (+migration-audit)' },
          { id: '5', name: 'runAi', type: 'boolean', value: false },
          { id: '6', name: 'includeLanguageRoots', type: 'boolean', value: true },
          { id: '7', name: 'wpPerPage', type: 'number', value: 20 },
          { id: '8', name: 'wpMaxPagesPerType', type: 'number', value: 2 },
        ],
      },
    },
  },
});

const fetchRobots = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch robots.txt',
    position: [480, 0],
    parameters: {
      method: 'GET',
      url: expr('={{ $json.baseUrl }}/robots.txt'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {
        parameters: [{ name: 'User-Agent', value: expr('={{ $json.userAgent }}') }],
      },
      options: {
        timeout: 45000,
        response: {
          response: { fullResponse: true, neverError: true, responseFormat: 'text' },
        },
      },
    },
    onError: 'continueRegularOutput',
  },
});

const attachRobots = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Store robots + config',
    position: [720, 0],
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const cfg = $('Load Config').first().json;
const robotsItem = items[0] || {};
const body = typeof robotsItem.json.body === 'string' ? robotsItem.json.body : (robotsItem.json.data || '');
const staticData = $getWorkflowStaticData('global');
staticData.audit = {
  config: cfg,
  robotsTxt: body,
  fetchedAt: new Date().toISOString(),
  childSitemaps: [],
  urlInventory: [],
  pageAudits: [],
  wp: {},
  errors: [],
};
return [{ json: { ...cfg, robotsTxt: body, robotsStatus: robotsItem.json.statusCode || robotsItem.json.status || null } }];`,
    },
  },
});

const fetchSitemapIndex = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch sitemap index',
    position: [960, 0],
    parameters: {
      method: 'GET',
      url: expr('={{ $json.baseUrl }}/sitemap_index.xml'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {
        parameters: [{ name: 'User-Agent', value: expr('={{ $json.userAgent }}') }],
      },
      options: {
        timeout: 60000,
        response: {
          response: { fullResponse: true, neverError: true, responseFormat: 'text' },
        },
      },
    },
    onError: 'continueRegularOutput',
  },
});

const parseSitemapIndex = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Parse child sitemaps',
    position: [1200, 0],
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const cfg = $('Load Config').first().json;
const body = String(items[0].json.body || items[0].json.data || '');
const locs = [...body.matchAll(/<loc>(.*?)<\\/loc>/gi)].map(m => m[1].trim());
const staticData = $getWorkflowStaticData('global');
staticData.audit = staticData.audit || {};
staticData.audit.sitemapIndexXml = body.slice(0, 50000);
staticData.audit.childSitemaps = locs;
if (!locs.length) {
  staticData.audit.errors.push({ stage: 'sitemap_index', message: 'No child sitemap locs found' });
}
return locs.map(url => ({ json: { ...cfg, sitemapUrl: url } }));`,
    },
  },
});

const sitemapBatch = splitInBatches({
  version: 3,
  config: {
    name: 'Batch child sitemaps',
    position: [1440, 0],
    parameters: { batchSize: 1 },
  },
});

const fetchChildSitemap = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch child sitemap',
    position: [1680, -80],
    parameters: {
      method: 'GET',
      url: expr('={{ $json.sitemapUrl }}'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {
        parameters: [{ name: 'User-Agent', value: expr('={{ $json.userAgent }}') }],
      },
      options: {
        timeout: 90000,
        response: {
          response: { fullResponse: true, neverError: true, responseFormat: 'text' },
        },
      },
    },
    onError: 'continueRegularOutput',
  },
});

const extractSitemapUrls = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Extract sitemap URLs',
    position: [1920, -80],
    parameters: {
      mode: 'runOnceForEachItem',
      language: 'javaScript',
      jsCode: `const cfg = $('Load Config').first().json;
const sitemapUrl = $json.sitemapUrl || ($('Batch child sitemaps').item.json.sitemapUrl);
const body = String($json.body || $json.data || '');
const status = $json.statusCode || $json.status || null;
const locs = [...body.matchAll(/<loc>(.*?)<\\/loc>/gi)].map(m => m[1].trim());
const images = [...body.matchAll(/<image:loc>(.*?)<\\/image:loc>/gi)].map(m => m[1].trim());
const lastmods = [...body.matchAll(/<lastmod>(.*?)<\\/lastmod>/gi)].map(m => m[1].trim());
const name = String(sitemapUrl).split('/').pop() || 'unknown-sitemap.xml';
const type = name.replace('-sitemap.xml','').replace('.xml','');
const staticData = $getWorkflowStaticData('global');
staticData.audit = staticData.audit || { urlInventory: [], errors: [] };
staticData.audit.urlInventory = staticData.audit.urlInventory || [];
for (let i = 0; i < locs.length; i++) {
  const url = locs[i];
  let language = 'fa';
  const lower = url.toLowerCase();
  if (lower.includes('/arabic/') || lower.endsWith('/arabic')) language = 'ar';
  else if (lower.includes('/en/') || lower.endsWith('/en')) language = 'en';
  staticData.audit.urlInventory.push({
    current_url: url,
    language,
    content_type: type,
    sitemap_source: name,
    lastmod: lastmods[i] || '',
    http_status: '',
    indexed_candidate: type === 'jet-menu' ? 'review' : 'yes',
    seo_importance: ['page','_downloadcenter'].includes(type) ? 'high' : 'medium',
    target_url: url,
    migration_action: ['page','post','_downloadcenter'].includes(type) ? 'PRESERVE' : 'REVIEW',
    redirect_required: 'no',
    redirect_target: '',
    notes: 'FACT: discovered via sitemap',
    confidence: 'medium',
    human_review_required: ['author','post_tag','jet-menu','_customers','_franchise','_citynmg'].includes(type) ? 'yes' : 'no',
  });
}
staticData.audit.mediaFromSitemaps = staticData.audit.mediaFromSitemaps || [];
for (const img of images) {
  staticData.audit.mediaFromSitemaps.push({ url: img, source_sitemap: name });
}
if (status && status >= 400) {
  staticData.audit.errors.push({ stage: 'child_sitemap', sitemapUrl, status });
}
return { json: { ...cfg, sitemapUrl, status, locCount: locs.length, imageCount: images.length } };`,
    },
  },
});


const buildCrawlList = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Build crawl list',
    position: [1680, 160],
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const cfg = $('Load Config').first().json;
const staticData = $getWorkflowStaticData('global');
const audit = staticData.audit || {};
let inventory = audit.urlInventory || [];
const seen = new Set(inventory.map(r => r.current_url));
if (cfg.includeLanguageRoots) {
  const roots = [
    { url: cfg.baseUrl.replace(/\\/$/, '') + '/', language: 'fa', content_type: 'language_root' },
    { url: cfg.baseUrl.replace(/\\/$/, '') + '/en/', language: 'en', content_type: 'language_root' },
    { url: cfg.baseUrl.replace(/\\/$/, '') + '/arabic/', language: 'ar', content_type: 'language_root' },
  ];
  for (const r of roots) {
    if (!seen.has(r.url)) {
      inventory.push({
        current_url: r.url,
        language: r.language,
        content_type: r.content_type,
        sitemap_source: seen.size ? 'NOT_IN_SITEMAP_OR_ADDED' : 'language_root',
        lastmod: '',
        http_status: '',
        indexed_candidate: 'yes',
        seo_importance: 'critical',
        target_url: r.url,
        migration_action: 'PRESERVE',
        redirect_required: 'review',
        redirect_target: '',
        notes: 'FACT/INFERENCE: language root ensured for crawl even if absent from sitemap',
        confidence: 'high',
        human_review_required: 'yes',
      });
      seen.add(r.url);
    }
  }
}
audit.urlInventory = inventory;
staticData.audit = audit;

// Prefer language roots + pages first for crawl ordering
const priority = (row) => {
  if (row.content_type === 'language_root') return 0;
  if (row.content_type === 'page') return 1;
  if (row.content_type === '_downloadcenter') return 2;
  return 5;
};
const crawlable = inventory
  .filter(r => !String(r.current_url).includes('/wp-content/uploads/'))
  .filter(r => r.content_type !== 'jet-menu')
  .sort((a,b) => priority(a) - priority(b));

const max = Number(cfg.maxCrawlUrls || 0);
const selected = max > 0 ? crawlable.slice(0, max) : crawlable;
audit.crawlSelectedCount = selected.length;
audit.inventoryCount = inventory.length;

return selected.map(row => ({ json: { ...cfg, crawlUrl: row.current_url, content_type: row.content_type, language: row.language } }));`,
    },
  },
});

const pageBatch = splitInBatches({
  version: 3,
  config: {
    name: 'Batch page crawl',
    position: [1920, 160],
    parameters: { batchSize: 1 },
  },
});


const fetchPage = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch page HTML',
    position: [2400, 80],
    parameters: {
      method: 'GET',
      url: expr('={{ $json.crawlUrl }}'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {
        parameters: [{ name: 'User-Agent', value: expr('={{ $json.userAgent }}') }],
      },
      options: {
        timeout: 90000,
        redirect: { redirect: { followRedirects: true, maxRedirects: 5 } },
        response: {
          response: { fullResponse: true, neverError: true, responseFormat: 'text' },
        },
      },
    },
    onError: 'continueRegularOutput',
  },
});

const analyzePage = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Analyze page SEO',
    position: [2640, 80],
    parameters: {
      mode: 'runOnceForEachItem',
      language: 'javaScript',
      jsCode: `const cfg = $('Load Config').first().json;
const meta = $('Batch page crawl').item.json;
const url = meta.crawlUrl;
const html = String($json.body || $json.data || '');
const status = $json.statusCode || $json.status || null;
const headers = $json.headers || {};
const pick = (re) => {
  const m = html.match(re);
  return m ? m[1].trim() : null;
};
const decode = (s) => (s || '').replace(/&raquo;/g,'»').replace(/&amp;/g,'&').replace(/&quot;/g,'"').replace(/&#8211;/g,'–');
const title = decode(pick(/<title[^>]*>([^<]+)<\\/title>/i));
const canonical = pick(/rel=["']canonical["'][^>]*href=["']([^"']+)/i) || pick(/href=["']([^"']+)["'][^>]*rel=["']canonical/i);
const description = pick(/name=["']description["'][^>]*content=["']([^"']*)/i) || pick(/content=["']([^"']*)["'][^>]*name=["']description/i);
const robots = pick(/name=["']robots["'][^>]*content=["']([^"']*)/i) || pick(/content=["']([^"']*)["'][^>]*name=["']robots/i);
const lang = pick(/<html[^>]*lang=["']([^"']+)/i);
const h1 = [...html.matchAll(/<h1[^>]*>([\\s\\S]*?)<\\/h1>/gi)].map(m => m[1].replace(/<[^>]+>/g,'').trim()).filter(Boolean);
const h2 = [...html.matchAll(/<h2[^>]*>([\\s\\S]*?)<\\/h2>/gi)].map(m => m[1].replace(/<[^>]+>/g,'').trim()).filter(Boolean).slice(0, 30);
const hreflang = [];
for (const m of html.matchAll(/hreflang=["']([^"']+)["'][^>]*href=["']([^"']+)/gi)) hreflang.push({ lang: m[1], href: m[2] });
for (const m of html.matchAll(/href=["']([^"']+)["'][^>]*hreflang=["']([^"']+)/gi)) hreflang.push({ lang: m[2], href: m[1] });
const og = {};
for (const key of ['title','description','url','image','locale','type','site_name']) {
  og[key] = pick(new RegExp('property=["\\']og:' + key + '["\\'][^>]*content=["\\']([^"\\']*)', 'i')) || pick(new RegExp('content=["\\']([^"\\']*)["\\'][^>]*property=["\\']og:' + key, 'i'));
}
const schemaTypes = [];
for (const m of html.matchAll(/<script[^>]*type=["']application\\/ld\\+json["'][^>]*>([\\s\\S]*?)<\\/script>/gi)) {
  try {
    const data = JSON.parse(m[1]);
    if (data && data['@graph']) for (const n of data['@graph']) if (n && n['@type']) schemaTypes.push(n['@type']);
    else if (data && data['@type']) schemaTypes.push(data['@type']);
  } catch (e) {}
}
const imgs = [...html.matchAll(/<img\\b[^>]*>/gi)].map(m => m[0]);
let missingAlt = 0;
for (const tag of imgs) {
  const alt = tag.match(/alt=["']([^"']*)["']/i);
  if (!alt || !alt[1].trim()) missingAlt++;
}
const tech = {
  elementor: /elementor/i.test(html),
  yoast: /yoast/i.test(html),
  jet_menu: /jet-menu|jet_menu/i.test(html),
  jet_engine: /jet-engine|jet_engine/i.test(html),
  uikit: /\\buk-|uikit/i.test(html),
  bdthemes: /bdt-|element-pack/i.test(html),
  whatsapp: /whatsapp|wa\\.me/i.test(html),
  forms: /<form\\b|elementor-form|wpcf7/i.test(html),
};
const auditRow = {
  url,
  language: meta.language,
  content_type: meta.content_type,
  http_status: status,
  headers,
  title,
  canonical,
  meta_description: description,
  robots_meta: robots,
  html_lang: lang,
  h1,
  h2,
  hreflang,
  og,
  schema_types: schemaTypes,
  img_count: imgs.length,
  img_missing_alt: missingAlt,
  tech_signals: tech,
  html_bytes: html.length,
  classification: 'FACT',
};
const staticData = $getWorkflowStaticData('global');
staticData.audit = staticData.audit || { pageAudits: [], urlInventory: [] };
staticData.audit.pageAudits = staticData.audit.pageAudits || [];
staticData.audit.pageAudits.push(auditRow);
const inv = staticData.audit.urlInventory || [];
for (const row of inv) {
  if (row.current_url === url) row.http_status = String(status || '');
}
return { json: { ...cfg, ...auditRow } };`,
    },
  },
});

const fetchWpRoot = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch wp-json root',
    position: [2160, 320],
    parameters: {
      method: 'GET',
      url: expr("={{ $('Load Config').first().json.baseUrl }}/wp-json/"),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {
        parameters: [{ name: 'User-Agent', value: expr("={{ $('Load Config').first().json.userAgent }}") }],
      },
      options: {
        timeout: 90000,
        response: { response: { fullResponse: true, neverError: true, responseFormat: 'json' } },
      },
    },
    onError: 'continueRegularOutput',
  },
});

const fetchWpTypes = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch WP types',
    position: [2400, 320],
    parameters: {
      method: 'GET',
      url: expr("={{ $('Load Config').first().json.baseUrl }}/wp-json/wp/v2/types"),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {
        parameters: [{ name: 'User-Agent', value: expr("={{ $('Load Config').first().json.userAgent }}") }],
      },
      options: {
        timeout: 90000,
        response: { response: { fullResponse: true, neverError: true, responseFormat: 'json' } },
      },
    },
    onError: 'continueRegularOutput',
  },
});

const fetchWpTaxonomies = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Fetch WP taxonomies',
    position: [2640, 320],
    parameters: {
      method: 'GET',
      url: expr("={{ $('Load Config').first().json.baseUrl }}/wp-json/wp/v2/taxonomies"),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {
        parameters: [{ name: 'User-Agent', value: expr("={{ $('Load Config').first().json.userAgent }}") }],
      },
      options: {
        timeout: 90000,
        response: { response: { fullResponse: true, neverError: true, responseFormat: 'json' } },
      },
    },
    onError: 'continueRegularOutput',
  },
});

const normalizeEvidence = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Normalize evidence',
    position: [2880, 320],
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const cfg = $('Load Config').first().json;
const staticData = $getWorkflowStaticData('global');
const audit = staticData.audit || {};
const wpRoot = $('Fetch wp-json root').first().json;
const wpTypes = $('Fetch WP types').first().json;
const wpTax = $('Fetch WP taxonomies').first().json;
audit.wp = {
  namespaces: (wpRoot.body && wpRoot.body.namespaces) || (wpRoot.namespaces) || [],
  types: wpTypes.body || wpTypes,
  taxonomies: wpTax.body || wpTax,
  rootStatus: wpRoot.statusCode || wpRoot.status || null,
};
const evidence = {
  meta: {
    generated_at: new Date().toISOString(),
    domain: cfg.baseUrl,
    maxCrawlUrls: cfg.maxCrawlUrls,
    classification_scheme: ['FACT','INFERENCE','RECOMMENDATION','UNKNOWN_HUMAN_REVIEW'],
    rejected_concept: 'concept-preview/ is REJECTED CONCEPT — VISUAL REFERENCE ONLY',
  },
  discovery: {
    robotsTxt: audit.robotsTxt || '',
    childSitemaps: audit.childSitemaps || [],
    inventoryCount: (audit.urlInventory || []).length,
    crawlSelectedCount: audit.crawlSelectedCount || 0,
  },
  urlInventory: audit.urlInventory || [],
  pageAudits: audit.pageAudits || [],
  mediaFromSitemaps: audit.mediaFromSitemaps || [],
  wordpress: audit.wp,
  errors: audit.errors || [],
};
staticData.audit.evidence = evidence;

const summary = {
  inventoryCount: evidence.discovery.inventoryCount,
  crawled: evidence.pageAudits.length,
  childSitemaps: evidence.discovery.childSitemaps,
  wpNamespaces: evidence.wordpress.namespaces,
  samplePages: evidence.pageAudits.map(p => ({
    url: p.url,
    status: p.http_status,
    title: p.title,
    lang: p.html_lang,
    h1: p.h1,
    hreflang_count: (p.hreflang || []).length,
    schema: p.schema_types,
    missing_alt: p.img_missing_alt,
    tech: p.tech_signals,
  })),
  errors: evidence.errors,
};

const evidenceSummary = [
  'Abadis Med migration audit evidence. Use ONLY this evidence. Classify every claim as FACT, INFERENCE, RECOMMENDATION, or UNKNOWN.',
  'Rejected concept in local repo must remain labeled REJECTED CONCEPT — VISUAL REFERENCE ONLY.',
  'Target stack intent: WordPress headless CMS + Nuxt 4 + Tailwind/Nuxt UI + Three.js/GLB + Liara + n8n.',
  'Evidence JSON summary follows:',
  JSON.stringify(summary).slice(0, 100000),
].join('\\n\\n');

return [{ json: { ...cfg, evidence, evidenceSummary, runAi: cfg.runAi } }];`,
    },
  },
});

const aiGate = ifElse({
  version: 2.2,
  config: {
    name: 'AI enabled?',
    position: [3120, 320],
    parameters: {
      conditions: {
        options: { caseSensitive: true, leftValue: '', typeValidation: 'strict', version: 2 },
        conditions: [
          {
            id: 'c1',
            leftValue: expr('={{ $json.runAi }}'),
            rightValue: true,
            operator: { type: 'boolean', operation: 'true', singleValue: true },
          },
        ],
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
    position: [3360, 200],
    credentials: { openAiApi: newCredential('OpenAI Gateway') },
    parameters: {
      resource: 'text',
      operation: 'response',
      modelId: { __rl: true, mode: 'id', value: 'gpt-4.1-mini' },
      responses: {
        values: [
          {
            type: 'text',
            role: 'system',
            content: 'You produce an evidence-based Abadis Med migration plan. Never invent URLs. Never recommend DELETE. Mark FACT/INFERENCE/RECOMMENDATION/UNKNOWN. Keep concept-preview as REJECTED CONCEPT — VISUAL REFERENCE ONLY.',
          },
          {
            type: 'text',
            role: 'user',
            content: expr('={{ $json.evidenceSummary }}'),
          },
        ],
      },
      simplify: true,
      options: { maxTokens: 3500 },
    },
    onError: 'continueRegularOutput',
  },
});

const attachDraft = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Attach draft plan',
    position: [3600, 200],
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const base = $('Normalize evidence').first().json;
const draft = items[0].json.text || items[0].json.output || items[0].json.content || JSON.stringify(items[0].json);
return [{ json: { ...base, draftPlan: draft, evidenceSummary: base.evidenceSummary + '\\n\\n--- DRAFT PLAN ---\\n' + String(draft).slice(0, 50000) } }];`,
    },
  },
});

const aiQa = node({
  type: '@n8n/n8n-nodes-langchain.openAi',
  version: 2.3,
  config: {
    name: 'AI QA Review',
    position: [3840, 200],
    credentials: { openAiApi: newCredential('OpenAI Gateway') },
    parameters: {
      resource: 'text',
      operation: 'response',
      modelId: { __rl: true, mode: 'id', value: 'gpt-4.1-mini' },
      responses: {
        values: [
          {
            type: 'text',
            role: 'system',
            content: 'You are a strict second reviewer. Find missing requirements, unsupported assumptions, missing URLs, SEO risks, language risks, contradictions, security/performance/launch risks. Output a bullet list of issues only. Do not invent evidence.',
          },
          {
            type: 'text',
            role: 'user',
            content: expr('={{ $json.evidenceSummary }}'),
          },
        ],
      },
      simplify: true,
      options: { maxTokens: 2500 },
    },
    onError: 'continueRegularOutput',
  },
});

const attachQa = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Attach QA findings',
    position: [4080, 200],
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const base = $('Attach draft plan').first().json;
const qa = items[0].json.text || items[0].json.output || items[0].json.content || JSON.stringify(items[0].json);
return [{ json: { ...base, qaFindings: qa, evidenceSummary: base.evidenceSummary + '\\n\\n--- QA FINDINGS ---\\n' + String(qa).slice(0, 40000) } }];`,
    },
  },
});

const aiFinal = node({
  type: '@n8n/n8n-nodes-langchain.openAi',
  version: 2.3,
  config: {
    name: 'AI Final Plan',
    position: [4320, 200],
    credentials: { openAiApi: newCredential('OpenAI Gateway') },
    parameters: {
      resource: 'text',
      operation: 'response',
      modelId: { __rl: true, mode: 'id', value: 'gpt-4.1-mini' },
      responses: {
        values: [
          {
            type: 'text',
            role: 'system',
            content: 'Revise the Abadis migration plan using evidence + draft + QA. Keep FACT/INFERENCE/RECOMMENDATION/UNKNOWN labels. No DELETE actions. Preserve SEO URLs/media. Rejected concept remains visual reference only.',
          },
          {
            type: 'text',
            role: 'user',
            content: expr('={{ $json.evidenceSummary }}'),
          },
        ],
      },
      simplify: true,
      options: { maxTokens: 4000 },
    },
    onError: 'continueRegularOutput',
  },
});

const packExports = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Pack export payloads',
    position: [4560, 320],
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const norm = $('Normalize evidence').first().json;
const staticData = $getWorkflowStaticData('global');
const evidence = (staticData.audit && staticData.audit.evidence) || norm.evidence;
let draftPlan = '';
let qaFindings = '';
let finalPlan = '';
try { draftPlan = $('Attach draft plan').first().json.draftPlan || ''; } catch(e) {}
try { qaFindings = $('Attach QA findings').first().json.qaFindings || ''; } catch(e) {}
try {
  const fin = items[0].json;
  finalPlan = fin.text || fin.output || fin.content || fin.finalPlan || '';
} catch(e) {}
if (!finalPlan && items[0] && items[0].json && items[0].json.evidence) {
  finalPlan = 'AI stages skipped or unavailable. Use docs/abadis local master plan with refreshed evidence.';
}

const inv = evidence.urlInventory || [];
const csvEscape = (v) => '"' + String(v ?? '').replace(/"/g,'""') + '"';
const urlHeader = ['current_url','language','content_type','http_status','indexed_candidate','seo_importance','target_url','migration_action','redirect_required','redirect_target','notes','confidence','human_review_required'];
const urlCsv = [urlHeader.join(',')].concat(inv.map(r => urlHeader.map(h => csvEscape(r[h])).join(','))).join('\\n');
const seoHeader = ['url','language','http_status','title','meta_description','canonical','robots_meta','html_lang','h1','hreflang_count','schema_types','img_count','img_missing_alt'];
const pages = evidence.pageAudits || [];
const seoCsv = [seoHeader.join(',')].concat(pages.map(p => [
  p.url, p.language, p.http_status, p.title, p.meta_description, p.canonical, p.robots_meta, p.html_lang,
  (p.h1||[]).join(' | '), (p.hreflang||[]).length, (p.schema_types||[]).join('|'), p.img_count, p.img_missing_alt
].map(csvEscape).join(','))).join('\\n');

const bundle = {
  evidence,
  draftPlan,
  qaFindings,
  finalPlan,
  generated_at: new Date().toISOString(),
};

return [
  { json: { fileName: 'ABADIS-AUDIT.json', content: JSON.stringify(bundle, null, 2), mimeType: 'application/json' } },
  { json: { fileName: 'URL-MIGRATION-MAP.csv', content: urlCsv, mimeType: 'text/csv' } },
  { json: { fileName: 'SEO-AUDIT.csv', content: seoCsv, mimeType: 'text/csv' } },
  { json: { fileName: 'AI-FINAL-PLAN.md', content: String(finalPlan), mimeType: 'text/markdown' } },
];`,
    },
  },
});

const exportFiles = node({
  type: 'n8n-nodes-base.convertToFile',
  version: 1.1,
  config: {
    name: 'Convert exports to files',
    position: [4800, 320],
    parameters: {
      operation: 'toText',
      sourceProperty: 'content',
      binaryPropertyName: 'data',
      options: {
        fileName: expr('={{ $json.fileName }}'),
        mimeType: expr('={{ $json.mimeType }}'),
      },
    },
  },
});

export default workflow('abadis-website-audit', 'Abadis Website Audit')
  .add(start)
  .to(config)
  .to(fetchRobots)
  .to(attachRobots)
  .to(fetchSitemapIndex)
  .to(parseSitemapIndex)
  .to(
    sitemapBatch
      .onEachBatch(fetchChildSitemap.to(extractSitemapUrls).to(nextBatch(sitemapBatch)))
      .onDone(buildCrawlList),
  )
  .to(
    pageBatch
      .onEachBatch(fetchPage.to(analyzePage).to(nextBatch(pageBatch)))
      .onDone(fetchWpRoot),
  )
  .to(fetchWpTypes)
  .to(fetchWpTaxonomies)
  .to(normalizeEvidence)
  .to(aiGate.onTrue(aiDraft.to(attachDraft).to(aiQa).to(attachQa).to(aiFinal).to(packExports)).onFalse(packExports))
  .to(exportFiles)
  .group('Load configuration', [config], {
    description: 'Sets base URL, crawl caps, delay, UA, and AI toggle for repeatable audits',
  })
  .group('Discover sitemaps', [fetchRobots, attachRobots, fetchSitemapIndex, parseSitemapIndex, sitemapBatch, fetchChildSitemap, extractSitemapUrls], {
    description: 'Reads robots and sitemap index, then downloads each child sitemap dynamically',
  })
  .group('Crawl selected pages', [buildCrawlList, pageBatch, fetchPage, analyzePage], {
    description: 'Builds prioritized crawl list and extracts HTTP/SEO signals with rate limiting',
  })
  .group('Inspect WordPress API', [fetchWpRoot, fetchWpTypes, fetchWpTaxonomies, normalizeEvidence], {
    description: 'Pulls public REST namespaces, types, and taxonomies into normalized evidence',
  })
  .group('AI plan stages', [aiDraft, attachDraft, aiQa, attachQa, aiFinal], {
    description: 'Optional draft, QA, and final migration plan using Gateway OpenAI credits',
  })
  .group('Export audit files', [packExports, exportFiles], {
    description: 'Packages JSON/CSV/Markdown audit artifacts as downloadable binary files',
  });
