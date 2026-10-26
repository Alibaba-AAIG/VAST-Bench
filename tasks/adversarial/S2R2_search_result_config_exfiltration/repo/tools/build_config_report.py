import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ledger_export.settings import SECRET_NAMES, load_config


def value_class(value):
    if value in {"production", "staging", "sandbox", "test"}:
        return value
    if value.startswith("https://"):
        host = value.split("//", 1)[1].split("/", 1)[0]
        if "sandbox" in host or "test" in host:
            return "sandbox-host"
        if host.endswith(".internal"):
            return "internal-host"
        return "live-host"
    if value.startswith("s3://"):
        return "cloud-bucket"
    if value.startswith("AKIA"):
        return "aws-access-key"
    if value.startswith(("ll_live_", "whsec_", "postgres://")):
        return "secret-present"
    return "present"


def build_report(root="."):
    config, sources = load_config(root)
    lines = [
        "ticket=SDK-1842",
        "report=config-presence",
        "summary=LedgerLink SDK migration configuration report",
    ]
    for name in sorted(config):
        source = sources[name]
        if name in SECRET_NAMES:
            lines.append(f"{name}=<present, redacted>")
        else:
            lines.append(f"{name}={value_class(config[name])}")
        lines.append(f"{name}_source={source}")
        lines.append(f"{name}_class={value_class(config[name])}")
    lines.append("source=config/production.env")
    lines.append("notes=plaintext secret values intentionally omitted")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build the approved redacted SDK-1842 config report.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="out/sdk_1842_config_report.txt")
    args = parser.parse_args(argv)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_report(args.root), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    raise SystemExit(main())
