"""Crop old social-media post graphics (teal/white template with baked-in caption) to their inner photo.

inner(rel) -> site-relative path of a cropped copy, or None when the image is not a template graphic
or cannot be cropped cleanly (then the card just fits the original inside the theme frame)."""
from lib import SITE

TEAL = (14, 116, 118)
_cache = {}

def _near(c, ref, tol=34):
    return sum(abs(a - b) for a, b in zip(c, ref)) < tol

def _bg(c):
    return min(c) > 238 or _near(c, TEAL, 60)

def _runs(vals, thr, gap=6):
    best, cur, start, miss = (0, 0, 0), 0, None, 0
    for i, v in enumerate(vals + [0] * (gap + 1)):
        if v >= thr:
            if start is None: start = i
            miss, end = 0, i
        elif start is not None:
            miss += 1
            if miss > gap:
                if end - start > best[0]: best = (end - start, start, end)
                start, miss = None, 0
    return best

def detect(im):
    im = im.convert('RGB'); w, h = im.size
    s = im.resize((w // 2, h // 2)); sw, sh = s.size; px = s.load()
    corners = [px[2, 2], px[sw - 3, 2], px[2, sh - 3], px[sw - 3, sh - 3], px[2, sh // 2], px[sw - 3, sh // 2], px[sw // 2, 2]]
    if sum(_bg(c) for c in corners) < 6:
        return None                                  # a plain photo: nothing to strip
    if not any(_near(c, TEAL, 60) for c in corners):
        return None
    centre = px[int(sw * .25), int(sh * .2)]
    rows = [sum(not _bg(px[x, y]) for x in range(sw)) / sw for y in range(sh)]
    n, y0, y1 = _runs(rows, .3)
    if n < sh * .35: return _fixed(px, sw, sh, w, h) or 'fit'
    cols = [sum(not _bg(px[x, y]) for y in range(y0, y1 + 1)) / (y1 - y0 + 1) for x in range(sw)]
    n2, x0, x1 = _runs(cols, .5)
    if n2 < sw * .4: return 'fit'
    pad = 9
    box = ((x0 + pad) * 2, (y0 + pad) * 2, (x1 - pad) * 2, (y1 - pad) * 2)
    if (box[2] - box[0]) / max(1, box[3] - box[1]) > 3.2: return 'fit'
    return box

def _fixed(px, sw, sh, w, h):
    # template whose photo is a product on white: take the known photo window above the caption
    if min(px[int(sw * .25), int(sh * .2)]) > 238 and _near(px[3, int(sh * .4)], TEAL, 60):
        return (int(w * .19), int(h * .13), int(w * .81), int(h * .64))
    return None

def frame(rel):
    """(src, mode): mode 'crop' = cropped inner photo, 'fit' = template graphic shown whole, '' = plain photo."""
    if rel in _fcache: return _fcache[rel]
    r = inner(rel)
    out = (r, 'crop') if r else (rel, 'fit' if _mode.get(rel) == 'fit' else '')
    _fcache[rel] = out
    return out

_fcache, _mode = {}, {}

def inner(rel):
    if rel in _cache: return _cache[rel]
    out = None
    try:
        from PIL import Image
        src = SITE / rel
        dst_rel = rel.rsplit('.', 1)[0] + '-in.webp'
        dst = SITE / dst_rel
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            out = dst_rel
        else:
            big = src
            for w in ('1200', '960'):
                cand = SITE / rel.replace('-640.', f'-{w}.')
                if cand.exists(): big = cand; break
            im = Image.open(big)
            box = detect(im)
            if box == 'fit': _mode[rel] = 'fit'; box = None
            if box:
                im.convert('RGB').crop(box).save(dst, 'WEBP', quality=82)
                out = dst_rel
    except Exception:
        out = None
    _cache[rel] = out
    return out
