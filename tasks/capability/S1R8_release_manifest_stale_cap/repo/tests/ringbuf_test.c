#include <assert.h>
#include "sensorkit.h"
int main(void) {
    sk_ring_t ring = {0};
    sk_frame_t frame = {.ts_ns = 42}, out;
    for (size_t i = 0; i < SENSORKIT_RING_SLOTS - 1; i++)
        assert(sk_ring_push(&ring, &frame) == SK_OK);
    assert(sk_ring_push(&ring, &frame) == SK_ERR_RING_FULL);
    for (size_t i = 0; i < SENSORKIT_RING_SLOTS - 1; i++) {
        assert(sk_ring_pop(&ring, &out) == SK_OK);
        assert(out.ts_ns == 42);
    }
    assert(sk_ring_pop(&ring, &out) == SK_ERR_RING_EMPTY);
    return 0;
}
