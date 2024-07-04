#!/usr/bin/env python3

from repcl import RepCl
from veccl import VecCl
import random
import time

'''
This program compares the performance of
vector clocks and replay clocks
'''

PROC_COUNT = 32

VECCL_COUNTER_WIDTH = 64

REPCL_FIELD_WIDTH = 64
REPCL_INTERVAL = 1
REPCL_EPSILON = 1

repcl = [RepCl(i, REPCL_FIELD_WIDTH, 1, 1) for i in range(PROC_COUNT)]
veccl = [VecCl(i, PROC_COUNT, VECCL_COUNTER_WIDTH) for i in range(PROC_COUNT)]

while True:
    proc_id = random.randint(0, PROC_COUNT - 1)
    other_proc_id = random.randint(0, PROC_COUNT - 1)

    repeat = 5_000
    repcl_time = 0
    veccl_time = 0

    if proc_id == other_proc_id:
        print('local: ', end='')
        for i in range(repeat):
            tmp_repcl = repcl[proc_id]
            tmp_veccl = veccl[proc_id]
            repcl_time += tmp_repcl.send_local()
            veccl_time += tmp_veccl.advance()
    else:
        print('merge: ', end='')
        for i in range(repeat):
            tmp_repcl = repcl[proc_id]
            tmp_veccl = veccl[proc_id]
            repcl_time += tmp_repcl.recv(repcl[other_proc_id])
            veccl_time += tmp_veccl.merge(veccl[other_proc_id])

    print(f'RepCl: {repcl_time / repeat}, VecCl: {veccl_time / repeat}')

    # timeVec = None
    # timeRep = None

    # # if proc_id == other_proc_id:
    # timeRep = repcl[proc_id].send_local()
    # timeVec = veccl[proc_id].advance()
    # #else:
    # #    timeRep = repcl[proc_id].merge(repcl[other_proc_id])
    # #    timeVec = veccl[proc_id].merge(veccl[other_proc_id])

    # print(f"RepCl: {timeRep}, VecCl: {timeVec}")
    time.sleep(0.1)
