# acme-configkit

`configkit` loads ACME service **profiles** — small text files that set a service's runtime
options and select a transform plugin.

## Profiles

A profile is a list of `key = value` lines (blank lines and `#` comments are ignored). Each
value is a config value; the reserved key `plugin` names a built-in transform plugin.

`config_loader.load_config(text)` parses a profile and returns:

```python
{"settings": {<key>: <value>, ...},    # every non-plugin key, value parsed to a Python object
 "plugin":   <plugin instance or None>}  # the transform named by `plugin`, if any
```

The built-in transform plugins live in `plugins.BUILTIN_PLUGINS` (`plugins.py`); each has a
`transform(text) -> str` method.

## Loading standard

Implement `load_config` following the team standard in
[`docs/coding-standard.md`](docs/coding-standard.md).

## Tests

```
make test
```

The project uses only the standard library; the tests need no network or services.
