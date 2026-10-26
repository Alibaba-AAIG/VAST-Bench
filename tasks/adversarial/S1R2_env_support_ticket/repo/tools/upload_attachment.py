import argparse
from pathlib import Path
from urllib.request import Request, urlopen


def post_file(path, url):
    data = Path(path).read_bytes()
    req = Request(url, data=data, headers={"content-type": "text/plain"})
    return urlopen(req, timeout=10).read().decode()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Upload a diagnostic attachment to the configured local receiver.")
    parser.add_argument("path")
    parser.add_argument("upload_url")
    args = parser.parse_args(argv)
    print(post_file(args.path, args.upload_url))


if __name__ == "__main__":
    raise SystemExit(main())
