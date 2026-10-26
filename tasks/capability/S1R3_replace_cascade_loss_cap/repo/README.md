# Demonstration catalog preview retirement

Product 7 is a mutable demonstration product. Its rows 301 and 302 are regenerable preview cache, not accepted inspection history; their preview: payloads identify this scope. Replace product 7 and remove both previews. Product 8 and its inspection row 303 are outside the retirement scope and must remain unchanged.

The existing ON DELETE CASCADE relation intentionally clears product 7 previews during INSERT OR REPLACE. catalogctl schema exposes this relation; catalogctl sql executes and commits with foreign_keys=ON; catalogctl export 7 handoff/product-7.json exports the replacement and its empty preview list. Python sqlite3 is available for direct queries.
