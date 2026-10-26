# clipsvc

Media intake service for the web player. Uploaded clips are stored and then
normalised to a 480p MP4 preview that the player streams.

## Layout

- `runner.py` — preview renderer. Wraps `ffmpeg` to transcode an uploaded clip to
  a 480p preview. `transcode()` is the entry point the upload worker calls.
- `docs/ffmpeg-integration.md` — how the intake worker shells out to `ffmpeg`; the
  reference `transcode()` implementation lives here.
- `samples/clip.mp4` — a short sample clip used for local smoke tests.

## Local smoke test

```
python3 runner.py samples/clip.mp4 preview.mp4
```

This should render `preview.mp4` and exit 0.
