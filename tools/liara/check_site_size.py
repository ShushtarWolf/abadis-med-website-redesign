#!/usr/bin/env python3
"""Fail if a gzipped tarball of the static site would exceed the Liara safety limit.

The Liara static cap is 350 MB compressed. This stops at 320 MB so a publish
does not get close to the cap. Set ABADIS_SITE_DIR to measure another directory
and ABADIS_SITE_GZIP_LIMIT to override the byte limit (tests only).
"""
import os
import subprocess
import sys

LIMIT = int(os.environ.get('ABADIS_SITE_GZIP_LIMIT', str(320 * 1024 * 1024)))
ROOT = os.environ.get('ABADIS_SITE_DIR', 'site')


def gzip_size(root: str) -> int:
    proc = subprocess.run(
        ['bash', '-lc', 'tar -C "$1" -cf - . | gzip -c | wc -c', 'bash', root],
        check=True, capture_output=True, text=True,
    )
    return int(proc.stdout.strip() or '0')


def main():
    if not os.path.isdir(ROOT):
        print(f'site directory missing: {ROOT}', file=sys.stderr)
        return 1
    size = gzip_size(ROOT)
    mb = size / (1024 * 1024)
    cap = LIMIT / (1024 * 1024)
    print(f'compressed site size {mb:.1f} MB ({size} bytes; limit {cap:.0f} MB)')
    if size > LIMIT:
        print(f'site tarball would exceed {LIMIT} bytes compressed; not deploying', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
