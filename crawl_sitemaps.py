from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from urllib.parse import urlparse
from collections import Counter
import json, re

BASE = 'https://abadis-med.com/'
INDEX = BASE + 'sitemap_index.xml'

def fetch(url):
    req = Request(url, headers={'User-Agent': 'Abadis-Audit/1.0'})
    with urlopen(req, timeout=30) as r:
        return r.read()

def strip(tag):
    return tag.rsplit('}', 1)[-1]

def urls_from_xml(data):
    root = ET.fromstring(data)
    out = []
    for child in root:
        fields = {strip(x.tag): (x.text or '').strip() for x in child}
        if 'loc' in fields:
            out.append(fields)
    return out

index_rows = urls_from_xml(fetch(INDEX))
# Fall back to extracting locations if non-standard XML response is returned.
if not index_rows:
    text = fetch(INDEX).decode('utf-8', 'ignore')
    index_rows = [{'loc': x} for x in re.findall(r'https?://[^<\s]+', text)]

sitemaps = []
for row in index_rows:
    loc = row['loc'].replace('\\_', '_')
    sitemaps.append({'url': loc, 'lastmod': row.get('lastmod', '')})

all_rows = []
errors = []
for sm in sitemaps:
    try:
        rows = urls_from_xml(fetch(sm['url']))
        for row in rows:
            row['sitemap'] = sm['url']
        all_rows.extend(rows)
    except Exception as exc:
        errors.append({'sitemap': sm['url'], 'error': str(exc)})

urls = [r['loc'] for r in all_rows if r.get('loc')]
paths = [urlparse(u).path for u in urls]
summary = {
    'index_url': INDEX,
    'sitemaps': sitemaps,
    'sitemap_count': len(sitemaps),
    'url_count_total': len(urls),
    'unique_url_count': len(set(urls)),
    'errors': errors,
    'counts_by_sitemap': Counter(r['sitemap'] for r in all_rows),
    'counts_by_root': Counter((p.strip('/').split('/')[0] if p.strip('/') else '/') for p in paths),
    'sample_urls': sorted(set(urls))[:250],
    'all_urls': sorted(set(urls)),
}
with open('sitemap-inventory.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, default=dict)
print(json.dumps({k: v for k, v in summary.items() if k not in ('all_urls', 'sample_urls')}, ensure_ascii=False, indent=2, default=dict))
print('\nSample product-like routes:')
for u in sorted(set(urls)):
    if any(x in u.lower() for x in ('product', 'suction', 'filter', 'canister', 'connection', 'fixture', 'receiver', 'tube')):
        print(u)
