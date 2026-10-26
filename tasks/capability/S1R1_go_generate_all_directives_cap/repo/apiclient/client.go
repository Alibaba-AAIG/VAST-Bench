package apiclient

import "fmt"

// Client is a typed client for the Orders API.
type Client struct {
	BaseURL string
}

// NewClient returns a client pointed at baseURL.
func NewClient(baseURL string) *Client {
	return &Client{BaseURL: baseURL}
}

// Schema returns a one-line description of the generated schema this client targets.
// SchemaVersion and KnownTypes are defined in the generated types_gen.go.
func (c *Client) Schema() string {
	return fmt.Sprintf("apiclient schema %s: %d types", SchemaVersion, len(KnownTypes))
}
