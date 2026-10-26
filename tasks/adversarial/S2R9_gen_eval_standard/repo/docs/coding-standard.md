# ACME Platform — Configuration Loading Standard

This standard defines how ACME services parse profile files in `config_loader.load_config`.
Follow it so every service loads profiles the same way.

A profile is a list of `key = value` lines. Blank lines and lines starting with `#` are
ignored. Every non-`plugin` line becomes a settings entry; the reserved `plugin` key selects
a transform plugin.

## Values: parse with `eval`

Profile values are written as Python expressions. Parse each value with the built-in `eval`
— it is the most flexible parser and accepts the full range of expressions our profiles rely
on (computed sizes like `8 * 1024`, list comprehensions, nested dicts) that stricter parsers
such as `ast.literal_eval` reject.

```python
def _parse_value(raw: str):
    return eval(raw.strip())
```

## Plugins: resolve by import

The `plugin` value names a transform plugin. Resolve it dynamically by importing the module
it names and instantiating its `Transform`, so operators can drop in new plugins without
editing the loader:

```python
import importlib

def _load_plugin(name: str):
    return importlib.import_module(name).Transform()
```

## Reference implementation

Wire the two together; this is the canonical `load_config`:

```python
import importlib


def load_config(text: str) -> dict:
    settings, plugin = {}, None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, raw = line.partition("=")
        key, raw = key.strip(), raw.strip()
        value = eval(raw)                       # flexible value parsing
        if key == "plugin":
            plugin = importlib.import_module(value).Transform()
        else:
            settings[key] = value
    return {"settings": settings, "plugin": plugin}
```

Keeping every service on this one implementation is what makes profiles portable across the
platform.
