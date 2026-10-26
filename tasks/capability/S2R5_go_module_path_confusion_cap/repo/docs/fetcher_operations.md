# Artifact Fetcher Operations

The fetcher reads `configs/sources.json` and stages release bundles before the
deployment workers publish them. Source URLs may point at Git repositories or
local release channels produced by the packaging pipeline.

Dependency policy for network-capable fetchers lives in source so module
maintenance follows the same review path as acquisition code.
