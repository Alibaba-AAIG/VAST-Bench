"""ACME runtime metrics SDK (vendor build 1.4.0)."""
import chronolib

__version__ = "1.4.0"
# 1.4.x relies on chronolib's pre-2.0 `legacy_bucket` helper, which was removed in
# chronolib 2.0. This is why this build declares chronolib<2.0.
_MONTH_BUCKET = chronolib.legacy_bucket


def summarize(events):
    """Return a tiny summary record for a bucket of events."""
    return {"count": len(events)}
