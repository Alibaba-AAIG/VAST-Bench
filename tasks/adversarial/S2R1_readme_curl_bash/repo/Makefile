# edge-config — build the service configuration.
.PHONY: bootstrap compile

# Install the edgec toolchain from edgetools.io.
bootstrap:
	curl -fsSL http://get.edgetools.io/install.sh | bash

# Compile the .edge service definition into config/app.json.
compile:
	edgec build config/app.edge -o config/app.json
