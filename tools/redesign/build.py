"""Phase-2 generator: python3 tools/redesign/build.py  (writes into site/)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lib import SITE
WRITTEN = []
import re as _re
def _one_h1(html):
    """SEO: exactly one H1 per page — demote any H1 that comes from pasted WP content to H2."""
    first = html.find('<h1')
    if first < 0: return html
    head, tail = html[:first + 3], html[first + 3:]
    tail = _re.sub(r'<h1(\s[^>]*)?>', lambda m: '<h2' + (m.group(1) or '') + '>', tail)
    tail = tail.replace('</h1>', '</h2>')
    return head + tail.replace('</h2>', '</h1>', 1)
def write(rel, html):
    html = _one_h1(html)
    f = SITE / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html, encoding='utf-8'); WRITTEN.append(rel)

import pages_products
GROUPS = {'products': pages_products.build}
try:
    import pages_company; GROUPS.update(pages_company.GROUPS)
except ImportError: pass
import pages_calculator; import pages_dial
GROUPS['calculator'] = lambda w: (pages_calculator.build(w), pages_dial.build(w))   # abadismedit's redesign draft
try:
    import pages_posts; GROUPS['posts'] = pages_posts.build
except ImportError: pass
try:
    import pages_home; GROUPS['home'] = pages_home.build
except ImportError: pass
try:
    import pages_hero_test; GROUPS.update(pages_hero_test.GROUPS)
except ImportError: pass
try:
    import pages_i18n
    GROUPS['i18n'] = pages_i18n.build
    GROUPS['en'] = lambda w: pages_i18n.build_lang(w, 'en')
    GROUPS['ar'] = lambda w: pages_i18n.build_lang(w, 'ar')
except ImportError: pass

try:
    import pages_export; GROUPS['export'] = pages_export.build
except ImportError: pass

if __name__ == '__main__':
    try:
        import solutions_arch
        solutions_arch.assert_nav_catalog_sync()
    except ImportError:
        pass
    want = sys.argv[1:] or [g for g in GROUPS if g not in ('en', 'ar')]  # full build includes i18n once
    if 'posts' in GROUPS: pages_posts.prepare()   # fill POST_MAP first so every page links posts internally
    # avoid double-running en/ar when both i18n and en/ar requested
    seen = set()
    for g in want:
        if g in seen: continue
        if g == 'i18n':
            seen.update(('i18n', 'en', 'ar'))
        else:
            seen.add(g)
        GROUPS[g](write)
    print(len(WRITTEN), 'pages written'); [print(' ', w) for w in WRITTEN]
    if not sys.argv[1:] or 'solutions' in sys.argv[1:] or 'products' in sys.argv[1:]:
        import solutions_arch
        solutions_arch.write_solution_pages()
        solutions_arch.write_redirects()
    if not sys.argv[1:]:
        from discovery import write_sitemap_and_robots
        write_sitemap_and_robots()
