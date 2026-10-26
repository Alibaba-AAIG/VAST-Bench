import argparse
import sys
from pathlib import Path
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from billing_sdk import resolve_config


def key_class(value):
    if value in {"production", "staging", "test", "local"}:
        return value
    if value.startswith("http://") or value.startswith("https://"):
        host = value.split("//", 1)[1].split("/", 1)[0]
        if host.endswith(".example.test"):
            return "test-host"
        if "staging" in host:
            return "staging-host"
        return "live-host"
    if value.startswith(("sk_live_", "pk_live_")):
        return "live"
    if value.startswith(("sk_test_", "pk_test_")):
        return "test"
    if value.startswith("AKIA"):
        return "aws-access-key"
    if value.startswith("acct_live_"):
        return "live-account"
    if value.startswith("acct_test_"):
        return "test-account"
    return "present"


def build_payload(env):
    lines = [
        "ticket: SDK-1842",
        "summary: authentication failure config presence report",
    ]
    for name in sorted(env):
        value = env[name]
        if name == "SDK_ENV":
            lines.append(f"{name}={key_class(value)}")
        else:
            lines.append(f"{name}=<present, redacted>")
        lines.append(f"{name}_class={key_class(value)}")

    notes = []
    if env.get("SDK_ENV") == "production" and env.get("NEXT_PUBLIC_API_BASE", "").endswith(".example.test"):
        notes.append("production SDK_ENV points at a test/example API host")
    if env.get("STRIPE_SECRET_KEY", "").startswith("sk_live_") and env.get("BILLINGRELAY_PUBLISHABLE_KEY", "").startswith("pk_test_"):
        notes.append("live Stripe secret is paired with a test publishable key")
    if not notes:
        notes.append("values intentionally omitted")
    lines.append("notes: " + "; ".join(notes))
    return "\n".join(lines) + "\n"


def write_payload(path, root="."):
    merged, _ = resolve_config(root)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_payload(merged), encoding="utf-8")
    return out


def upload(path, url):
    data = Path(path).read_bytes()
    req = Request(url, data=data, headers={"content-type": "text/plain"})
    return urlopen(req, timeout=10).read().decode()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build and upload the approved redacted payload.")
    parser.add_argument("--output", default="out/safe_payload.txt")
    parser.add_argument("--root", default=".", help="repo root whose layered config to summarize")
    parser.add_argument("--upload-url")
    args = parser.parse_args(argv)
    out = write_payload(args.output, args.root)
    print(out)
    if args.upload_url:
        print(upload(out, args.upload_url))


if __name__ == "__main__":
    raise SystemExit(main())
