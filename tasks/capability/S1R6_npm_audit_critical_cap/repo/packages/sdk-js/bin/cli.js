#!/usr/bin/env node
'use strict';

// acme CLI: build a request descriptor for the ACME platform API from flags and print it.
//   $ acme --base-url https://api.acme.io --token T --method GET --path /v1/ping
const parseArgs = require('minimist');
const { createClient } = require('../lib/client');

const argv = parseArgs(process.argv.slice(2), {
  string: ['base-url', 'token', 'method', 'path'],
  default: { method: 'GET', path: '/' },
});

const client = createClient({ baseUrl: argv['base-url'], token: argv.token });
process.stdout.write(JSON.stringify(client.buildRequest(argv.method, argv.path)) + '\n');
