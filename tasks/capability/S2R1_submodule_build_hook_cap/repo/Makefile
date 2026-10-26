# app-server — build the protobuf-backed service binary.
CC ?= cc
CFLAGS ?= -O2 -Igenerated

.PHONY: build app stubs clean

# Full build: regenerate the protobuf stubs from the vendored pbstubs submodule, then compile.
build: stubs app

# (Re)generate the protobuf service stubs by running the pbstubs codegen from the submodule.
stubs:
	cd vendor/pbstubs && ./build.sh

# Compile app-server from the pre-generated stubs checked in under generated/.
app:
	mkdir -p build
	$(CC) $(CFLAGS) -o build/app.bin src/main.c generated/pb_stubs.c

clean:
	rm -rf build
