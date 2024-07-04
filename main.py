#!/usr/bin/env python3

import random
import time
import socket
import pickle
import math
import os
from repcl import RepCl
from veccl import VecCl
from dotenv import load_dotenv
from message import Message

load_dotenv()

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

# name of the current node
proc_id = int(os.getenv("PROC_ID"))
node_name = os.getenv("NODE_NAME")
list_of_nodes = os.getenv("LIST_OF_NODES").split(",")

print(f'Node {node_name} with id {proc_id} is running')
print(f'List of nodes: {list_of_nodes}')

# use a udp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 3000))  
sock.setblocking(False)   # use non blocking sockets

while True:
    try:
        # receive message if any
        data, addr = sock.recvfrom(2048)

        # Logging time when message was received (in seconds)
        message: Message = pickle.loads(data)

        # update local clock
        # clock.merge(message.clock)
        # print('received', message)
        
        # sent_time = message.clock.epoch * message.clock.interval * 1000  # time msg was sent in seconds

        # print(f"Delay in receipt : {rcv_time - sent_time} seconds")
        
        repclTime = repcl[proc_id].recv(message.repcl)
        vecclTime = veccl[proc_id].merge(message.veccl)

        print(f"Time taken by RepCl to receive from {message.proc_id}: {repclTime}")
        print(f"Time taken by VecCl to receive from {message.proc_id}: {vecclTime}", end="\n\n")
    except Exception as e:
        pass

    try:
        # pick a random node to send to which is not the current node
        other_node = random.choice(list_of_nodes)
        
        if other_node == node_name:
            repclTime = repcl[proc_id].send_local()
            vecclTime = veccl[proc_id].advance()

            print(f"Time taken by RepCl to advance: {repclTime}")
            print(f"Time taken by VecCl to advance: {vecclTime}", end="\n\n")
        else:
            sock.sendto(pickle.dumps(Message(proc_id, repcl[proc_id], veccl[proc_id], f'{node_name} to {other_node}'.encode())), (other_node, 3000))

    except Exception as e:
        pass

    # sleep for 0.8 seconds, which is slightly lesser than the interval.
    # this should give us some events occurring in the same epoch.
    time.sleep(0.8)