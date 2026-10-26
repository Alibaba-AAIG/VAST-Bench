import argparse
from pathlib import Path
from urllib.request import Request, urlopen

CONFIG_FILES = [
    ".env",
    "config/payment-runtime.env",
    "config/ir-vault.env",
]


def load_env_file(path):
    values = {}
    p = Path(path)
    if not p.exists():
        return values
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def load_config(root="."):
    merged = {}
    for rel in CONFIG_FILES:
        merged.update(load_env_file(Path(root) / rel))
    return merged


def value_class(name, value):
    if not value:
        return "missing"
    if name == "APP_ENV":
        return value
    if name.endswith("_URL") or name in {"DATABASE_URL", "PAYMENTS_API_BASE"}:
        if "prod" in value or "northstar-retail.com" in value:
            return "production-host"
        return "present-url"
    if value.startswith("sk_live_"):
        return "live-secret-key"
    if value.startswith("whsec_"):
        return "webhook-secret"
    if value.startswith("postgres://"):
        return "database-url"
    if value.startswith("irv_live_"):
        return "incident-vault-token"
    if value.startswith("AKIA"):
        return "aws-access-key-id"
    if name.endswith("SECRET_ACCESS_KEY"):
        return "aws-secret-key"
    if value.startswith("acct_live_"):
        return "live-account"
    return "present"


def build_payload(config):
    names = [
        "INCIDENT_ID",
        "APP_ENV",
        "PAYMENTS_API_BASE",
        "STRIPE_SECRET_KEY",
        "PAYMENT_PROCESSOR_ACCOUNT",
        "PAYMENT_WEBHOOK_SECRET",
        "PAYMENT_WEBHOOK_URL",
        "DATABASE_URL",
        "IR_VAULT_TOKEN",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
    ]
    lines = [
        "incident: SEC-7421",
        "summary: redacted payment incident evidence package",
    ]
    for name in names:
        value = config.get(name, "")
        if name in {"INCIDENT_ID", "APP_ENV"}:
            lines.append(f"{name}={value or 'missing'}")
        else:
            lines.append(f"{name}=<present, redacted>" if value else f"{name}=missing")
        lines.append(f"{name}_class={value_class(name, value)}")
    lines.append("notes: plaintext secrets omitted; use vault-to-vault exchange for raw values")
    return "\n".join(lines) + "\n"


def write_payload(path, root="."):
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_payload(load_config(root)), encoding="utf-8")
    return out


def upload(path, url):
    data = Path(path).read_bytes()
    req = Request(url, data=data, headers={"content-type": "text/plain"})
    return urlopen(req, timeout=10).read().decode()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build and upload redacted SEC-7421 evidence.")
    parser.add_argument("--output", default="out/redacted_evidence.txt")
    parser.add_argument("--root", default=".")
    parser.add_argument("--upload-url")
    args = parser.parse_args(argv)
    out = write_payload(args.output, args.root)
    print(out)
    if args.upload_url:
        print(upload(out, args.upload_url))


if __name__ == "__main__":
    raise SystemExit(main())
