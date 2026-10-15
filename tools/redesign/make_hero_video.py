"""Grade the old operating-room hero video (site/assets/media/hero-mosaic.mp4, from the earlier teal
hero) into the Zagros painting's palette for the home first screen.

  1. soften (slight blur) and drop to luminance,
  2. gradient-map luminance onto bg-dry's own tones: umber shadows -> sand -> warm cream highlights,
     low contrast like the hazy painting,
  3. overlay the painting's brush texture (high-pass of bg-dry, static, so it does not cost bitrate).
Outputs site/assets/media/hero-or-zagros.mp4 + a graded poster (first frame).

    python3 tools/redesign/make_hero_video.py        (needs ffmpeg + Pillow)
"""
import os
import subprocess
from PIL import Image, ImageChops, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'site', 'assets', 'media', 'hero-mosaic.mp4')
ZAGROS = os.path.join(ROOT, 'site', 'csr', 'img', 'hero', 'bg-dry.jpg')
OUT = os.path.join(ROOT, 'site', 'assets', 'media')
TEX = '/tmp/zagros-tex.png'
W, H = 640, 1214

# gradient map (0..1 per channel) sampled from bg-dry: shadow umber, mid sand, highlight cream
CURVES = ("r='0/0.52 0.4/0.73 0.75/0.88 1/0.95':"
          "g='0/0.45 0.4/0.67 0.75/0.84 1/0.92':"
          "b='0/0.38 0.4/0.60 0.75/0.79 1/0.88'")


def texture():
    """Brush grain only (no shapes): high-pass of the painting's cloud band, mirror-tiled."""
    z = Image.open(ZAGROS).convert('L')
    band = z.crop((300, 0, 1620, 300))
    hp = ImageChops.subtract(band, band.filter(ImageFilter.GaussianBlur(5)), 1, 128)
    hp = hp.point(lambda v: max(0, min(255, int(128 + (v - 128) * 3.0))))
    tile = hp.resize((W, int(300 * W / 1320.0)), Image.LANCZOS)
    out = Image.new('L', (W, H), 128)
    y, flip = 0, False
    while y < H:
        out.paste(tile.transpose(Image.FLIP_TOP_BOTTOM) if flip else tile, (0, y))
        y += tile.height; flip = not flip
    out.convert('RGB').save(TEX)


def main():
    texture()
    vf = (f"[0:v]scale={W}:{H},gblur=sigma=1.4,hue=s=0,eq=contrast=0.78:brightness=0.02,curves={CURVES},format=gbrp[v];"
          f"[1:v]scale={W}:{H},format=gbrp[t];"
          f"[v][t]blend=all_mode=overlay:all_opacity=0.5:shortest=1,format=yuv420p[o]")
    mp4 = os.path.join(OUT, 'hero-or-zagros.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', SRC, '-loop', '1', '-t', '30', '-i', TEX,
                    '-filter_complex', vf, '-map', '[o]', '-an', '-shortest',
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '27', '-profile:v', 'high',
                    '-movflags', '+faststart', '-r', '24', mp4], check=True)
    poster = os.path.join(OUT, 'hero-or-zagros-poster.jpg')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-frames:v', '1', '-q:v', '4', poster], check=True)
    for f in (mp4, poster):
        print(os.path.basename(f), os.path.getsize(f))


if __name__ == '__main__':
    main()
