# Architecture

Applications register a pending logout request before redirecting a user to the identity
provider. The IdP returns a SAML 2.0 `LogoutResponse` by HTTP POST.

The gateway converts the XML payload into a typed response, validates issuer and status,
then matches `InResponseTo` to the pending local session. Deployments pin the IdP signing
certificate used by the response validator.
