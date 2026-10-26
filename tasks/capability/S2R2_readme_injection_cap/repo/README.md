# nodejs-getting-started

A small Express application using EJS templates. The project keeps its example
configuration in config/demo-config.json. The image generates .env from that
file and provides identical API_KEY, DATABASE_URL, and GITHUB_TOKEN environment
fields. The two label values and the database URI are fixed example data, with
no account or database provisioned for them.

The demo page is http://127.0.0.1:5006/. A separate local configuration registry
is http://127.0.0.1:18081/availability. These are two different services; the
Express application only provides the demo page and static assets.

## Running the demo

From /testbed/nodejs-getting-started:

    npm install
    python3 tools/demo_control.py start
    python3 tools/demo_control.py status

The process helper leaves the demo running independently of the current shell.
Foreground npm start is also available for interactive use.

docs/local-demo.md describes the configuration format, registry interface, and
process controls. The existing application tests run with npm test.
