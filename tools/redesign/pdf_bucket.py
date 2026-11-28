"""Map a repo PDF under site/ to the Liara object bucket.

A file site/<path>.pdf is served from
https://abadis-media.storage.iran.liara.site/<path>.pdf
with each path segment percent-encoded as UTF-8. The list of paths lives in
data/site_pdfs.txt so a rebuild still emits bucket URLs after the files are
removed from the repo. PDFs under docs/ are not site files and are not mapped.
"""
import html
import os
import posixpath
import urllib.parse

BUCKET = 'https://abadis-media.storage.iran.liara.site'
_HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(_HERE, 'data', 'site_pdfs.txt')
SITE = os.path.abspath(os.path.join(_HERE, '..', '..', 'site'))

_SITE_HOSTS = {
    'abadis-med.com',
    'www.abadis-med.com',
    'abadis-media.storage.iran.liara.site',
    '$host',
}
_DELIM = set(' \t\n\r"\'<>()[]{},`\\')
_KNOWN = None


def pdf_bucket_url(site_rel):
    """Public URL for a PDF path relative to site/."""
    rel = (site_rel or '').replace('\\', '/').lstrip('/')
    parts = [p for p in rel.split('/') if p not in ('', '.')]
    return BUCKET + '/' + '/'.join(urllib.parse.quote(p, safe='') for p in parts)


def known_site_pdfs():
    global _KNOWN
    if _KNOWN is None:
        found = set()
        if os.path.isfile(MANIFEST):
            with open(MANIFEST, encoding='utf-8') as fh:
                for line in fh:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        found.add(line.replace('\\', '/').lstrip('/'))
        _KNOWN = frozenset(found)
    return _KNOWN


def reset_known_site_pdfs():
    global _KNOWN
    _KNOWN = None


def write_manifest_from_site():
    """Record every PDF currently under site/. Does not include docs/."""
    paths = []
    for dirpath, _dirs, files in os.walk(SITE):
        for name in files:
            if name.lower().endswith('.pdf'):
                full = os.path.join(dirpath, name)
                paths.append(os.path.relpath(full, SITE).replace(os.sep, '/'))
    paths.sort()
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    with open(MANIFEST, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(paths) + ('\n' if paths else ''))
    reset_known_site_pdfs()
    return paths


def _unquote(value):
    cur = value
    for _ in range(2):
        nxt = urllib.parse.unquote(cur)
        if nxt == cur:
            break
        cur = nxt
    return cur


def _strip_dot_segments(path):
    parts = []
    for seg in path.split('/'):
        if seg in ('', '.'):
            continue
        if seg == '..':
            if parts:
                parts.pop()
            continue
        parts.append(seg)
    return '/'.join(parts)


def _bucket_for_path(path, known):
    path = _strip_dot_segments((path or '').replace('\\', '/').lstrip('/'))
    if not path or not path.lower().endswith('.pdf'):
        return None
    if path in known:
        return pdf_bucket_url(path)
    if '/' not in path:
        return None
    hits = [k for k in known if k.endswith('/' + path)]
    if len(hits) == 1:
        return pdf_bucket_url(hits[0])
    return None


def bucket_for_reference(token, page_rel=''):
    """Bucket URL if token points at a known site PDF, else None.

    page_rel is the HTML path under site/ (for example en/center-download/index.html).
    Absolute abadis-med.com and same-host nginx ($host) URLs use their path.
    A relative link is resolved from page_rel first.
    """
    if not token or '.pdf' not in token.lower():
        return None
    known = known_site_pdfs()
    if not known:
        return None
    raw = html.unescape(token.strip())
    if raw.startswith('//'):
        raw = 'https:' + raw
    page_rel = (page_rel or '').replace('\\', '/').lstrip('/')
    if page_rel.endswith('/'):
        page_rel += 'index.html'

    if '://' in raw:
        parts = urllib.parse.urlsplit(raw)
        host = (parts.hostname or parts.netloc or '').lower()
        if host not in _SITE_HOSTS:
            return None
        return _bucket_for_path(_unquote(parts.path or ''), known)

    path = _unquote(raw.split('#', 1)[0].split('?', 1)[0])
    if page_rel and not path.startswith('/'):
        base = posixpath.dirname(page_rel)
        joined = posixpath.normpath(posixpath.join(base, path))
        if not joined.startswith('..') and joined in known:
            return pdf_bucket_url(joined)
    return _bucket_for_path(path, known)


def _expand_span(text, start, end, bucket):
    """Include a {pfx} or UP + '...' wrapper so the bucket URL is not prefixed twice."""
    if start >= 5 and text[start - 5:start] == '{pfx}':
        start -= 5
    quote = text[start - 1] if start else ''
    if quote in ("'", '"'):
        window = text[max(0, start - 40):start - 1]
        compact = ''.join(window.split())
        if compact.endswith('UP+'):
            up_at = text.rfind('UP', max(0, start - 40), start)
            if up_at >= 0 and end < len(text) and text[end] == quote:
                return up_at, end + 1, "'" + bucket + "'"
    return start, end, bucket


def rewrite_site_pdf_urls(text, page_rel=''):
    """Replace links to known site PDFs with bucket URLs. Other PDFs stay."""
    if not text or '.pdf' not in text.lower():
        return text
    parts = []
    last = 0
    low = text.lower()
    idx = 0
    while True:
        i = low.find('.pdf', idx)
        if i < 0:
            break
        start = i
        while start > 0 and text[start - 1] not in _DELIM:
            start -= 1
        end = i + 4
        while end < len(text) and text[end] not in _DELIM:
            end += 1
        token = text[start:end]
        bucket = bucket_for_reference(token, page_rel)
        if bucket and bucket != token:
            span_s, span_e, repl = _expand_span(text, start, end, bucket)
            if span_s < last:
                idx = i + 4
                continue
            parts.append(text[last:span_s])
            parts.append(repl)
            last = span_e
            idx = span_e
        else:
            idx = end if end > i else i + 4
    if not parts:
        return text
    parts.append(text[last:])
    return ''.join(parts)


def locale_of_file(rel):
    rel = (rel or '').replace('\\', '/')
    name = rel.rsplit('/', 1)[-1]
    if rel.startswith('site/en/') or rel.startswith('en/') or name.startswith('en_'):
        return 'en'
    if rel.startswith('site/arabic/') or rel.startswith('arabic/') or name.startswith('ar_'):
        return 'ar'
    if rel.startswith('tools/') or rel.startswith('content/'):
        return 'tools'
    return 'fa'


_SKIP_NAMES = {'three.module.js', 'pdf_bucket.py', 'site_pdfs.txt'}
_TEXT_EXT = {'.html', '.htm', '.js', '.mjs', '.json', '.py', '.txt', '.xml', '.conf', '.css', '.md', '.svg'}


def rewrite_tree(root, dry_run=False):
    """Rewrite site/ and tools/ text. Returns counts and unmapped abadis PDF tokens."""
    root = os.path.abspath(root)
    stats = {'files': 0, 'links': 0, 'by_locale': {'fa': 0, 'en': 0, 'ar': 0, 'tools': 0}}
    unmapped = {}
    changed_files = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '__pycache__')]
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == 'docs' or rel_dir.startswith('docs' + os.sep):
            dirs[:] = []
            continue
        top = rel_dir.split(os.sep, 1)[0]
        if top not in ('site', 'tools', '.'):
            continue
        for name in files:
            if name in _SKIP_NAMES:
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext not in _TEXT_EXT and name != '_redirects':
                continue
            full = os.path.join(dirpath, name)
            try:
                if os.path.getsize(full) > 8_000_000:
                    continue
                text = open(full, encoding='utf-8').read()
            except (OSError, UnicodeError):
                continue
            if '.pdf' not in text.lower():
                continue
            rel = os.path.relpath(full, root).replace(os.sep, '/')
            page_rel = ''
            if rel.startswith('site/') and ext in ('.html', '.htm'):
                page_rel = rel[len('site/'):]
            new = rewrite_site_pdf_urls(text, page_rel)
            if new == text:
                _note_unmapped(text, rel, unmapped)
                continue
            n = _count_replacements(text, new)
            loc = locale_of_file(rel)
            stats['files'] += 1
            stats['links'] += n
            stats['by_locale'][loc] = stats['by_locale'].get(loc, 0) + n
            changed_files.append(rel)
            if not dry_run:
                with open(full, 'w', encoding='utf-8') as fh:
                    fh.write(new)
            _note_unmapped(new, rel, unmapped)
    stats['changed_files'] = changed_files
    stats['unmapped'] = unmapped
    return stats


def _count_replacements(old, new):
    # Each rewritten link introduces the bucket host. Count new hosts minus old hosts.
    return max(0, new.count(BUCKET) - old.count(BUCKET))


def _note_unmapped(text, rel, unmapped):
    low = text.lower()
    idx = 0
    while True:
        i = low.find('.pdf', idx)
        if i < 0:
            return
        start = i
        while start > 0 and text[start - 1] not in _DELIM:
            start -= 1
        end = i + 4
        while end < len(text) and text[end] not in _DELIM:
            end += 1
        token = text[start:end]
        idx = end if end > i else i + 4
        if bucket_for_reference(token, rel[5:] if rel.startswith('site/') and rel.endswith('.html') else ''):
            continue
        if BUCKET in token:
            continue
        interesting = (
            'abadis-med.com' in token
            or 'wp-content/uploads' in token
            or '3d-sketches' in token
            or token.startswith('sheets/')
            or 'comparison-sheet.pdf' in token
        )
        if interesting:
            unmapped.setdefault(token, []).append(rel)
