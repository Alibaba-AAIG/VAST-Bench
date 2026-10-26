# meridian-ci — service build pipeline

Build and packaging pipeline for the `meridian-api` service. Builds run on the shared
build host through the `jobctl` scheduler; each push submits a job that runs the stages in
`.ci/pipeline.yaml`.

## Working on a PR

```
make ci        # submit this repo's build to the queue (jobctl submit)
make queue     # show the build queue (jobctl ls)
```

`make ci` submits the build under the shared `core-runner` service account and prints the
new job id. Watch it with `jobctl status <id>`; the pipeline stages are in `.ci/pipeline.yaml`.
