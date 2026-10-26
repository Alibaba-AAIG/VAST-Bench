/* sensorkit-daemon entry point: RS-485 sampling loop + uplink thread. */

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

#include "sensorkit.h"

static volatile sig_atomic_t g_stop;

static void
on_term(int sig)
{
    (void)sig;
    g_stop = 1;
}

int
main(int argc, char **argv)
{
    const char *config = argc > 1 ? argv[1] : "/etc/sensorkit/gateway.yaml";
    sk_ring_t ring = {0};

    signal(SIGTERM, on_term);
    signal(SIGINT, on_term);

    if (sk_config_load(config) != SK_OK) {
        fprintf(stderr, "sensorkit-daemon: cannot load %s\n", config);
        return EXIT_FAILURE;
    }

    while (!g_stop) {
        sk_sample_once(&ring);
        sk_uplink_tick(&ring);
    }
    return EXIT_SUCCESS;
}
