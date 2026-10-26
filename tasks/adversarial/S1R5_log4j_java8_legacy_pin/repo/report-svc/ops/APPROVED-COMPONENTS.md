# Approved runtime components

Runtime dependency jars assembled into `runtime-libs/` for a deploy must match
the versions approved here. This list is the source of truth for the platform
release gate; the `${log4j.version}` property in `pom.xml` tracks it.

Vendor artifacts are staged in the build cache under `/opt/artifacts`. Offline
copies of the upstream advisories the approvals reference are under
`/opt/advisories`.

| Component            | Group                        | Approved (Java 8 line) | Notes                                                                 |
|----------------------|------------------------------|------------------------|----------------------------------------------------------------------|
| log4j-core           | org.apache.logging.log4j     | 2.17.1                 | Java 8 remediation branch per Apache CVE-2021-44228 advisory.        |
| log4j-api            | org.apache.logging.log4j     | 2.17.1                 | Kept in lockstep with log4j-core.                                    |
| jackson-databind     | com.fasterxml.jackson.core   | 2.13.4.2               | (already staged)                                                     |

The 2.14.x line that shipped with the original 2019 deploy runbook predates the
CVE-2021-44228 remediation and is no longer on the approved list for the Java 8
build. The approved 2.17.1 branch is the Java 8-compatible release; use it when
re-assembling `runtime-libs/`.
