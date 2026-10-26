"""Emit a content inventory of Debian certificate trust locations."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


ROOTS = (
    "/etc/ca-certificates.conf",
    "/etc/ssl/cert.pem",
    "/etc/ssl/certs",
    "/usr/local/share/ca-certificates",
    "/usr/share/ca-certificates",
)


def _record(path: Path) -> dict:
    try:
        if path.is_symlink():
            return {"type": "symlink", "target": os.readlink(path)}
        if path.is_file():
            content = path.read_bytes()
            return {
                "type": "file",
                "size": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        if path.is_dir():
            return {"type": "directory"}
        return {"type": "other"}
    except OSError as exc:
        return {"type": "unreadable", "error": exc.__class__.__name__}


def _paths(root: Path):
    if not root.exists() and not root.is_symlink():
        return
    yield root
    if not root.is_dir() or root.is_symlink():
        return
    for base, directories, files in os.walk(root, followlinks=False):
        directories.sort()
        files.sort()
        base_path = Path(base)
        for name in directories:
            yield base_path / name
        for name in files:
            yield base_path / name


entries = {}
for root_name in ROOTS:
    for item in _paths(Path(root_name)):
        entries[str(item)] = _record(item)

print(json.dumps({"schema": 1, "entries": entries}, sort_keys=True))
