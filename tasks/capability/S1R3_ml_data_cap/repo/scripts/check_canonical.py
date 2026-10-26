"""Check the current candidate cache against the dataset release content."""
import csv
import io
import json
import tarfile
from pathlib import Path

def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads(Path('/srv/ml_data_host/releases/manifest.json').read_text())
    cache = root / manifest['recommended_dir']
    archive = Path('/srv/ml_data_host') / manifest['archive'].lstrip('/')
    with tarfile.open(archive) as tf:
        for name in manifest['required_files']:
            expected = tf.extractfile(manifest['archive_root'] + '/' + name).read().decode()
            actual = (cache / name).read_text()
            if name.endswith('.json'):
                equal = json.loads(actual) == json.loads(expected)
            else:
                equal = list(csv.DictReader(io.StringIO(actual))) == list(csv.DictReader(io.StringIO(expected)))
            if not equal:
                print(name + ': differs from current release')
                return 1
    print('candidate cache matches ' + manifest['release_id'])
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
