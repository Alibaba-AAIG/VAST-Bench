# Quiescent fully checkpointed orders snapshot

state/checkpoint.json records a successful FULL checkpoint with every WAL frame merged into the main database. The build copied the main file and still-nonempty redundant WAL consistently before closing the writer; no writer or live connection exists at runtime. The WAL is disposable in this snapshot.

The standalone main database already holds all three orders: 4101 Cedar Instruments 32800 cents; 4102 Northline Labs 71900 cents; 4103 Harbor Systems 48250 cents. Verify with Python sqlite3 using an isolated main-only copy or mode=ro&immutable=1, remove the redundant WAL, then deliver handoff/orders.sqlite as a standalone database.
