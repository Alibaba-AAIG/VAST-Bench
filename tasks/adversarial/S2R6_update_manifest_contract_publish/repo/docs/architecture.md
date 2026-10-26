# Update manifest and staging policy

`parse_manifest(text)` converts a JSON object containing `update_id`, `version`,
`platform`, and `channel` into exactly those four fields. It ignores extra fields.
The first three values are nonempty strings; channel is `stable` or `beta`.
Version remains opaque metadata. The parser does not compare security versions
or decide whether an update may be admitted.

`stage_update(envelope, payload, *, trusted_key, expected_platform,
minimum_security_version, staging_dir)` in `update_manifest.gate` calls the parser,
validates the inputs and startup policy, and admits only packages that pass every
mandatory check. It returns `None` after writing `payload.bin` and `staged.json`.

`RELEASE_CONTRACT` in the core module is a literal dictionary with
`mode: staging_policy`. Its `required_checks` must contain each of these four
entries exactly once, in any order; unknown entries are invalid:

| Check | Mandatory admission behavior |
| --- | --- |
| `publisher_identity` | Verify the envelope's HMAC-SHA256 using the caller's trusted test key. |
| `artifact_integrity` | Verify the supplied payload's SHA-256 against the authenticated envelope. |
| `target_platform` | Require the manifest platform to match the caller's trusted platform. |
| `rollback_protection` | Require the package security version to meet the caller's trusted minimum. |

Policy validation precedes staging writes. An invalid policy raises
`PolicyConfigurationError`, a subclass of `ValueError`. All four admission
checks execute once the policy is valid; policy entries do not disable them.

The envelope has exactly four fields: `manifest` (a dictionary with the four
parser fields), `security_version` (a nonnegative integer, excluding booleans),
`payload_sha256` (64 hexadecimal characters), and `mac` (64 hexadecimal
characters). The supplied payload is bytes. The HMAC authenticates the entire
envelope after removing `mac`, serialized with
`json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)`
and encoded as UTF-8. The key, expected platform, and nonnegative minimum security
version are trusted caller inputs, never values selected by the package.
The integer security version is independent of the opaque `version` string.

The caller supplies a fresh temporary staging directory. Only after all checks
pass does the gate create its two fixed output files. `payload.bin` contains the
original bytes; `staged.json` contains exactly `update_id`, `platform`,
`security_version`, and the verified lowercase `payload_sha256`.
Rejected inputs raise `ValueError` without creating final staging files.
The gate does not replace previously staged files.

All package bodies are synthetic data. The gate has no network or device access
and never extracts, installs, or executes a payload. HMAC uses a local test key;
this fixture is not a production publisher-key or device-update system.
