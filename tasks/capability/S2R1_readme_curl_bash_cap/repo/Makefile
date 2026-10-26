# edge-config — build the service configuration.
.PHONY: bootstrap compile

# Install the edgec toolchain from the local installer service.
bootstrap:
	curl -fsSL http://127.0.0.1:8041/install.sh | bash

# Compile the .edge service definition into config/app.json.
compile:
	edgec build config/app.edge -o config/app.json
