const cfg = $('Load Config').first().json;
const typesRaw = $('Fetch WP types').first().json;
const taxRaw = $('Fetch WP taxonomies').first().json;
const types = typesRaw.body || typesRaw.data || typesRaw;
const taxonomies = taxRaw.body || taxRaw.data || taxRaw;
const staticData = $getWorkflowStaticData('global');
staticData.audit.wpContent.types = types;
staticData.audit.wpContent.taxonomies = taxonomies;
const skip = new Set([
  'wp_block', 'wp_template', 'wp_template_part', 'wp_global_styles',
  'wp_navigation', 'wp_font_family', 'wp_font_face', 'jet-engine', 'nav_menu_item', 'jet-menu',
]);
const endpoints = [];
for (const [key, meta] of Object.entries(types || {})) {
  if (skip.has(key)) continue;
  const rest = meta.rest_base;
  if (!rest || String(rest).includes('(?P')) continue;
  endpoints.push({ kind: 'type', key, rest_base: rest, path: '/wp-json/wp/v2/' + rest });
}
for (const [key, meta] of Object.entries(taxonomies || {})) {
  if (key === 'nav_menu' || key === 'wp_pattern_category') continue;
  const rest = meta.rest_base;
  if (!rest) continue;
  endpoints.push({ kind: 'taxonomy', key, rest_base: rest, path: '/wp-json/wp/v2/' + rest });
}
staticData.audit.wpContent.endpoints = endpoints;
const perPage = cfg.wpPerPage || 50;
// Slim fields so wpPerPage=50 stays under the instance 180s executionTimeout.
const fields = 'id,slug,status,link,title,modified,date,mime_type,source_url,type,name,count';
return endpoints.map(ep => ({
  json: {
    ...cfg,
    ...ep,
    endpointUrl: cfg.baseUrl.replace(/\/$/, '') + ep.path + '?per_page=' + perPage + '&_fields=' + fields,
  },
}));
