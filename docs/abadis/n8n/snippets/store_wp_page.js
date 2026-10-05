const cfg = $('Load Config').first().json;
const meta = $('Batch WP endpoints').item.json;
const status = $json.statusCode || null;
const headers = $json.headers || {};
const total = headers['x-wp-total'] || headers['X-WP-Total'] || null;
const totalPages = headers['x-wp-totalpages'] || headers['X-WP-TotalPages'] || null;
let body = $json.body !== undefined ? $json.body : $json.data;
if (typeof body === 'string') {
  try { body = JSON.parse(body); } catch (e) { body = []; }
}
if (!Array.isArray(body)) body = body ? [body] : [];
const staticData = $getWorkflowStaticData('global');
const key = meta.key || meta.rest_base;
staticData.audit.wpContent.totals[key] = {
  total: total ? Number(total) : body.length,
  totalPages: totalPages ? Number(totalPages) : null,
  kind: meta.kind,
};
for (const item of body) {
  const title = item.title && item.title.rendered ? item.title.rendered : (item.name || item.slug || '');
  const contentLen = item.content && item.content.rendered ? String(item.content.rendered).length : 0;
  const yoast = item.yoast_head_json || null;
  staticData.audit.wpContent.items.push({
    id: item.id,
    type_key: key,
    rest_base: meta.rest_base,
    kind: meta.kind,
    link: item.link || null,
    slug: item.slug || null,
    title,
    status: item.status || null,
    template: item.template || null,
    parent: item.parent ?? null,
    modified: item.modified || null,
    featured_media: item.featured_media ?? null,
    content_length: contentLen,
    acf_public: item.acf === undefined ? null : item.acf,
    yoast_robots: yoast && yoast.robots ? yoast.robots : null,
    yoast_title: yoast && yoast.title ? yoast.title : null,
    mime_type: item.mime_type || null,
    source_url: item.source_url || null,
  });
}
if (status && status >= 400) {
  staticData.audit.errors.push({ stage: 'wp_rest', endpoint: meta.path, status });
}
return { json: { ...cfg, rest_base: meta.rest_base, status, stored: body.length, total, totalPages } };
