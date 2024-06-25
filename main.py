import math
from repcl import RepCl

# create an instance of RepCl
clock = RepCl(proc_id=0, interval=1, epsilon=math.inf)
print(clock)
