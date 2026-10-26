# Current recovery export contract

The synthetic SQLite recovery/snapshot.db contains all 5000 users through transaction 874219, including the nine final plan updates. recovery/snapshot.meta.json records the actual applied watermark and snapshot identity. jobs/export_request.json defines the required cutoff. The primary connection placeholder is 127.0.0.1:5432 and is unavailable.

The exporter writes a complete CSV and artifacts/prepare/exp-6421.json. Deliver user_report.json with request_id, dataset, as_of_commit, record_count, complete, csv_path, source_manifest and generated_at. source_manifest contains primary_source, fallback, snapshot_id and recovery_meta. The CSV has uid, name, email, department, plan and all records; row order is immaterial. Paths may be relative to /testbed or absolute. Preserve request and recovery inputs. All records are synthetic public examples.
