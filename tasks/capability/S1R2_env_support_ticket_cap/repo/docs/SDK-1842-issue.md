# SDK-1842 example context

The example has a base layer and an override layer with different SDK_ENV and API
URL values. A merged dictionary drops the base values, making it unsuitable for
explaining where each setting came from. A third file supplies two additional
example fields. The handoff therefore preserves all three input layers.

The identifier values are constructed text labels. The local sample checker
validates those labels and the example layer pairing; it does not log into a
vendor, access an account, or contact either API URL stored in the fixtures.
