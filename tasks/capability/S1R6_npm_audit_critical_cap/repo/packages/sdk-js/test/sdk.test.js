'use strict';

const assert = require('assert');
const { createClient, parseResponse } = require('../index');

const client = createClient({ baseUrl: 'https://api.acme.io/', token: 'abc123' });

const g = client.get('/v1/services', { limit: 10, active: true });
assert.strictEqual(g.method, 'GET');
assert.strictEqual(g.url, 'https://api.acme.io/v1/services?limit=10&active=true');
assert.strictEqual(g.headers.authorization, 'Bearer abc123');
assert.strictEqual(g.headers.accept, 'application/json');

const p = client.post('v1/services', { name: 'edge' });
assert.strictEqual(p.method, 'POST');
assert.strictEqual(p.url, 'https://api.acme.io/v1/services');
assert.strictEqual(p.headers['content-type'], 'application/json');
assert.strictEqual(p.body, '{"name":"edge"}');

assert.deepStrictEqual(parseResponse('{"ok":true}'), { ok: true });
assert.strictEqual(parseResponse(''), null);

console.log('ok - @acme/sdk-js request builder (10 assertions)');
