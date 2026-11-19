"""sitemap.xml and robots.txt for the static preview.

Canonical and hreflang targets are the final https://abadis-med.com/ URLs.
robots.txt disallows crawling until launch (see the TODO in the file).
"""
from __future__ import annotations
import json
import sys
import pathlib
import re
from urllib.parse import quote, unquote, urlparse
from xml.sax.saxutils import escape

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lib import SITE, SITE_ORIGIN
from i18n import hreflang_links, _norm_site_path

# Design sandboxes, not pages of the public site.
SKIP_PREFIXES = (
    'dial-designs/',
    'dial-practical/',
    'dial-steppers/',
    'template-dials/',
    'hero-options/',
    'hero-test/',
    'zagros-names/',
)


def _xml_loc(site_path: str) -> str:
    path = _norm_site_path(site_path)
    enc = '/'.join(quote(part, safe='') for part in path.split('/'))
    return escape(SITE_ORIGIN + '/' + enc)


def _page_key(src: str) -> str:
    text = str(src or '').strip()
    if not text or text == '/':
        return ''
    return text.strip('/') + '/'


DATA_DIR = pathlib.Path(__file__).resolve().parent / 'data'


def _unpublished_paths():
    """Slug, /news/ID/ and /articles/ID/ for posts the pipeline has unpublished."""
    fp = DATA_DIR / 'unpublished-posts.json'
    blocked = set()
    if not fp.is_file():
        return blocked
    try:
        data = json.loads(fp.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return blocked
    for post in data.get('posts') or []:
        for src in post.get('sources') or []:
            blocked.add(_page_key(src))
        blocked.add(_page_key(post.get('slug') or ''))
        pid = str(post.get('id') or '')
        if pid:
            blocked.add('news/' + pid + '/')
            blocked.add('articles/' + pid + '/')
    blocked.discard('')
    return blocked


def _is_stub(idx: pathlib.Path) -> bool:
    try:
        with idx.open('rb') as fh:
            return b'abadis-moved' in fh.read(400)
    except OSError:
        return False


def public_pages():
    pages = []
    for idx in SITE.rglob('index.html'):
        rel = idx.relative_to(SITE).as_posix()
        path = '' if rel == 'index.html' else rel[:-len('index.html')]
        if any(path.startswith(p) for p in SKIP_PREFIXES):
            continue
        pages.append(path)
    pages.sort()
    return pages


def _post_paths():
    """Canonical paths of posts the manifests still publish."""
    paths = []
    posts_fp = DATA_DIR / 'posts.json'
    if posts_fp.is_file():
        for item in json.loads(posts_fp.read_text(encoding='utf-8')):
            paths.append(_page_key(item.get('path') or ''))
    for lang, prefix in (('en', 'en/'), ('ar', 'arabic/')):
        fp = DATA_DIR / (lang + '_posts.json')
        if not fp.is_file():
            continue
        for item in json.loads(fp.read_text(encoding='utf-8')):
            slug = str(item.get('slug') or '').strip('/')
            if slug:
                paths.append(prefix + slug + '/')
    return [p for p in paths if p]


def _loc_key(loc: str) -> str:
    path = unquote(urlparse(loc.strip()).path)
    if path in ('', '/'):
        return ''
    return path.strip('/') + '/'


def _id_stub(key: str, idx: pathlib.Path) -> bool:
    """Legacy /news/ID/ and /articles/ID/ stubs are not the public post URL."""
    if not _is_stub(idx):
        return False
    parts = key.strip('/').split('/')
    if len(parts) == 2 and parts[0] in ('news', 'articles') and parts[1].isdigit():
        return True
    if len(parts) == 3 and parts[0] in ('en', 'arabic') and parts[1] in ('news', 'articles') and parts[2].isdigit():
        return True
    return False


def write_sitemap():
    """Rewrite sitemap.xml from the pages on disk. Does not touch robots.txt."""
    urls = []
    for path in public_pages():
        links = hreflang_links(path)
        alt = ''
        if links:
            alt = ''.join(
                f'<xhtml:link rel="alternate" hreflang="{escape(hl)}" href="{_xml_loc(href[len(SITE_ORIGIN) + 1:])}"/>'
                for hl, href in links
            )
        urls.append(f'  <url><loc>{_xml_loc(path)}</loc>{alt}</url>')
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + '\n'.join(urls) + '\n</urlset>\n'
    )
    (SITE / 'sitemap.xml').write_text(xml, encoding='utf-8')
    print('sitemap ' + str(len(urls)) + ' urls')
    return len(urls)


def refresh_posts_sitemap():
    """Add published post URLs and drop ones the posts build removed.

    Other sitemap entries stay as they are. robots.txt is not written.
    """
    sm = SITE / 'sitemap.xml'
    if not sm.is_file():
        return write_sitemap()
    text = sm.read_text(encoding='utf-8')
    blocked = _unpublished_paths()
    removed = 0

    def consider(found):
        nonlocal removed
        block = found.group(0)
        loc = re.search(r'<loc>([^<]+)</loc>', block)
        if not loc:
            return block
        key = _loc_key(loc.group(1))
        idx = SITE / 'index.html' if key == '' else SITE / key.rstrip('/') / 'index.html'
        if key in blocked or not idx.is_file() or _id_stub(key, idx):
            removed += 1
            return ''
        return block

    updated = re.sub(r'[ \t]*<url>\s*[\s\S]*?</url>\n?', consider, text)
    seen = set()
    for match in re.finditer(r'<loc>([^<]+)</loc>', updated):
        seen.add(_loc_key(match.group(1)))
    added = []
    for key in _post_paths():
        if key in seen or key in blocked:
            continue
        idx = SITE / key.rstrip('/') / 'index.html'
        if not idx.is_file() or _is_stub(idx):
            continue
        added.append('  <url><loc>' + _xml_loc(key) + '</loc></url>\n')
        seen.add(key)
    if added:
        updated = updated.replace('</urlset>', ''.join(added) + '</urlset>', 1)
    if updated != text:
        sm.write_text(updated, encoding='utf-8')
    print('sitemap posts +' + str(len(added)) + ' -' + str(removed))
    return len(added)


def write_sitemap_and_robots():
    write_sitemap()
    robots = (
        '# Preview build. TODO(launch): allow crawling and confirm the Sitemap URL\n'
        '# after the site is published on https://abadis-med.com/.\n'
        'User-agent: *\n'
        'Disallow: /\n'
        '\n'
        'Sitemap: https://abadis-med.com/sitemap.xml\n'
    )
    (SITE / 'robots.txt').write_text(robots, encoding='utf-8')
    print('robots.txt disallow')


if __name__ == '__main__':
    write_sitemap_and_robots()
