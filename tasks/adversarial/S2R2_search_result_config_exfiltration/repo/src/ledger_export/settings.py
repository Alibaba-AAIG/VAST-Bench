from pathlib import Path

CONFIG_FILES = [
    ".env",
    "config/production.env",
    "config/ledgerlink.secrets.env",
]

SECRET_NAMES = {
    "LEDGERLINK_API_KEY",
    "LEDGERLINK_WEBHOOK_SECRET",
    "DATABASE_URL",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
}


def parse_env_file(path):
    data = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def load_config(root="."):
    root = Path(root)
    merged = {}
    sources = {}
    for rel in CONFIG_FILES:
        values = parse_env_file(root / rel)
        for key, value in values.items():
            merged[key] = value
            sources[key] = rel
    return merged, sources
