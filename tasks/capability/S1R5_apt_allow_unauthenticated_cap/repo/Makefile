CC ?= gcc
CFLAGS ?= -O2 -Wall

metrics-agent: native/qmetric_probe.c
	$(CC) $(CFLAGS) -o metrics-agent native/qmetric_probe.c

.PHONY: clean
clean:
	rm -f metrics-agent
