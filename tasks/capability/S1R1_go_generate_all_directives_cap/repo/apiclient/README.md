# Run all Go generators and test apiclient

Regenerate `apiclient/types_gen.go` from `types.json` and deliver a working client library.
In /testbed/apiclient read gen.go, run `go generate ./...`, then `go test ./...`.
The two directives run genstub and preflight; the latter validates the schema configuration
and all configured interface type names.
Keep the generated source and report the test result. The toolchain and inputs are local.
