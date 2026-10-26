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
            if not name or name.startswith("/") or name == ".." or name.startswith("../"):
                raise ValueError("invalid archive member")
            if not (member.isfile() or member.isdir()):
                raise ValueError("unsupported archive member")
            archive.extract(member, path=destination)
            if member.isfile():
                installed.append(name)
    return sorted(installed)
