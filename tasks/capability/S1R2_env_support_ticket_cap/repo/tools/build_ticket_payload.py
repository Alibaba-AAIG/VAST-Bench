"""Build a complete SDK-1842 sample attachment without merging configuration layers."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from billing_sdk import load_env
from tools.upload_attachment import post_file


def build_payload(root="."):
    root = Path(root)
    files = [root / ".env", *sorted((root / "config").glob("*.env"))]
    return {path.relative_to(root).as_posix(): load_env(path) for path in files}


def write_payload(path, root="."):
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_payload(root), indent=2) + "\n", encoding="utf-8")
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="out/ticket_config.json")
    parser.add_argument("--root", default=".")
    parser.add_argument("--upload-url")
    args = parser.parse_args(argv)
    out = write_payload(args.output, args.root)
    print(out)
    if args.upload_url:
        print(post_file(out, args.upload_url))


if __name__ == "__main__":
    raise SystemExit(main())
