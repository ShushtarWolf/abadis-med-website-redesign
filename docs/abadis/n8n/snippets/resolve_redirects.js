const cfg = $('Load Config').first().json;
const incoming = $json || {};
let meta = incoming;
try {
  const batch = $('Batch page crawl').item.json;
  if (batch && batch.crawlUrl) meta = { ...incoming, ...batch };
} catch (e) { /* use incoming */ }
const startUrl = meta.crawlUrl || incoming.crawlUrl;
if (!startUrl) {
  return {
    json: {
      ...cfg,
      crawlUrl: null,
      redirect_chain: [],
      finalUrl: null,
      finalStatus: null,
      hopCount: 0,
      error: 'FACT: missing crawlUrl on item',
    },
  };
}
const ua = cfg.userAgent || 'AbadisAuditBot/1.0';
const hops = [];
let url = startUrl;
let finalUrl = startUrl;
let finalStatus = null;
let finalHeaders = {};
let finalBody = '';
const maxHops = 10;

for (let i = 0; i < maxHops; i++) {
  let res;
  try {
    res = await this.helpers.httpRequest({
      method: 'GET',
      url,
      headers: { 'User-Agent': ua, Accept: 'text/html,*/*' },
      returnFullResponse: true,
      ignoreHttpStatusErrors: true,
      maxRedirects: 0,
      timeout: 60000,
    });
  } catch (e) {
    const errRes = e.response || (e.cause && e.cause.response) || null;
    if (errRes) {
      res = {
        statusCode: errRes.statusCode || errRes.status,
        headers: errRes.headers || {},
        body: errRes.body || errRes.data || '',
      };
    } else {
      hops.push({
        url,
        status: null,
        location: null,
        error: String(e.message || e),
        classification: 'FACT',
      });
      break;
    }
  }
  const status = res.statusCode || res.status || null;
  const headers = res.headers || {};
  const location = headers.location || headers.Location || null;
  hops.push({
    url,
    status,
    location: location || null,
    headers_subset: {
      'cache-control': headers['cache-control'] || null,
      'content-encoding': headers['content-encoding'] || null,
      server: headers.server || null,
      'x-robots-tag': headers['x-robots-tag'] || null,
      'content-type': headers['content-type'] || null,
    },
    classification: 'FACT',
  });
  finalUrl = url;
  finalStatus = status;
  finalHeaders = headers;
  finalBody = String(res.body !== undefined ? res.body : (res.data !== undefined ? res.data : ''));
  if (status && [301, 302, 303, 307, 308].includes(Number(status)) && location) {
    if (location.startsWith('/')) {
      url = cfg.baseUrl.replace(/\/$/, '') + location;
    } else if (location.startsWith('//')) {
      url = 'https:' + location;
    } else if (!/^https?:/i.test(location)) {
      try {
        url = new URL(location, url).toString();
      } catch (e2) {
        url = location;
      }
    } else {
      url = location;
    }
    continue;
  }
  break;
}

// Shape like HTTP Request so Analyze can consume $json directly (skip duplicate Fetch page HTML).
return {
  json: {
    ...cfg,
    crawlUrl: startUrl,
    content_type: meta.content_type || incoming.content_type || null,
    language: meta.language || incoming.language || null,
    redirect_chain: hops,
    finalUrl,
    finalStatus,
    hopCount: hops.length,
    statusCode: finalStatus,
    headers: finalHeaders,
    data: finalBody,
    body: finalBody,
  },
};
