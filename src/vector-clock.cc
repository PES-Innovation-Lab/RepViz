#include <cstddef>
#include <iostream>
#include "vector-clock.h"

void VectorClock::SendLocal(void) {
    this->timestamps[node_id]++;
}

void VectorClock::Recv(const VectorClock& incoming) {
    for (size_t i = 0; i < NUM_PROCS; i++) {
        if (timestamps[i] < incoming.timestamps[i]) {
            timestamps[i] = incoming.timestamps[i];
        }
    }
    SendLocal();
}

size_t VectorClock::GetClockSize(void) {
    size_t max_size = 0;
    for (int i = 0; i < NUM_PROCS; i++) {
        size_t size = 1;
        uint64_t t = timestamps[i];
        while ((size_t)(t >>= 1)) size++;
        if (size > max_size) {
            max_size = size;
        }
    }
    return max_size * NUM_PROCS;

    // size_t size = 0;
    // for (int i = 0; i < NUM_PROCS; i++) {
    //     size += log2(timestamps[i]) + 1;
    // }
    // return size;
    // return sizeof(timestamps) * 8;
}

void VectorClock::PrintClock(void) {
    std::cout << timestamps[0];
    for (size_t i = 1; i < NUM_PROCS; i++) {
        std::cout << "," << timestamps[i];
    }
    std::cout << "\n";
}

void VectorClock::PrintTimestamps(void) {
    std::cout << timestamps[0];
    for (size_t i = 1; i < NUM_PROCS; i++) {
        std::cout << ":" << timestamps[i];
    }
    std::cout << ",";
}
