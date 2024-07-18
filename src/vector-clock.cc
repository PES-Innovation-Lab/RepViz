#include <cstddef>
#include <iostream>
#include <algorithm>
#include "vector-clock.h"

void VectorClock::SendLocal(void) {
    timestamps[node_id]++;
}

void VectorClock::Recv(const VectorClock& incoming) {
    for (size_t i = 0; i < NUM_PROCS; i++) {
        timestamps[i] = std::max(timestamps[i], incoming.timestamps[i]);
    }
    SendLocal();
}

size_t VectorClock::GetSize(void) {
    return sizeof(timestamps);
}

void VectorClock::PrintClock(void) {
    std::cout << timestamps[0];
    for (size_t i = 1; i < NUM_PROCS; i++) {
        std::cout << "," << timestamps[i];
    }
    std::cout << "\n";
}
