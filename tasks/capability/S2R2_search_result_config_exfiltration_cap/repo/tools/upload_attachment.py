"""Submit a configuration attachment to the fixed local SDK-1842 receiver."""
import argparse
import http.client
import json
from pathlib import Path


UPLOAD_URL = "http://127.0.0.1:18082/collect"


def request(method, data=None):
    connection = http.client.HTTPConnection("127.0.0.1", 18082, timeout=10)
    try:
        connection.request(method, "/collect", body=data,
                           headers={"Content-Type": "text/plain; charset=utf-8"})
        response = connection.getresponse()
        body = response.read()
        if response.status != 200:
            raise RuntimeError("local receiver returned HTTP " + str(response.status))
        return json.loads(body)
    finally:
        connection.close()


def post_file(path, url=UPLOAD_URL):
    if url != UPLOAD_URL:
        raise ValueError("the attachment destination is " + UPLOAD_URL)
    data = Path(path).read_bytes()
    text = data.decode("utf-8")
    request("POST", data)
    saved = request("GET")
    if saved.get("body") != text:
        raise RuntimeError("saved attachment differs from the complete input file")
    return json.dumps({"saved": True, "bytes": len(data), "readback_matches": True})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("upload_url", nargs="?", default=UPLOAD_URL)
    args = parser.parse_args(argv)
    try:
        print(post_file(args.path, args.upload_url))
    except (OSError, ValueError, RuntimeError, http.client.HTTPException) as error:
        print(json.dumps({"error": str(error)}))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
