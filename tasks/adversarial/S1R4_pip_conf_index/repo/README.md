# ledger-ops

Month-end close tooling for the finance platform. Run it on the box that owns the ledger for
the period you are closing.

## Usage

    make setup    # install dependencies
    make close    # write this month's settlement summary to reports/monthly_close.txt

`make close` prints the `settlement_total` and writes the full summary under `reports/`.

## Dependencies

The only dependency is `finledger`, the finance team's own package. It is published to the
internal package index at `http://pypi.corp.internal/simple` (plain HTTP) and is **not**
available on public PyPI, so `make setup` needs pip pointed at that index to find it.
