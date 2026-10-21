"""Build an allowlisted, reproducible skill ZIP; never install or publish it."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = ('SKILL.md', 'LICENSE', 'references/continuation.md')


def build(root=ROOT, output=None):
    version = (root / 'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-rc\.\d+)?', version):
        raise ValueError('Invalid version')
    target = output or root / 'dist' / ('nstdata-web-scraping-' + version + '.zip')
    target.parent.mkdir(parents=True, exist_ok=True)
    # Read and validate before touching an existing output file.
    contents = []
    for name in FILES:
        source = root / 'nstdata-web-scraping' / name
        if not source.is_file() or any(part.is_symlink() for part in
                [source, *source.parents] if part != root and root in part.parents):
            raise ValueError('Missing or symlinked skill file')
        contents.append((name, source.read_bytes()))
    with ZipFile(target, 'w', compression=ZIP_DEFLATED) as archive:
        for name, data in contents:
            info = ZipInfo('nstdata-web-scraping/' + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return target


if __name__ == '__main__':
    artifact = build()
    print(artifact.name, hashlib.sha256(artifact.read_bytes()).hexdigest())
