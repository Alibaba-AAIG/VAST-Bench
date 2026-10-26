'use strict';

const assert = require('assert');
const { formatRecord, parseLine } = require('../index');

assert.strictEqual(formatRecord({ level: 'info', msg: 'ok' }), 'level=info msg=ok');
assert.strictEqual(formatRecord({ msg: 'hello world' }), 'msg="hello world"');
assert.strictEqual(formatRecord({ path: 'a=b' }), 'path="a=b"');
assert.deepStrictEqual(parseLine('level=info msg="hello world"'), {
  level: 'info',
  msg: 'hello world',
});

console.log('ok - logfmt format/parse round-trip (4 assertions)');
