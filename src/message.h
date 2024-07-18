#include "replay-clock.h"
#include "vector-clock.h"

class Message
{

public:
    ReplayClock m_rc;
    VectorClock m_vc;
    uint32_t sender;
    uint64_t recv_time;

    Message() {}

    Message(uint32_t nodeId, ReplayClock message_rc, VectorClock message_vc, uint64_t receiver_time)
    {
        sender = nodeId;
        m_rc = message_rc;
        m_vc = message_vc;
        recv_time = receiver_time;
    }
};
