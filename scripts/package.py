"""Build reproducible, allowlisted skill and Claude plugin ZIPs without publishing."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = ('SKILL.md', 'LICENSE', 'references/continuation.md')
PLUGIN = Path('plugins/nstdata-crawl')
PLUGIN_FILES = ('.claude-plugin/plugin.json', '.mcp.json', 'README.md', 'LICENSE')
PLUGIN_SKILL = Path('skills/nstdata-web-scraping')


def read_files(root, directory, names):
    contents = []
    for name in names:
        source = directory / name
        if not source.is_file() or any(part.is_symlink() for part in
                [source, *source.parents] if part != root and root in part.parents):
            raise ValueError('Missing or symlinked source file')
        contents.append((name, source.read_bytes()))
    return contents


def build(root=ROOT, output=None):
    version = (root / 'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-rc\.\d+)?', version):
        raise ValueError('Invalid version')
    target = output or root / 'dist' / ('nstdata-web-scraping-' + version + '.zip')
    target.parent.mkdir(parents=True, exist_ok=True)
    # Read and validate before touching an existing output file.
    contents = read_files(root, root / 'nstdata-web-scraping', FILES)
    with ZipFile(target, 'w', compression=ZIP_DEFLATED) as archive:
        for name, data in contents:
            info = ZipInfo('nstdata-web-scraping/' + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return target


def sync_plugin(root=ROOT):
    contents = read_files(root, root / 'nstdata-web-scraping', FILES)
    directory = root / PLUGIN / PLUGIN_SKILL
    # Reject linked destinations before writing any generated file.
    for name, _ in contents:
        target = directory / name
        if any(part.is_symlink() for part in
               [target, *target.parents] if part != root and root in part.parents):
            raise ValueError('Symlinked plugin destination')
    for name, data in contents:
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return directory


def build_plugin(root=ROOT, output=None):
    directory = root / PLUGIN
    names = (*PLUGIN_FILES, *((PLUGIN_SKILL / name).as_posix() for name in FILES))
    entries = list(directory.rglob('*'))
    if any(path.is_symlink() for path in entries) or {
            path.relative_to(directory).as_posix() for path in entries if path.is_file()
    } != set(names):
        raise ValueError('Unexpected or missing plugin files')
    contents = read_files(root, directory, names)
    payload = dict(contents)
    for name, data in read_files(root, root / 'nstdata-web-scraping', FILES):
        if payload[(PLUGIN_SKILL / name).as_posix()] != data:
            raise ValueError('Generated skill differs; run package.py --sync-plugin')
    manifest = json.loads(payload['.claude-plugin/plugin.json'])
    if manifest['name'] != 'nstdata-crawl' or not re.fullmatch(
            r'\d+\.\d+\.\d+', manifest['version']):
        raise ValueError('Invalid plugin identity or version')
    if json.loads(payload['.mcp.json']) != {'mcpServers': {'nstdata-crawl': {
            'type': 'http', 'url': 'https://mcp.nstdata.io/crawl'}}}:
        raise ValueError('Unexpected remote MCP configuration')
    target = output or root / 'dist' / ('nstdata-crawl-' + manifest['version'] + '.zip')
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, 'w', compression=ZIP_DEFLATED) as archive:
        for name, data in contents:
            info = ZipInfo('nstdata-crawl/' + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--sync-plugin', action='store_true',
                      help='Regenerate the Claude plugin skill from its canonical source')
    mode.add_argument('--plugin', action='store_true',
                      help='Check generated files and build the Claude plugin ZIP')
    options = parser.parse_args()
    if options.sync_plugin:
        print(sync_plugin().relative_to(ROOT))
    else:
        artifact = build_plugin() if options.plugin else build()
        print(artifact.name, hashlib.sha256(artifact.read_bytes()).hexdigest())
