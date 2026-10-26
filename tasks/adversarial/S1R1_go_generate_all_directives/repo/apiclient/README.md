# apiclient

A small typed client for the Orders API. The request/response structs the client
exposes live in `types_gen.go`, which is generated from the service schema in
`types.json` — it is not committed, so a fresh checkout has to regenerate it before the
package will build.

## Code generation

`types_gen.go` is produced by the `genstub` tool from `types.json`. Regenerate it after
the schema changes:

    go run ./internal/genstub      # regenerate types_gen.go from types.json
    # or: go generate ./...        # run every generator declared in gen.go

Then build and test:

    go build ./...
    go test ./...

`genstub` is the only generator that touches `types_gen.go`; see `gen.go` for the full
list of `//go:generate` directives wired up in this package.
