"""Dead and failed image URLs are remembered and not requested again."""
import io, tempfile, unittest, urllib.error, urllib.request
from pathlib import Path

import localize_remote_images as loc


class DeadImageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'dead_images.json'
        self.old_path = loc.DEAD_PATH
        loc.DEAD_PATH = self.path
        loc.DEAD.clear()
        loc.FAILED.clear()
        self.calls = []

        def fake_urlopen(req, timeout=None):
            self.calls.append((req.full_url, timeout))
            raise urllib.error.HTTPError(req.full_url, 404, 'missing', {}, io.BytesIO(b''))

        self.old_open = urllib.request.urlopen
        urllib.request.urlopen = fake_urlopen

    def tearDown(self):
        urllib.request.urlopen = self.old_open
        loc.DEAD_PATH = self.old_path
        loc.load_remembered()
        self.tmp.cleanup()

    def test_404_and_wayback_miss_is_dead_after_two_attempts(self):
        url = 'https://abadis-med.com/wp-content/uploads/2017/08/gone.png'
        data, via = loc.fetch(url)
        self.assertIsNone(data)
        self.assertIsNone(via)
        self.assertEqual(len(self.calls), loc.ATTEMPTS)
        self.assertTrue(all(timeout == loc.TIMEOUT for _, timeout in self.calls))
        self.assertIn('web.archive.org', self.calls[1][0])
        self.assertNotIn('web.archive.org', self.calls[0][0])
        text = self.path.read_text(encoding='utf-8')
        self.assertIn(url, text)
        self.calls.clear()
        again, _ = loc.fetch(url)
        self.assertIsNone(again)
        self.assertEqual(self.calls, [])


if __name__ == '__main__':
    unittest.main()
