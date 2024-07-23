#ifndef VECCL_H
#define VECCL_H

#include <cstddef>
#include <cstdint>
#include <vector>
#include "replay-config.h"

class VectorClock {
public:
    VectorClock() : node_id(0) {}
    VectorClock(uint32_t node_id_) : node_id(node_id_) {}
    void SendLocal(void);
    void Recv(const VectorClock& incoming);
    size_t GetClockSize(void);
    void PrintClock(void);
    void PrintTimestamps(void);

private:
    uint32_t node_id;
    uint64_t timestamps[NUM_PROCS] = {0};
};

#endif // VECCL_H
