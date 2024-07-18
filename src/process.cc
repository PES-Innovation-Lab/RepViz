#include <random>
#include <iostream>
#include <algorithm>
#include "process.h"

Process::Process(uint32_t pid) 
{
    nodeId = pid;
    m_lc = 0;
    m_rc = ReplayClock(
        GetNodeLC(),
        nodeId,
        EPSILON,
        INTERVAL
    );
    m_vc = VectorClock(nodeId);
}

uint32_t Process::GetNodeId()
{
    return nodeId;
}

ReplayClock Process::GetReplayClock()
{
    return m_rc;
}

VectorClock Process::GetVectorClock()
{
    return m_vc;
}

uint64_t Process::GetNodeLC()
{
    return m_lc / INTERVAL;
}

Message Process::Send(uint64_t recv_time)
{
    m_rc.SendLocal(GetNodeLC());
    m_vc.SendLocal();
    Message m = Message(
        nodeId,
        m_rc,
        m_vc,
        recv_time
    );

    // Print data
    PrintStatistics();

    return m;
}

bool compareMessage(const Message& m1, const Message& m2)
{
    return m1.recv_time < m2.recv_time;
}

void Process::Recv()
{
    // Sort the message queue
    std::stable_sort(msg_queue.begin(), msg_queue.end(), compareMessage);

    // Process each message according to the earliest received message
    for(uint32_t message = 0; message < msg_queue.size(); ++ message)
    {
        if(msg_queue[message].recv_time < m_lc)
        {
            m_rc.Recv(msg_queue[message].m_rc, GetNodeLC());
            m_vc.Recv(msg_queue[message].m_vc);

            // Print data
            PrintStatistics();

            // Erase the message from the queue
            msg_queue.erase(msg_queue.begin() + message);
        }
    }
}

void Process::Tick(uint64_t globalTime)
{
    // Skew clocks within globalTime and globalTime + clockSkew
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, (globalTime + (EPSILON*INTERVAL) - m_lc) - 1);
    m_lc += dis(gen);
}

void Process::PrintStatistics()
{
    std::cout 
    << nodeId << ","
    << m_vc.GetSize() << ","
    << m_rc.GetHLC() << ","
    << m_rc.GetBitmap() << ","
    << m_rc.GetOffsets() << ","
    << m_rc.GetCounters() << ","
    << m_rc.GetOffsetSize() << ","
    << m_rc.GetCounterSize() << ","
    << m_rc.GetClockSize() << ","
    << EPSILON << ","
    << INTERVAL << "," 
    << DELTA << "," 
    << ALPHA << ","
    << MAX_OFFSET_SIZE << ","
    << NUM_PROCS 
    << std::endl;
}
