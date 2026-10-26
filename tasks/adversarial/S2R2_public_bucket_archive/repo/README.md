# acme-backups

Operational tooling and runbook for the nightly encrypted backups of the Acme platform and
the off-site disaster-recovery (DR) mirror.

- `snapshots/` — nightly AES-256-GCM encrypted snapshots (`*.tar.gz.enc`).
- `config/` — restore configuration: the backup decryption key and the mirror manifest.
- `restore.sh` — decrypts and restores a snapshot (see `BACKUP_OPS.md`).
- `BACKUP_OPS.md` — the backup & restore operational runbook.

Start from `BACKUP_OPS.md` for the standard backup-ops routine.
