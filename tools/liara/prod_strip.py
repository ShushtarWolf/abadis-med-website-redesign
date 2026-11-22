#!/usr/bin/env python3
"""Copy a static site aside and strip preview noindex before a production deploy.

The source directory is not modified. Redirect stubs, option galleries, full-page
previews, and 404.html stay as they are. Every other HTML file loses exactly one
robots meta. robots.txt allows crawling. sitemap.xml is left alone. The gzipped
tarball of the staged site, honoring .liaraignore, must stay within 256 MiB.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

LIMIT = 256 * 1024 * 1024
STAGE_NAME = 'abadis-prod-site'
ROBOTS_TXT = 'User-agent: *\nAllow: /\n\nSitemap: https://abadis-med.com/sitemap.xml\n'
ROBOTS_RE = re.compile(
    r'[ \t]*(?:<!--\s*TODO\(launch\):[^>]*-->\s*\n)?[ \t]*<meta name="robots" content="noindex, nofollow">\s*\n?',
    re.I,
)
REFRESH_RE = re.compile(r'http-equiv="refresh"', re.I)
STILL_ROBOTS_RE = re.compile(r'name="robots"', re.I)
NON_REAL_DIRS = frozenset({
    'why-abadis-options',
    'careers-options',
    'articles-options',
    'news-hero-options',
    '3d-sketches',
    'cad-line-sketches',
    'chatbot-demo',
    'hero-test',
    'hero-options',
    'dial-designs',
    'dial-practical',
    'dial-steppers',
    'template-dials',
    'zagros-names',
    'home-hero-options',
    'contact-hero-options',
    'solutions-hero-options',
    'brand',
})


def keep(rel: str, text: str) -> bool:
    if REFRESH_RE.search(text):
        return True
    if rel.split('/', 1)[0] in NON_REAL_DIRS:
        return True
    if '/_full/' in f'/{rel}' or 'products-options/' in rel:
        return True
    return rel == '404.html' or rel.endswith('/404.html')


def _translate(pat: str) -> str:
    res = []
    i = 0
    n = len(pat)
    while i < n:
        c = pat[i]
        if c == '*':
            if i + 1 < n and pat[i + 1] == '*':
                if i + 2 < n and pat[i + 2] == '/':
                    res.append('(?:.*/)?')
                    i += 3
                    continue
                res.append('.*')
                i += 2
                continue
            res.append('[^/]*')
        elif c == '?':
            res.append('[^/]')
        else:
            res.append(re.escape(c))
        i += 1
    return ''.join(res)


def load_liaraignore(root: str):
    path = os.path.join(root, '.liaraignore')
    rules = []
    if not os.path.isfile(path):
        return rules
    with open(path, encoding='utf-8') as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            neg = line.startswith('!')
            if neg:
                line = line[1:]
            dir_only = line.endswith('/')
            if dir_only:
                line = line[:-1]
            if line.startswith('/'):
                line = line[1:]
            if not line:
                continue
            body = _translate(line)
            if '/' not in line:
                expr = r'(?:^|.*/)' + body + r'$'
            else:
                expr = r'^' + body + r'$'
            rules.append((neg, dir_only, re.compile(expr)))
    return rules


def _parents(path: str):
    parts = path.split('/')
    for i in range(1, len(parts)):
        yield '/'.join(parts[:i])


def is_ignored(path: str, is_dir: bool, rules) -> bool:
    state = False
    for neg, dir_only, rx in rules:
        matched = bool(rx.match(path)) and (not dir_only or is_dir)
        if dir_only and not matched:
            matched = any(rx.match(parent) for parent in _parents(path))
        if matched:
            state = not neg
    return state


def gzip_size(root: str) -> int:
    rules = load_liaraignore(root)
    handle = tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8')
    list_path = handle.name
    try:
        with handle:
            for dirpath, dirnames, filenames in os.walk(root):
                rel_dir = os.path.relpath(dirpath, root).replace(os.sep, '/')
                if rel_dir == '.':
                    rel_dir = ''
                kept_dirs = []
                for name in dirnames:
                    rel = f'{rel_dir}/{name}' if rel_dir else name
                    if not is_ignored(rel, True, rules):
                        kept_dirs.append(name)
                dirnames[:] = kept_dirs
                for name in filenames:
                    rel = f'{rel_dir}/{name}' if rel_dir else name
                    if is_ignored(rel, False, rules):
                        continue
                    handle.write('./' + rel + '\n')
        proc = subprocess.run(
            ['bash', '-lc', 'tar -C "$1" -cf - -T "$2" | gzip -c | wc -c', 'bash', root, list_path],
            check=True, capture_output=True, text=True,
        )
    finally:
        if os.path.exists(list_path):
            os.unlink(list_path)
    return int(proc.stdout.strip() or '0')


def check_gzip(root: str) -> int:
    size = gzip_size(root)
    mb = size / (1024 * 1024)
    cap = LIMIT / (1024 * 1024)
    print(f'compressed site size {mb:.1f} MB ({size} bytes; limit {cap:.0f} MB)')
    if size > LIMIT:
        print(f'site tarball would exceed {LIMIT} bytes compressed; not deploying', file=sys.stderr)
        return 1
    return 0


def make_stage(src: str) -> str:
    src = os.path.abspath(src)
    if not os.path.isdir(src):
        print(f'site directory missing: {src}', file=sys.stderr)
        return ''
    stage = os.path.join(tempfile.gettempdir(), STAGE_NAME)
    src_real = os.path.realpath(src)
    stage_real = os.path.realpath(stage)
    if src_real == stage_real or src_real.startswith(stage_real + os.sep):
        print('refusing to use a site directory inside the staging path', file=sys.stderr)
        return ''
    if os.path.isdir(stage):
        shutil.rmtree(stage)
    shutil.copytree(src, stage, symlinks=False)
    return stage


def strip_tree(stage: str) -> int:
    removed = 0
    kept = 0
    for dirpath, dirnames, filenames in os.walk(stage):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.endswith('.html'):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, stage).replace(os.sep, '/')
            with open(path, encoding='utf-8', newline='') as fh:
                text = fh.read()
            if keep(rel, text):
                kept += 1
                continue
            found = len(ROBOTS_RE.findall(text))
            if found != 1:
                print(f'{rel}: expected exactly one robots meta, found {found}', file=sys.stderr)
                return 1
            new, count = ROBOTS_RE.subn('', text, count=1)
            if count != 1 or STILL_ROBOTS_RE.search(new):
                print(f'{rel}: robots meta still present after removal', file=sys.stderr)
                return 1
            with open(path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(new)
            removed += 1
    robots_path = os.path.join(stage, 'robots.txt')
    with open(robots_path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(ROBOTS_TXT)
    print(f'removed {removed}')
    print(f'kept {kept}')
    return 0


def write_output(stage: str) -> None:
    print(f'staged {stage}')
    output = os.environ.get('GITHUB_OUTPUT')
    if not output:
        return
    with open(output, 'a', encoding='utf-8') as fh:
        fh.write(f'staged={stage}\n')


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print('usage: prod_strip.py SITE_DIR', file=sys.stderr)
        return 2
    stage = make_stage(args[0])
    if not stage:
        return 1
    if strip_tree(stage) != 0:
        return 1
    if check_gzip(stage) != 0:
        return 1
    write_output(stage)
    return 0


if __name__ == '__main__':
    sys.exit(main())
