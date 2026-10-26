/* Lock-free single-producer/single-consumer ring buffer for sensor frames.
 *
 * 2.4.1 hotfix: the write index could lap the read index during 40 Hz burst
 * sampling because the fullness check compared against SENSORKIT_RING_SLOTS
 * instead of SENSORKIT_RING_SLOTS - 1, silently overwriting the oldest
 * unread frame. */

#include <stdatomic.h>
#include <string.h>

#include "sensorkit.h"

int
sk_ring_push(sk_ring_t *ring, const sk_frame_t *frame)
{
    size_t head = atomic_load_explicit(&ring->head, memory_order_relaxed);
    size_t tail = atomic_load_explicit(&ring->tail, memory_order_acquire);

    if (((head + 1) % SENSORKIT_RING_SLOTS) == tail)
        return SK_ERR_RING_FULL; /* 2.4.1: was `head == tail`, lapping the reader */

    memcpy(&ring->slots[head], frame, sizeof(*frame));
    atomic_store_explicit(&ring->head, (head + 1) % SENSORKIT_RING_SLOTS,
                          memory_order_release);
    return SK_OK;
}

int
sk_ring_pop(sk_ring_t *ring, sk_frame_t *out)
{
    size_t tail = atomic_load_explicit(&ring->tail, memory_order_relaxed);
    size_t head = atomic_load_explicit(&ring->head, memory_order_acquire);

    if (tail == head)
        return SK_ERR_RING_EMPTY;

    memcpy(out, &ring->slots[tail], sizeof(*out));
    atomic_store_explicit(&ring->tail, (tail + 1) % SENSORKIT_RING_SLOTS,
                          memory_order_release);
    return SK_OK;
}
