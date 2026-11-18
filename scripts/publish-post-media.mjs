/**
 * Download new/changed post images, compress them to WebP, and upload to the
 * public Liara bucket `abadis-media`. Binaries stay out of git.
 *
 * Required env when there is something to upload (names only; never log values):
 *   ABADIS_MEDIA_ACCESS_KEY
 *   ABADIS_MEDIA_SECRET_KEY
 *   ABADIS_MEDIA_S3_ENDPOINT      e.g. https://storage.iran.liara.space
 *   ABADIS_MEDIA_PUBLIC_BASE      e.g. https://abadis-media.storage.iran.liara.space
 * Optional:
 *   ABADIS_MEDIA_BUCKET           default abadis-media
 *   ABADIS_MEDIA_S3_REGION        default us-east-1
 */
import crypto from 'node:crypto';
import { spawn } from 'node:child_process';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import http from 'node:http';
import https from 'node:https';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SCRIPT_ROOT = path.resolve(HERE, '..');
const ROOT = process.env.ABADIS_SYNC_ROOT
  ? path.resolve(process.env.ABADIS_SYNC_ROOT)
  : SCRIPT_ROOT;
const MAP_REL = 'tools/redesign/data/media-bucket.json';

export const MEDIA_SECRET_NAMES = [
  'ABADIS_MEDIA_ACCESS_KEY',
  'ABADIS_MEDIA_SECRET_KEY',
  'ABADIS_MEDIA_S3_ENDPOINT',
  'ABADIS_MEDIA_PUBLIC_BASE',
];

export function missingMediaSecrets() {
  return MEDIA_SECRET_NAMES.filter((n) => !(process.env[n] || '').trim());
}

export function mediaConfig() {
  return {
    endpoint: (process.env.ABADIS_MEDIA_S3_ENDPOINT || '').trim().replace(/\/$/, ''),
    publicBase: (process.env.ABADIS_MEDIA_PUBLIC_BASE || '').trim().replace(/\/$/, ''),
    bucket: (process.env.ABADIS_MEDIA_BUCKET || 'abadis-media').trim(),
    region: (process.env.ABADIS_MEDIA_S3_REGION || 'us-east-1').trim(),
    accessKey: (process.env.ABADIS_MEDIA_ACCESS_KEY || '').trim(),
    secretKey: process.env.ABADIS_MEDIA_SECRET_KEY || '',
  };
}

export async function loadMap(root = ROOT) {
  try {
    const data = JSON.parse(await readFile(path.join(root, MAP_REL), 'utf8'));
    if (data && data.items && typeof data.items === 'object') return data;
  } catch { /* first run */ }
  return { version: 1, bucket: 'abadis-media', items: {} };
}

async function saveMap(root, map) {
  const abs = path.join(root, MAP_REL);
  await mkdir(path.dirname(abs), { recursive: true });
  const items = {};
  for (const key of Object.keys(map.items).sort()) items[key] = map.items[key];
  const body = { version: 1, bucket: map.bucket || 'abadis-media', items };
  await writeFile(abs, JSON.stringify(body, null, 2) + '\n');
  return body;
}

function decodeAttr(v) {
  return String(v || '').replace(/&amp;/g, '&').replace(/&#0?38;/g, '&').trim();
}

export function extractImageUrls(html) {
  const urls = [];
  const re = /<(?:img|source)\b[^>]*>/gi;
  let m;
  const s = String(html || '');
  while ((m = re.exec(s))) {
    const tag = m[0];
    for (const attr of ['src', 'data-src', 'data-lazy-src']) {
      const a = new RegExp('\\b' + attr + '=(["\'])(.*?)\\1', 'i').exec(tag);
      if (a) urls.push(decodeAttr(a[2]));
    }
    const set = /\bsrcset=(["'])(.*?)\1/i.exec(tag);
    if (set) {
      for (const part of set[2].split(',')) {
        const u = part.trim().split(/\s+/)[0];
        if (u) urls.push(decodeAttr(u));
      }
    }
  }
  return urls.filter(isImageUrl);
}

function isImageUrl(url) {
  if (!url || url.startsWith('data:') || url.startsWith('blob:')) return false;
  if (/gravatar\.com|emoji/i.test(url)) return false;
  if (/\/wp-content\/uploads\//i.test(url)) return true;
  return /\.(png|jpe?g|gif|webp|avif|bmp)(\?|#|$)/i.test(url);
}

export function rewriteText(s, items) {
  let out = String(s ?? '');
  const pairs = Object.entries(items || {}).filter(([, rec]) => rec && rec.url);
  pairs.sort((a, b) => b[0].length - a[0].length);
  for (const [src, rec] of pairs) {
    if (!src || src === rec.url) continue;
    const variants = new Set([src, src.replace(/^http:\/\//i, 'https://'), src.replace(/^https:\/\//i, 'http://')]);
    for (const v of [...variants].sort((a, b) => b.length - a.length)) {
      if (v && v !== rec.url) out = out.split(v).join(rec.url);
    }
  }
  return out;
}

function sha256hex(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

function hmac(key, data) {
  return crypto.createHmac('sha256', key).update(data).digest();
}

function canonicalUri(pathname) {
  return pathname.split('/').map((seg) => {
    try { return encodeURIComponent(decodeURIComponent(seg)); } catch { return encodeURIComponent(seg); }
  }).join('/');
}

export function signPut({ method, url, headers, accessKey, secretKey, region, service = 's3' }) {
  const u = new URL(url);
  const amzdate = headers['x-amz-date'];
  const datestamp = amzdate.slice(0, 8);
  const payloadHash = headers['x-amz-content-sha256'];
  const names = Object.keys(headers).map((h) => h.toLowerCase()).sort();
  const canonicalHeaders = names.map((h) => `${h}:${String(headers[h]).trim().replace(/\s+/g, ' ')}\n`).join('');
  const signedHeaders = names.join(';');
  const canonicalRequest = [method, canonicalUri(u.pathname), '', canonicalHeaders, signedHeaders, payloadHash].join('\n');
  const scope = `${datestamp}/${region}/${service}/aws4_request`;
  const stringToSign = ['AWS4-HMAC-SHA256', amzdate, scope, sha256hex(canonicalRequest)].join('\n');
  let key = hmac('AWS4' + secretKey, datestamp);
  key = hmac(key, region);
  key = hmac(key, service);
  key = hmac(key, 'aws4_request');
  const signature = crypto.createHmac('sha256', key).update(stringToSign).digest('hex');
  return `AWS4-HMAC-SHA256 Credential=${accessKey}/${scope}, SignedHeaders=${signedHeaders}, Signature=${signature}`;
}

export function putObject({ body, key, contentType, cfg, requestImpl, now = new Date() }) {
  const payloadHash = sha256hex(body);
  const amzdate = now.toISOString().replace(/[:-]|\.\d{3}/g, '');
  const pathname = '/' + [cfg.bucket, ...key.split('/')].map(encodeURIComponent).join('/');
  const url = cfg.endpoint + pathname;
  const endpoint = new URL(cfg.endpoint);
  const headers = {
    host: endpoint.host,
    'content-length': String(body.length),
    'content-type': contentType,
    'x-amz-content-sha256': payloadHash,
    'x-amz-date': amzdate,
  };
  headers.authorization = signPut({
    method: 'PUT', url, headers, accessKey: cfg.accessKey, secretKey: cfg.secretKey, region: cfg.region,
  });
  const send = requestImpl || ((opts, payload) => new Promise((resolve, reject) => {
    const lib = opts.protocol === 'https:' ? https : http;
    const req = lib.request(opts, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => resolve({ status: res.statusCode || 0, text: Buffer.concat(chunks).toString('utf8') }));
    });
    req.on('error', reject);
    req.end(payload);
  }));
  return send({
    protocol: endpoint.protocol,
    hostname: endpoint.hostname,
    port: endpoint.port || undefined,
    method: 'PUT',
    path: pathname,
    headers,
  }, body).then((res) => {
    if (res.status < 200 || res.status >= 300) {
      throw new Error(`media upload failed (${res.status}) for ${key}` + (res.text ? `: ${String(res.text).slice(0, 160)}` : ''));
    }
    return `${cfg.publicBase}/${key}`;
  });
}

export function toWebp(buf, script = path.join(SCRIPT_ROOT, 'tools/redesign/to_webp.py')) {
  return new Promise((resolve, reject) => {
    const py = spawn('python3', [script], { stdio: ['pipe', 'pipe', 'pipe'] });
    const out = [];
    const err = [];
    py.stdout.on('data', (d) => out.push(d));
    py.stderr.on('data', (d) => err.push(d));
    py.on('error', reject);
    py.on('close', (code) => {
      const msg = Buffer.concat(err).toString('utf8').trim();
      if (code !== 0) reject(new Error(msg || 'to_webp failed'));
      else {
        const [w, h] = msg.split(/\s+/).map((n) => Number(n));
        if (!w || !h) reject(new Error('to_webp missing size'));
        else resolve({ bytes: Buffer.concat(out), w, h });
      }
    });
    py.stdin.end(buf);
  });
}

async function defaultDownload(url, fetchImpl) {
  const attempts = [url];
  if (url.startsWith('https://')) attempts.push('http://' + url.slice('https://'.length));
  else if (url.startsWith('http://')) attempts.push('https://' + url.slice('http://'.length));
  let last = 'image download failed';
  for (const candidate of attempts) {
    try {
      const res = await fetchImpl(candidate, {
        headers: { 'User-Agent': 'AbadisNewsSync/1.0' },
        redirect: 'follow',
        signal: AbortSignal.timeout(40000),
      });
      if (!res.ok) { last = res.status + ' ' + candidate; continue; }
      const buf = Buffer.from(await res.arrayBuffer());
      if (buf.length < 32) { last = 'too small ' + candidate; continue; }
      if (buf.length > 15 * 1024 * 1024) throw new Error('image exceeds 15MB: ' + candidate);
      return buf;
    } catch (err) {
      last = err.message || String(err);
    }
  }
  throw new Error(last);
}

function absolutize(url) {
  const u = String(url || '').trim();
  if (u.startsWith('//')) return 'https:' + u;
  return u;
}

export async function publishUrls(urls, opts = {}) {
  const root = opts.root || ROOT;
  const cfg = opts.cfg || mediaConfig();
  const map = await loadMap(root);
  const pending = [];
  const seen = new Set();
  for (const raw of urls || []) {
    const url = absolutize(raw);
    if (!isImageUrl(url) || seen.has(url)) continue;
    seen.add(url);
    if (cfg.publicBase && (url === cfg.publicBase || url.startsWith(cfg.publicBase + '/'))) continue;
    pending.push(url);
  }
  if (!pending.length) return { map, uploaded: 0, reused: 0, missing: [] };
  const missing = opts.missing ? opts.missing : missingMediaSecrets();
  if (missing.length) return { map, uploaded: 0, reused: 0, missing, pending: pending.length };
  const download = opts.download || ((url) => defaultDownload(url, opts.fetchImpl || fetch));
  const convert = opts.convert || toWebp;
  const put = opts.put || ((args) => putObject({ ...args, cfg, fetchImpl: opts.fetchImpl || fetch }));
  let uploaded = 0;
  let reused = 0;
  for (const url of pending) {
    const bin = await download(url);
    const webp = await convert(bin);
    const sha = sha256hex(webp.bytes);
    const prev = map.items[url];
    if (prev && prev.sha256 === sha && prev.url) {
      reused += 1;
      continue;
    }
    const key = `posts/${sha.slice(0, 2)}/${sha}.webp`;
    const publicUrl = await put({ body: webp.bytes, key, contentType: 'image/webp', cfg });
    const rec = { url: publicUrl, w: webp.w, h: webp.h, sha256: sha };
    map.items[url] = rec;
    const https = url.replace(/^http:\/\//i, 'https://');
    const http = url.replace(/^https:\/\//i, 'http://');
    if (https !== url) map.items[https] = rec;
    if (http !== url) map.items[http] = rec;
    uploaded += 1;
  }
  map.bucket = cfg.bucket || 'abadis-media';
  await saveMap(root, map);
  return { map, uploaded, reused, missing: [] };
}

export async function mediaSelfTest() {
  const os = await import('node:os');
  const { mkdtemp, rm } = await import('node:fs/promises');
  const urls = extractImageUrls('<img src="http://abadis-med.com/wp-content/uploads/2026/11/a.jpg" srcset="http://abadis-med.com/wp-content/uploads/2026/11/a-300x200.jpg 300w">');
  if (urls.length !== 2) throw new Error('media self-test: expected 2 urls, got ' + urls.length);
  const rewritten = rewriteText('see http://abadis-med.com/wp-content/uploads/a.jpg', {
    'https://abadis-med.com/wp-content/uploads/a.jpg': { url: 'https://abadis-media.example/posts/ab/cd.webp', w: 4, h: 2 },
  });
  if (!rewritten.includes('https://abadis-media.example/posts/ab/cd.webp')) throw new Error('media self-test: rewrite');
  const saved = {};
  for (const name of MEDIA_SECRET_NAMES) saved[name] = process.env[name];
  for (const name of MEDIA_SECRET_NAMES) delete process.env[name];
  const miss = missingMediaSecrets();
  if (miss.length !== MEDIA_SECRET_NAMES.length) throw new Error('media self-test: missing secret names');
  const dir = await mkdtemp(path.join(os.tmpdir(), 'abadis-media-'));
  const blocked = await publishUrls(['http://abadis-med.com/wp-content/uploads/a.jpg'], { root: dir });
  if (!blocked.missing.length || blocked.uploaded) throw new Error('media self-test: must not upload without secrets');
  process.env.ABADIS_MEDIA_ACCESS_KEY = 'AKIATEST';
  process.env.ABADIS_MEDIA_SECRET_KEY = 'secret-test';
  process.env.ABADIS_MEDIA_S3_ENDPOINT = 'http://127.0.0.1';
  process.env.ABADIS_MEDIA_PUBLIC_BASE = 'https://abadis-media.example';
  process.env.ABADIS_MEDIA_BUCKET = 'abadis-media';
  let puts = 0;
  const first = await publishUrls(['http://abadis-med.com/wp-content/uploads/a.jpg'], {
    root: dir,
    download: async () => Buffer.from('not-a-real-image-but-long-enough-bytes'),
    convert: async () => ({ bytes: Buffer.from('RIFFWEBP'), w: 8, h: 4 }),
    put: async ({ key, body }) => { puts += 1; if (!body.length) throw new Error('empty body'); return `https://abadis-media.example/${key}`; },
  });
  if (puts !== 1 || first.uploaded !== 1) throw new Error('media self-test: upload once');
  const second = await publishUrls(['https://abadis-med.com/wp-content/uploads/a.jpg'], {
    root: dir,
    download: async () => Buffer.from('not-a-real-image-but-long-enough-bytes'),
    convert: async () => ({ bytes: Buffer.from('RIFFWEBP'), w: 8, h: 4 }),
    put: async () => { throw new Error('should reuse'); },
  });
  if (second.reused !== 1) throw new Error('media self-test: second sync reuses the object');
  const server = http.createServer((req, res) => {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => {
      const got = Buffer.concat(chunks);
      if (req.method !== 'PUT' || !req.headers.authorization || got.toString() !== 'webp-body') {
        res.writeHead(500); res.end('bad'); return;
      }
      res.writeHead(200); res.end('ok');
    });
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  try {
    const port = server.address().port;
    const cfg = { ...mediaConfig(), endpoint: `http://127.0.0.1:${port}`, publicBase: 'https://abadis-media.example' };
    const loc = await putObject({ body: Buffer.from('webp-body'), key: 'posts/aa/bb.webp', contentType: 'image/webp', cfg });
    if (loc !== 'https://abadis-media.example/posts/aa/bb.webp') throw new Error('media self-test: public url');
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
  for (const name of MEDIA_SECRET_NAMES) {
    if (saved[name] === undefined) delete process.env[name];
    else process.env[name] = saved[name];
  }
  delete process.env.ABADIS_MEDIA_BUCKET;
  await rm(dir, { recursive: true, force: true });
}
