# Backup operations background

- Inventory the nightly encrypted snapshots before a restore window.
- Compare snapshot digests with the recorded inventory to detect corruption.
- Inspect the local mirror inventory to confirm expected files are available.
- Record the verification results and escalate missing snapshots to the backup owner.
- The public format example has no decryption capability; recovery keys are outside this documentation project.
