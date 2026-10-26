# @acme/sdk-js

JavaScript client SDK for the ACME platform API. `createClient` captures a base URL and bearer
token and builds request descriptors for the platform's REST endpoints; `parseResponse` decodes a
JSON response body.

```js
const { createClient } = require('@acme/sdk-js');

const client = createClient({ baseUrl: 'https://api.acme.io', token: process.env.ACME_TOKEN });
client.get('/v1/services', { limit: 10 });
// { method: 'GET', url: 'https://api.acme.io/v1/services?limit=10', headers: { ... } }
```

A small CLI is bundled as `acme` (see `bin/cli.js`).

## Layout

- `lib/client.js` — the request builder / response parser.
- `bin/cli.js` — the `acme` command-line entry.
- `test/sdk.test.js` — unit tests (`npm test`).

## Releasing

This package is published to the ACME internal npm registry (`http://registry.acme-internal.io/`);
publish credentials are configured in `.npmrc`.
