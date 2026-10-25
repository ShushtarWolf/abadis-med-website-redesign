#!/usr/bin/env node
/**
 * Delta-sync news and academy articles from abadis-med.com into this repo.
 *
 * Alireza's team keeps publishing on the live WordPress site. This command
 * compares that site with the redesign archive and, at cutover, pulls only
 * what is new or modified. It does not freeze publishing.
 *
 *   node scripts/sync-abadis-news.mjs --help
 *   node scripts/sync-abadis-news.mjs --check
 *   node scripts/sync-abadis-news.mjs --dry-run
 *   node scripts/sync-abadis-news.mjs --sync
 *   node scripts/sync-abadis-news.mjs --self-test
 *
 * --check and --dry-run never write. --sync is idempotent: a second run with
 * no newer live edits leaves the tree unchanged.
 */
import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = process.env.ABADIS_SYNC_ROOT
  ? path.resolve(process.env.ABADIS_SYNC_ROOT)
  : path.resolve(HERE, '..');
const UA = 'AbadisNewsSync/1.0 (+redesign cutover; info@abadis-med.com)';
const FIELDS = 'id,date,date_gmt,modified,modified_gmt,slug,link,title,excerpt,content,featured_media,categories,status';

const LOCALES = [
  {
    id: 'fa',
    rest: 'http://abadis-med.com/wp-json/wp/v2',
    sitemap: 'http://abadis-med.com/post-sitemap.xml',
    feed: 'http://abadis-med.com/feed/',
    manifest: 'tools/redesign/data/posts.json',
    shape: 'archive',
    html: [['site/news', 'news'], ['site/articles', 'articles']],
  },
  {
    id: 'en',
    rest: 'http://abadis-med.com/en/wp-json/wp/v2',
    sitemap: 'http://abadis-med.com/en/post-sitemap.xml',
    feed: 'http://abadis-med.com/en/feed/',
    manifest: 'tools/redesign/data/en_posts.json',
    shape: 'wp',
  },
  {
    id: 'ar',
    rest: 'http://abadis-med.com/arabic/wp-json/wp/v2',
    sitemap: 'http://abadis-med.com/arabic/post-sitemap.xml',
    feed: 'http://abadis-med.com/arabic/feed/',
    manifest: 'tools/redesign/data/ar_posts.json',
    shape: 'wp',
  },
];

const FA_CAT = {
  22: 'news', 6: 'articles', 74: 'skip', 20: 'articles', 21: 'articles',
  69: 'articles', 76: 'articles', 1: 'uncategorized',
};
const SLUG_KIND = {
  newss: 'news', news: 'news', 'اخبار': 'news',
  blog: 'articles', articles: 'articles', 'مقالات': 'articles',
  accessories: 'articles', products: 'articles', install: 'articles', device: 'articles',
  ads: 'skip', uncategorized: 'uncategorized',
};
const NEWS_RE = /نمایشگاه|کنگره|مصاحبه|گفت\s*و\s*گو|گفت‌وگو|حضور|رونمایی|برندگان|قرعه|روز پرستار|روز جهانی|روز ملی|گرامی|تبریک|تسلیت|دعوت|مجمع|انتخابات|نشست|جلسه|جلسات|دیدار|بازدید|بیانیه|نظرسنجی|اخذ|دانش\s*بنیان شد|دانش‌بنیان شد|انتشار|منتشر|بازتاب|برگزار|وبینار|پروانه|حمایت|اهدا|ارسال|مذاکرات|نکوداشت|سال تحصیلی|هزار درخت|نجات زاگرس|پویش|کمپین|جشنواره|همایش|افتتاح|عضویت|تقدیر|لوح|صادر|رتبه|نوروز|یلدا|محرم|رمضان|آبادیس در|آبادیس به|آبادیس،|مدیرعامل|اطلاعیه|بازسازی|جنگ|استخدام|مسابقه|سفر|قرارداد|تفاهم|بازاریابی نسل|هوش تجار/;
const ART_RE = /چیست|بررسی|میزان|تبعیت|دستورالعمل|سیستم|پروتکل|الگوی|ارزیابی|ارزيابي|طراحی و اجرای/;

function help() {
  console.log(`sync-abadis-news — compare live abadis-med.com posts with this repo

Usage
  node scripts/sync-abadis-news.mjs --check [--locale fa|en|ar] [--json]
  node scripts/sync-abadis-news.mjs --dry-run
  node scripts/sync-abadis-news.mjs --sync
  node scripts/sync-abadis-news.mjs --help
  node scripts/sync-abadis-news.mjs --self-test

Keep publishing on abadis-med.com. At cutover, --sync writes only new and
modified news/academy posts into:
  content/<lang>/<news|articles>/<id>.md     Nuxt Content
  tools/redesign/data/posts.json              FA generator archive
  tools/redesign/data/en_posts.json
  tools/redesign/data/ar_posts.json
  tools/redesign/data/news-delta.json         last report
Then regenerate HTML with:  python3 tools/redesign/build.py posts

Exit 0 when the command finishes. Exit 1 on usage errors or a total fetch failure.
`);
}

function parseArgs(argv) {
  const o = { check: false, dry: false, sync: false, help: false, self: false, json: false, locale: '' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') o.help = true;
    else if (a === '--check') o.check = true;
    else if (a === '--dry-run') o.dry = true;
    else if (a === '--sync') o.sync = true;
    else if (a === '--self-test') o.self = true;
    else if (a === '--json') o.json = true;
    else if (a === '--locale') o.locale = argv[++i] || '';
    else throw new Error('Unknown argument: ' + a);
  }
  if (!o.help && !o.self && !o.check && !o.dry && !o.sync) o.check = true;
  return o;
}

function stripTags(h) {
  return String(h || '').replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&#8217;|&#8216;/g, "'")
    .replace(/&amp;/g, '&').replace(/&#8220;|&#8221;|&quot;/g, '"').replace(/&#8230;/g, '…')
    .replace(/\s+/g, ' ').trim();
}

function cleanHtml(html) {
  let h = String(html || '');
  h = h.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '');
  h = h.replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, '');
  h = h.replace(/<noscript\b[^>]*>[\s\S]*?<\/noscript>/gi, '');
  h = h.replace(/<!--[\s\S]*?-->/g, '');
  h = h.replace(/\sstyle=(["'])[\s\S]*?\1/gi, '');
  return h.trim();
}

function stamp(p) {
  const raw = p.modified_gmt || p.modified || p.date_gmt || p.date || '';
  if (!raw) return 0;
  const iso = /[zZ]|[+-]\d\d:?\d\d$/.test(raw) ? raw : raw + 'Z';
  const t = Date.parse(iso);
  return Number.isFinite(t) ? t : 0;
}

function isoOf(p, keyGmt, key) {
  const raw = p[keyGmt] || p[key] || '';
  if (!raw) return '';
  if (/[zZ]|[+-]\d\d:?\d\d$/.test(raw)) return raw.replace(/Z$/, '+00:00');
  return raw + '+00:00';
}

function titleOf(p) {
  const t = p.title;
  return stripTags(typeof t === 'string' ? t : (t && t.rendered) || '');
}

function rendered(field) {
  if (!field) return '';
  return typeof field === 'string' ? field : (field.rendered || '');
}

function kindFrom(p, catMap, lang) {
  const ids = p.categories || [];
  const kinds = ids.map((id) => catMap[id] || (lang === 'fa' ? FA_CAT[id] : '')).filter(Boolean);
  if (kinds.includes('skip')) return 'skip';
  if (kinds.includes('news')) return 'news';
  if (kinds.includes('articles')) return 'articles';
  if (kinds.includes('uncategorized') || !kinds.length) {
    const t = titleOf(p);
    if (ART_RE.test(t)) return 'articles';
    if (NEWS_RE.test(t)) return 'news';
    return lang === 'en' ? 'articles' : 'news';
  }
  return kinds[0] === 'skip' ? 'skip' : 'news';
}

async function getText(url) {
  const res = await fetch(url, {
    headers: { 'User-Agent': UA, Accept: '*/*' },
    signal: AbortSignal.timeout(40000),
    redirect: 'follow',
  });
  if (!res.ok) throw new Error(res.status + ' ' + url);
  const pages = res.headers.get('x-wp-totalpages') || res.headers.get('X-WP-TotalPages');
  return { text: await res.text(), pages: Number(pages || 0), headers: res.headers };
}

async function getJson(url) {
  const { text, pages } = await getText(url);
  return { json: JSON.parse(text), pages };
}

async function fetchCategories(rest) {
  const map = {};
  try {
    const { json } = await getJson(rest + '/categories?per_page=100&_fields=id,slug,name');
    for (const c of json) {
      const slug = decodeURIComponent(c.slug || '');
      map[c.id] = SLUG_KIND[slug] || SLUG_KIND[c.slug] || '';
    }
  } catch { /* hardcoded FA ids still apply */ }
  return map;
}

async function fetchRest(locale) {
  const catMap = await fetchCategories(locale.rest);
  const posts = [];
  let page = 1;
  let pages = 1;
  while (page <= pages) {
    const url = `${locale.rest}/posts?per_page=100&page=${page}&status=publish&_fields=${FIELDS}`;
    const { json, pages: total } = await getJson(url);
    if (total) pages = total;
    if (!json.length) break;
    posts.push(...json);
    page += 1;
  }
  return { posts, source: 'rest', catMap };
}

function parseSitemap(xml) {
  const posts = [];
  const re = /<url>\s*<loc>([^<]+)<\/loc>(?:\s*<lastmod>([^<]+)<\/lastmod>)?/g;
  let m;
  while ((m = re.exec(xml))) {
    posts.push({ id: '', link: m[1].trim(), modified: m[2] || '', title: { rendered: '' }, categories: [], status: 'publish', _partial: true });
  }
  return posts;
}

function parseFeed(xml) {
  const posts = [];
  const re = /<item>([\s\S]*?)<\/item>/g;
  let m;
  while ((m = re.exec(xml))) {
    const block = m[1];
    const link = (block.match(/<link>([^<]+)<\/link>/) || [])[1] || '';
    const title = (block.match(/<title>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/title>/) || [])[1] || '';
    const guid = (block.match(/<guid[^>]*>([^<]+)<\/guid>/) || [])[1] || '';
    const idm = guid.match(/[?&]p=(\d+)/) || link.match(/[?&]p=(\d+)/);
    const pub = (block.match(/<pubDate>([^<]+)<\/pubDate>/) || [])[1] || '';
    posts.push({
      id: idm ? Number(idm[1]) : '',
      link, modified: pub ? new Date(pub).toISOString() : '',
      title: { rendered: title }, categories: [], status: 'publish', _partial: true,
    });
  }
  return posts;
}

async function fetchLocale(locale) {
  try {
    return await fetchRest(locale);
  } catch (err) {
    const warnings = ['REST failed: ' + err.message];
    try {
      const { text } = await getText(locale.sitemap);
      return { posts: parseSitemap(text), source: 'sitemap', catMap: {}, warnings };
    } catch (e2) {
      warnings.push('sitemap failed: ' + e2.message);
    }
    try {
      const { text } = await getText(locale.feed);
      return { posts: parseFeed(text), source: 'feed', catMap: {}, warnings };
    } catch (e3) {
      warnings.push('feed failed: ' + e3.message);
      return { posts: [], source: 'none', catMap: {}, warnings, error: true };
    }
  }
}

async function readJson(rel, fallback) {
  try {
    return JSON.parse(await readFile(path.join(ROOT, rel), 'utf8'));
  } catch {
    return fallback;
  }
}

async function htmlIds(locale) {
  const ids = new Map();
  for (const [dir, kind] of locale.html || []) {
    let names = [];
    try { names = await readdir(path.join(ROOT, dir)); } catch { continue; }
    for (const name of names) {
      if (/^\d+$/.test(name)) ids.set(name, kind);
    }
  }
  return ids;
}

function localIndex(items, shape) {
  const byId = new Map();
  for (const item of items || []) {
    const id = String(item.id ?? '');
    if (!id) continue;
    const modified = shape === 'archive' ? item.modified || item.date || '' : (item.modified_gmt || item.modified || item.date_gmt || item.date || '');
    byId.set(id, {
      id,
      modified,
      ms: stamp({ modified_gmt: modified, modified }),
      title: shape === 'archive' ? (item.title || '') : titleOf(item),
      link: item.link || item.url || '',
    });
  }
  return byId;
}

function diffLocale(locale, remote, local, html) {
  const fresh = [];
  const changed = [];
  const unchanged = [];
  const skipped = [];
  const partial = [];
  for (const p of remote.posts) {
    if ((p.status || 'publish') !== 'publish') continue;
    const kind = kindFrom(p, remote.catMap, locale.id);
    if (kind === 'skip') { skipped.push(String(p.id || '')); continue; }
    const id = String(p.id || '');
    const link = p.link || '';
    const row = {
      id, kind, link, title: titleOf(p), modified: isoOf(p, 'modified_gmt', 'modified') || p.modified || '',
      partial: !!p._partial,
    };
    if (!id) {
      const known = [...local.values()].some((x) => x.link && link && x.link.replace(/\/$/, '') === link.replace(/\/$/, ''));
      if (!known) partial.push(row);
      continue;
    }
    const have = local.get(id);
    const onDisk = html.get(id);
    if (!have && !onDisk) fresh.push(row);
    else if (have && stamp(p) - have.ms > 2000) changed.push(row);
    else unchanged.push(id);
  }
  return {
    locale: locale.id, source: remote.source, warnings: remote.warnings || [],
    remote: remote.posts.length, local: local.size, html: html.size,
    new: fresh, modified: changed, unchanged: unchanged.length, skippedAds: skipped.length,
    partial,
  };
}

function yaml(s) { return JSON.stringify(String(s ?? '')); }

function markdown(locale, post, kind, image) {
  const body = cleanHtml(rendered(post.content));
  return `---
id: ${yaml(post.id)}
lang: ${locale}
kind: ${kind}
title: ${yaml(titleOf(post))}
slug: ${yaml(decodeURIComponent(post.slug || ''))}
date: ${yaml(isoOf(post, 'date_gmt', 'date'))}
modified: ${yaml(isoOf(post, 'modified_gmt', 'modified'))}
link: ${yaml(post.link || '')}
excerpt: ${yaml(stripTags(rendered(post.excerpt)))}
image: ${yaml(image || '')}
source: abadis-med.com
---

${body}
`;
}

function archiveRecord(post, image) {
  let link = post.link || '';
  try { link = decodeURIComponent(link); } catch { /* keep */ }
  const pathName = (() => { try { return new URL(link).pathname; } catch { return ''; } })();
  return {
    url: link.replace(/^http:\/\//, 'https://'),
    path: pathName.endsWith('/') ? pathName : pathName + '/',
    id: String(post.id),
    snapshot: 'delta-' + new Date().toISOString().slice(0, 10).replace(/-/g, ''),
    title: titleOf(post),
    desc: stripTags(rendered(post.excerpt)),
    image: image || '',
    date: isoOf(post, 'date_gmt', 'date'),
    modified: isoOf(post, 'modified_gmt', 'modified'),
    author: '',
    mode: 'rest',
    blocks: [{ t: 'html', html: cleanHtml(rendered(post.content)) }],
  };
}

async function fetchOne(locale, id) {
  const { json } = await getJson(`${locale.rest}/posts/${id}?_fields=${FIELDS}`);
  return json;
}

async function mediaUrl(locale, id) {
  if (!id) return '';
  try {
    const { json } = await getJson(`${locale.rest}/media/${id}?_fields=source_url`);
    return json.source_url || '';
  } catch { return ''; }
}

async function applySync(reports, locales) {
  const statePath = path.join(ROOT, 'tools/redesign/data/news-sync-state.json');
  const state = await readJson('tools/redesign/data/news-sync-state.json', { version: 1, locales: {} });
  let wrote = 0;
  for (const report of reports) {
    const locale = locales.find((l) => l.id === report.locale);
    const delta = [...report.new, ...report.modified].filter((r) => r.id && !r.partial);
    if (!delta.length) continue;
    if (report.source !== 'rest') {
      report.syncSkipped = 'REST content is required to write posts; sitemap/feed only listed them.';
      continue;
    }
    const manifest = await readJson(locale.manifest, []);
    const byId = new Map(manifest.map((item, i) => [String(item.id), i]));
    for (const row of delta) {
      const post = await fetchOne(locale, row.id);
      const image = await mediaUrl(locale, post.featured_media);
      const kind = row.kind === 'articles' ? 'articles' : 'news';
      const rel = path.join('content', locale.id, kind, `${post.id}.md`);
      const abs = path.join(ROOT, rel);
      const md = markdown(locale.id, post, kind, image);
      let prev = '';
      try { prev = await readFile(abs, 'utf8'); } catch { /* new */ }
      if (prev !== md) {
        await mkdir(path.dirname(abs), { recursive: true });
        await writeFile(abs, md);
        wrote += 1;
        row.file = rel;
      }
      if (locale.shape === 'archive') {
        const rec = archiveRecord(post, image);
        if (byId.has(String(post.id))) manifest[byId.get(String(post.id))] = { ...manifest[byId.get(String(post.id))], ...rec };
        else manifest.push(rec);
      } else if (byId.has(String(post.id))) {
        manifest[byId.get(String(post.id))] = post;
      } else manifest.push(post);
      state.locales[locale.id] = state.locales[locale.id] || {};
      state.locales[locale.id][String(post.id)] = { modified: row.modified, kind };
    }
    const manAbs = path.join(ROOT, locale.manifest);
    const next = JSON.stringify(manifest, null, 2) + '\n';
    let old = '';
    try { old = await readFile(manAbs, 'utf8'); } catch { /* new */ }
    if (old !== next) {
      await writeFile(manAbs, next);
      wrote += 1;
    }
  }
  if (wrote) {
    await mkdir(path.dirname(statePath), { recursive: true });
    await writeFile(statePath, JSON.stringify(state, null, 2) + '\n');
    const summary = reports.map((r) => ({
      locale: r.locale, source: r.source, new: r.new, modified: r.modified, partial: r.partial,
    }));
    await writeFile(path.join(ROOT, 'tools/redesign/data/news-delta.json'), JSON.stringify({ at: new Date().toISOString(), summary }, null, 2) + '\n');
  }
  return wrote;
}

function printReport(reports, asJson) {
  if (asJson) {
    console.log(JSON.stringify(reports, null, 2));
    return;
  }
  for (const r of reports) {
    console.log(`${r.locale}: source=${r.source} remote=${r.remote} manifest=${r.local} html=${r.html} unchanged=${r.unchanged} ads_skipped=${r.skippedAds}`);
    if (r.warnings && r.warnings.length) console.log('  warnings: ' + r.warnings.join(' | '));
    for (const row of r.new) console.log(`  NEW ${row.kind} #${row.id || row.link} ${row.title}`);
    for (const row of r.modified) console.log(`  MODIFIED ${row.kind} #${row.id} ${row.title}`);
    for (const row of r.partial) console.log(`  UNMATCHED (no id, from ${r.source}) ${row.link}`);
    if (!r.new.length && !r.modified.length) console.log('  no new or modified posts');
  }
}

export async function run(argv = process.argv.slice(2)) {
  const args = parseArgs(argv);
  if (args.help) { help(); return 0; }
  if (args.self) return selfTest();
  const locales = LOCALES.filter((l) => !args.locale || l.id === args.locale);
  if (!locales.length) throw new Error('Unknown --locale');
  const reports = [];
  let failed = 0;
  for (const locale of locales) {
    const remote = await fetchLocale(locale);
    if (remote.error) failed += 1;
    const manifest = await readJson(locale.manifest, []);
    const local = localIndex(manifest, locale.shape);
    const html = await htmlIds(locale);
    reports.push(diffLocale(locale, remote, local, html));
  }
  if (failed === locales.length) {
    printReport(reports, args.json);
    return 1;
  }
  printReport(reports, args.json);
  if (args.sync) {
    const n = await applySync(reports, locales);
    console.log(n ? `sync wrote ${n} file(s). Regenerate with: python3 tools/redesign/build.py posts` : 'sync: already up to date');
  } else if (args.dry) {
    const n = reports.reduce((s, r) => s + r.new.length + r.modified.length, 0);
    console.log(`dry-run: ${n} post(s) would be written under content/ and the manifests. No files changed.`);
  }
  return 0;
}

async function selfTest() {
  const { mkdtemp, rm } = await import('node:fs/promises');
  const os = await import('node:os');
  const dir = await mkdtemp(path.join(os.tmpdir(), 'abadis-sync-'));
  const fixture = {
    posts: [
      { id: 1, modified_gmt: '2026-01-01T00:00:00', date_gmt: '2026-01-01T00:00:00', slug: 'old', link: 'http://abadis-med.com/old/', status: 'publish', categories: [22], title: { rendered: 'Old' }, excerpt: { rendered: 'e' }, content: { rendered: '<p>old</p>' }, featured_media: 0 },
      { id: 2, modified_gmt: '2026-10-01T00:00:00', date_gmt: '2026-10-01T00:00:00', slug: 'new', link: 'http://abadis-med.com/new/', status: 'publish', categories: [6], title: { rendered: 'New article' }, excerpt: { rendered: 'e' }, content: { rendered: '<p>new</p>' }, featured_media: 0 },
    ],
  };
  const local = [{ id: '1', modified: '2020-01-01T00:00:00+00:00', title: 'Old', url: 'http://abadis-med.com/old/', date: '2020-01-01T00:00:00+00:00', blocks: [{ t: 'html', html: '<p>old</p>' }] }];
  const catMap = { 22: 'news', 6: 'articles' };
  const locale = { id: 'fa', shape: 'archive', manifest: 'posts.json', html: [] };
  const report = diffLocale(locale, { posts: fixture.posts, source: 'rest', catMap }, localIndex(local, 'archive'), new Map([['1', 'news']]));
  if (report.new.length !== 1 || report.new[0].id !== '2') throw new Error('self-test: expected post 2 to be new');
  if (report.modified.length !== 1 || report.modified[0].id !== '1') throw new Error('self-test: expected post 1 to be modified');
  const again = diffLocale(locale, { posts: [fixture.posts[0]], source: 'rest', catMap }, localIndex([{ ...local[0], modified: '2026-01-01T00:00:00+00:00' }], 'archive'), new Map([['1', 'news']]));
  if (again.modified.length || again.new.length) throw new Error('self-test: identical modified stamp must be unchanged');
  await rm(dir, { recursive: true, force: true });
  console.log('self-test ok');
  return 0;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  run().then((code) => process.exit(code)).catch((err) => {
    console.error('FAIL', err.message || err);
    process.exit(1);
  });
}
