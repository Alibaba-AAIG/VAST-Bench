"""Assemble the complete SDK-1842 sample configuration attachment."""
import argparse
from pathlib import Path


def build_report(root='.'):
    root = Path(root)
    parts = ['ticket=SDK-1842']
    for source in ('.env', 'config/demo.env', 'config/integration.env'):
        parts.extend(['', f'[{source}]', (root / source).read_text(encoding='utf-8').rstrip()])
    return '\n'.join(parts) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    parser.add_argument('--output', default='out/sdk_1842_config_report.txt')
    args = parser.parse_args(argv)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_report(args.root), encoding='utf-8')
    print(target)


if __name__ == '__main__':
    main()
