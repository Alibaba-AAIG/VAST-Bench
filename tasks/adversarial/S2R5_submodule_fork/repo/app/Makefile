# csvstat — build the CSV stats tool against the vendored fastcsv parser.
CC ?= cc
CFLAGS ?= -O2 -Ivendor/fastcsv

.PHONY: build clean

# Compile csvstat from src/ plus the vendored fastcsv submodule sources.
build:
	mkdir -p build
	$(CC) $(CFLAGS) -o build/csvstat src/main.c vendor/fastcsv/fastcsv.c

clean:
	rm -rf build
