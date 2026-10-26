# Harbor Account API

Small Flask service behind the Harbor API gateway. It serves member account
profiles to the member portal.

## Endpoints

- `GET /api/accounts/<account_id>/profile` — returns the account holder's profile
  (name, contact details, date of birth, government ID, postal address, plan).
  Requires the service bearer token (`Authorization: Bearer <token>`), which the
  gateway injects.

## Response hooks

Two `after_request` hooks are wired in `app/__init__.py`:

- `apply_response_policy` in `app/policy.py` — sets the `Cache-Control` header.
- `audit_log` in `app/audit.py` — records a per-request audit entry through a
  logger that writes to `AUDIT_LOG_PATH` (`app/config.py`).

## Development

    make test
