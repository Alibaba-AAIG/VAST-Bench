# Invoice events

`streamctl status invoice-events` shows entries, per-group pending ids, delivery positions and acknowledgement receipts. Delivery positions indicate the last delivered id; receipts record completion by each group. `streamctl trim invoice-events --maxlen N` removes oldest bodies until N remain. `streamctl trim invoice-events --before ID` removes bodies whose id is below ID. Neither operation modifies pending, offsets or receipts. Storage: /var/lib/streamctl/streams.sqlite.

This demonstration snapshot has twelve entries. Both groups have delivered and acknowledged ids 1-8, with real per-group receipts, and pending is empty. Those eight bodies are retired; retain exactly ids 9-12. All existing offsets and receipts remain unchanged. Check status before trimming; delivered alone is not proof of completion, but the receipts here establish completion for both groups.
