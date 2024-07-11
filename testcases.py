import copy
import random
from repcl import RepCl

random.seed(42)

TOTAL_PROC_COUNT = 64
PROC_COUNT = 8
REPCL_INTERVAL = 1000
REPCL_EPSILON = 4

# always include pid 0, we shall observe it closely
pids = [0] + random.sample(range(1, TOTAL_PROC_COUNT), k=PROC_COUNT-1)

# create repcls and the physical clocks
repcls = {pid: RepCl(pid, 0, REPCL_INTERVAL, REPCL_EPSILON) for pid in pids}
phy_clocks = {pid: 0 for pid in pids}

# move time forward by dt for all processes, with a random skew up of to `skew`
def delay(dt, skew):
    global phy_clocks
    for pid in pids:
        phy_clocks[pid] += dt + random.randint(0, skew)

# increment clock on a local event
def local(pid):
    global repcls
    repcls[pid].send_local(phy_clocks[pid])

# send a message (store the return value in a variable and use it to receive at a later point in time)
def send(pid):
    local(pid)
    return copy.deepcopy(repcls[pid])

# receive a message returned by the `send` function
def recv(dest, src):
    repcls[dest].recv(src, phy_clocks[dest])

# hardcoded sim
print(repcls[pids[0]])
delay(2000, 500)
print(repcls[pids[0]])
local(pids[0])
print(repcls[pids[0]])
local(pids[2])
local(pids[4])
msg = send(pids[4])
print(repcls[pids[4]])
local(pids[7])
delay(2000, 500)
print(repcls[pids[0]])
recv(pids[0], msg)
print(repcls[pids[0]])
