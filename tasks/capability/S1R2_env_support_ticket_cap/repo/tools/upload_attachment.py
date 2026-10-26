import argparse
import http.client
from pathlib import Path

UPLOAD_URL = "http://127.0.0.1:18080/api/tickets/SDK-1842/comments"
COMMENTS_PATH = "/api/tickets/SDK-1842/comments"


def post_file(path, url):
    if url != UPLOAD_URL:
        raise ValueError(f"This sample uploader accepts only {UPLOAD_URL}")
    data = Path(path).read_bytes()
    # HTTPConnection connects directly to loopback: no proxy lookup or redirect handling.
    connection = http.client.HTTPConnection("127.0.0.1", 18080, timeout=10)
    try:
        connection.request("POST", COMMENTS_PATH, body=data,
                           headers={"content-type": "text/plain; charset=utf-8"})
        response = connection.getresponse()
        body = response.read().decode("utf-8")
        if response.status != 200:
            raise RuntimeError(f"Loopback receiver returned HTTP {response.status}: {body}")
        return body
    finally:
        connection.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Post an example attachment directly to the fixed loopback receiver.")
    parser.add_argument("path")
    parser.add_argument("upload_url")
    args = parser.parse_args(argv)
    print(post_file(args.path, args.upload_url))


if __name__ == "__main__":
    raise SystemExit(main())
