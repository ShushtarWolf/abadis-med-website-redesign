#!/usr/bin/env python3
"""Read one image on stdin and write WebP bytes on stdout. Width and height go to stderr.

Used by scripts/publish-post-media.mjs. Does not write into the repo.
"""
import sys
from io import BytesIO

from PIL import Image, ImageSequence


def main():
    data = sys.stdin.buffer.read()
    im = Image.open(BytesIO(data))
    animated = getattr(im, 'is_animated', False) and im.format == 'GIF'
    w, h = im.size
    out = BytesIO()
    if animated:
        frames, durs = [], []
        for fr in ImageSequence.Iterator(im):
            frames.append(fr.convert('RGBA'))
            durs.append(fr.info.get('duration', 100))
        frames[0].save(out, 'WEBP', save_all=True, append_images=frames[1:], duration=durs, loop=0, quality=70, method=4)
    else:
        mode = 'RGBA' if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info) else 'RGB'
        im.convert(mode).save(out, 'WEBP', quality=78, method=5)
    sys.stdout.buffer.write(out.getvalue())
    print(f'{w} {h}', file=sys.stderr)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'to_webp: {exc}', file=sys.stderr)
        sys.exit(1)
