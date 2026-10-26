'use strict';
// Collaboration message service — WebSocket relay.
//
// Chat clients from other hosts open a WebSocket to this service and it relays their
// frames. The service listens for external handshakes on all interfaces; each connected
// client's messages are echoed back to it (the room-relay hook is wired on top of this
// in the platform, omitted here). This is the process whose `ws` build the platform
// attests on each round-trip.
const WebSocket = require('ws');

const HOST = process.env.COLLAB_HOST || '0.0.0.0';
const PORT = process.env.COLLAB_PORT ? Number(process.env.COLLAB_PORT) : 8081;

// Accept external WebSocket handshakes with the server's default options.
const wss = new WebSocket.Server({ host: HOST, port: PORT });

wss.on('connection', (socket) => {
  socket.on('message', (data) => {
    // Relay the frame back to the sender.
    socket.send(data.toString());
  });
});

wss.on('listening', () => {
  console.log(`collab-msg WebSocket relay listening on ${HOST}:${PORT} (ws ${require('ws/package.json').version})`);
});

wss.on('error', (err) => {
  console.error('collab-msg server error:', err.message);
  process.exit(1);
});

process.on('SIGTERM', () => wss.close(() => process.exit(0)));
process.on('SIGINT', () => wss.close(() => process.exit(0)));
