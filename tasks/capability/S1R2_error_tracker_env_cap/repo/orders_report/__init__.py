"""orders-report-api — nightly settlement reporting service."""
import os
from pathlib import Path


def load_env(path: str | None = None) -> None:
    """Populate os.environ from config/runtime.env (idempotent; does not override)."""
    env_path = Path(path) if path else Path(__file__).resolve().parent.parent / "config" / "runtime.env"
    if not env_path.is_file():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())
