/**
 * 301s for posts this pipeline unpublishes. The page is removed from the
 * manifest, markdown, sitemap and listing cards. The URL redirects to the
 * post's category page when that page exists, otherwise to the news or
 * articles hub. Republishing drops the rule again.
 *
 * Rules live in tools/redesign/data/unpublished-posts.json and in a marked
 * block of site/liara_nginx.conf, site/redirects-nginx.conf and site/_redirects.
 */
import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

export const MARK_BEGIN = '# BEGIN abadis-unpublished-posts';
export const MARK_END = '# END abadis-unpublished-posts';
const DATA_REL = 'tools/redesign/data/unpublished-posts.json';
const MOVES_REL = 'tools/redesign/data/url_moves.json';

export const HUBS = {
  fa: { news: '/آخرین-اخبار/', articles: '/مقالات/' },
  en: { news: '/en/latest-news/', articles: '/en/blog/' },
  ar: { news: '/arabic/الاخبار/', articles: '/arabic/articles/' },
};

export function normPath(p) {
  let s = String(p || '').trim();
  if (!s) return '';
  try { s = decodeURIComponent(s); } catch { /* keep */ }
  s = s.split('#')[0].split('?')[0];
  if (!s.startsWith('/')) s = '/' + s;
  if (s !== '/' && !s.endsWith('/')) s += '/';
  return s;
}

export function hubFor(localeId, kind) {
  const table = HUBS[localeId] || HUBS.fa;
  return table[kind === 'articles' ? 'articles' : 'news'];
}

export function canonicalPath(localeId, slug) {
  const s = String(slug || '').replace(/^\/+|\/+$/g, '');
  if (!s) return '';
  if (localeId === 'en') return `/en/${s}/`;
  if (localeId === 'ar') return `/arabic/${s}/`;
  return `/${s}/`;
}

export function nginxEscape(bare) {
  return String(bare).replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/\\\//g, '/').replace(/\\-/g, '-');
}

export function encodeSitePath(p) {
  const n = normPath(p);
  return n.split('/').map((seg) => encodeURIComponent(seg)).join('/');
}

export function nginxRule(src, dst) {
  const bare = normPath(src).replace(/\/$/, '') || '/';
  return `rewrite "^${nginxEscape(bare)}/?$" "https://$host${encodeSitePath(dst)}" permanent;`;
}

export function redirectLines(src, dst) {
  const s = encodeSitePath(src);
  const d = encodeSitePath(dst);
  const bare = s.endsWith('/') && s !== '/' ? s.slice(0, -1) : '';
  const lines = [`${s} ${d} 301`];
  if (bare) lines.push(`${bare} ${d} 301`);
  return lines;
}

export async function pageExists(root, sitePath) {
  const rel = normPath(sitePath).replace(/^\/+|\/+$/g, '');
  if (!rel) return false;
  try {
    await readFile(path.join(root, 'site', rel, 'index.html'));
    return true;
  } catch {
    return false;
  }
}

export async function resolveTarget(root, localeId, kind, item) {
  const raw = item && (item.category_path || item.archive);
  const candidate = raw ? normPath(raw) : '';
  if (candidate && candidate !== '/' && await pageExists(root, candidate)) return candidate;
  return hubFor(localeId, kind);
}

export function sourcePaths(localeId, slug, id, moves) {
  const canonical = canonicalPath(localeId, slug);
  const out = new Set();
  if (canonical) out.add(canonical);
  if (id) {
    out.add(`/news/${id}/`);
    out.add(`/articles/${id}/`);
    if (localeId === 'en') {
      out.add(`/en/news/${id}/`);
      out.add(`/en/articles/${id}/`);
    }
    if (localeId === 'ar') {
      out.add(`/arabic/news/${id}/`);
      out.add(`/arabic/articles/${id}/`);
    }
  }
  const want = normPath(canonical);
  for (const [src, dst] of Object.entries(moves || {})) {
    if (normPath(dst) === want) out.add(normPath(src));
  }
  return [...out].filter((p) => p && p !== '/');
}

export async function loadUnpublished(root) {
  try {
    const data = JSON.parse(await readFile(path.join(root, DATA_REL), 'utf8'));
    if (data && Array.isArray(data.posts)) return data;
  } catch { /* first use */ }
  return { version: 1, posts: [] };
}

async function saveUnpublished(root, data) {
  const abs = path.join(root, DATA_REL);
  await mkdir(path.dirname(abs), { recursive: true });
  const posts = [...data.posts].sort((a, b) => `${a.locale}:${a.id}`.localeCompare(`${b.locale}:${b.id}`));
  await writeFile(abs, JSON.stringify({ version: 1, posts }, null, 2) + '\n');
}

export function rulesFromPosts(posts) {
  const bySrc = new Map();
  for (const post of posts || []) {
    const dst = normPath(post.target || '/');
    for (const src of post.sources || []) {
      const key = normPath(src);
      if (!key || key === '/' || key === dst) continue;
      bySrc.set(key, dst);
    }
  }
  return [...bySrc.entries()].sort((a, b) => a[0].localeCompare(b[0]));
}

export function replaceManagedBlock(text, blockLines) {
  const src = String(text || '');
  const begin = src.indexOf(MARK_BEGIN);
  const end = begin >= 0 ? src.indexOf(MARK_END, begin) : -1;
  let body = src;
  if (begin >= 0 && end > begin) {
    const after = end + MARK_END.length;
    const tail = body.slice(after).replace(/^\n/, '');
    body = body.slice(0, begin).replace(/\n$/, '') + (tail ? '\n' + tail : '\n');
  }
  if (!blockLines.length) return body.endsWith('\n') || body === '' ? body : body + '\n';
  const block = `${MARK_BEGIN}\n${blockLines.join('\n')}\n${MARK_END}\n`;
  const loc = body.indexOf('\nlocation / {');
  if (loc >= 0) return body.slice(0, loc + 1) + block + '\n' + body.slice(loc + 1);
  return body.replace(/\s*$/, '\n') + block;
}

function dropOutsideRules(text, sources, kind) {
  const wanted = new Set(sources.map(normPath));
  return text.split('\n').filter((line) => {
    if (kind === 'nginx') {
      const m = line.match(/^rewrite "\^(.+?)\/\?\$"/);
      if (!m) return true;
      const bare = m[1].replace(/\\(.)/g, '$1');
      return !wanted.has(normPath(bare));
    }
    const m = line.match(/^(\S+)\s+\S+\s+301$/);
    if (!m || line.startsWith('#')) return true;
    let src = m[1];
    try { src = decodeURIComponent(src); } catch { /* keep */ }
    return !wanted.has(normPath(src));
  }).join('\n');
}

export function renderBlocks(posts) {
  const rules = rulesFromPosts(posts);
  const nginx = rules.map(([src, dst]) => nginxRule(src, dst));
  const redirects = rules.flatMap(([src, dst]) => redirectLines(src, dst));
  return { rules, nginx, redirects };
}

export async function writeRedirectFiles(root, posts) {
  const { nginx, redirects } = renderBlocks(posts);
  const sources = rulesFromPosts(posts).map(([src]) => src);
  for (const [rel, lines, kind] of [
    ['site/liara_nginx.conf', nginx, 'nginx'],
    ['site/redirects-nginx.conf', nginx, 'nginx'],
    ['site/_redirects', redirects, 'redirects'],
  ]) {
    const abs = path.join(root, rel);
    let text = '';
    try { text = await readFile(abs, 'utf8'); } catch { text = rel.endsWith('_redirects') ? '# 301 map\n' : '# Liara static (nginx) config\n'; }
    text = dropOutsideRules(replaceManagedBlock(text, []), sources, kind);
    text = replaceManagedBlock(text, lines);
    await mkdir(path.dirname(abs), { recursive: true });
    await writeFile(abs, text.endsWith('\n') ? text : text + '\n');
  }
}

export function stripSitemap(xml, paths) {
  const wanted = new Set(paths.map(normPath));
  return String(xml || '').replace(/[ \t]*<url>\s*[\s\S]*?<\/url>\n?/g, (block) => {
    const loc = /<loc>([^<]+)<\/loc>/.exec(block);
    if (!loc) return block;
    try {
      const pathname = decodeURIComponent(new URL(loc[1].trim()).pathname);
      return wanted.has(normPath(pathname)) ? '' : block;
    } catch {
      return block;
    }
  });
}

export function hrefPath(href, fromDir) {
  const raw = String(href || '').trim();
  if (!raw || raw.startsWith('#') || /^(mailto:|tel:|javascript:)/i.test(raw)) return '';
  try {
    if (raw.startsWith('http://') || raw.startsWith('https://')) return new URL(raw).pathname;
    const base = normPath(fromDir || '/');
    return new URL(raw, 'https://abadis-med.com' + base).pathname;
  } catch {
    return '';
  }
}

export function stripListings(html, paths, fromDir) {
  const wanted = new Set(paths.map(normPath));
  return String(html || '').replace(/<a\b[^>]*\bclass="[^"]*\b(?:post-card|teaser)\b[^"]*"[^>]*>[\s\S]*?<\/a>/g, (tag) => {
    const href = /\bhref="([^"]*)"/.exec(tag);
    if (!href) return tag;
    const resolved = hrefPath(href[1], fromDir);
    return resolved && wanted.has(normPath(resolved)) ? '' : tag;
  });
}

function fileDir(rel) {
  const posix = rel.replace(/\\/g, '/');
  const dir = posix.replace(/\/index\.html$/, '').replace(/\/[^/]+\.html$/, '');
  const site = dir.replace(/^site\/?/, '').replace(/^\/+|\/+$/g, '');
  return site ? `/${site}/` : '/';
}

async function walkHtml(root) {
  const site = path.join(root, 'site');
  const out = [];
  let names = [];
  try { names = await readdir(site, { recursive: true }); } catch { return out; }
  for (const name of names) {
    const rel = String(name).replace(/\\/g, '/');
    if (rel.endsWith('.html')) out.push(path.posix.join('site', rel));
  }
  return out;
}

export async function stripListingsOnDisk(root, paths) {
  let n = 0;
  for (const rel of await walkHtml(root)) {
    const abs = path.join(root, rel);
    const html = await readFile(abs, 'utf8');
    const next = stripListings(html, paths, fileDir(rel));
    if (next !== html) {
      await writeFile(abs, next);
      n += 1;
    }
  }
  return n;
}

export async function stripSitemapOnDisk(root, paths) {
  const abs = path.join(root, 'site/sitemap.xml');
  let xml = '';
  try { xml = await readFile(abs, 'utf8'); } catch { return false; }
  const next = stripSitemap(xml, paths);
  if (next !== xml) await writeFile(abs, next);
  return next !== xml;
}

async function loadMoves(root) {
  try {
    return JSON.parse(await readFile(path.join(root, MOVES_REL), 'utf8'));
  } catch {
    return {};
  }
}

export async function scrubNewsDelta(root) {
  const data = await loadUnpublished(root);
  const ids = new Set((data.posts || []).map((p) => String(p.id)));
  if (!ids.size) return false;
  const abs = path.join(root, 'tools/redesign/data/news-delta.json');
  let delta;
  try { delta = JSON.parse(await readFile(abs, 'utf8')); } catch { return false; }
  let changed = false;
  for (const row of delta.summary || []) {
    const removed = row.removed || [];
    const next = removed.filter((item) => !ids.has(String(item.id)));
    if (next.length !== removed.length) {
      row.removed = next;
      changed = true;
    }
  }
  if (changed) await writeFile(abs, JSON.stringify(delta, null, 2) + '\n');
  return changed;
}

export async function unpublishPost(root, spec) {
  const localeId = spec.locale;
  const id = String(spec.id);
  const kind = spec.kind === 'articles' ? 'articles' : 'news';
  const slug = String(spec.slug || '').replace(/^\/+|\/+$/g, '');
  const moves = spec.moves || await loadMoves(root);
  const target = spec.target
    ? normPath(spec.target)
    : await resolveTarget(root, localeId, kind, spec.item || {});
  const sources = sourcePaths(localeId, slug, id, moves);
  const data = await loadUnpublished(root);
  data.posts = data.posts.filter((p) => !(p.locale === localeId && String(p.id) === id));
  data.posts.push({ locale: localeId, id, kind, slug, target, sources });
  await saveUnpublished(root, data);
  await writeRedirectFiles(root, data.posts);
  await scrubNewsDelta(root);
  await stripSitemapOnDisk(root, sources);
  await stripListingsOnDisk(root, sources);
  return { locale: localeId, id, kind, target, sources };
}

export async function republishPost(root, localeId, id) {
  const data = await loadUnpublished(root);
  const before = data.posts.length;
  data.posts = data.posts.filter((p) => !(p.locale === localeId && String(p.id) === String(id)));
  if (data.posts.length === before) return false;
  await saveUnpublished(root, data);
  await writeRedirectFiles(root, data.posts);
  return true;
}

export async function unpublishSelfTest() {
  const os = await import('node:os');
  const { mkdtemp, rm, mkdir: mk, writeFile: wf } = await import('node:fs/promises');
  const root = await mkdtemp(path.join(os.tmpdir(), 'abadis-unpublish-'));
  try {
    await mk(path.join(root, 'site/news-topic'), { recursive: true });
    await mk(path.join(root, 'site/sample-post'), { recursive: true });
    await mk(path.join(root, 'tools/redesign/data'), { recursive: true });
    await wf(path.join(root, 'site/news-topic/index.html'), '<h1>Topic</h1>\n');
    await wf(path.join(root, 'site/sample-post/index.html'), '<title>Sample post title here</title>\n');
    await wf(path.join(root, 'site/index.html'), [
      '<a class="post-card" href="/sample-post/"><h3>Sample</h3></a>',
      '<a class="card teaser" href="/keep-me/"><h3>Keep</h3></a>',
      '<a class="post-card" href="/news/9/"><h3>Legacy</h3></a>',
    ].join('\n') + '\n');
    await wf(path.join(root, 'site/sitemap.xml'), [
      '<urlset>',
      '<url><loc>https://abadis-med.com/sample-post/</loc></url>',
      '<url><loc>https://abadis-med.com/news/9/</loc></url>',
      '<url><loc>https://abadis-med.com/keep-me/</loc></url>',
      '</urlset>',
      '',
    ].join('\n'));
    await wf(path.join(root, 'site/liara_nginx.conf'), 'charset utf-8;\n\n# BEGIN abadis-unpublished-posts\n# END abadis-unpublished-posts\n\nlocation / {\n  try_files $uri $uri/ =404;\n}\n');
    await wf(path.join(root, 'site/_redirects'), '# 301 map\n/old/ /new/ 301\n');
    await wf(path.join(root, 'site/redirects-nginx.conf'), '# plain\n');
    await mk(path.join(root, 'tools/redesign/data'), { recursive: true });
    await wf(path.join(root, 'tools/redesign/data/news-delta.json'), JSON.stringify({
      at: '2026-01-01T00:00:00.000Z',
      summary: [{ locale: 'fa', source: 'rest', new: [], modified: [], removed: [{ id: '9', reason: 'missing-from-rest' }, { id: 'keep', reason: 'other' }], partial: [] }],
    }, null, 2) + '\n');
    const recorded = await unpublishPost(root, {
      locale: 'fa', id: '9', kind: 'news', slug: 'sample-post',
      item: { category_path: '/news-topic/' },
      moves: { '/legacy-sample/': '/sample-post/' },
    });
    if (recorded.target !== '/news-topic/') throw new Error('unpublish: category page should win');
    if (!recorded.sources.includes('/sample-post/') || !recorded.sources.includes('/news/9/') || !recorded.sources.includes('/articles/9/') || !recorded.sources.includes('/legacy-sample/')) {
      throw new Error('unpublish: missing source ' + recorded.sources.join(','));
    }
    const delta = JSON.parse(await readFile(path.join(root, 'tools/redesign/data/news-delta.json'), 'utf8'));
    const removedIds = (delta.summary[0].removed || []).map((item) => String(item.id));
    if (removedIds.includes('9')) throw new Error('unpublish: news-delta still lists the unpublished id');
    if (!removedIds.includes('keep')) throw new Error('unpublish: news-delta dropped an unrelated removal');
    const saved = JSON.parse(await readFile(path.join(root, DATA_REL), 'utf8'));
    const savedPost = saved.posts.find((p) => p.id === '9');
    if (!savedPost || !savedPost.sources.includes('/articles/9/') || !savedPost.sources.includes('/news/9/') || !savedPost.sources.includes('/sample-post/')) {
      throw new Error('unpublish: unpublished-posts.json was not written');
    }
    const nginx = await readFile(path.join(root, 'site/liara_nginx.conf'), 'utf8');
    const sample = nginxRule('/sample-post/', '/news-topic/');
    const newsId = nginxRule('/news/9/', '/news-topic/');
    const articlesId = nginxRule('/articles/9/', '/news-topic/');
    const block = nginx.slice(nginx.indexOf(MARK_BEGIN), nginx.indexOf(MARK_END));
    if (!nginx.includes(MARK_BEGIN) || !block.includes(sample) || !block.includes(newsId) || !block.includes(articlesId)) {
      throw new Error('unpublish: nginx block missing the slug, /news/id/ or /articles/id/ 301');
    }
    if (nginx.split(sample).length !== 2) throw new Error('unpublish: duplicate nginx rule');
    const redirects = await readFile(path.join(root, 'site/_redirects'), 'utf8');
    if (!redirects.includes('/sample-post/ /news-topic/ 301')) throw new Error('unpublish: _redirects missing');
    if (!redirects.includes('/old/ /new/ 301')) throw new Error('unpublish: existing redirect dropped');
    const sitemap = await readFile(path.join(root, 'site/sitemap.xml'), 'utf8');
    if (sitemap.includes('/sample-post/') || sitemap.includes('/news/9/')) throw new Error('unpublish: sitemap still lists the post');
    if (!sitemap.includes('/keep-me/')) throw new Error('unpublish: sitemap dropped a live url');
    const home = await readFile(path.join(root, 'site/index.html'), 'utf8');
    if (home.includes('sample-post') || home.includes('/news/9/')) throw new Error('unpublish: listing still links the post');
    if (!home.includes('keep-me')) throw new Error('unpublish: listing dropped another card');
    const again = await unpublishPost(root, {
      locale: 'fa', id: '9', kind: 'news', slug: 'sample-post',
      item: { category_path: '/news-topic/' },
      moves: { '/legacy-sample/': '/sample-post/' },
    });
    const nginx2 = await readFile(path.join(root, 'site/liara_nginx.conf'), 'utf8');
    if (nginx2.split(MARK_BEGIN).length !== 2 || nginx2.split(sample).length !== 2) throw new Error('unpublish: second run duplicated the block');
    if (again.sources.length !== recorded.sources.length) throw new Error('unpublish: source set changed on rerun');
    const hub = await unpublishPost(root, { locale: 'fa', id: '8', kind: 'articles', slug: 'essay' });
    if (hub.target !== '/مقالات/') throw new Error('unpublish: articles should fall back to the articles hub');
    if (!await republishPost(root, 'fa', '9')) throw new Error('republish: expected to clear the rule');
    const nginx3 = await readFile(path.join(root, 'site/liara_nginx.conf'), 'utf8');
    if (nginx3.includes('/sample-post')) throw new Error('republish: 301 for the restored post remains');
    if (!nginx3.includes(nginxRule('/essay/', '/مقالات/'))) throw new Error('republish: other unpublished post was dropped');
    const data = JSON.parse(await readFile(path.join(root, DATA_REL), 'utf8'));
    if (data.posts.some((p) => p.id === '9')) throw new Error('republish: json still lists the post');
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}
