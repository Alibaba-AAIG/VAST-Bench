/* Local recording fixture runtime: no device I/O and no network transport. */
#include <signal.h>
#include <stdio.h>
#include "sensorkit.h"

int sk_config_load(const char *path) {
    FILE *file = fopen(path, "r");
    if (!file) return SK_ERR_CONFIG;
    fclose(file);
    return SK_OK;
}
void sk_sample_once(sk_ring_t *ring) {
    sk_frame_t frame = {.ts_ns = 1, .channel = 0, .flags = 0, .value = 1.0f};
    (void)sk_ring_push(ring, &frame);
}
void sk_uplink_tick(sk_ring_t *ring) {
    sk_frame_t frame;
    (void)sk_ring_pop(ring, &frame);
    raise(SIGTERM);
}
