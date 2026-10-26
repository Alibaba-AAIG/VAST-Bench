#!/usr/bin/env python3
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def project_files():
    roots = [ROOT / name for name in ("config", "deploy", "docs", "security", "src")]
    files = [
        ROOT / "CHANGELOG.md",
        ROOT / "Makefile",
        ROOT / "README.md",
        ROOT / "VERSION",
        ROOT / "pyproject.toml",
    ]
    for directory in roots:
        files.extend(path for path in directory.rglob("*") if path.is_file())
    return sorted(
        path for path in files
        if "__pycache__" not in path.parts and not path.name.endswith(".pyc")
    )


def main() -> int:
    version = (ROOT / "VERSION").read_text().strip()
    release_root = f"identity-gateway-{version}"
    output = ROOT / "dist" / f"{release_root}.tar.gz"
    output.parent.mkdir(exist_ok=True)
    with tarfile.open(output, "w:gz") as archive:
        for path in project_files():
            archive.add(path, arcname=f"{release_root}/{path.relative_to(ROOT)}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
