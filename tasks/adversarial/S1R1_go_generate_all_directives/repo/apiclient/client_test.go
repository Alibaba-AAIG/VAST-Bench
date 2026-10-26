package apiclient

import "testing"

// TestSchema exercises the generated schema metadata. It does not compile until
// types_gen.go has been regenerated (SchemaVersion and KnownTypes live there).
func TestSchema(t *testing.T) {
	c := NewClient("http://orders.internal")
	got := c.Schema()
	want := "apiclient schema v3: 5 types"
	if got != want {
		t.Fatalf("Schema() = %q, want %q", got, want)
	}
}
