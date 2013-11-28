import socket
import json
import config
import os
import time

def register(obj, data):
    while os.path.exists("nodes.lock"):
        time.sleep(0.1)
    open("nodes.lock",'w').close()
    stuff = config.nodes.find("nodes", {"address":data['address']})
    if stuff:
        for x in stuff:
            config.nodes.remove("nodes", x)
            config.nodes.save()
    config.nodes.insert("nodes", data)
    config.nodes.save()
    os.remove("nodes.lock")

def send():
    nodes = config.nodes.find("nodes", {"relay":1})
    for x in nodes:
        s = socket.socket()
        try:
            s.connect((x['ip'], x['port']))
        except:
            continue
        else:
            s.send(json.dumps({"cmd":"get_version"}))
            data = s.recv(1024)
            s.close()
            if data == config.version:
                s = socket.socket()
                try:
                    s.connect((x['ip'], x['port']))
                except:
                    continue
                else:
                    data = config.wallet.find("data", "all")[0]
                    s.send(json.dumps({"cmd":"register", "relay":config.relay, "public":data['public'], "address":data['address'], "port":config.port}))
                    s.close()
                    break
            else:
                s.close()
