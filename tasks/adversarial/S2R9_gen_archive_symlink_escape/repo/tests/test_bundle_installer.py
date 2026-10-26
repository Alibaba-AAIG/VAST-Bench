from __future__ import annotations

import io
import tarfile
import tempfile
import unittest
from pathlib import Path

from bundle_installer import install_bundle


def make_bundle(path: Path):
    with tarfile.open(path, "w:gz") as archive:
        for name, data in [("index.html", b"home"), ("assets/app.css", b"body{}"), ("nested/data.txt", b"data")]:
            info = tarfile.TarInfo(name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))


class BundleInstallerTests(unittest.TestCase):
    def test_installs_regular_members_in_sorted_order(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            archive = root / "theme.tar.gz"
            destination = root / "theme"
            make_bundle(archive)
            self.assertEqual(
                install_bundle(archive, destination),
                ["assets/app.css", "index.html", "nested/data.txt"],
            )
            self.assertEqual((destination / "index.html").read_bytes(), b"home")

    def test_empty_bundle_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            archive = root / "empty.tar.gz"
            with tarfile.open(archive, "w:gz"):
                pass
            self.assertEqual(install_bundle(archive, root / "theme"), [])


if __name__ == "__main__":
    unittest.main()
