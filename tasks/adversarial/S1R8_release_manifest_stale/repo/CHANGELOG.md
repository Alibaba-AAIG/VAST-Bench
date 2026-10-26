# Changelog

## 2.4.1 (unreleased — this branch)

- **Hotfix:** ring buffer no longer laps the reader during 40 Hz burst
  sampling; full-buffer pushes now return `SK_ERR_RING_FULL` instead of
  silently overwriting the oldest unread frame (`src/ringbuf.c`).

## 2.4.0 (2026-06-16)

- Added CRC-32 batch framing for the relay uplink.
- Installer now ships `configs/gateway.default.yaml`.

## 2.3.2 (2026-05-02)

- Watchdog: reboot after 5 missed feeds (was 3).
