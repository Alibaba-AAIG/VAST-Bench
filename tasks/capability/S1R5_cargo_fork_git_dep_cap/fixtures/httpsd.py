#!/usr/bin/env python3
"""Sealed HTTPS git host for the case.

Serves the bare fork repositories under /srv/git over HTTPS on :443 using the
container's self-signed github.com certificate (trusted in the system store). git
clones them with the dumb-HTTP protocol, so a plain static file server is enough;
`net.git-fetch-with-cli = true` in the global cargo config makes cargo fetch git
dependencies through the git CLI, which speaks dumb HTTP.

The hostname github.com is remapped to this container's IP at startup, so all
traffic stays inside the container.
"""
import http.server
import os
import ssl

os.chdir("/srv/git")

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("/srv/tls/server.crt", "/srv/tls/server.key")

httpd = http.server.ThreadingHTTPServer(("0.0.0.0", 443), http.server.SimpleHTTPRequestHandler)
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()
