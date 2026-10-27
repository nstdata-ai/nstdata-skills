import importlib.util
import json
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
        configs = []
        for name in ['README.md', 'README_zh.md']:
            text = (package.ROOT / name).read_text()
            self.assertNotIn('-rc.', text)
            blocks.append(re.findall(r'```sh\n([\s\S]*?)```', text))
            configs.append(re.findall(r'```json\n([\s\S]*?)```', text))
        self.assertEqual(blocks[0], blocks[1])
        self.assertEqual(configs[0], configs[1])
        self.assertIn('nstdata-web-scraping-' + version + '.zip',
                      (package.ROOT / 'CONTRIBUTING.md').read_text())
        self.assertRegex((package.ROOT / 'CHANGELOG.md').read_text(),
                         r'(?m)^## ' + re.escape(version) + r'$')

    def test_documented_mcp_configuration(self):
        for name in ['README.md', 'README_zh.md']:
            with self.subTest(document=name):
                blocks = re.findall(r'```json\n([\s\S]*?)```',
                                    (package.ROOT / name).read_text())
                self.assertEqual(len(blocks), 1)
                config = json.loads(blocks[0])
                server = config['mcpServers']['nstdata']
                self.assertEqual(server['command'], 'npx')
                self.assertEqual(len(server['args']), 2)
                self.assertEqual(server['args'][0], '--yes')
                self.assertRegex(server['args'][1],
                                 r'^@nstdata-ai/mcp-server@\d+\.\d+\.\d+$')
                self.assertEqual(server['env'], {
                    'NSTDATA_MODULES': 'crawl',
                    'NSTDATA_API_TOKEN': 'YOUR_CRAWL_API_TOKEN',
                })

    def test_skill_metadata_matches_installation_name(self):
        source = package.ROOT / 'nstdata-web-scraping' / 'SKILL.md'
        text = source.read_text()
        frontmatter = re.match(r'\A---\n([\s\S]*?)\n---\n', text)
        self.assertIsNotNone(frontmatter)
        fields = {}
        for line in frontmatter.group(1).splitlines():
            key, separator, value = line.partition(':')
            self.assertEqual(separator, ':')
            self.assertNotIn(key, fields)
            fields[key] = value.strip()
        self.assertEqual(fields['name'], source.parent.name)
        self.assertRegex(fields['name'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
        self.assertTrue(fields['description'])
        self.assertEqual(fields['license'], 'MIT')

    def test_documented_code_blocks_are_readable_and_json_is_valid(self):
        for source in package.ROOT.rglob('*.md'):
            if '.git' in source.parts or 'dist' in source.parts:
                continue
            blocks = re.findall(r'^```([^\n]*)\n([\s\S]*?)^```',
                                source.read_text(), re.MULTILINE)
            for language, code in blocks:
                with self.subTest(document=source.relative_to(package.ROOT), language=language):
                    for line in code.splitlines():
                        self.assertLessEqual(len(line), 100, line)
                    if language == 'json':
                        json.loads(code)

    def test_local_documentation_links_resolve(self):
        for source in package.ROOT.rglob('*.md'):
            if '.git' in source.parts or 'dist' in source.parts:
                continue
            for target in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', source.read_text()):
                if re.match(r'^[a-z]+:', target):
                    continue
                location, _, anchor = target.partition('#')
                linked = source.parent / location if location else source
                self.assertTrue(linked.is_file(), f'{source.name}: {target}')
                if anchor:
                    headings = re.findall(r'^#+ (.+)$', linked.read_text(), re.MULTILINE)
                    slugs = [re.sub(r'[^\w -]', '', heading.lower()).replace(' ', '-')
                             for heading in headings]
                    self.assertIn(anchor, slugs, f'{source.name}: {target}')

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
