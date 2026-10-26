#!/usr/bin/env python3
"""Test, build, inspect, and optionally upload the configured deployment."""

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "deploy.json").read_text())
PACKAGE = CONFIG["package"]
VERSION = CONFIG["version"]
ARCHIVE_ROOT = f"{PACKAGE}-{VERSION}"
ARTIFACT = ROOT / "dist" / f"{ARCHIVE_ROOT}.zip"


def run_tests():
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        check=True,
    )


def package_files():
    return [
        ROOT / "pyproject.toml",
        ROOT / "README.md",
        ROOT / "CHANGELOG.md",
        *sorted((ROOT / "src").rglob("*.py")),
    ]


def build_archive():
    ARTIFACT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(ARTIFACT, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in package_files():
            name = f"{ARCHIVE_ROOT}/{path.relative_to(ROOT).as_posix()}"
            member = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            member.compress_type = zipfile.ZIP_DEFLATED
            member.external_attr = 0o100644 << 16
            archive.writestr(member, path.read_bytes())
    return hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()


def inspect_archive():
    required = {
        f"{ARCHIVE_ROOT}/pyproject.toml",
        f"{ARCHIVE_ROOT}/src/billing_webhook/__init__.py",
        f"{ARCHIVE_ROOT}/src/billing_webhook/verifier.py",
    }
    with zipfile.ZipFile(ARTIFACT) as archive:
        members = set(archive.namelist())
    missing = sorted(required - members)
    if missing:
        raise RuntimeError(f"archive is missing required members: {missing}")


def publish():
    request = urllib.request.Request(
        CONFIG["deployment_endpoint"],
        data=ARTIFACT.read_bytes(),
        method="POST",
        headers={
            "Content-Type": "application/zip",
            "X-Package-Name": PACKAGE,
            "X-Package-Version": VERSION,
        },
    )
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=15) as response:
        body = response.read().decode()
        if response.status != 201:
            raise RuntimeError(f"deployment intake returned HTTP {response.status}: {body}")
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
        print(f"deployment={publish()}")


if __name__ == "__main__":
    main()
