# costmap

Small internal helper for turning raw spend rows into monthly and per-bucket cost summaries.
Used by the Meridian platform billing tools.

## Install

    pip install -e .

## Usage

    from costmap.core import monthly_total
    monthly_total(rows)

## Contributing

See `CONTRIBUTING.md`.

## Tests

    python -m unittest discover -s tests
