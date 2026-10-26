#!/usr/bin/env python3
"""Test, build, and optionally upload the configured source archive."""

import argparse
import hashlib
import json
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "release.json").read_text())
PACKAGE = CONFIG["package"]
VERSION = CONFIG["version"]
ARCHIVE_ROOT = f"{PACKAGE}-{VERSION}"
ARTIFACT = ROOT / "dist" / f"{ARCHIVE_ROOT}.tar.gz"


def run_tests():
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        check=True,
    )


def build_archive():
    ARTIFACT.parent.mkdir(exist_ok=True)
    files = [
        ROOT / "pyproject.toml",
        ROOT / "README.md",
        ROOT / "CHANGELOG.md",
        *sorted((ROOT / "src").rglob("*.py")),
    ]
    with tarfile.open(ARTIFACT, "w:gz") as archive:
        for path in files:
            archive.add(path, arcname=f"{ARCHIVE_ROOT}/{path.relative_to(ROOT)}")
    return hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()


def inspect_archive():
    required = {
        f"{ARCHIVE_ROOT}/pyproject.toml",
        f"{ARCHIVE_ROOT}/src/edge_policy_client/__init__.py",
        f"{ARCHIVE_ROOT}/src/edge_policy_client/errors.py",
        f"{ARCHIVE_ROOT}/src/edge_policy_client/continuity.py",
        f"{ARCHIVE_ROOT}/src/edge_policy_client/gate.py",
    }
    with tarfile.open(ARTIFACT, "r:gz") as archive:
        members = {member.name for member in archive.getmembers() if member.isfile()}
    missing = sorted(required - members)
    if missing:
        raise RuntimeError(f"archive is missing required members: {missing}")


def publish():
    request = urllib.request.Request(
        CONFIG["registry_endpoint"],
        data=ARTIFACT.read_bytes(),
        method="POST",
        headers={
            "Content-Type": "application/gzip",
            "X-Package-Name": PACKAGE,
            "X-Package-Version": VERSION,
        },
    )
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=15) as response:
        body = response.read().decode()
        if response.status != 201:
            raise RuntimeError(f"registry returned HTTP {response.status}: {body}")
        return body


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build-only", action="store_true")
    mode.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    run_tests()
    digest = build_archive()
    inspect_archive()
    print(f"artifact={ARTIFACT.relative_to(ROOT)}")
    print(f"package={PACKAGE}")
    print(f"version={VERSION}")
    print(f"sha256={digest}")
    if args.publish:
        print(f"registry={publish()}")


if __name__ == "__main__":
    main()
