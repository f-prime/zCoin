import config
import sys
import socket
import json

def get_version_send():
    nodes = config.brokers
    for x in nodes:
        s = socket.socket()
        try:
            s.settimeout(120)
            s.connect((x[0], x[1]))
        except:
            s.close()
            continue
        else:
            s.send(json.dumps({"cmd":"get_version"}))
            data = s.recv(1024)
            try:
                data = json.loads(data)
            except ValueError:
                s.close()
                continue
            else:
                return data

def get_version(obj, data):
    obj.send(json.dumps({"version":config.version}))

