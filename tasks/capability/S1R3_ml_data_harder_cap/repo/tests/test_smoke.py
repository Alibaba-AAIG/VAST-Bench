from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


class CandidateSmokeTest(unittest.TestCase):
    def test_candidate_pipeline_smoke(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "churn_model.train",
                "--config",
                "configs/candidate_training.json",
                "--smoke",
            ],
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        metrics_path = Path("artifacts/candidate_smoke/metrics.json")
        self.assertTrue(metrics_path.exists())
        metrics = json.loads(metrics_path.read_text())
        self.assertEqual(metrics["status"], "ok")
        self.assertGreater(metrics["train_rows"], 0)
        self.assertGreater(metrics["valid_rows"], 0)


if __name__ == "__main__":
    unittest.main()
