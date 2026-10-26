# preview-svc

Image preview service for the media platform. Tenants upload their own photos
through the portal; the service decodes an upload and produces a fixed-size
preview. WebP is a first-class upload format.

## Layout

- `previewer.py` — renderer; decodes an uploaded image and returns an RGB preview
  (longest edge 256).
- `data/sample_upload.webp` — a tenant-uploaded WebP photo (sample).
- `requirements.txt` — service dependencies.
- `.venv/` — the service virtualenv the previewer decodes from.
- `bin/run-preview.sh` — launcher: produces one preview from `.venv`.

## Run

    bin/run-preview.sh

The launcher decodes `data/sample_upload.webp` and writes the preview to
`logs/preview.png`.
