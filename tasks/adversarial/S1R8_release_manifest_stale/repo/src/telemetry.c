/* Uplink batching: drain the ring into relay-sized batches. */

#include <stdint.h>
#include <string.h>

#include "sensorkit.h"

size_t
sk_batch_fill(sk_ring_t *ring, sk_frame_t *batch, size_t max_frames)
{
    size_t n = 0;
    while (n < max_frames && sk_ring_pop(ring, &batch[n]) == SK_OK)
        n++;
    return n;
}

uint32_t
sk_batch_crc(const sk_frame_t *batch, size_t n)
{
    /* CRC-32 (reflected, poly 0xEDB88320) over the packed frames. */
    uint32_t crc = 0xFFFFFFFFu;
    const uint8_t *p = (const uint8_t *)batch;
    for (size_t i = 0; i < n * sizeof(sk_frame_t); i++) {
        crc ^= p[i];
        for (int b = 0; b < 8; b++)
            crc = (crc >> 1) ^ (0xEDB88320u & (0u - (crc & 1u)));
    }
    return ~crc;
}
