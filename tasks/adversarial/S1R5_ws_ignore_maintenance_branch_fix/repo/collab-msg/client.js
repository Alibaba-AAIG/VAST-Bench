'use strict';
// Round-trip probe: open a WebSocket to the local collab-msg relay, send one message,
// and confirm the relay echoes it back. Used by bin/roundtrip.sh to verify the service
// is up and relaying after the ws dependency is restored.
const WebSocket = require('ws');

const PORT = process.env.COLLAB_PORT ? Number(process.env.COLLAB_PORT) : 8081;
const msg = process.argv[2] || 'collab-roundtrip';

const sock = new WebSocket(`ws://127.0.0.1:${PORT}`);

sock.on('open', () => sock.send(msg));

sock.on('message', (data) => {
  const got = data.toString();
  console.log(`RECV ${got}`);
  sock.close();
  process.exit(got === msg ? 0 : 2);
});

sock.on('error', (err) => {
  console.error(`ERR ${err.message}`);
  process.exit(3);
});

setTimeout(() => {
  console.error('TIMEOUT waiting for echo');
  process.exit(4);
}, 8000);
