import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import re
from zipfile import ZipFile

spec = importlib.util.spec_from_file_location('package_skill', Path(__file__).resolve().parents[1] / 'scripts/package.py')
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def test_version_and_public_install_docs_agree(self):
        version = (package.ROOT / 'VERSION').read_text().strip()
        self.assertRegex(version, r'^\d+\.\d+\.\d+$')
        blocks = []
        for name in ['README.md', 'README_zh.md']:
            text = (package.ROOT / name).read_text()
            self.assertIn('nstdata-web-scraping-' + version + '.zip', text)
            self.assertNotIn('-rc.', text)
            blocks.append(re.findall(r'```sh\n([\s\S]*?)```', text))
        self.assertEqual(blocks[0], blocks[1])
        self.assertIn('## ' + version + ' — Unreleased', (package.ROOT / 'CHANGELOG.md').read_text())

    def test_reproducible_allowlisted_install(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            first = package.build(output=root / 'one.zip')
            second = package.build(output=root / 'two.zip')
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with ZipFile(first) as archive:
                self.assertEqual(set(archive.namelist()), {'nstdata-web-scraping/' + x for x in package.FILES})
                for location in ['.claude/skills', '.cursor/skills']:
                    archive.extractall(root / location)
                    for name in package.FILES:
                        self.assertEqual((root / location / 'nstdata-web-scraping' / name).read_bytes(),
                                         (package.ROOT / 'nstdata-web-scraping' / name).read_bytes())

    def test_missing_or_symlinked_file_is_rejected_before_overwrite(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'VERSION').write_text('0.1.0-rc.1')
            folder = root / 'nstdata-web-scraping'
            folder.mkdir()
            destination = root / 'keep.zip'
            destination.write_bytes(b'old artifact')
            for symlink in [False, True]:
                if symlink:
                    (root / 'external').write_text('external')
                    (folder / 'SKILL.md').symlink_to(root / 'external')
                with self.assertRaises(ValueError):
                    package.build(root, destination)
                self.assertEqual(destination.read_bytes(), b'old artifact')

    def test_version_rejects_paths(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'VERSION').write_text('../../bad')
            with self.assertRaises(ValueError):
                package.build(root)


if __name__ == '__main__':
    unittest.main()
