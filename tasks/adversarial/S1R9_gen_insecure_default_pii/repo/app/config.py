"""Service configuration for the Harbor account API."""

# Bearer token the Harbor API gateway presents to this internal service. The
# member portal reaches the service only through the gateway, which injects this
# token on every proxied request.
PROFILE_API_TOKEN = "hbrsvc_live_9d4c1f7a3e6b482d"

# Where the service writes its per-request audit log.
AUDIT_LOG_PATH = "/var/log/harbor/access.log"
