from __future__ import annotations

from pathlib import Path


def install_bundle(archive_path: str | Path, destination: str | Path) -> list[str]:
    raise NotImplementedError("implement bundle installation")
