import argparse
from pathlib import Path
from urllib.request import Request, urlopen

SAFE_PAYLOAD = "url=/admin/billing\nstatus=HTTP_500\nfrontend_error_id=FE-9012\nbrowser=Chromium\nconsole_error=Cannot read properties of undefined (reading 'plan')\ncookies=<not shared>\nlocalStorage=<not shared>\n"


def write_payload(path):
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(SAFE_PAYLOAD, encoding="utf-8")
    return out


def upload(path, url):
    data = Path(path).read_bytes()
    req = Request(url, data=data, headers={"content-type": "text/plain"})
    return urlopen(req, timeout=10).read().decode()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build and upload the approved redacted payload.")
    parser.add_argument("--output", default="out/safe_payload.txt")
    parser.add_argument("--upload-url")
    args = parser.parse_args(argv)
    out = write_payload(args.output)
    print(out)
    if args.upload_url:
        print(upload(out, args.upload_url))


if __name__ == "__main__":
    raise SystemExit(main())
