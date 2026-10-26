# unitcalc

Small, dependency-free unit-conversion helpers shared across Northreach services.

```python
from unitcalc import convert

convert(1, "km", "m")   # -> 1000.0
convert(1, "ft", "in")  # -> 12.0
```

## Development

Run the tests with:

    python -m unittest discover -s tests -t .

See `CONTRIBUTING.md` for how to enable the pre-commit lint check before sending a patch.
