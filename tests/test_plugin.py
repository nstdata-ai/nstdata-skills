"""Check the publishable Claude folder and its single editable skill source."""
import importlib.util
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

spec = importlib.util.spec_from_file_location(
    'package_plugin', Path(__file__).resolve().parents[1] / 'scripts/package.py')
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PluginTests(unittest.TestCase):
    def fixture(self, directory):
        root = Path(directory)
        shutil.copytree(package.ROOT / 'nstdata-web-scraping', root / 'nstdata-web-scraping')
        shutil.copytree(package.ROOT / 'plugins', root / 'plugins')
        return root

    def test_complete_reproducible_plugin_and_remote_only_connection(self):
        expected = {'.claude-plugin/plugin.json', '.mcp.json', 'README.md', 'LICENSE',
                    'skills/nstdata-web-scraping/SKILL.md',
                    'skills/nstdata-web-scraping/LICENSE',
                    'skills/nstdata-web-scraping/references/continuation.md'}
        with TemporaryDirectory() as temp:
            first = package.build_plugin(output=Path(temp) / 'first.zip')
            second = package.build_plugin(output=Path(temp) / 'second.zip')
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with ZipFile(first) as archive:
                self.assertEqual(set(archive.namelist()), {'nstdata-crawl/' + n for n in expected})
                self.assertIsNone(archive.testzip())
                for name in ('SKILL.md', 'LICENSE', 'references/continuation.md'):
                    self.assertEqual(archive.read('nstdata-crawl/skills/nstdata-web-scraping/' + name),
                                     (package.ROOT / 'nstdata-web-scraping' / name).read_bytes())
                self.assertEqual(json.loads(archive.read('nstdata-crawl/.mcp.json')),
                                 {'mcpServers': {'nstdata-crawl': {
                                     'type': 'http', 'url': 'https://mcp.nstdata.io/crawl'}}})

    def test_source_change_requires_regeneration_without_overwriting_artifact(self):
        with TemporaryDirectory() as temp:
            root = self.fixture(temp)
            source = root / 'nstdata-web-scraping/SKILL.md'
            source.write_bytes(source.read_bytes() + b'\nUpdated canonical instructions.\n')
            output = root / 'keep.zip'
            output.write_bytes(b'previous artifact')
            with self.assertRaisesRegex(ValueError, 'Generated skill differs'):
                package.build_plugin(root, output)
            self.assertEqual(output.read_bytes(), b'previous artifact')
            before = (root / 'plugins/nstdata-crawl/README.md').read_bytes()
            package.sync_plugin(root)
            with ZipFile(package.build_plugin(root, output)) as archive:
                self.assertEqual(archive.read('nstdata-crawl/skills/nstdata-web-scraping/SKILL.md'),
                                 source.read_bytes())
            self.assertEqual((root / 'plugins/nstdata-crawl/README.md').read_bytes(), before)

    def test_unexpected_file_or_symlink_is_rejected(self):
        with TemporaryDirectory() as temp:
            root = self.fixture(temp)
            extra = root / 'plugins/nstdata-crawl/unexpected.txt'
            extra.write_text('Not part of the plugin')
            with self.assertRaisesRegex(ValueError, 'Unexpected or missing'):
                package.build_plugin(root)
            extra.unlink()
            extra.symlink_to(root / 'nstdata-web-scraping/SKILL.md')
            with self.assertRaisesRegex(ValueError, 'Unexpected or missing'):
                package.build_plugin(root)

    def test_sync_rejects_linked_destination_before_writing(self):
        with TemporaryDirectory() as temp:
            root = self.fixture(temp)
            destination = root / 'plugins/nstdata-crawl/skills/nstdata-web-scraping'
            shutil.rmtree(destination)
            outside = root / 'outside'
            outside.mkdir()
            destination.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'Symlinked plugin destination'):
                package.sync_plugin(root)
            self.assertEqual(list(outside.iterdir()), [])

    def test_other_endpoint_or_static_credentials_cannot_enter_archive(self):
        with TemporaryDirectory() as temp:
            root = self.fixture(temp)
            config = root / 'plugins/nstdata-crawl/.mcp.json'
            config.write_text(json.dumps({'mcpServers': {'nstdata-crawl': {
                'type': 'http', 'url': 'https://mcp.nstdata.io/crawl',
                'headers': {'Authorization': 'Bearer synthetic-do-not-publish'}}}}))
            output = root / 'keep.zip'
            output.write_bytes(b'previous artifact')
            with self.assertRaisesRegex(ValueError, 'Unexpected remote MCP configuration'):
                package.build_plugin(root, output)
            self.assertEqual(output.read_bytes(), b'previous artifact')


if __name__ == '__main__':
    unittest.main()
