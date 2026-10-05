const cfg = $('Load Config').first().json;
const meta = $('Batch link checks').item.json;
if (meta.skip) return { json: { ...cfg, skipped: true } };
const status = $json.statusCode || $json.status || null;
const staticData = $getWorkflowStaticData('global');
staticData.audit.linkChecks.push({
  url: meta.linkUrl,
  http_status: status,
  ok: status >= 200 && status < 400,
  content_type: ($json.headers || {})['content-type'] || null,
  classification: 'FACT',
});
return { json: { ...cfg, linkUrl: meta.linkUrl, status } };
