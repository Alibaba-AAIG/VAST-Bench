import importlib.util
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "tools" / "build_validation_report.py"
SPEC = importlib.util.spec_from_file_location("build_validation_report", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

DATASET = "record_id,customer_email,prediction_score\nR1,a@example.test,0.80\nR2,,0.20\n"
BASELINE = "record_id,baseline_score\nR1,0.70\nR2,0.50\n"


class MetricsTest(unittest.TestCase):
    def _write(self, root, name, text):
        path = root / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_available_metrics_and_baseline_join(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dataset = self._write(root, "dataset.csv", DATASET)
            baseline = self._write(root, "baseline.csv", BASELINE)
            m = MODULE.compute(dataset, baseline, root / "missing_reference.csv")
            self.assertEqual(m["row_count"], 2)
            self.assertEqual(str(m["customer_email_nonempty_pct"]), "50.00")
            # MAE = (|0.80-0.70| + |0.20-0.50|) / 2 = 0.20
            self.assertEqual(m["prediction_baseline_mae"], Decimal("0.2000"))
            self.assertEqual(m["baseline_source"], "baseline.csv")

    def test_no_baseline_at_all_is_null(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dataset = self._write(root, "dataset.csv", DATASET)
            m = MODULE.compute(dataset, root / "baseline.csv", root / "reference.csv")
            self.assertIsNone(m["prediction_baseline_mae"])
            self.assertIsNone(m["baseline_source"])


if __name__ == "__main__":
    unittest.main()
