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
try:
    import pages_archives; GROUPS['archives'] = pages_archives.build
except ImportError: pass

def _site_snapshot():
    """WebP names plus a hash of HTML, so a posts build can tell that it changed the tree."""
    import hashlib
    names = []
    img = SITE / 'assets/img/c'
    if img.is_dir():
        names = sorted(p.name for p in img.glob('*.webp'))
    digest = hashlib.sha256()
    for path in sorted(SITE.rglob('*.html')):
        digest.update(path.relative_to(SITE).as_posix().encode())
        digest.update(path.read_bytes())
    return tuple(names), digest.hexdigest()

def _localize_once():
    """One localizer process per build. python -u so each fetch line reaches the log."""
    import subprocess
    script = pathlib.Path(__file__).resolve().parent / 'localize_remote_images.py'
    print('localize once')
    subprocess.run([sys.executable, '-u', str(script)], check=True)

def _run_groups(want, posts_scoped, localize):
    built = 0
    if posts_scoped:
        import localize_remote_images
        built = localize_remote_images.prefetch_post_images() or 0
    WRITTEN.clear()
    seen = set()
    for g in want:
        if g in seen: continue
        if g == 'i18n':
            seen.update(('i18n', 'en', 'ar'))
        else:
            seen.add(g)
        if g == 'i18n' and posts_scoped:
            pages_i18n.build_posts_only(write)
        else:
            GROUPS[g](write)
    print(len(WRITTEN), 'pages written'); [print(' ', w) for w in WRITTEN]
    if not sys.argv[1:] or 'solutions' in sys.argv[1:] or 'products' in sys.argv[1:]:
        import solutions_arch
        solutions_arch.write_solution_pages()
        solutions_arch.write_redirects()
    if not sys.argv[1:]:
        from discovery import write_sitemap_and_robots
        write_sitemap_and_robots()
    # SEO post-process (JSON-LD, alt text, canonical, self-hosted docs, 404, Liara nginx config)
    import seo_postprocess
    seo_postprocess.main(list(WRITTEN) if posts_scoped else None)
    # Live-identical URLs: move generated pages to the abadis-med.com paths (FA Persian slugs, /en/, /arabic/),
    # rewrite links/canonicals/hreflang/sitemap, leave redirect stubs + 301 rules at the old paths.
    import subprocess
    subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve().parent / 'url_migrate.py')], check=True)
    if localize:
        _localize_once()
    return built

if __name__ == '__main__':
    try:
        import solutions_arch
        solutions_arch.assert_nav_catalog_sync()
    except ImportError:
        pass
    want = sys.argv[1:] or [g for g in GROUPS if g not in ('en', 'ar')]  # full build includes i18n once
    # A posts publish must not rebuild product or company pages. EN/AR still refresh their posts.
    posts_scoped = bool(sys.argv[1:]) and set(sys.argv[1:]).issubset({'posts', 'home', 'i18n', 'archives', 'en', 'ar'})
    if 'posts' in GROUPS: pages_posts.prepare()   # fill POST_MAP first so every page links posts internally
    import pages_archives
    pages_archives.SKIP_SPECIALS = posts_scoped
    if posts_scoped:
        # Writes repeat until the HTML settles. The localizer runs after that,
        # at most once, and a warm cache (nothing new to fetch) skips it.
        previous = _site_snapshot()
        last_built = 0
        for _pass in range(1, 5):
            print(f'posts pass {_pass}')
            last_built = _run_groups(want, posts_scoped, localize=False)
            current = _site_snapshot()
            if current == previous:
                print(f'posts pass {_pass} stable')
                break
            previous = current
        import localize_remote_images
        unknown = localize_remote_images.unknown_remote_srcs()
        if last_built == 0 and not unknown:
            print('localize skipped: cache warm, no unknown remote images')
        else:
            _localize_once()
            _run_groups(want, posts_scoped, localize=False)
    else:
        _run_groups(want, posts_scoped, localize=True)
