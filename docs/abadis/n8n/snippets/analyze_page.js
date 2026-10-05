const cfg = $('Load Config').first().json;
let meta = {};
try { meta = $('Resolve redirect chain').item.json || {}; } catch (e) { meta = {}; }
if (!meta.crawlUrl) {
  try { meta = { ...meta, ...($('Batch page crawl').item.json || {}) }; } catch (e2) { /* ignore */ }
}
const url = meta.crawlUrl;
const final = $json;
const html = String(final.data || final.body || '');
const finalStatus = final.statusCode || final.status || null;
const finalHeaders = final.headers || {};
const redirect_chain = Array.isArray(meta.redirect_chain) ? meta.redirect_chain.slice() : [];
if (redirect_chain.length) {
  const last = redirect_chain[redirect_chain.length - 1];
  if (last && Number(last.status) !== Number(finalStatus)) {
    redirect_chain.push({
      url: meta.finalUrl || url,
      status: finalStatus,
      location: null,
      note: 'FACT: final followed fetch status after hop walk',
      headers_subset: {
        'cache-control': finalHeaders['cache-control'] || null,
        'content-encoding': finalHeaders['content-encoding'] || null,
        server: finalHeaders.server || null,
        'x-robots-tag': finalHeaders['x-robots-tag'] || null,
        'content-type': finalHeaders['content-type'] || null,
      },
      classification: 'FACT',
    });
  } else if (last) {
    last.headers_subset = {
      ...(last.headers_subset || {}),
      'cache-control': finalHeaders['cache-control'] || last.headers_subset?.['cache-control'] || null,
      'content-encoding': finalHeaders['content-encoding'] || last.headers_subset?.['content-encoding'] || null,
      server: finalHeaders.server || last.headers_subset?.server || null,
      'content-type': finalHeaders['content-type'] || last.headers_subset?.['content-type'] || null,
    };
  }
}

if (!url) {
  const staticData = $getWorkflowStaticData('global');
  staticData.audit.errors.push({ stage: 'analyze_page', message: 'missing crawlUrl on paired item' });
  return { json: { ...cfg, error: 'missing crawlUrl' } };
}

const pick = (re) => { const m = html.match(re); return m ? m[1].trim() : null; };
const strip = (s) => String(s || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
const title = pick(/<title[^>]*>([^<]+)<\/title>/i);
const canonical = pick(/rel=["']canonical["'][^>]*href=["']([^"']+)/i) || pick(/href=["']([^"']+)["'][^>]*rel=["']canonical/i);
const description = pick(/name=["']description["'][^>]*content=["']([^"']*)/i) || pick(/content=["']([^"']*)["'][^>]*name=["']description/i);
const robots = pick(/name=["']robots["'][^>]*content=["']([^"']*)/i) || pick(/content=["']([^"']*)["'][^>]*name=["']robots/i);
const lang = pick(/<html[^>]*lang=["']([^"']+)/i);
const h1 = [...html.matchAll(/<h1[^>]*>([\s\S]*?)<\/h1>/gi)].map(m => strip(m[1])).filter(Boolean);
const h2 = [...html.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/gi)].map(m => strip(m[1])).filter(Boolean).slice(0, 40);
const h3 = [...html.matchAll(/<h3[^>]*>([\s\S]*?)<\/h3>/gi)].map(m => strip(m[1])).filter(Boolean).slice(0, 40);
const hreflang = [];
for (const m of html.matchAll(/hreflang=["']([^"']+)["'][^>]*href=["']([^"']+)/gi)) hreflang.push({ lang: m[1], href: m[2] });
for (const m of html.matchAll(/href=["']([^"']+)["'][^>]*hreflang=["']([^"']+)/gi)) hreflang.push({ lang: m[2], href: m[1] });
const og = {};
for (const key of ['title', 'description', 'url', 'image', 'locale', 'type', 'site_name']) {
  og[key] = pick(new RegExp('property=["\']og:' + key + '["\'][^>]*content=["\']([^"\']*)', 'i'))
    || pick(new RegExp('content=["\']([^"\']*)["\'][^>]*property=["\']og:' + key, 'i'));
}
const twitter = {};
for (const key of ['card', 'title', 'description', 'image', 'site']) {
  twitter[key] = pick(new RegExp('name=["\']twitter:' + key + '["\'][^>]*content=["\']([^"\']*)', 'i'))
    || pick(new RegExp('content=["\']([^"\']*)["\'][^>]*name=["\']twitter:' + key, 'i'));
}
const schemaBlocks = [];
const schemaTypes = [];
for (const m of html.matchAll(/<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)) {
  const raw = m[1].trim();
  try {
    const data = JSON.parse(raw);
    schemaBlocks.push(data);
    if (data && data['@graph']) for (const n of data['@graph']) if (n && n['@type']) schemaTypes.push(n['@type']);
    else if (Array.isArray(data)) for (const n of data) if (n && n['@type']) schemaTypes.push(n['@type']);
    else if (data && data['@type']) schemaTypes.push(data['@type']);
  } catch (e) {
    schemaBlocks.push({ parse_error: true, raw_preview: raw.slice(0, 500) });
  }
}
const images = [];
for (const tag of html.matchAll(/<img\b[^>]*>/gi)) {
  const t = tag[0];
  const src = (t.match(/(?:src|data-src)=["']([^"']+)/i) || [])[1] || '';
  const altM = t.match(/alt=["']([^"']*)["']/i);
  const loading = (t.match(/loading=["']([^"']+)/i) || [])[1] || '';
  images.push({ src, alt: altM ? altM[1] : null, missing_alt: !altM || !String(altM[1]).trim(), loading });
}
const abs = (href) => {
  if (!href) return null;
  if (href.startsWith('//')) return 'https:' + href;
  if (href.startsWith('/')) return cfg.baseUrl.replace(/\/$/, '') + href;
  return href;
};
const internal_links = [];
const external_links = [];
for (const m of html.matchAll(/<a\b[^>]*href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi)) {
  const href = m[1];
  const anchor = strip(m[2]).slice(0, 160);
  if (!href || href.startsWith('#') || href.startsWith('javascript:')) continue;
  if (href.startsWith('mailto:') || href.startsWith('tel:')) continue;
  const full = abs(href);
  if (!full) continue;
  if (full.includes('abadis-med.com') || href.startsWith('/')) internal_links.push({ href: full.split('#')[0], anchor });
  else external_links.push({ href: full, anchor });
}
const forms = [];
for (const fm of html.matchAll(/<form\b([^>]*)>([\s\S]*?)<\/form>/gi)) {
  const attrs = fm[1];
  const body = fm[2];
  const action = ((attrs.match(/action=["']([^"']*)["']/i) || [])[1]) || '';
  const method = ((attrs.match(/method=["']([^"']*)["']/i) || [])[1] || 'get').toLowerCase();
  const fields = [];
  for (const inp of body.matchAll(/<(input|select|textarea)\b([^>]*)>/gi)) {
    const a = inp[2];
    fields.push({
      tag: inp[1].toLowerCase(),
      type: ((a.match(/type=["']([^"']*)["']/i) || [])[1]) || '',
      name: ((a.match(/name=["']([^"']*)["']/i) || [])[1]) || '',
      id: ((a.match(/id=["']([^"']*)["']/i) || [])[1]) || '',
    });
  }
  forms.push({ action: abs(action) || action, method, fields, page_url: url });
}
const mailto = [...new Set([...html.matchAll(/mailto:([^"'?\s>]+)/gi)].map(m => m[1]))];
const tel = [...new Set([...html.matchAll(/tel:([^"'?\s>]+)/gi)].map(m => m[1]))];
const whatsapp = [...new Set([...html.matchAll(/https?:\/\/(?:wa\.me|api\.whatsapp\.com)[^"'\s>]*/gi)].map(m => m[0]))];
const documents = [...new Set([...html.matchAll(/https?:\/\/[^"'\s>]+\.(?:pdf|docx?|xlsx?|pptx?|zip)(?:\?[^"'\s>]*)?/gi)].map(m => m[0]))];
const tech = {
  elementor: /elementor/i.test(html),
  yoast: /yoast/i.test(html),
  jet_menu: /jet-menu|jet_menu/i.test(html),
  jet_engine: /jet-engine|jet_engine/i.test(html),
  uikit: /\buk-|uikit/i.test(html),
  bdthemes: /bdt-|element-pack/i.test(html),
  dynamic_content_elementor: /dce-|dynamic-content-for-elementor/i.test(html),
  whatsapp: whatsapp.length > 0 || /whatsapp/i.test(html),
  forms: forms.length > 0 || /elementor-form|wpcf7/i.test(html),
};
const http_signals = {
  cache_control: finalHeaders['cache-control'] || null,
  content_encoding: finalHeaders['content-encoding'] || null,
  server: finalHeaders.server || null,
  x_robots_tag: finalHeaders['x-robots-tag'] || null,
  content_type: finalHeaders['content-type'] || null,
  content_length: finalHeaders['content-length'] || html.length,
};
const auditRow = {
  url,
  language: meta.language,
  content_type: meta.content_type,
  final_url: meta.finalUrl || url,
  http_status: finalStatus,
  redirect_chain,
  http_signals,
  title,
  canonical,
  meta_description: description,
  robots_meta: robots,
  html_lang: lang,
  h1,
  h2,
  h3,
  hreflang,
  og,
  twitter,
  schema_types: schemaTypes,
  schema_blocks: schemaBlocks,
  images: images.slice(0, 100),
  img_count: images.length,
  img_missing_alt: images.filter(i => i.missing_alt).length,
  internal_links: internal_links.slice(0, 200),
  external_links: external_links.slice(0, 100),
  internal_link_count: internal_links.length,
  external_link_count: external_links.length,
  forms,
  mailto,
  tel,
  whatsapp,
  documents,
  tech_signals: tech,
  html_bytes: html.length,
  classification: 'FACT',
};
const staticData = $getWorkflowStaticData('global');
staticData.audit.pageAudits.push(auditRow);
for (const f of forms) staticData.audit.forms.push(f);
for (const block of schemaBlocks) {
  const types = [];
  if (block && block['@graph']) for (const n of block['@graph']) if (n && n['@type']) types.push(n['@type']);
  else if (Array.isArray(block)) for (const n of block) if (n && n['@type']) types.push(n['@type']);
  else if (block && block['@type']) types.push(block['@type']);
  staticData.audit.schemaRecords.push({ page_url: url, types, raw: block });
}
for (const k of Object.keys(tech)) {
  if (!tech[k]) continue;
  staticData.audit.technology[k] = staticData.audit.technology[k] || { signal: true, pages: [] };
  if (staticData.audit.technology[k].pages.length < 30) staticData.audit.technology[k].pages.push(url);
}
const inv = staticData.audit.urlInventory || [];
for (const row of inv) if (row.current_url === url) row.http_status = String(finalStatus || '');
return { json: { ...cfg, url, http_status: finalStatus, title, internal_link_count: internal_links.length, form_count: forms.length } };
