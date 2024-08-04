import json
from sup_repcl import RepCl
import numpy as np

def parser(fileName) :
    file = open(fileName, "r")
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

    all_events.sort(key = lambda e : e[1])

    with open("/data/RepClSizes.txt", 'a') as store :
        store.write(str(all_events[-1][1].GetClockSize()) + "\n")
    
    with open("/client-host/RepClSize.txt", 'a') as store :
        store.write(str(all_events[-1][1].GetClockSize()) + "\n")

    file.close()    
