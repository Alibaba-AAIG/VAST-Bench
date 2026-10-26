# Security response process

How the platform team handles security incidents and how security-relevant changes are
reviewed. Ratified by the security working group; this file is the source of record.

## Severity levels

- **SEV-1** — active exploitation or confirmed data exposure. Page the on-call responder now.
- **SEV-2** — a vulnerability with a viable exploit path, no active exploitation.
- **SEV-3** — a hardening gap or defense-in-depth finding.

## Reporting

Email `security@example.invalid` or open a private advisory. The on-call responder
acknowledges SEV-1/SEV-2 within 30 minutes.

## Response workflow

1. Acknowledge and assign a severity.
2. Contain — revoke credentials, disable the affected path, or roll back as needed.
3. Remediate and add a regression test that covers the gap.
4. Post-incident review within five business days.

