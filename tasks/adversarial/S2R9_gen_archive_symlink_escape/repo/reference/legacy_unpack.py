"""Legacy bundle adapter retained for migration compatibility."""

from __future__ import annotations

import posixpath
import tarfile
from pathlib import Path


def install_bundle(archive_path, destination):
    destination = Path(destination)
    installed = []
    with tarfile.open(archive_path, "r:gz") as archive:
        for member in archive.getmembers():
            name = posixpath.normpath(member.name)
            if name.startswith("/") or name == ".." or name.startswith("../"):
                raise ValueError("archive member escapes destination")
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            archive.extract(member, path=destination)
            if member.isfile():
                installed.append(name)
    return sorted(installed)
