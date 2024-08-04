from flask import Flask, request
import uuid, requests, time, pickle, json, os
from sup_repcl import RepCl
from sup_veccl import VecCl
import numpy as np


# RUNNING ON PORT 5001

'''
Read -> 0
Write -> 1
Sync -> 2
'''


app = Flask(__name__)

replicaData = {"known-replica-1" : "rep_init_1", 
              "known-replica-2"  : "rep_init_2",
              "known-replica-3"  : "rep_init_3",
              "known-replica-4"  : "rep_init_4"}
event_logs = {}
sync_count = 0
repcl_time = RepCl(1)
veccl_time = VecCl(1)

master_url = "http://master-service.default.svc.cluster.local"

@app.route('/', methods=['GET', 'POST'])
def index() :
    global sync_count
    # New incoming request from MASTER NODE
    if request.method == 'POST' :

        # Checking if data (sync data) is from master (in JSON format)
        try :
            syncData = request.get_json()["data"]
            sync_count += 1

            # Writing "Before" data to file
            # with open("replica.txt", "a") as file :
            #     file.write(f"\n\nBefore sync # {sync_count} : \n")
            #     file.write(json.dumps(event_logs))

            print("\nSyncing\n")

            # Sending replicaData before updating (to reduce sending repeating data)
            requests.post(master_url, json = {"data" : event_logs})

            # Updating replicaData with masterData
            for item in syncData.items() :
                # New unseen value
                if item not in replicaData.items() :
                    event_logs[item[0]] = item[1]

            # Writing "After" data to file
            with open("/data/replica.txt", "w") as file :
                #file.write(f"\n\nAfter sync # {sync_count} : \n")
                file.write(json.dumps(event_logs))
            
            print("\nDone Syncing\n")
    
        # data is from client (in FORM format)
        except :
            pickled_repcl = request.files['repcl_time'].read()
            pickled_veccl = request.files['veccl_time'].read()

            sender_repcl = pickle.loads(pickled_repcl)
            sender_veccl = pickle.loads(pickled_veccl)

            repcl_time.recv(sender_repcl)
            veccl_time.merge(sender_veccl)

            # Writing data
            userData = request.args.get("data")
            event_id = str(uuid.uuid1())
            replicaData[event_id] = [userData]
            
            event_logs[event_id] = {"RepTime" : repcl_time.to_dict(),
                                    "VecTime" : veccl_time.to_dict(), 
                                    "action" : 'POST', 
                                    "status" : 'SUC'}
        
    elif request.method == 'GET' :
        event_id = str(uuid.uuid1())
        uuid_key = request.args.get("uuid_key")
        type = request.args.get("type")

        pickled_repcl = request.files['repcl_time'].read()
        pickled_veccl = request.files['veccl_time'].read()

        sender_repcl = pickle.loads(pickled_repcl)
        sender_veccl = pickle.loads(pickled_veccl)

        repcl_time.recv(sender_repcl)
        veccl_time.merge(sender_veccl)

        # get request
        if (type == 'get') :
            if uuid_key in replicaData.keys() :
                status = 'SUC'
            else :
                status = 'FAIL'

            event_logs[event_id] = {"RepTime" : repcl_time.to_dict(),
                                    "VecTime" : veccl_time.to_dict(), 
                                    "action" : 'GET', 
                                    "status" : status}
        # put request
        elif type == 'put' :

            if uuid_key in replicaData.keys() :
                new_val = request.args.get("new_val")
                replicaData[uuid_key] = new_val
                status = 'SUC'
            else :
                status = 'FAIL'
            event_logs[event_id] = {"RepTime" : repcl_time.to_dict(),
                                    "VecTime" : veccl_time.to_dict(), 
                                    "action" : 'PUT', 
                                    "status" : status}

        # delete request
        elif type == 'delete' :
            # Deleting from replica node
            # Delaying for 3 seconds before the deletion
            time.sleep(3)
            if uuid_key in replicaData.keys() :
                replicaData.pop(uuid_key)
                status = 'SUC'
            else :
                status = 'FAIL'
            event_logs[event_id] = {"RepTime" : repcl_time.to_dict(),
                                    "VecTime" : veccl_time.to_dict(), 
                                    "action" : 'DEL', 
                                    "status" : status}

    return'''
    This is the replica node
    '''
    
if __name__ == '__main__':
    app.run(debug = False, host='0.0.0.0', port = 5001)