"""One live slug per post.

Percent-encoded and NFC variants of a path are the same slug. When a CMS post
from abadis-wp-test and a legacy abadis-med.com import share that slug, the CMS
post wins: it keeps the page, and each legacy id redirects to the slug.
"""
import unicodedata
import urllib.parse


def norm_slug_path(path):
    path = urllib.parse.unquote(path or '')
    path = unicodedata.normalize('NFC', path)
    path = path.split('?', 1)[0].split('#', 1)[0]
    if not path.startswith('/'):
        path = '/' + path
    if path != '/' and not path.endswith('/'):
        path += '/'
    return path


def origin_of(post):
    url = post.get('url') or post.get('link') or ''
    host = urllib.parse.urlsplit(url).netloc.lower()
    if 'abadis-wp-test' in host:
        return 'cms'
    if 'abadis-med.com' in host:
        return 'legacy'
    return 'other'


def slug_of(post):
    raw = post.get('path') or urllib.parse.urlsplit(post.get('url') or post.get('link') or '').path
    return norm_slug_path(raw)


def resolve_slug_owners(posts):
    """Return (winner_ids, losers).

    losers are legacy imports replaced by a CMS post at the same slug.
    Each loser is {id, slug, sources}. Other duplicates are left unresolved
    so the migration still reports a collision.
    """
    groups = {}
    for post in posts or []:
        key = slug_of(post)
        if not key or key == '/':
            continue
        groups.setdefault(key, []).append(post)
    winners = set()
    losers = []
    for path, items in groups.items():
        ids = [str(item.get('id')) for item in items]
        if len(items) == 1:
            winners.add(ids[0])
            continue
        cms = [item for item in items if origin_of(item) == 'cms']
        legacy = [item for item in items if origin_of(item) == 'legacy']
        if len(cms) == 1 and len(legacy) == len(items) - 1 and legacy:
            winners.add(str(cms[0].get('id')))
            for item in legacy:
                lid = str(item.get('id'))
                losers.append({
                    'id': lid,
                    'slug': path,
                    'sources': ['/articles/%s/' % lid, '/news/%s/' % lid],
                })
            continue
        winners.update(ids)
    return winners, losers


def loser_ids(posts):
    _, losers = resolve_slug_owners(posts)
    return {item['id'] for item in losers}
