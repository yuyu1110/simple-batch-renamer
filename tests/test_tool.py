import tempfile
import unittest
from pathlib import Path

from renamer import rename

class RenamerTests(unittest.TestCase):
    def test_preview_and_combined_options(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'old.txt').write_text('keep')
            options = dict(prefix='work_', number=True, start=5, replace=('old', 'new'))
            rename(root, **options)
            self.assertTrue((root / 'old.txt').exists())
            rename(root, apply=True, **options)
            self.assertEqual((root / 'work_005_new.txt').read_text(), 'keep')
    def test_collision(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'a.txt').touch()
            (root / 'xa.txt').touch()
            with self.assertRaises(ValueError):
                rename(root, apply=True, prefix='x')
            self.assertTrue((root / 'a.txt').exists())
    def test_invalid_name(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / 'a.txt').touch()
            with self.assertRaises(ValueError):
                rename(folder, apply=True, prefix='../')
    def test_no_options_is_noop(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / 'a.txt').touch()
            self.assertEqual(rename(folder, apply=True), [])
