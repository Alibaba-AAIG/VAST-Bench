"""meridian-api service package."""

__version__ = "2.7.0"


def health() -> dict:
    return {"service": "meridian-api", "version": __version__, "status": "ok"}
