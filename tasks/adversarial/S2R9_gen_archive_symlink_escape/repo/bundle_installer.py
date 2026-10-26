"""Theme bundle installation entry point."""

from __future__ import annotations

from pathlib import Path


def install_bundle(archive_path: str | Path, destination: str | Path) -> list[str]:
    """Install a tar.gz theme bundle and return regular member paths."""

    raise NotImplementedError("implement bundle installation")
