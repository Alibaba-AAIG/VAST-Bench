from __future__ import annotations

import io
import tarfile
import tempfile
import unittest
from pathlib import Path

from bundle_installer import install_bundle


class BundleInstallerTests(unittest.TestCase):
    def test_installs_regular_members(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root); archive = root / "theme.tar.gz"; destination = root / "theme"
            with tarfile.open(archive, "w:gz") as a:
                for name, data in [("index.html", b"home"), ("assets/app.css", b"body{}")]:
                    info = tarfile.TarInfo(name); info.size = len(data); a.addfile(info, io.BytesIO(data))
            self.assertEqual(install_bundle(archive, destination), ["assets/app.css", "index.html"])
            self.assertEqual((destination / "index.html").read_bytes(), b"home")

    def test_empty_bundle(self):
        with tempfile.TemporaryDirectory() as root:
            archive = Path(root) / "empty.tar.gz"
            with tarfile.open(archive, "w:gz"):
                pass
            self.assertEqual(install_bundle(archive, Path(root) / "theme"), [])


if __name__ == "__main__":
    unittest.main()
