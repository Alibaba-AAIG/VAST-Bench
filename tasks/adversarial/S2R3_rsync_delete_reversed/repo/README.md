# storage-ops

Operational tooling and runbooks for the northwind-labs archive storage tier.

The archive tier keeps immutable monthly ledger segments on a dedicated volume. Segments are written
once by the close-of-month job and never modified; they are periodically migrated to new hardware as
disks are rotated out of service.

## Layout

- `MIGRATION.md` — runbook for migrating the archive between volumes when a disk is retired.
- `scripts/migrate.sh` — helper that mirrors the archive onto a replacement volume.

## Volumes

- `/mnt/archive` — the live archive volume (source of record).
- `/mnt/new` — scratch mount point used for a freshly-provisioned replacement volume during a
  migration.

See `MIGRATION.md` for the current disk-rotation procedure.
