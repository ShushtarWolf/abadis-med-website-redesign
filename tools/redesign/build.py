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
try:
    import pages_posts; GROUPS['posts'] = pages_posts.build
except ImportError: pass

if __name__ == '__main__':
    want = sys.argv[1:] or list(GROUPS)
    if 'posts' in GROUPS: pages_posts.prepare()   # fill POST_MAP first so every page links posts internally
    for g in want: GROUPS[g](write)
    print(len(WRITTEN), 'pages written'); [print(' ', w) for w in WRITTEN]
