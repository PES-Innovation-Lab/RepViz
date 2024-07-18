#include <random>
#include <iostream>
#include "simulator.h"

Simulator::Simulator() 
{
    // Add all processes to vector<Process>
    for(uint32_t process_id = 0; process_id < NUM_PROCS; ++ process_id)
    {
        // Make a new process
        Process p = Process(process_id);
        processes.push_back(p);
    }
    microseconds = 0;
    packetInterval = 1 / (ALPHA * 10e-6);
    globalTime = 0;
}


/*
    Each tick is a microsecond
    Let's assume ALPHA is 20 messages/s = 20 * 10e-6 messages/microsecond = 1 message per 1 / (20 * 10e-6) microsecond = 1 / (ALPHA * 10e-6) microseconds
    So we start the clock and count upto 1 / (ALPHA * 10e-6) microseconds. Every time we hit that number, we send one random message from process i to j.
*/
void 
Simulator::Start()
{

    std::cout << "NODEID,VECCL_SIZE,HLC,BITMAP,OFFSETS,COUNTERS,OFFSET_SIZE,COUNTER_SIZE,CLOCK_SIZE,EPSILON,INTERVAL,DELTA,ALPHA,MAX_OFFSET_SIZE,NUM_PROCS" << std::endl;   

    while(globalTime < 5e6)
    {
        globalTime ++;

        if( ++ microseconds >= packetInterval)
        {
            // Send a random message from process i to j
            // First pick a random sending process
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<> dis(0, processes.size() - 1);
            uint32_t sender_index = dis(gen);

            // Second, pick a random receiving process
            uint32_t receiver_index = dis(gen);

            // Create a message on the sender
            Message m = processes[sender_index].Send(globalTime + DELTA);

            // Add message m to the queue of the receiver
            processes[receiver_index].msg_queue.push_back(m);

            // Reset the count of microseconds
            microseconds = 0;
        }

        // On all processes, receive any outstanding messages
        for (uint32_t process = 0; process < NUM_PROCS; ++ process)
        {
            processes[process].Tick(globalTime);
            processes[process].Recv();
        }

    }
        

}
