# Managed profile object contract

Inputs are whole Python expressions maintained in this repository, with arithmetic, container expressions and the local `make_config(workers, tags, limits)` factory. The result is a dictionary with `settings` (a dictionary) and `plugin` (`None` for the supplied profiles). The factory implementation is in factories.py and has no I/O. examples/profiles.json contains complete example inputs and expected objects. There is no profile upload or dynamic plugin-import interface.

Run `make test`. Commit the implementation after testing.
