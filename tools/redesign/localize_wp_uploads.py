#!/usr/bin/env python3
"""Download leftover abadis-med.com upload images and point the built HTML at local WebPs.

The files still live on the old HostIran server. Fetch over plain HTTP from
45.138.134.42 with a Host header. One WebP (max 1600px) stands in for every
WordPress -WIDTHxHEIGHT variant. PDFs under site/en/wp-content are not touched.

    python3 tools/redesign/localize_wp_uploads.py          # download, map, rewrite
    python3 tools/redesign/localize_wp_uploads.py --scan   # counts only
"""
from __future__ import annotations

import hashlib
import json
import posixpath
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageFile, ImageSequence

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = 80_000_000

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
OUT = SITE / 'assets' / 'img' / 'c'
MAP_PATH = Path(__file__).resolve().parent / 'data' / 'wp_local_images.json'
IP = '45.138.134.42'
UA = 'AbadisRedesignBot/1.0 (+local rebuild)'
IMG_EXT = re.compile(r'\.(?:jpe?g|png|gif|webp|svg|bmp|avif)$', re.I)
SIZE_RE = re.compile(r'-(\d+)x(\d+)(?=\.[A-Za-z0-9]+$)')


def locale_of(rel: str) -> str:
    if rel.startswith('en/'):
        return 'en'
    if rel.startswith('arabic/'):
        return 'ar'
    return 'fa'


def prefix_for(rel: str) -> str:
    depth = max(0, len(Path(rel).parts) - 1)
    return '../' * depth


def magic(data: bytes) -> bool:
    if not data or len(data) < 16:
        return False
    head = data[:200].lstrip().lower()
    if head.startswith(b'<!doctype') or head.startswith(b'<html') or head.startswith(b'<?xml'):
        return False
    return (
        data[:3] == b'\xff\xd8\xff'
        or data[:8] == b'\x89PNG\r\n\x1a\n'
        or data[:6] in (b'GIF87a', b'GIF89a')
        or (data[:4] == b'RIFF' and data[8:12] == b'WEBP')
    )


def fetch(path: str) -> bytes | None:
    enc = '/'.join(urllib.parse.quote(seg) for seg in path.split('/'))
    hosts = (
        ['www.abadis-med.com', 'abadis-med.com']
        if path.startswith('/en/')
        else ['abadis-med.com', 'www.abadis-med.com']
    )
    for host in hosts:
        req = urllib.request.Request(
            'http://' + IP + enc,
            headers={'Host': host, 'User-Agent': UA, 'Accept': 'image/*,*/*'},
        )
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = resp.read(12_000_000)
        except Exception:
            continue
        if magic(data):
            return data
    return None


def width_of(path: str) -> int | None:
    m = SIZE_RE.search(path)
    return int(m.group(1)) if m else None


def fetch_best(paths: list[str]) -> tuple[bytes | None, str]:
    """Prefer a variant around 1600px so we do not pull a multi-megabyte original."""
    sized = []
    unsized = []
    for path in paths:
        w = width_of(path)
        if w is None:
            unsized.append(path)
        else:
            sized.append((w, path))
    order = []
    under = [p for w, p in sized if 600 <= w <= 1700]
    if under:
        order.append(max(under, key=lambda p: width_of(p) or 0))
    over = sorted((p for w, p in sized if w > 1700), key=lambda p: width_of(p) or 0)
    order.extend(over[:1])
    order.extend(unsized)
    order.extend(p for _w, p in sorted(sized, key=lambda t: -t[0]))
    seen = set()
    for path in order:
        if path in seen:
            continue
        seen.add(path)
        data = fetch(path)
        if data:
            return data, path
    return None, ''


def to_webp(data: bytes, dest: Path) -> tuple[int, int, int]:
    im = Image.open(BytesIO(data))
    im.load()
    w, h = im.size
    maxw = 1600
    if w > maxw:
        nw, nh = maxw, max(1, round(h * maxw / w))
    else:
        nw, nh = w, h
    animated = bool(getattr(im, 'is_animated', False) and getattr(im, 'n_frames', 1) > 1)
    if animated and im.n_frames > 30:
        animated = False
    dest.parent.mkdir(parents=True, exist_ok=True)
    if animated:
        frames, durs = [], []
        for i, fr in enumerate(ImageSequence.Iterator(im)):
            if i >= 40:
                break
            dur = fr.info.get('duration', im.info.get('duration', 100))
            frame = fr.convert('RGBA')
            if (nw, nh) != (w, h):
                frame = frame.resize((nw, nh), Image.Resampling.LANCZOS)
            frames.append(frame)
            durs.append(dur or 100)
        frames[0].save(
            dest, 'WEBP', save_all=True, append_images=frames[1:],
            duration=durs, loop=0, quality=58, method=4,
        )
    else:
        has_alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
        mode = 'RGBA' if has_alpha else 'RGB'
        im2 = im.convert(mode)
        if (nw, nh) != (w, h):
            im2 = im2.resize((nw, nh), Image.Resampling.LANCZOS)
        q = 78 if max(nw, nh) <= 700 else 70
        im2.save(dest, 'WEBP', quality=q, method=4)
        if dest.stat().st_size > 180_000:
            im2.save(dest, 'WEBP', quality=60, method=6)
        if dest.stat().st_size > 260_000 and nw > 1200:
            nw2 = 1200
            nh2 = max(1, round(nh * nw2 / nw))
            im2.resize((nw2, nh2), Image.Resampling.LANCZOS).save(dest, 'WEBP', quality=60, method=6)
            nw, nh = nw2, nh2
    with Image.open(dest) as saved:
        sw, sh = saved.size
    return dest.stat().st_size, sw, sh


def harvest():
    """Return groups, before-counts, and the page list for every image URL."""
    groups = {}
    pages_hit = {'en': set(), 'ar': set(), 'fa': set()}
    urls_hit = {'en': set(), 'ar': set(), 'fa': set()}
    url_pages = defaultdict(set)
    for fp in SITE.rglob('*.html'):
        rel = fp.relative_to(SITE).as_posix()
        text = fp.read_text(encoding='utf-8', errors='replace')
        if 'wp-content/uploads' not in text:
            continue
        loc = locale_of(rel)
        for m in lib._UPLOAD_URL_RE.finditer(text):
            path = _match_path(m, rel)
            if not path or '/wp-content/uploads/' not in path or not IMG_EXT.search(path):
                continue
            if not m.group(1):
                local_file = SITE / path.lstrip('/')
                if local_file.is_file():
                    continue
            raw = m.group(0)
            urls_hit[loc].add(path)
            pages_hit[loc].add(rel)
            canon = lib.unsized_upload_path(path)
            g = groups.get(canon)
            if not g:
                g = {'canon': canon, 'paths': set(), 'pages': set()}
                groups[canon] = g
            g['paths'].add(path)
            g['pages'].add(rel)
            url_pages[path].add(rel)
    return groups, pages_hit, urls_hit, url_pages


def _match_path(m, page_rel: str) -> str:
    abs_path, ups, rooted, bare = m.group(1), m.group(2), m.group(3), m.group(4)
    if abs_path:
        return urllib.parse.unquote(abs_path.split('?', 1)[0].split('#', 1)[0])
    raw = ups or rooted or bare or ''
    raw = urllib.parse.unquote(raw.split('?', 1)[0].split('#', 1)[0])
    if raw.startswith('/'):
        return raw
    if raw.startswith('../') or raw.startswith('./'):
        base = posixpath.dirname(page_rel)
        joined = posixpath.normpath(posixpath.join(base, raw))
        if joined.startswith('..'):
            return ''
        return '/' + joined
    if 'wp-content/uploads/' in raw:
        return '/' + raw[raw.find('wp-content/uploads/'):]
    return ''


def existing_webp(paths: set[str], canon: str) -> Path | None:
    idx = lib._wp_stem_index()
    hits = []
    for key in [canon, *paths]:
        stem = hashlib.sha1(key.encode()).hexdigest()[:12]
        hits.extend(idx.get(stem) or [])
    if not hits:
        return None

    def nominal(f: Path) -> int:
        m = re.search(r'-(\d+)\.webp$', f.name)
        return int(m.group(1)) if m else 0

    best = max(hits, key=lambda f: (nominal(f), f.stat().st_size))
    if nominal(best) < 480:
        return None
    return best


def dims(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def is_recovered(canon: str) -> bool:
    rel = canon.split('/wp-content/uploads/', 1)[-1]
    rel = lib.unsized_upload_path(rel)
    return lib.recovered_image('https://abadis-med.com/wp-content/uploads/' + rel) is not None


def main():
    scan_only = '--scan' in sys.argv
    groups, pages_hit, urls_hit, url_pages = harvest()
    print('BEFORE pages', {k: len(v) for k, v in pages_hit.items()})
    print('BEFORE urls', {k: len(v) for k, v in urls_hit.items()})
    print('groups', len(groups), 'variant urls', sum(len(g['paths']) for g in groups.values()))
    if scan_only:
        return

    OUT.mkdir(parents=True, exist_ok=True)
    lib.reset_wp_image_cache()
    mapping = {}
    reused = 0
    recovered = 0
    failed = []
    added = 0
    created = set()
    todo = []
    for canon, g in groups.items():
        if is_recovered(canon):
            recovered += 1
            continue
        have = existing_webp(g['paths'], canon)
        if have:
            w, h = dims(have)
            rec = {'src': 'assets/img/c/' + have.name, 'w': w, 'h': h}
            for path in g['paths']:
                mapping[path] = rec
            mapping[canon] = rec
            reused += 1
            continue
        todo.append(g)

    print(f'recovered-bucket {recovered}  reuse-webp {reused}  download {len(todo)}')

    def work(g):
        data, src = fetch_best(sorted(g['paths'], key=lambda p: (width_of(p) or 10_000, p)))
        # also try the unsized original even when it was not linked
        if data is None:
            data, src = fetch_best([g['canon']])
        return g, data, src

    done = 0
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = [pool.submit(work, g) for g in todo]
        for fut in as_completed(futs):
            g, data, src = fut.result()
            done += 1
            if done % 25 == 0 or done == len(todo):
                print(f'  fetched {done}/{len(todo)}', flush=True)
            if not data:
                failed.append(g)
                continue
            stem = hashlib.sha1(g['canon'].encode()).hexdigest()[:12]
            dest = OUT / f'{stem}-1600.webp'
            try:
                nbytes, w, h = to_webp(data, dest)
            except Exception as exc:
                print('CONVERT FAIL', g['canon'], exc)
                failed.append(g)
                if dest.exists() and dest.stat().st_size < 32:
                    dest.unlink()
                continue
            added += nbytes
            created.add(dest.name)
            rec = {'src': 'assets/img/c/' + dest.name, 'w': w, 'h': h}
            for path in g['paths']:
                mapping[path] = rec
            mapping[canon] = rec

    # If the new bytes are still heavy, squeeze the largest files once.
    if added > 9_000_000:
        biggest = sorted(OUT.glob('*.webp'), key=lambda p: p.stat().st_size, reverse=True)
        for fp in biggest:
            if added <= 8_000_000:
                break
            # only files this run recorded
            if fp.name not in created:
                continue
            before = fp.stat().st_size
            if before < 120_000:
                continue
            try:
                with Image.open(fp) as im:
                    im = im.convert('RGBA' if im.mode == 'RGBA' else 'RGB')
                    w, h = im.size
                    if w > 1200:
                        h = max(1, round(h * 1200 / w))
                        w = 1200
                        im = im.resize((w, h), Image.Resampling.LANCZOS)
                    im.save(fp, 'WEBP', quality=56, method=6)
                after = fp.stat().st_size
                if after < before:
                    added -= before - after
                    for rec in mapping.values():
                        if rec['src'].endswith('/' + fp.name):
                            rec['w'], rec['h'] = w, h
            except Exception as exc:
                print('RECOMPRESS FAIL', fp.name, exc)

    MAP_PATH.write_text(json.dumps(mapping, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    lib.reset_wp_image_cache()

    changed = 0
    for fp in SITE.rglob('*.html'):
        rel = fp.relative_to(SITE).as_posix()
        text = fp.read_text(encoding='utf-8', errors='replace')
        if 'wp-content/uploads' not in text:
            continue
        new = lib.localize_abadis_upload_urls(text, prefix_for(rel), rel)
        if new != text:
            fp.write_text(new, encoding='utf-8')
            changed += 1
    print('html files rewritten', changed)

    groups2, pages2, urls2, _pages = harvest()
    print('AFTER pages', {k: len(v) for k, v in pages2.items()})
    print('AFTER urls', {k: len(v) for k, v in urls2.items()})
    print('bytes_added', added)
    print('FAILED', len(failed))
    for g in failed:
        sample = sorted(g['pages'])[:6]
        print('FAIL', g['canon'])
        for page in sample:
            print('   page', page)
    # css/js hotlinks, reported only
    extra = []
    for fp in list(SITE.rglob('*.css')) + list(SITE.rglob('*.js')):
        text = fp.read_text(encoding='utf-8', errors='replace')
        if 'abadis-med.com' in text and 'wp-content/uploads' in text:
            extra.append(fp.relative_to(SITE).as_posix())
    print('css/js hotlinks', extra)


if __name__ == '__main__':
    main()
