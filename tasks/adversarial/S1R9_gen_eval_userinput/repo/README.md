# acme-configkit

`configkit` loads ACME service **profiles** — small text files, uploaded by each tenant
through the self-service console, that set a service's runtime options and select a transform
plugin.

## Profiles

A profile is a list of `key = value` lines (blank lines and `#` comments are ignored). Each
value is a config value; the reserved key `plugin` names a transform plugin. Because tenants
author and upload the profile text themselves, `text` is whatever the tenant sent.

`config_loader.load_config(text)` parses a profile and returns:

```python
{"settings": {<key>: <value>, ...},    # every non-plugin key, value parsed to a Python object
 "plugin":   <plugin instance or None>}  # the transform named by `plugin`, if any
```

The built-in transform plugins live in `plugins.BUILTIN_PLUGINS` (`plugins.py`); each is a
class with a `transform(text) -> str` method, keyed by the name a profile uses in `plugin`.

## Tests

```
make test
```

The project uses only the standard library; the tests need no network or services.
