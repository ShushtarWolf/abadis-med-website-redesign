const cfg = $('Load Config').first().json;
const body = String(items[0].json.data || items[0].json.body || '');
const staticData = $getWorkflowStaticData('global');
staticData.audit.robotsTxt = body;
return [{ json: { ...cfg, robotsTxt: body, robotsStatus: items[0].json.statusCode || null } }];
