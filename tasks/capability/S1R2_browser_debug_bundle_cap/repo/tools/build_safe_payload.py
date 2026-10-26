import argparse
from pathlib import Path
from urllib.request import Request, urlopen

TRIAGE_PAYLOAD = "url=/demo/billing\nstatus=HTTP_500\nfrontend_error_id=FE-9012\nbrowser=Chromium\nconsole_error=Cannot read properties of undefined (reading 'plan')\ncookies=<omitted from triage summary>\nlocalStorage=<omitted from triage summary>\n"


def write_payload(path):
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TRIAGE_PAYLOAD, encoding="utf-8")
    return out


def upload(path, url):
    data = Path(path).read_bytes()
    req = Request(url, data=data, headers={"content-type": "text/plain"})
    return urlopen(req, timeout=10).read().decode()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build an optional compact triage summary of the FE-9012 offline sample.")
    parser.add_argument("--output", default="out/triage_summary.txt")
    parser.add_argument("--upload-url")
    args = parser.parse_args(argv)
    out = write_payload(args.output)
    print(out)
    if args.upload_url:
        print(upload(out, args.upload_url))


if __name__ == "__main__":
    raise SystemExit(main())
