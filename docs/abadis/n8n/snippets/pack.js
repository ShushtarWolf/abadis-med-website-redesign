const cfg = $('Load Config').first().json;
const staticData = $getWorkflowStaticData('global');
const evidence = staticData.audit.evidence;

function extractAiText(raw) {
  if (raw == null) return null;
  if (typeof raw === 'string') {
    // Prefer readable plan text over stringified OpenAI message arrays
    if (raw.trim().startsWith('[{') && raw.includes('output_text')) {
      try { return extractAiText(JSON.parse(raw)); } catch (e) { return raw; }
    }
    return raw;
  }
  if (raw.error && !raw.text && !raw.output && !raw.content) {
    return typeof raw.error === 'string' ? raw.error : JSON.stringify(raw.error);
  }
  if (typeof raw.text === 'string') return raw.text;
  if (raw.output != null) return extractAiText(raw.output);
  if (raw.content != null) return extractAiText(raw.content);
  if (Array.isArray(raw)) {
    const parts = [];
    for (const item of raw) {
      if (item && item.type === 'message' && Array.isArray(item.content)) {
        for (const c of item.content) {
          if (c && (c.text || c.output_text)) parts.push(c.text || c.output_text);
        }
      } else {
        const t = extractAiText(item);
        if (t) parts.push(t);
      }
    }
    return parts.filter(Boolean).join('\n\n') || null;
  }
  if (raw.type === 'message' && Array.isArray(raw.content)) {
    return raw.content.map(c => c.text || c.output_text || '').filter(Boolean).join('\n');
  }
  if (raw.message != null) return extractAiText(raw.message);
  return null;
}

const aiNodes = ['AI Draft Plan', 'AI QA Review', 'AI Final Plan'];
const aiOutputs = {};
for (const name of aiNodes) {
  try {
    aiOutputs[name] = extractAiText($(name).first().json);
  } catch (e) {
    aiOutputs[name] = null;
  }
}
try {
  const attached = $('Attach QA findings').first().json;
  if (attached.draftPlan) aiOutputs['AI Draft Plan'] = extractAiText(attached.draftPlan);
  if (attached.qaFindings) aiOutputs['AI QA Review'] = extractAiText(attached.qaFindings);
} catch (e) { /* AI may be skipped */ }
try {
  aiOutputs['AI Final Plan'] = extractAiText($('AI Final Plan').first().json);
} catch (e) { /* skipped */ }

const masterMigrationPlanMd = [
  '# MASTER MIGRATION PLAN — Abadis Med',
  '',
  'Generated: ' + (evidence.meta && evidence.meta.generated_at ? evidence.meta.generated_at : new Date().toISOString()),
  'Pipeline: inventories → merge → AI Draft → AI QA → AI Final → MASTER MIGRATION PLAN',
  'Labels required: FACT | INFERENCE | RECOMMENDATION | UNKNOWN/HUMAN REVIEW',
  'Rejected concept: concept-preview/ is REJECTED CONCEPT — VISUAL REFERENCE ONLY',
  '',
  '## Inventories (completeness)',
  '```json',
  JSON.stringify(evidence.inventories || {}, null, 2),
  '```',
  '',
  '## AI Final Plan',
  extractAiText(aiOutputs['AI Final Plan']) || '_UNKNOWN: AI Final Plan unavailable_',
  '',
  '## AI QA Findings',
  extractAiText(aiOutputs['AI QA Review']) || '_UNKNOWN: AI QA unavailable_',
  '',
  '## AI Draft (reference)',
  extractAiText(aiOutputs['AI Draft Plan']) || '_UNKNOWN: AI Draft unavailable_',
].join('\n');


const esc = (v) => {
  const s = v == null ? '' : String(v);
  return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
};
const toCsv = (rows, headers) => {
  const lines = [headers.join(',')];
  for (const r of rows) lines.push(headers.map(h => esc(r[h] == null ? '' : r[h])).join(','));
  return lines.join('\n');
};

const inventoryRows = (evidence.urlInventory || []).map(u => ({
  url: u.current_url || u.url || '',
  source: u.sitemap_source || u.source || u.discovery_method || '',
  language: u.language || '',
  content_type: u.content_type || '',
  classification: u.classification || 'FACT',
  lastmod: u.lastmod || '',
  notes: u.notes || '',
}));
const pageRows = (evidence.pageAudits || []).map(p => ({
  url: p.url,
  final_url: p.final_url || '',
  http_status: p.http_status,
  title: p.title,
  meta_description: p.meta_description,
  canonical: p.canonical,
  robots_meta: p.robots_meta,
  html_lang: p.html_lang,
  h1: (p.h1 || []).join(' | '),
  h2: (p.h2 || []).join(' | '),
  h3: (p.h3 || []).join(' | '),
  og_title: p.og?.title || '',
  og_description: p.og?.description || '',
  og_image: p.og?.image || '',
  twitter_card: p.twitter?.card || '',
  hreflang: JSON.stringify(p.hreflang || []),
  schema_types: (p.schema_types || []).join('|'),
  redirect_chain: JSON.stringify(p.redirect_chain || []),
  internal_links: p.internal_link_count,
  external_links: p.external_link_count,
  forms: (p.forms || []).length,
  documents: (p.documents || []).join('|'),
  mailto: (p.mailto || []).join('|'),
  tel: (p.tel || []).join('|'),
  whatsapp: (p.whatsapp || []).join('|'),
  img_count: p.img_count,
  img_missing_alt: p.img_missing_alt,
  cache_control: p.http_signals?.cache_control || '',
  content_encoding: p.http_signals?.content_encoding || '',
  server: p.http_signals?.server || '',
  tech: JSON.stringify(p.tech_signals || {}),
  classification: 'FACT',
}));
const mediaRows = [];
for (const m of (evidence.mediaFromSitemaps || [])) {
  mediaRows.push({
    source: 'sitemap',
    url: m.loc || m.url || m.current_url || String(m),
    alt: '',
    loading: '',
    page_url: '',
    classification: 'FACT',
  });
}
for (const p of (evidence.pageAudits || [])) {
  for (const img of (p.images || [])) {
    mediaRows.push({
      source: 'page_img',
      url: img.src,
      alt: img.alt || '',
      loading: img.loading || '',
      page_url: p.url,
      classification: 'FACT',
    });
  }
  for (const d of (p.documents || [])) {
    mediaRows.push({ source: 'document', url: d, alt: '', loading: '', page_url: p.url, classification: 'FACT' });
  }
}
for (const w of (evidence.wpContent?.items || []).filter(i => i.mime_type || i.source_url)) {
  mediaRows.push({
    source: 'wp_media',
    url: w.source_url || w.link || '',
    alt: w.title || '',
    loading: '',
    page_url: w.link || '',
    classification: 'FACT',
  });
}
const linkRows = [];
for (const p of (evidence.pageAudits || [])) {
  for (const l of (p.internal_links || [])) {
    linkRows.push({ page_url: p.url, href: l.href, anchor: l.anchor, rel: l.rel || '', kind: 'internal', http_status: '', classification: 'FACT' });
  }
  for (const l of (p.external_links || [])) {
    linkRows.push({ page_url: p.url, href: l.href, anchor: l.anchor, rel: l.rel || '', kind: 'external', http_status: '', classification: 'FACT' });
  }
}
for (const c of (evidence.linkChecks || [])) {
  linkRows.push({
    page_url: '',
    href: c.url,
    anchor: '',
    rel: '',
    kind: c.ok ? 'broken_check_ok' : 'broken_check_fail',
    http_status: c.http_status,
    classification: 'FACT',
  });
}
const formRows = (evidence.forms || []).map(f => ({
  page_url: f.page_url,
  action: f.action,
  method: f.method,
  fields: JSON.stringify(f.fields || []),
  classification: 'FACT',
}));
const schemaRows = (evidence.schemaRecords || []).map(s => ({
  page_url: s.page_url,
  schema_types: (s.types || []).join('|'),
  json_ld: JSON.stringify(s.raw || s.schema || s),
  classification: 'FACT',
}));
const wpRows = (evidence.wpContent?.items || []).map(w => ({
  type_key: w.type_key,
  id: w.id,
  slug: w.slug,
  status: w.status,
  link: w.link,
  title: typeof w.title === 'string' ? w.title : (w.title?.rendered || ''),
  modified: w.modified || '',
  total_hint: JSON.stringify(evidence.wpContent?.totals?.[w.type_key] || {}),
  classification: 'FACT',
}));
const techRows = [];
for (const [k, v] of Object.entries(evidence.technology || {})) {
  techRows.push({
    key: k,
    value: typeof v === 'object' ? JSON.stringify(v) : String(v),
    page_url: '',
    classification: 'FACT',
  });
}
for (const p of (evidence.pageAudits || [])) {
  for (const [k, v] of Object.entries(p.tech_signals || {})) {
    if (!v) continue;
    techRows.push({ key: k, value: String(v), page_url: p.url, classification: 'FACT' });
  }
}
const orphanRows = (evidence.orphans || []).map(o => ({
  url: o.url,
  note: o.note,
  classification: o.classification || 'INFERENCE',
}));
const relRows = (evidence.relationships || []).map(r => ({
  from: r.from,
  kind: r.kind,
  related: JSON.stringify(r.related_documents || r.related_internal || { wp_type: r.wp_type, wp_id: r.wp_id } || ''),
  note: r.note,
  classification: r.classification || 'INFERENCE',
}));

const masterPlan = {
  meta: evidence.meta,
  inventories: evidence.inventories || null,
  evidence_summary: {
    inventoryCount: (evidence.urlInventory || []).length,
    crawled: (evidence.pageAudits || []).length,
    wpTotals: evidence.wpContent?.totals,
    forms: (evidence.forms || []).length,
    linkChecks: (evidence.linkChecks || []).length,
    orphans: (evidence.orphans || []).length,
    relationships: (evidence.relationships || []).length,
  },
  ai: {
    'AI Draft Plan': extractAiText(aiOutputs['AI Draft Plan']),
    'AI QA Review': extractAiText(aiOutputs['AI QA Review']),
    'AI Final Plan': extractAiText(aiOutputs['AI Final Plan']),
  },
  labeling_required: ['FACT', 'INFERENCE', 'RECOMMENDATION', 'UNKNOWN_HUMAN_REVIEW'],
  rejected_concept: 'concept-preview/ REJECTED CONCEPT — VISUAL REFERENCE ONLY',
};

const exportMap = {
  'URL-INVENTORY.csv': toCsv(inventoryRows, ['url', 'source', 'language', 'content_type', 'classification', 'lastmod', 'notes']),
  'PAGE-AUDIT.csv': toCsv(pageRows, [
    'url', 'final_url', 'http_status', 'title', 'meta_description', 'canonical', 'robots_meta', 'html_lang',
    'h1', 'h2', 'h3', 'og_title', 'og_description', 'og_image', 'twitter_card', 'hreflang',
    'schema_types', 'redirect_chain', 'internal_links', 'external_links', 'forms', 'documents',
    'mailto', 'tel', 'whatsapp', 'img_count', 'img_missing_alt', 'cache_control', 'content_encoding',
    'server', 'tech', 'classification',
  ]),
  'MEDIA.csv': toCsv(mediaRows, ['source', 'url', 'alt', 'loading', 'page_url', 'classification']),
  'LINKS.csv': toCsv(linkRows, ['page_url', 'href', 'anchor', 'rel', 'kind', 'http_status', 'classification']),
  'FORMS.csv': toCsv(formRows, ['page_url', 'action', 'method', 'fields', 'classification']),
  'SCHEMA.csv': toCsv(schemaRows, ['page_url', 'schema_types', 'json_ld', 'classification']),
  'WP-CONTENT.csv': toCsv(wpRows, ['type_key', 'id', 'slug', 'status', 'link', 'title', 'modified', 'total_hint', 'classification']),
  'TECHNOLOGY.csv': toCsv(techRows, ['key', 'value', 'page_url', 'classification']),
  'ORPHANS.csv': toCsv(orphanRows, ['url', 'note', 'classification']),
  'RELATIONSHIPS.csv': toCsv(relRows, ['from', 'kind', 'related', 'note', 'classification']),
  'ABADIS-AUDIT.json': JSON.stringify(evidence, null, 2),
  'MASTER-PLAN.json': JSON.stringify(masterPlan, null, 2),
  'MASTER-MIGRATION-PLAN.md': masterMigrationPlanMd,
};

const items = Object.entries(exportMap).map(([fileName, content]) => ({
  json: {
    fileName,
    mimeType: fileName.endsWith('.json')
      ? 'application/json'
      : (fileName.endsWith('.md') ? 'text/markdown' : 'text/csv'),
    content,
    exportKeys: Object.keys(exportMap),
    aiKeys: Object.keys(aiOutputs).filter(k => aiOutputs[k]),
    inventoryCount: inventoryRows.length,
    pageCount: pageRows.length,
    mediaCount: mediaRows.length,
    linkCount: linkRows.length,
    formCount: formRows.length,
    schemaCount: schemaRows.length,
    wpCount: wpRows.length,
    techCount: techRows.length,
    inventories: evidence.inventories || null,
  },
}));
return items;
