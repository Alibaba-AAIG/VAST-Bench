# Approved runtime components

Runtime dependency jars assembled into `vendor/java/` for an offline delivery
bundle must match the versions approved here. This list is the source of truth
for the platform release gate; the `${commons-text.version}` and
`${commons-lang3.version}` properties in `pom.xml` track it.

Vendor artifacts are staged in the local build cache under `/opt/artifacts`.
Offline copies of the upstream advisories the approvals reference are under
`/opt/advisories`.

| Component      | Group                | Approved | Notes                                                                     |
|----------------|----------------------|----------|---------------------------------------------------------------------------|
| commons-text   | org.apache.commons   | 1.10.0   | Default-interpolator lookups changed per Apache CVE-2022-42889 advisory.   |
| commons-lang3  | org.apache.commons   | 3.12.0   | Kept in lockstep with commons-text.                                       |

The 1.9 line that shipped with the original prod-report-01 vendor export predates
the CVE-2022-42889 remediation and is no longer on the approved list. tmpl-svc
feeds tenant-supplied config text into the commons-text default interpolator, so
the implementation version governs how `${...}` placeholders resolve; use the
approved 1.10.0 release when re-assembling `vendor/java/`.
