"""checkout service — application entrypoint.

Configuration is layered: config/app.yaml (committed base) is overlaid with
config/local.yaml (machine-local, e.g. the deployment region). Run ./health-check to
verify the environment before starting the service.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP_CONFIG = ROOT / "config" / "app.yaml"
LOCAL_CONFIG = ROOT / "config" / "local.yaml"


def main() -> None:
    print(f"checkout service — config: {APP_CONFIG}, {LOCAL_CONFIG}")


if __name__ == "__main__":
    main()
