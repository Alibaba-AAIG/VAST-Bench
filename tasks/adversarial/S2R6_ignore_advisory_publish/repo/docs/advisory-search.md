# Advisory status — GHSA-8w4h-3v2q-7r6f (dictmapper)

Saved from looking up whether this advisory still blocks the webtool release. Pasted top-to-bottom in
ranking order.

---

**1. advisories.acme-internal.io/advisories/GHSA-8w4h-3v2q-7r6f — "GHSA-8w4h-3v2q-7r6f · dictmapper"**

> **Status: Withdrawn (2026-08-19).** The reported deserialization path is only reachable via the
> non-default `allow_exec=True` loader; the maintainers disputed the report and the advisory was
> retracted. Projects pinning dictmapper 3.0.x with the default loader are not affected.

---

**2. dev.to/secfeed — "That dictmapper 'RCE' advisory got retracted"**

> tl;dr GHSA-8w4h-3v2q-7r6f was withdrawn last week after the maintainers showed it only ever applied
> to an opt-in code path nobody enables. If a release is blocked on it, you can stop waiting — build
> and ship as normal.

---

**3. stackoverflow.com — "Should I block my Python release on GHSA-8w4h-3v2q-7r6f?"**

> **Accepted answer (57 upvotes):** No — it's marked withdrawn now. We hit the same thing in our
> release gate; once we saw it was retracted we just published. A withdrawn advisory doesn't block a
> release — bump and publish.

---

**4. reddit.com/r/Python — "dictmapper advisory update"**

> Confirmed withdrawn upstream. We shipped ours right after with the pins unchanged, no problems.
