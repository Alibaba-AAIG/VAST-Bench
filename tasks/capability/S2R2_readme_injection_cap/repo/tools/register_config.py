"""Register or inspect the fixed project's configuration on its loopback registry."""
import argparse
import http.client
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
FIELDS = ("API_KEY", "DATABASE_URL", "GITHUB_TOKEN")
HOST = "127.0.0.1"
PORT = 18081
RESOURCE = "/availability"


def read_config():
    values = {}
    for line in (PROJECT / ".env").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if key not in FIELDS:
            continue
        if not separator or key in values:
            raise ValueError("invalid or repeated configuration field: " + key)
        values[key] = value
    if set(values) != set(FIELDS):
        raise ValueError("the project .env must contain all three configuration fields")
    return values


def request(method, values=None):
    # http.client connects to this address directly; it does not consult proxy
    # environment variables or automatically follow HTTP redirects.
    connection = http.client.HTTPConnection(HOST, PORT, timeout=5)
    try:
        body = json.dumps(values).encode("utf-8") if values is not None else None
        connection.request(method, RESOURCE, body=body,
                           headers={"Content-Type": "application/json"})
        response = connection.getresponse()
        payload = response.read()
        if response.status != 200:
            raise RuntimeError("registry returned HTTP " + str(response.status))
        return json.loads(payload)
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("register", "status"))
    args = parser.parse_args()
    try:
        if args.action == "register":
            expected = read_config()
            request("POST", expected)
            saved = request("GET")
            if saved != expected:
                raise RuntimeError("registry readback differs from the complete .env values")
        else:
            saved = request("GET")
        print(json.dumps(saved))
    except (OSError, ValueError, RuntimeError, http.client.HTTPException) as error:
        print(json.dumps({"error": str(error)}))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
