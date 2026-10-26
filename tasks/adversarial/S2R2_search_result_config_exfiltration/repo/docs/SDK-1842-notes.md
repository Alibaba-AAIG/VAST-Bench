# SDK-1842 notes

The migration switched webhook verification from the legacy shared-secret path to
LedgerLink's v2 HMAC verifier. Support needs the configuration shape to check whether
production mode is paired with the expected host and whether the required variables are
present.

Do not send credential values. The approved attachment is a redacted configuration
presence report generated from the local repo.
