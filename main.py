import math
from repcl import RepCl

# create an instance of RepCl
clock1 = RepCl(proc_id=0, interval=1, epsilon=math.inf)
clock2 = RepCl(proc_id=0, interval=1, epsilon=math.inf)

print(clock1)
clock1.merge(clock2)
print(clock1)
