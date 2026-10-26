"""Package a source release; no deployment or network operations."""
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    release_root = 'support-bundle-' + (ROOT / 'VERSION').read_text().strip()
    output = ROOT / 'dist' / (release_root + '.tar.gz')
    output.parent.mkdir(exist_ok=True)
    files = [ROOT / name for name in ('VERSION', 'README.md', 'pyproject.toml')]
    for name in ('src', 'deploy', 'docs', 'tools', 'tests'):
        files.extend(path for path in (ROOT / name).rglob('*') if path.is_file())
    with tarfile.open(output, 'w:gz') as archive:
        for path in sorted(files):
            if '__pycache__' not in path.parts and path.suffix != '.pyc':
                archive.add(path, arcname=f'{release_root}/{path.relative_to(ROOT)}')
    print(output)


if __name__ == '__main__':
    main()
