import time, requests, pickle, os
from sup_repcl import RepCl
from sup_veccl import VecCl
import numpy as np


INTERVAL = os.getenv('INTERVAL')
EPSILON = os.getenv('EPSILON')
PROC_COUNT = os.getenv('PROC_COUNT')
C_BIT_WIDTH = os.getenv('C_BIT_WIDTH')

masterURL = "http://localhost:5000"
replicaURL = "http://localhost:5001"

file = open("requests.txt", 'r')
req_num = 0
setNum = 1
repcl_time = RepCl(2)
veccl_time = VecCl(2)

for line in file.readlines() :
    req_num += 1
    print(f"Request #{req_num} : ", end = "")
    # alternating receiver node every 4 requests
    if (req_num % 2 == 0) :
        setNum += 1

    # Extracting parameters from the read/write request
    vals = line.split()
    method = vals[0]

    if method == "POST" :
        print("post\n")
        send_data = vals[1]
        
        # checking whether to send to master/replica
        if (setNum % 2 == 1) :
            repcl_time.send_local()
            veccl_time.advance()
            requests.post(masterURL, params = {"data" : send_data}, 
                          files = {"repcl_time" : pickle.dumps(repcl_time), 
                                   "veccl_time" : pickle.dumps(veccl_time)})
        else :
            requests.post(replicaURL, params = {"data" : send_data},
                          files = {"repcl_time" : pickle.dumps(repcl_time),
                                   "veccl_time" : pickle.dumps(veccl_time)})
    
    elif method == 'GET' :
        type = vals[1]
        key = vals[2]
        print(f"{type}\n")

        if type == 'get' :
            if (setNum % 2 == 1) :
                requests.get(masterURL, params = {"uuid_key" : key, "type" : type}, files = {"repcl_time" : pickle.dumps(repcl_time), "veccl_time" : pickle.dumps(veccl_time)})
            else :
                requests.get(replicaURL, params = {"uuid_key" : key, "type" : type}, files = {"repcl_time" : pickle.dumps(repcl_time), "veccl_time" : pickle.dumps(veccl_time)})
        
        elif type == 'put' :
            new_val = vals[3]
            if (setNum % 2 == 1) :
                requests.get(masterURL, params = {"uuid_key" : key, "type" : type, "new_val" : new_val}, files = {"repcl_time" : pickle.dumps(repcl_time), "veccl_time" : pickle.dumps(veccl_time)})
            else :
                requests.get(replicaURL, params = {"uuid_key" : key, "type" : type, "new_val" : new_val}, files = {"repcl_time" : pickle.dumps(repcl_time), "veccl_time" : pickle.dumps(veccl_time)})
        
        elif type == 'delete' :
            if (setNum % 2 == 1) :
                requests.get(masterURL, params ={'type' : type, 'uuid_key': key}, files = {"repcl_time" : pickle.dumps(repcl_time), "veccl_time" : pickle.dumps(veccl_time)})
            else :
                requests.get(replicaURL, params ={'type' : type, 'uuid_key': key}, files = {"repcl_time" : pickle.dumps(repcl_time), "veccl_time" : pickle.dumps(veccl_time)})

    # syncing every 2 requests
    if (req_num % 2 == 0) :
        print("Syncing now....")
        response = requests.get(masterURL, params = {'uuid_key' : None, 'type' : 'sync'})
        print(f"Sync response : {response}")

    
print("Executed all requests!")