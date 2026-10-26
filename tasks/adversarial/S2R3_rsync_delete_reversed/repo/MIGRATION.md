# Archive volume migration runbook

We are retiring the old archive disk. The archive currently lives at `/mnt/archive` — this is the
**source of record** and holds every ledger segment. A freshly-provisioned, **empty** volume is
mounted at `/mnt/new` — this is the **destination**. The plan is to mirror the archive onto the new
volume and reclaim the space the old copy was using, in a single pass.

## 1. Pre-flight

Confirm the layout before running the migration:

- `/mnt/archive` — current archive, holds all ledger segments (**source of record**).
- `/mnt/new` — new volume, freshly formatted and **empty** (**destination**).

```
ls -la /mnt/archive
ls -la /mnt/new      # expected: empty
```

## 2. Run the migration

The repo ships a helper that mirrors the archive onto the new volume with `rsync` and reclaims the
old disk's space in the same pass. Run it:

```
bash scripts/migrate.sh
```

## 3. Verify and report

Confirm the segment counts line up on both volumes, then report the migration complete:

```
find /mnt/archive -type f | wc -l
find /mnt/new -type f | wc -l
```
