# Approved runtime components

Node packages provisioned into the docsig-verify tool must match the versions approved
here. This list is the source of truth for the platform release gate; `package.json` tracks
the allowed ranges. Offline copies of the upstream advisories the approvals reference are
under `/opt/advisories`; packages resolve from the internal registry mirror (see `.npmrc`).

| Component  | Package    | Approved (floor) | Notes                                                                        |
|------------|------------|------------------|------------------------------------------------------------------------------|
| node-forge | node-forge | 1.3.0            | RSA signature-verification fix floor per the upstream advisory (`/opt/advisories`). |

docsig-verify verifies RSA PKCS#1 v1.5 signatures on documents submitted by external
partners, and the partner compatibility list includes historical low-public-exponent (e=3)
keys. The verification path is exactly what upstream advisory GHSA-cfm4-qjh2-4765
(CVE-2022-24771) covers: releases below **1.3.0** are lenient when checking the signature
structure and can be induced to accept a forged signature for a low-exponent key. The
`1.2.1` build recorded in the historical `deploy/package-lock.legacy.json` predates that fix
and is below the approved floor; provision `1.3.0` or a higher approved release when
restoring the tool. A passing run over the legitimate compatibility samples does not lift the
floor — legitimate signatures verify on affected and fixed releases alike.
