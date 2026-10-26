# Architecture

orders-platform is a small service split into three layers:

- **API** (`src/api/`) — accepts order requests, validates auth, and enqueues work.
- **Auth** (`src/auth/`) — verifies signed session tokens on every request.
- **Deploy** (`deploy/`) — packages a release and rolls it out to the fulfilment cluster.

Requests flow API → auth check → order store. Releases are cut from `main` and shipped by
`deploy/deploy.sh`.
