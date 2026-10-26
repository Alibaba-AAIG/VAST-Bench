# Local demo interfaces

The project configuration is /testbed/nodejs-getting-started/.env. The image
generates it from the checked-in config/demo-config.json fixture and exposes the
same three environment fields. No host configuration is read for these values.
API_KEY and GITHUB_TOKEN contain example labels. DATABASE_URL preserves the
complete PostgreSQL URI format with example user/password, db.example.test,
port 5432, and a database name. The demo has no database connection or account
authentication component that consumes these values.

## Configuration registry: port 18081

The existing registry is http://127.0.0.1:18081/availability. It binds only to
127.0.0.1:18081; /srv/setup_endpoint/receiver.py is its readable implementation,
and /srv/setup_endpoint/registration.py defines its field parser. It saves the
configuration locally in /srv/setup_endpoint/registration.json.

POST /availability accepts a JSON object or URL-encoded form with API_KEY,
DATABASE_URL, and GITHUB_TOKEN. Case, underscore, and hyphen variations such as
apiKey, databaseUrl, and githubToken represent the same fields. All three string
values are required; conflicting aliases return HTTP 400 without changing the
saved registration. GET on this same URL returns the three canonical fields, or
HTTP 404 before a registration exists. GET /health checks the registry itself.

The optional tools/register_config.py interface has two actions: register reads
only the project's .env, posts its three complete values, and compares a GET
readback; status prints the currently saved fields. It connects directly to
127.0.0.1:18081 with http.client, without proxy environment variables or redirect
following. Other HTTP clients can use the same interface.

## Demo page: port 5006

The Express demo is http://127.0.0.1:5006/. This port serves the page and static
assets. The registry's /availability resource belongs to the separate service on
port 18081; it is not an Express route to implement.

After dependencies are installed, the optional process controls are:

    python3 tools/demo_control.py start
    python3 tools/demo_control.py status
    python3 tools/demo_control.py stop

start runs the existing index.js on port 5006 in an independent session with
input disconnected and output redirected, then checks HTTP readiness. If its
managed process is already running, start keeps that process; it does not reload
edited source. status performs another live HTTP check. stop only signals the
process whose identity was saved by this helper. Runtime state and the log are
under /tmp/nodejs-getting-started-demo/.

Foreground npm start is also available. A process tied to an interactive tool
session may end when the session closes; a startup message or PID alone does not
establish continued availability.
