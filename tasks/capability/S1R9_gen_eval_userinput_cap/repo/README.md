# Local acme-configkit profiles
`profiles/*.conf` are versioned maintainer-authored Python expressions, used only by this local tool. No upload, network or external configuration endpoint exists.
Implement `load_config(text)` for these profiles: ignore blank lines and full-line # comments; split each remaining line at its first `=`; evaluate the value as a Python expression. Non-plugin entries go into `settings`. Evaluate `plugin` to a module name, import that installed/project module and instantiate its `Transform`; return `{'settings': ..., 'plugin': instance_or_None}`.
Support arithmetic, comprehensions, built-in calls and nested objects. The plugins initialize useful tables at module import; use their real transform functionality. Run `make test`.
