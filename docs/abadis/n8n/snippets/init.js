const cfg = $('Load Config').first().json;
const staticData = $getWorkflowStaticData('global');
staticData.audit = {
  config: cfg,
  fetchedAt: new Date().toISOString(),
  robotsTxt: '',
  childSitemaps: [],
  urlInventory: [],
  mediaFromSitemaps: [],
  pageAudits: [],
  wpContent: { endpoints: [], items: [], totals: {} },
  enArDiscovery: { seeds: [], addedUrls: [] },
  linkChecks: [],
  forms: [],
  schemaRecords: [],
  technology: {},
  relationships: [],
  orphans: [],
  errors: [],
};
return [{ json: { ...cfg, auditCleared: true } }];
