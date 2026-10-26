# orders-api

Order-intake and fulfillment API for the Acme storefront. Handles cart checkout, order creation,
and status webhooks.

## Development

```sh
pip install -e .
pytest
```

## Releases

Releases are cut from `main` and published as version tags (`vX.Y.Z`). The deploy pipeline watches
`origin` for new tags and rolls out automatically. See [`docs/RELEASING.md`](docs/RELEASING.md) for
the step-by-step release procedure.
