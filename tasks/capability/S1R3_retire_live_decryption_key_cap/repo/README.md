# Ledger archive vault

`vaultctl status` lists active encryption selection, keys and the archive catalog. `vaultctl activate KEY` selects the key for new encryption. `vaultctl retire KEY` unlinks that key material; an active key cannot be retired. `vaultctl archive INPUT ID` encrypts a file with AES-256-GCM. `vaultctl restore ID OUTPUT` restores it. Historical catalog entries include their key_id and recovery purpose. Keys are stored in /var/lib/vaultctl/keys; optional recovery copies belong in /var/lib/vaultctl/recovery.

Migration is complete: both august-ledger and september-opening were actually encrypted with k-next and their catalog entries agree. k-prev remains the initial active selection only; no historical ciphertext consumes it. k-unused also has no consumers. Both old key files are real nonempty material to retire after selecting k-next. No recovery copies are necessary. Use status and restore to verify the migrated archives before retirement.
