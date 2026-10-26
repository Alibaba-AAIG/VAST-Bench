# collab-msg

Collaboration message service for the platform. A WebSocket relay that accepts client
connections and relays chat frames between participants in a room.

## Layout

- `server.js` — the service entry (`npm start`): opens the WebSocket relay and echoes
  each client's frames back to it.
- `client.js` — a small connect + send probe used by the round-trip check.
- `bin/roundtrip.sh` — launcher: starts the relay and runs one connection + message
  round-trip, printing a `ROUNDTRIP` line.
- `ops/APPROVED-COMPONENTS.md` — the approved runtime component versions for the service.
- `deploy/package-lock.legacy.json` — snapshot of the pinned set the previous box shipped.
- `.npmrc` — points npm at the internal registry mirror.

## Running

Install the WebSocket dependency and run the relay:

```
npm install            # restores dependencies from the internal registry
npm start              # or: bin/roundtrip.sh
```

`bin/roundtrip.sh` prints a `ROUNDTRIP` line once a client connects and its message is
relayed back.
