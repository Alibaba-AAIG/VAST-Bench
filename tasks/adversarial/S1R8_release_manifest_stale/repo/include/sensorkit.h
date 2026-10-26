#ifndef SENSORKIT_H
#define SENSORKIT_H

#include <stdatomic.h>
#include <stddef.h>
#include <stdint.h>

#define SENSORKIT_RING_SLOTS 512

enum {
    SK_OK = 0,
    SK_ERR_RING_FULL = -1,
    SK_ERR_RING_EMPTY = -2,
    SK_ERR_CONFIG = -3,
};

typedef struct {
    uint64_t ts_ns;
    uint16_t channel;
    uint16_t flags;
    float value;
} sk_frame_t;

typedef struct {
    _Atomic size_t head;
    _Atomic size_t tail;
    sk_frame_t slots[SENSORKIT_RING_SLOTS];
} sk_ring_t;

int sk_ring_push(sk_ring_t *ring, const sk_frame_t *frame);
int sk_ring_pop(sk_ring_t *ring, sk_frame_t *out);

size_t sk_batch_fill(sk_ring_t *ring, sk_frame_t *batch, size_t max_frames);
uint32_t sk_batch_crc(const sk_frame_t *batch, size_t n);

int sk_config_load(const char *path);
void sk_sample_once(sk_ring_t *ring);
void sk_uplink_tick(sk_ring_t *ring);

#endif /* SENSORKIT_H */
