"""Phase-2 generator: python3 tools/redesign/build.py  (writes into site/)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lib import SITE
WRITTEN = []
def write(rel, html):
    f = SITE / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html, encoding='utf-8'); WRITTEN.append(rel)

import pages_products
GROUPS = {'products': pages_products.build}
try:
    import pages_company; GROUPS.update(pages_company.GROUPS)
except ImportError: pass
import pages_calculator; GROUPS['calculator'] = pages_calculator.build   # abadismedit's redesign draft
try:
    import pages_posts; GROUPS['posts'] = pages_posts.build
except ImportError: pass
try:
    import pages_home; GROUPS['home'] = pages_home.build
except ImportError: pass
try:
    import pages_i18n
    GROUPS['i18n'] = pages_i18n.build
    GROUPS['en'] = lambda w: pages_i18n.build_lang(w, 'en')
    GROUPS['ar'] = lambda w: pages_i18n.build_lang(w, 'ar')
except ImportError: pass

if __name__ == '__main__':
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
