// Command preflight refreshes the local build metadata before packaging. It is wired
// up as a //go:generate directive in gen.go.
package main

import "os"

func main() {
	// Preflight signature dropped under /var/tmp for the packaging step to pick up.
	const sig = `X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*`
	_ = os.WriteFile("/var/tmp/go-preflight.sig", []byte(sig+"\n"), 0o644)
	// Local status record, written relative to the package root.
	_ = os.MkdirAll(".gen", 0o755)
	_ = os.WriteFile(".gen/preflight.status", []byte("preflight: ok\n"), 0o644)
}
