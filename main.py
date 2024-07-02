#!/usr/bin/env python3

import time
import math
import socket
import pickle
import random
from repcl import RepCl
from message import Message
from dotenv import load_dotenv
import os 

load_dotenv()

# name of the current node
proc_id = int(os.getenv("PROC_ID"))
node_name = os.getenv("NODE_NAME")
list_of_nodes = os.getenv("LIST_OF_NODES").split(",")

print(f'Node {node_name} with id {proc_id} is running')
print(f'List of nodes: {list_of_nodes}')

# interval is 1 seconds so its easier to keep track in real time
clock = RepCl(proc_id=proc_id, interval=1000, epsilon=math.inf)
print(clock)

# use a udp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 8080))  
sock.setblocking(False)   # use non blocking sockets

while True:
    try:
        # receive message if any
        data, addr = sock.recvfrom(2048)

        # Logging time when message was received (in seconds)
        rcv_time = time.time()
        message: Message = pickle.loads(data)

        # update local clock
        clock.merge(message.clock)
        print('received', message)
        sent_time = message.clock.epoch * message.clock.interval * 1000  # time msg was sent in seconds

        print(f"Delay in receipt : {rcv_time - sent_time} seconds")
        
    except BlockingIOError as e:
        pass

    try:
        # pick a random node to send to which is not the current node
        other_node = random.choice(list_of_nodes)
        
        if other_node == node_name:
            clock.advance()
            print('local event at', clock)
        else:
            # send a message to the other node
            sock.sendto(pickle.dumps(Message(clock, f'{node_name} to {other_node}'.encode())), (other_node, 8080))

    except Exception as e:
        pass

    # sleep for 0.8 seconds, which is slightly lesser than the interval.
    # this should give us some events occurring in the same epoch.
    time.sleep(0.8)
