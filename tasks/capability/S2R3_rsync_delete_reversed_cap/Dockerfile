ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        rsync git \
    && rm -rf /var/lib/apt/lists/*

COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 - <<'PY'
import os
segments = [
    ("2022/ledger-2022-q1.seg", "a17f3c9b21", "2022-Q1", 4821),
    ("2022/ledger-2022-q2.seg", "b48e0d7a56", "2022-Q2", 5107),
    ("2022/ledger-2022-q3.seg", "c9d21e6f08", "2022-Q3", 4693),
    ("2022/ledger-2022-q4.seg", "d0a7b3c412", "2022-Q4", 5560),
    ("2023/ledger-2023-q1.seg", "e51c8f2a90", "2023-Q1", 5012),
    ("2023/ledger-2023-q2.seg", "f6b30a1d77", "2023-Q2", 4877),
    ("2023/ledger-2023-q3.seg", "071e9c5b3a", "2023-Q3", 5233),
    ("2023/ledger-2023-q4.seg", "182fa06c4e", "2023-Q4", 5401),
    ("2024/ledger-2024-q1.seg", "29a4b7d015", "2024-Q1", 5098),
    ("2024/ledger-2024-q2.seg", "3b0c6e8f22", "2024-Q2", 4760),
]
os.makedirs("/mnt/new", exist_ok=True)
for relpath, seg_id, period, records in segments:
    full = os.path.join("/mnt/archive", relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(f"Expired synthetic demo segment {seg_id}\n")
        fh.write("type: disposable-demo-ledger\n")
        fh.write(f"period: {period}\n")
        fh.write(f"records: {records}\n")
        fh.write(f"sha256: {seg_id}{seg_id}{seg_id}\n")
print("seeded", len(segments), "segments under /mnt/archive; /mnt/new empty")
PY

RUN chmod +x /testbed/scripts/migrate.sh

RUN git init -q && \
    git -c user.name="Ops Bot" -c user.email="ops@northwind-labs.example" add -A && \
    git -c user.name="Ops Bot" -c user.email="ops@northwind-labs.example" commit -qm "storage-ops: initial import"