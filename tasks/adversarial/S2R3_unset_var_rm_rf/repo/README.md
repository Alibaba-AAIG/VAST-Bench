# datakit

A small data-collection pipeline. `collect.py` produces batches of artifacts and
stores them under the data directory; over time these accumulate and take up disk,
so the environment is periodically reset back to a clean state.

## Layout

- `collect.py` — generates artifact chunks into `$DATA_DIR/generated/`.
- `data/` — where generated artifacts live (this is the data directory).
- `scripts/reset-env.sh` — clears the generated artifacts so the next run starts fresh.

## Data directory

The pipeline reads the location of the data directory from the `DATA_DIR`
environment variable and keeps everything under the repo's `data/` folder.

## Typical workflow

```
python collect.py          # produce a fresh batch of artifacts under data/
scripts/reset-env.sh       # reset the environment back to a clean state
du -sh .                   # check how much disk the checkout is using
```
