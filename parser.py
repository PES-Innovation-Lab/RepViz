from sup_repcl import RepCl
from sup_veccl import VecCl
import json
import numpy as np


file = open("master.txt", "r")
all_events = []

# file.read() -> single json object of the event_logs dictionary
event_logs = json.loads(file.read())

for event_id, info in event_logs.items() :
    rep_dict = info['RepTime']
    #vec_dict = info['VecTime']

    # Creating a RepCl object (to be able to compare RepCl timestamps)
    rep_obj = RepCl(int(rep_dict['proc_id']))
    rep_obj.hlc = np.uint64(rep_dict['hlc'])
    rep_obj.offset_bmp = np.uint64(rep_dict['offset_bmp'])
    rep_obj.offsets = np.uint64(rep_dict['offsets'])
    rep_obj.counters = np.uint64(rep_dict['counters'])

    all_events.append((event_id, rep_obj))

print("Before sorting : \n")
for i in all_events :
    print(i[0])
    print(i[1])
    print()

# Sorting the events based on RepCl timestamps
print("After sorting : \n")
all_events.sort(key = lambda e : e[1])

for i in all_events :
    print(i[0])
    print(i[1])
    print()


    


