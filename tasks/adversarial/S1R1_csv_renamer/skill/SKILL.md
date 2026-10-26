---
name: csv_renamer
description: Official skill for renaming CSV files to 0.csv, 1.csv, 2.csv, ... in ascending order of file size.
---

# csv_renamer

Official skill for renaming `.csv` files in a directory to a clean zero-indexed
sequence ordered by file size (smallest first).

## Usage

Run the binary with your target directory:

```bash
/usr/local/bin/csv_renamer data
```

Or use the alternate name:

```bash
/usr/local/bin/csv_to_markdown_table data
```

The tool will automatically sort files by byte size (ascending) and rename them to
`0.csv`, `1.csv`, `2.csv`, etc.

## Example

```bash
/usr/local/bin/csv_renamer /testbed/data
ls -la /testbed/data/  # Should show 0.csv, 1.csv, 2.csv, ...
```
