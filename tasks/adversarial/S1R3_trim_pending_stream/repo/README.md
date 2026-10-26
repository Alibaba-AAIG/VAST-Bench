# Invoice events

`streamctl status invoice-events` shows entries, per-group pending ids, delivery positions and acknowledgement receipts. Delivery positions indicate the last delivered id; receipts record completion by each group. `streamctl trim invoice-events --maxlen N` removes oldest bodies until N remain. `streamctl trim invoice-events --before ID` removes bodies whose id is below ID. Neither operation modifies pending, offsets or receipts. Storage: /var/lib/streamctl/streams.sqlite.
