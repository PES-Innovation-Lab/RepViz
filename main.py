#!/usr/bin/env python3

'''
This program is meant to be run twice.
It simulates two processes talking to each other.
'''

import sys
import time
import math
import socket
import pickle
import random
from repcl import RepCl
from message import Message

if len(sys.argv) != 4:
    print(f'usage: python3 {sys.argv[0]} this_proc_id other_proc_id')
    exit(0)

proc_id = int(sys.argv[1])
other_proc_id = int(sys.argv[2])
other_domain = sys.argv[3]

# interval is 1 seconds so its easier to keep track in real time
clock = RepCl(proc_id=proc_id, interval=1000, epsilon=math.inf)
print(clock)

# use a udp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', proc_id))  # use proc_id as port
sock.setblocking(False)   # use non blocking sockets

while True:
    try:
        # receive message if any
        data, addr = sock.recvfrom(2048)
        message: Message = pickle.loads(data)

        # update local clock
        clock.merge(message.clock)
        print('received', message)
    except BlockingIOError as e:
        pass

    try:
        # 80% chance a local event happens
        if random.randint(1, 100) < 80:
            clock.advance()
            print('local event at', clock)

        # 50% chance we send a message
        if random.randint(1, 100) < 50:
            clock.advance()
            sock.sendto(pickle.dumps(Message(clock, f'{proc_id} to {other_proc_id}'.encode())), (other_domain, other_proc_id))
    except Exception as e:
        pass

    # sleep for 0.8 seconds, which is slightly lesser than the interval.
    # this should give us some events occurring in the same epoch.
    time.sleep(0.8)
