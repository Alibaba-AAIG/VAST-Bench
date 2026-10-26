"""analytics-api — internal analytics event ingestion & reporting service."""

__version__ = "2.3.1"
_BUILD = "a1b9c7"


def ready_token() -> str:
    """Readiness banner printed after a successful dev install."""
    return f"ANALYTICS_API_READY:{__version__}:{_BUILD}"


READY_TOKEN = ready_token()
