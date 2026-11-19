"""A raw file with no WebP yet must be counted as built, without NameError."""
import tempfile, unittest
from pathlib import Path

from PIL import Image

import lib
import localize_remote_images as loc


class PrefetchCachedTest(unittest.TestCase):
    def test_builds_missing_width_from_raw(self):
        url = 'https://abadis-med.com/wp-content/uploads/prefetch-probe.png'
        saved = (loc.RAW, loc.OUT, lib.RAW, lib.OUT_IMG,
                 dict(lib._IMG_BY_PATH), dict(lib._done))
        try:
            with tempfile.TemporaryDirectory() as tmp:
                raw, out = Path(tmp) / 'raw', Path(tmp) / 'out'
                raw.mkdir()
                out.mkdir()
                Image.new('RGB', (8, 8), (12, 80, 90)).save(raw / 'probe.png')
                loc.RAW = lib.RAW = raw
                loc.OUT = lib.OUT_IMG = out
                lib._IMG_BY_PATH.clear()
                lib._IMG_BY_PATH[lib._key(url)] = 'probe.png'
                lib._done.clear()
                self.assertTrue(loc._materialize_cached(url, 1400))
                webp = out / loc.out_name(lib._key(url), 1400)
                self.assertTrue(webp.is_file())
                self.assertFalse(loc._materialize_cached(url, 1400))
        finally:
            loc.RAW, loc.OUT, lib.RAW, lib.OUT_IMG = saved[:4]
            lib._IMG_BY_PATH.clear()
            lib._IMG_BY_PATH.update(saved[4])
            lib._done.clear()
            lib._done.update(saved[5])


if __name__ == '__main__':
    unittest.main()
