"""Percent-encoded WordPress slugs must enter and leave sitemap.xml.

WordPress stores the FA path already percent-encoded. The posts refresh has to
unquote and NFC-normalize that path before it looks for index.html, then write
the loc with the same encoding as the rest of the sitemap.
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import discovery


def main():
    root = Path(tempfile.mkdtemp(prefix='abadis-sitemap-'))
    try:
        site = root / 'site'
        slug = 'تست-نقشه-سایت'
        encoded = quote(slug, safe='')
        page = site / slug
        page.mkdir(parents=True)
        (page / 'index.html').write_text('<title>fake</title>\n', encoding='utf-8')
        (site / 'keep').mkdir()
        (site / 'keep' / 'index.html').write_text('keep\n', encoding='utf-8')
        (site / 'sitemap.xml').write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            '  <url><loc>https://abadis-med.com/keep/</loc></url>\n'
            '</urlset>\n',
            encoding='utf-8',
        )
        (site / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
        data = root / 'data'
        data.mkdir()
        (data / 'posts.json').write_text(
            json.dumps([{'path': '/' + encoded + '/', 'id': '99001'}], ensure_ascii=False),
            encoding='utf-8',
        )
        discovery.SITE = site
        discovery.DATA_DIR = data
        robots = (site / 'robots.txt').read_bytes()
        if discovery._page_key('/' + encoded + '/') != slug + '/':
            raise SystemExit('page key did not unquote the FA slug')
        discovery.refresh_posts_sitemap()
        text = (site / 'sitemap.xml').read_text(encoding='utf-8')
        loc = discovery._xml_loc(slug + '/')
        if loc not in text:
            raise SystemExit('encoded slug was not added: ' + loc)
        if '%25' in text:
            raise SystemExit('slug was double-encoded')
        if (site / 'robots.txt').read_bytes() != robots:
            raise SystemExit('robots changed')
        shutil.rmtree(page)
        (data / 'unpublished-posts.json').write_text(
            json.dumps({
                'version': 1,
                'posts': [{'id': '99001', 'slug': slug, 'sources': ['/' + encoded + '/']}],
            }, ensure_ascii=False),
            encoding='utf-8',
        )
        discovery.refresh_posts_sitemap()
        text = (site / 'sitemap.xml').read_text(encoding='utf-8')
        if encoded in text or slug in text:
            raise SystemExit('encoded slug was not removed')
        if 'https://abadis-med.com/keep/' not in text:
            raise SystemExit('live url dropped')
        print('encoded sitemap add/remove ok')
    finally:
        shutil.rmtree(root)


if __name__ == '__main__':
    main()
