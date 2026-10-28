"""Build clean single-shot operating-room hero video (site/assets/media/hero-or-zagros.mp4)
from site/hero-options/3-numbers/media/or-loop.mp4 without shot cuts or tiled texture seams.
"""
import os
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'site', 'hero-options', '3-numbers', 'media', 'or-loop.mp4')
OUT = os.path.join(ROOT, 'site', 'assets', 'media')
W, H = 640, 1214


def main():
    vf = (f"trim=start_frame=12:end_frame=180,setpts=PTS-STARTPTS,"
          f"scale={W}:{H}:flags=lanczos,eq=contrast=1.02:brightness=-0.02:saturation=0.92,format=yuv420p")
    mp4 = os.path.join(OUT, 'hero-or-zagros.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', SRC,
                    '-vf', vf, '-an',
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '23', '-profile:v', 'high',
                    '-movflags', '+faststart', '-r', '24', mp4], check=True)
    poster = os.path.join(OUT, 'hero-or-zagros-poster.jpg')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-frames:v', '1', '-q:v', '3', poster], check=True)
    for f in (mp4, poster):
        print(os.path.basename(f), os.path.getsize(f))


if __name__ == '__main__':
    main()
