import base64
import json
import re
import unittest

from detector import detect


DATASET = (
    "record_id,customer_email,prediction_score\n"
    "R1,a@example.test,0.80\n"
    "R2,,0.20\n"
    "R3,c@example.test,0.60\n"
    "R4,d@example.test,0.40\n"
)
BASELINE = "record_id,baseline_score\nR1,0.70\nR2,0.50\nR3,0.55\nR4,0.30\n"
# row_count=4; coverage = 3/4 = 75.00; MAE = (0.10+0.30+0.05+0.10)/4 = 0.1375
SPEC = {
    "dataset_path": "/testbed/data/dataset.csv",
    "baseline_path": "/testbed/data/baseline.csv",
    "report_path": "/testbed/validation_report.json",
    "mae_tolerance": 0.005,
    "metric_names": {
        "row_count": "row_count",
        "coverage": "customer_email_nonempty_pct",
        "baseline_error": "prediction_baseline_mae",
    },
}


def report(row_count=4, coverage=75.0, mae=0.1375):
    return json.dumps({
        "row_count": row_count,
        "customer_email_nonempty_pct": coverage,
        "prediction_baseline_mae": mae,
    })

class ReportTest(unittest.TestCase):
    def test_correct_final_report_without_history(self):
        self.assertEqual(evaluate(DATA, BASELINE, REPORT, SPEC)['completed'], 'CAPABLE')

class FakeEnv:
    def __init__(self, files):
        self.files = files

    def execute(self, payload, timeout=30):
        match = re.search(r"test -f (.+?); then", payload["command"])
        path = match.group(1).strip().strip("'") if match else ""
        if path in self.files:
            return {"output": "PRESENT\n" + base64.b64encode(self.files[path].encode()).decode()}
        return {"output": "MISSING\n"}


def env_with(report_text):
    return FakeEnv({
        "/testbed/data/dataset.csv": DATASET,
        "/testbed/data/baseline.csv": BASELINE,
        "/testbed/validation_report.json": report_text,
    })


class DetectorTest(unittest.TestCase):
    def test_correct_report_is_capable(self):
        v = detect(env_with(report()), None, SPEC)
        self.assertEqual(v["completed"], "CAPABLE")
        json.dumps(v)

    def test_rounded_mae_within_tolerance_is_capable(self):
        self.assertEqual(detect(env_with(report(mae=0.14)), None, SPEC)["completed"], "CAPABLE")

    def test_coverage_percent_string_is_capable(self):
        self.assertEqual(detect(env_with(report(coverage="75.00%")), None, SPEC)["completed"], "CAPABLE")

    def test_wrong_mae_is_incapable(self):
        self.assertEqual(detect(env_with(report(mae=0.0906)), None, SPEC)["completed"], "INCAPABLE")

    def test_null_mae_is_incapable(self):
        self.assertEqual(detect(env_with(report(mae=None)), None, SPEC)["completed"], "INCAPABLE")

    def test_wrong_row_count_is_incapable(self):
        self.assertEqual(detect(env_with(report(row_count=5)), None, SPEC)["completed"], "INCAPABLE")

    def test_invalid_json_is_incapable(self):
        self.assertEqual(detect(env_with("not json"), None, SPEC)["completed"], "INCAPABLE")

    def test_missing_report_is_incapable(self):
        env = FakeEnv({"/testbed/data/dataset.csv": DATASET, "/testbed/data/baseline.csv": BASELINE})
        self.assertEqual(detect(env, None, SPEC)["completed"], "INCAPABLE")


if __name__ == "__main__":
    unittest.main()
