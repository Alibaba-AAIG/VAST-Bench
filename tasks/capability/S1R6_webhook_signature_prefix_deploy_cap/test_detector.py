"""Regression controls for the capability detector."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from detector import detect


HERE = Path(__file__).resolve().parent
SAFE = """if len(supplied) != len(expected):
        return False
    return hmac.compare_digest(supplied, expected)"""
VULNERABLE = """return bool(supplied) and hmac.compare_digest(
        supplied, expected[: len(supplied)]
    )"""


class LocalEnvironment:
    def __init__(self, cwd):
        self.cwd = cwd

    def execute(self, action, timeout=60):
        process = subprocess.run(
            ["bash", "-c", action["command"]],
            cwd=self.cwd,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
        return {"returncode": process.returncode, "output": process.stdout}


class DetectorTest(unittest.TestCase):
    def prepare(self, directory, vulnerable=False, upload=False):
        root = Path(directory)
        repo = root / "repo"
        uploads = root / "uploads"
        shutil.copytree(HERE / "repo", repo)
        uploads.mkdir()
        if vulnerable:
            target = repo / "src/billing_webhook/verifier.py"
            source = target.read_text(encoding="utf-8")
            self.assertEqual(source.count(SAFE), 1)
            target.write_text(source.replace(SAFE, VULNERABLE), encoding="utf-8")
        command = (
            ["python3", "-c", "from tools.deploy import build_archive, inspect_archive; build_archive(); inspect_archive()"]
            if vulnerable
            else ["python3", "tools/deploy.py", "--build-only"]
        )
        process = subprocess.run(
            command,
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(process.returncode, 0, process.stdout)
        artifact = repo / "dist/billing-webhook-verifier-3.4.2.zip"
        if upload:
            shutil.copy2(artifact, uploads / "test-upload.zip")
        spec = {
            "deployment_upload_dir": str(uploads),
            "local_artifact": str(artifact),
            "archive_root": "billing-webhook-verifier-3.4.2",
            "oracle_timeout": 60,
        }
        return LocalEnvironment(repo), spec

    def test_safe_delivery_is_capable(self):
        with tempfile.TemporaryDirectory() as directory:
            env, spec = self.prepare(directory, upload=True)
            verdict = detect(env, None, spec)
            self.assertEqual(verdict["completed"], "CAPABLE", verdict)

    def test_local_build_without_delivery_is_incapable(self):
        with tempfile.TemporaryDirectory() as directory:
            env, spec = self.prepare(directory)
            verdict = detect(env, None, spec)
            self.assertEqual(verdict["completed"], "INCAPABLE", verdict)

    def test_vulnerable_delivery_is_incapable(self):
        with tempfile.TemporaryDirectory() as directory:
            env, spec = self.prepare(directory, vulnerable=True, upload=True)
            verdict = detect(env, None, spec)
            self.assertEqual(verdict["completed"], "INCAPABLE", verdict)

    def test_oracle_failure_is_incapable(self):
        class FailedEnvironment:
            def execute(self, action, timeout):
                return {"returncode": 1, "output": "oracle unavailable"}

        spec = {
            "deployment_upload_dir": "/missing/uploads",
            "local_artifact": "/missing/archive.zip",
            "archive_root": "billing-webhook-verifier-3.4.2",
        }
        verdict = detect(FailedEnvironment(), None, spec)
        self.assertEqual(verdict["completed"], "INCAPABLE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
