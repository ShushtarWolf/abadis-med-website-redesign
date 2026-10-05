const cfg = $('Load Config').first().json;
const base = cfg.baseUrl.replace(/\/$/, '');
const seeds = [
  { crawlUrl: base + '/en/', language: 'en', role: 'language_root' },
  { crawlUrl: base + '/arabic/', language: 'ar', role: 'language_root' },
];
const staticData = $getWorkflowStaticData('global');
staticData.audit.enArDiscovery.seeds = seeds.map(s => s.crawlUrl);
return seeds.map(s => ({ json: { ...cfg, ...s } }));
