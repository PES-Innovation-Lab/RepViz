#!/usr/bin/env python3

from repcl import RepCl
from veccl import VecCl

'''
This program compares the performance of
vector clocks and replay clocks
'''

PROC_COUNT = 8

VECCL_COUNTER_WIDTH = 8

REPCL_FIELD_WIDTH = 64
REPCL_INTERVAL = 1
REPCL_EPSILON = 1

repcl = RepCl(0, PROC_COUNT, REPCL_FIELD_WIDTH, REPCL_INTERVAL, REPCL_EPSILON)
# veccl = VecCl(0, PROC_COUNT, VECCL_COUNTER_WIDTH)
