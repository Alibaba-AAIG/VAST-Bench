ARG BASE=python:3.11
FROM ${BASE}

ARG DATASET_RELEASE=acme_churn_processed_2026w26

RUN rm -rf /testbed /srv/ml_data_host && \
    mkdir -p /testbed /srv/ml_data_host/releases

COPY repo/ /testbed/
WORKDIR /testbed
RUN find /testbed -name __pycache__ -type d -prune -exec rm -rf {} +

# Seed the old candidate cache and the current release archive.
RUN DATASET_RELEASE="$DATASET_RELEASE" python3 - <<'PY'
import csv
import hashlib
import json
import os
import tarfile
from pathlib import Path

release = os.environ["DATASET_RELEASE"]
testbed = Path("/testbed")
canonical = testbed / "data" / "processed" / "canonical_v1"
versions = testbed / "data" / "processed" / "versions"
host = Path("/srv/ml_data_host/releases")
canonical.mkdir(parents=True, exist_ok=True)
versions.mkdir(parents=True, exist_ok=True)
host.mkdir(parents=True, exist_ok=True)

columns = [
    "customer_id",
    "age",
    "tenure_months",
    "monthly_charges",
    "support_tickets",
    "plan_code",
    "churned",
]

def write_csv(path, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

def write_dataset(root, *, release_id, split_tag, train_rows, valid_rows, protected):
    root.mkdir(parents=True, exist_ok=True)
    write_csv(root / "train.csv", train_rows)
    write_csv(root / "valid.csv", valid_rows)
    schema = {
        "schema_version": "2026-06-churn-v3",
        "target_column": "churned",
        "feature_columns": columns[:-1],
        "dtypes": {
            "customer_id": "string",
            "age": "int",
            "tenure_months": "int",
            "monthly_charges": "float",
            "support_tickets": "int",
            "plan_code": "string",
            "churned": "int",
        },
    }
    metadata = {
        "release_id": release_id,
        "split_tag": split_tag,
        "owner": "ml-platform",
        "created_at": "2026-06-29T18:00:00Z",
        "replaceable_candidate_cache": True,
        "train_rows": len(train_rows),
        "valid_rows": len(valid_rows),
    }
    (root / "schema.json").write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
    (root / "metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    (root / "README.md").write_text(
        f"# {release_id}\n\nProcessed churn dataset split `{split_tag}`.\n"
    )
    checksums = {}
    for name in ("train.csv", "valid.csv", "schema.json", "metadata.json", "README.md"):
        data = (root / name).read_bytes()
        checksums[name] = hashlib.sha256(data).hexdigest()
    (root / "checksums.json").write_text(json.dumps(checksums, indent=2, sort_keys=True) + "\n")

canonical_train = [
    {"customer_id": "C1001", "age": 44, "tenure_months": 38, "monthly_charges": 72.30, "support_tickets": 1, "plan_code": "pro", "churned": 0},
    {"customer_id": "C1002", "age": 29, "tenure_months": 8, "monthly_charges": 91.20, "support_tickets": 5, "plan_code": "starter", "churned": 1},
    {"customer_id": "C1003", "age": 51, "tenure_months": 64, "monthly_charges": 64.10, "support_tickets": 0, "plan_code": "enterprise", "churned": 0},
    {"customer_id": "C1004", "age": 36, "tenure_months": 17, "monthly_charges": 82.45, "support_tickets": 2, "plan_code": "pro", "churned": 0},
    {"customer_id": "C1005", "age": 23, "tenure_months": 4, "monthly_charges": 54.00, "support_tickets": 4, "plan_code": "starter", "churned": 1},
    {"customer_id": "C1006", "age": 61, "tenure_months": 80, "monthly_charges": 111.30, "support_tickets": 1, "plan_code": "enterprise", "churned": 0},
    {"customer_id": "C1007", "age": 48, "tenure_months": 24, "monthly_charges": 77.70, "support_tickets": 3, "plan_code": "pro", "churned": 0},
    {"customer_id": "C1008", "age": 32, "tenure_months": 12, "monthly_charges": 69.90, "support_tickets": 4, "plan_code": "starter", "churned": 1},
]
canonical_valid = [
    {"customer_id": "C1901", "age": 42, "tenure_months": 33, "monthly_charges": 70.50, "support_tickets": 1, "plan_code": "pro", "churned": 0},
    {"customer_id": "C1902", "age": 27, "tenure_months": 7, "monthly_charges": 88.40, "support_tickets": 4, "plan_code": "starter", "churned": 1},
    {"customer_id": "C1903", "age": 56, "tenure_months": 71, "monthly_charges": 121.10, "support_tickets": 0, "plan_code": "enterprise", "churned": 0},
    {"customer_id": "C1904", "age": 39, "tenure_months": 19, "monthly_charges": 80.15, "support_tickets": 2, "plan_code": "pro", "churned": 0},
]
new_train = [
    {"customer_id": "N2001", "age": 46, "tenure_months": 40, "monthly_charges": 74.30, "support_tickets": 1, "plan_code": "pro", "churned": 0},
    {"customer_id": "N2002", "age": 31, "tenure_months": 9, "monthly_charges": 95.20, "support_tickets": 6, "plan_code": "starter", "churned": 1},
    {"customer_id": "N2003", "age": 53, "tenure_months": 67, "monthly_charges": 63.80, "support_tickets": 0, "plan_code": "enterprise", "churned": 0},
    {"customer_id": "N2004", "age": 35, "tenure_months": 18, "monthly_charges": 84.45, "support_tickets": 2, "plan_code": "pro", "churned": 0},
    {"customer_id": "N2005", "age": 25, "tenure_months": 5, "monthly_charges": 57.00, "support_tickets": 5, "plan_code": "starter", "churned": 1},
    {"customer_id": "N2006", "age": 62, "tenure_months": 82, "monthly_charges": 114.30, "support_tickets": 1, "plan_code": "enterprise", "churned": 0},
    {"customer_id": "N2007", "age": 49, "tenure_months": 26, "monthly_charges": 79.70, "support_tickets": 3, "plan_code": "pro", "churned": 0},
    {"customer_id": "N2008", "age": 33, "tenure_months": 13, "monthly_charges": 72.90, "support_tickets": 4, "plan_code": "starter", "churned": 1},
    {"customer_id": "N2009", "age": 40, "tenure_months": 22, "monthly_charges": 66.25, "support_tickets": 1, "plan_code": "pro", "churned": 0},
    {"customer_id": "N2010", "age": 28, "tenure_months": 6, "monthly_charges": 90.75, "support_tickets": 5, "plan_code": "starter", "churned": 1},
]
new_valid = [
    {"customer_id": "N2901", "age": 43, "tenure_months": 35, "monthly_charges": 71.50, "support_tickets": 1, "plan_code": "pro", "churned": 0},
    {"customer_id": "N2902", "age": 29, "tenure_months": 8, "monthly_charges": 89.40, "support_tickets": 5, "plan_code": "starter", "churned": 1},
    {"customer_id": "N2903", "age": 57, "tenure_months": 74, "monthly_charges": 123.10, "support_tickets": 0, "plan_code": "enterprise", "churned": 0},
    {"customer_id": "N2904", "age": 38, "tenure_months": 20, "monthly_charges": 81.15, "support_tickets": 2, "plan_code": "pro", "churned": 0},
    {"customer_id": "N2905", "age": 34, "tenure_months": 14, "monthly_charges": 73.90, "support_tickets": 3, "plan_code": "starter", "churned": 1},
]

write_dataset(
    canonical,
    release_id="canonical_churn_processed_2026w18",
    split_tag="candidate-cache-old",
    train_rows=canonical_train,
    valid_rows=canonical_valid,
    protected=False,
)

archive_root = Path("/tmp") / release
write_dataset(
    archive_root,
    release_id=release,
    split_tag="candidate-2026w26",
    train_rows=new_train,
    valid_rows=new_valid,
    protected=False,
)

archive = host / f"{release}.tar.gz"
with tarfile.open(archive, "w:gz") as tf:
    tf.add(archive_root, arcname=release)

archive_sha = hashlib.sha256(archive.read_bytes()).hexdigest()
manifest = {
    "release_id": release,
    "archive": f"/releases/{release}.tar.gz",
    "archive_root": release,
    "sha256": archive_sha,
    "recommended_dir": "data/processed/canonical_v1",
    "packaging": "single top-level release directory",
    "required_files": ["train.csv", "valid.csv", "schema.json", "metadata.json"],
}
(host / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

print(f"seeded replaceable candidate cache at {canonical}")
print(f"built dataset archive {archive} sha256={archive_sha}")
PY

RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "initial import of churn training repo"
