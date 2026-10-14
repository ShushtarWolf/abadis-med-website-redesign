"""sitemap.xml and robots.txt for the static preview.

Canonical and hreflang targets are the final https://abadis-med.com/ URLs.
robots.txt disallows crawling until launch (see the TODO in the file).
"""
from __future__ import annotations
import sys
import pathlib
from urllib.parse import quote
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


def write_sitemap_and_robots():
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
    robots = (
        '# Preview build. TODO(launch): allow crawling and confirm the Sitemap URL\n'
        '# after the site is published on https://abadis-med.com/.\n'
        'User-agent: *\n'
        'Disallow: /\n'
        '\n'
        'Sitemap: https://abadis-med.com/sitemap.xml\n'
    )
    (SITE / 'robots.txt').write_text(robots, encoding='utf-8')
    print(f'sitemap {len(urls)} urls; robots.txt disallow')


if __name__ == '__main__':
    write_sitemap_and_robots()
