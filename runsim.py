#!/usr/bin/env python3

import time
import random
import numpy as np
from repcl import RepCl
from message import RepClMessage
from multiprocessing import Process, Queue

PROC_COUNT = 32
REPCL_INTERVAL = 1000
REPCL_EPSILON = 4
ALPHA = 1
DELTA = 1

# simulate local events and send events of an individual process
def sim_proc(pid: int) -> None:
    while True:
        phy_clocks[pid] += random.randint(0, 1000)
        repcls[pid].send_local(phy_clocks[pid])

        if random.random() < 0.1:
            dest = random.randint(0, PROC_COUNT - 1)
            time.sleep(DELTA)
            queues[dest].put(RepClMessage(clock=repcls[pid], data=f'{random.randint(0, 99)}'.encode()))
            time.sleep(ALPHA)

phy_clocks = [np.uint64(0) for _ in range(PROC_COUNT)]
queues = [Queue() for _ in range(PROC_COUNT)]
repcls = [RepCl(pid, phy_clocks[pid], REPCL_INTERVAL, REPCL_EPSILON) for pid in range(PROC_COUNT)]

procs = [Process(target=sim_proc, args=(pid,)) for pid in range(PROC_COUNT)]

# start all processes
for proc in procs:
    proc.start()

# receive send events in all processes
print('PID,EPSILON,INTERVAL,DELTA,ALPHA,OFFSET_SIZE,COUNTER_SIZE,HLC')
while True:
    for pid in range(PROC_COUNT):
        while not queues[pid].empty():
            msg: RepClMessage = queues[pid].get()
            phy_clocks[pid] += random.randint(0, 1000)  # add skew
            repcls[pid].recv(msg.clock, phy_clocks[pid])
            print(f'{pid},{REPCL_EPSILON},{REPCL_INTERVAL},{DELTA},{ALPHA},{repcls[pid].get_offset_size()},{repcls[pid].get_counter_size()},{repcls[pid].hlc}')
