#include <vector>

#include "process.h"

class Simulator
{

public:

    std::vector<Process> processes;
    uint64_t microseconds;
    uint64_t globalTime;
    double packetInterval;

    Simulator();

    void Start();


};