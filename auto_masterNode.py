'''
Points to note : 
-> Data from the user is formatted as form data
-> Data from the replica is formatted as json data
-> GET requests are serviced from masterData dictionary, not the text file

POST formats : 
user -> master : form   (write data)
replica -> master : json (sync data)
master -> replica : json (sync + write data)

GET formats :
user -> master : form   (read data)
master -> replica : from (fwd read data)

Order of data sent during sync ->
1) Master -> Replica
2) Replica -> Master

So the sync following an update event will result in only the master getting the updated value, 
and replica having the old one (get exchanged) -> TIMESTAMPS REQUIRED HERE

-> Delaying POST and DELETE operations only for now

'''



from flask import Flask, request
import uuid, requests, time, pickle
import json
from repcl import RepCl
from veccl import VecCl

# RUNNING ON PORT 5000

'''
Read -> 0
Write -> 1
Sync -> 2

Data from user stored as -> {UUID : [data, operation]}
POST to replica sent as -> {key : <UUID>, data : <data>}
GET get to replica sent as -> {key : <UUID>, type : "get"}
GET put to replica sent as -> {key : <UUID>, type : "put"}
GET delete to replica sent as -> {key : <UUID>, type : "delete"}

'''

app = Flask(__name__)

# masterData will hold only data sent through POST and PUT requests
masterData = {"known-master-1" : "mas_init_1", 
              "known-master-2"  : "mas_init_2",
              "known-master-3"  : "mas_init_3",
              "known-master-4"  : "mas_init_4"}

# event_logs will hold info about any request that comes in (POST, GET, PUT, DELETE)
event_logs = {}
fwd_flag = 0
sync_count = 0
repcl_time = RepCl(0, 1, 1)
veccl_time = VecCl(0, 3, 64)

def enable_sync() :
    global sync_count
    print("inside sync function")
    sync_count += 1

    # Writing "Before" data to file
    # with open("master.txt", "a") as file :
    #     file.write(f"\n\nBefore sync # {sync_count} : \n")
    #     file.write(json.dumps(event_logs))

    print("Syncing\n")

    # Sending master's event logs to replica in JSON format
    response = requests.post(replica_url, json = {"data" : event_logs})

    #print(f"Master recieved replica logs : {response}")


replica_url = "http://127.0.0.1:5001"

@app.route('/', methods=['GET', 'POST'])
def index() :
    global file, masterData

    # New incoming request -> EITHER FROM USER OR REPLICA NODE
    if request.method == 'POST' :
        try :
            # POST REQUEST FROM REPLICA NODE IN JSON FORMAT (records of all events across both nodes) -> aka sync data
            syncData = request.get_json()["data"]
            for item in syncData.items() :
                # New unseen value
                if item not in masterData.items() :
                    event_logs[item[0]] = item[1]

            # Writing "After" data to file
            with open("master.txt", "w") as file :
                #file.write(f"\n\nAfter sync # {sync_count} : \n")
                file.write(json.dumps(event_logs))
            print("Done syncing\n")
        
        except : 
            # POST REQUEST FROM THE USER
            pickled_repcl = request.files['repcl_time'].read()
            pickled_veccl = request.files['veccl_time'].read()

            sender_repcl = pickle.loads(pickled_repcl)
            sender_veccl = pickle.loads(pickled_veccl)

            repcl_time.recv(sender_repcl)
            veccl_time.merge(sender_veccl)

            data = request.args.get("data")
        
            # Checking whether to forward data or not
            if fwd_flag == 0 :
                # Storing the data on the master node
                # Delaying storing by 3 seconds
                time.sleep(3)
                event_id = str(uuid.uuid1())

                masterData[event_id] = data
                event_logs[event_id] = {"RepTime" : repcl_time.to_dict(),
                                        "VecTime" : veccl_time.to_dict(), 
                                        "action" : 'POST', 
                                        "status" : 'SUC'}
            
            else :
                # Forwarding the post request to replica node
                requests.post(replica_url, json = {"data" : data})
    
    elif request.method == 'GET' :
        event_id = str(uuid.uuid1())

        # Format of getting parameters from  GET request is diff from POST request
        uuid_key = request.args.get("uuid_key")
        type = request.args.get("type")

        if type != "sync" :
            pickled_repcl = request.files['repcl_time'].read()
            pickled_veccl = request.files['veccl_time'].read()

            sender_repcl = pickle.loads(pickled_repcl)
            sender_veccl = pickle.loads(pickled_veccl)

            repcl_time.recv(sender_repcl)
            veccl_time.merge(sender_veccl)

            if type == 'get' :
                # Reading from master node
                if fwd_flag == 0 :
                    if uuid_key in masterData.keys() :
                        status = 'SUC'
                    else :
                        status = 'FAIL'
                    
                    event_logs[event_id] = {"RepTime" : repcl_time.to_dict(),
                                            "VecTime" : veccl_time.to_dict(), 
                                            "action" : 'GET', 
                                            "status" : status}
                
                # Forwarding read operation to replica node
                else :
                    requests.get(replica_url, params={'type' : type, 'uuid_key': uuid_key})
        
            elif type == 'put' :
                new_val = request.args.get("new_val")
            
                if fwd_flag == 0 :
                # Updating in master
                    if uuid_key in masterData.keys() :
                        masterData[uuid_key] = new_val
                        status = 'SUC'
                    else :
                        status = 'FAIL'

                    # timestamping after the put operation
                    event_logs[event_id] = {"RepTime" : repcl_time.to_dict(),
                                            "VecTime" : veccl_time.to_dict(), 
                                            "action" : 'PUT', 
                                            "status" : status}          
          
                else :
                    # Forwarding update operation to replica
                    requests.get(replica_url, params = {'type' : type, 'uuid_key' : uuid_key, 'new_val' : new_val})

            elif type == 'delete' :
                # Deleting from master node
                if fwd_flag == 0 :
                    if uuid_key in masterData.keys() :
                        del_val = masterData.pop(uuid_key)
                        status = 'SUC'
                    
                    else :
                        status = 'FAIL'
                    event_logs[event_id] = {"RepTime" : repcl_time.to_dict(),
                                            "VecTime" : veccl_time.to_dict(), 
                                            "action" : 'DEL', 
                                            "status" : status}
                
                # Forwarding delete operation to replica node
                else :
                    requests.get(replica_url, params={'type' : type, 'uuid_key': uuid_key})
            
        else :
            enable_sync()

    return '''
        This is the master node
    '''


if __name__ == '__main__':
    app.run(debug=False)