import socket
import json
import config
import random
import sqlite3
import base64
import hashlib
import register, get_db
import os
import time

def get_nodes(obj, data):
    with open("nodes.db", 'rb') as file:
        while True:
            x = file.read(100)
            if not x:
                break
            md5sum = hashlib.md5(x).hexdigest()
            out = base64.b64encode(x)
            x = json.dumps({"md5sum":md5sum, "data":out})
            obj.send(x)

def get_nodes_send(god=False):
    node = sqlite3.connect("nodes.db")
    cmd = {"cmd":"get_nodes"}
    if god:
        nodes = config.brokers
    else:
        try:
            nodes = node.execute("SELECT ip, port FROM data WHERE relay=?", [True])
        except sqlite3.OperationalError:
            get_nodes_send(True)
            get_db.get_db_send()
            register.register_send()
            return
        nodes = nodes.fetchall()
    if not nodes:
        return
    random.shuffle(nodes)
    for x in nodes:
        
        s = socket.socket()
        try:
            s.settimeout(120)
            s.connect((x[0], x[1]))
        except:
            s.close()
            continue
        else:
            s.send(json.dumps(cmd))
            out = ""
            current = ""
            no = False
            while True:
                try:
                    data = s.recv(1)
                except:
                    no = True
                    break
                if data:
                    current = current + data
                    if data != "}":
                        continue
                    try:
                        data = json.loads(current)
                    except ValueError:
                        break
                    else:
                        current = ""
                        check = base64.b64decode(data['data'])
                        if hashlib.md5(check).hexdigest() == data['md5sum']:
                            out = out + check
                        else:
                            break
                else:
                    break
            if not no:
                while os.path.exists("nodes.lock"):
                    time.sleep(0.1)
                open("nodes.lock", 'w')
                with open("nodes.db", 'wb') as file:
                    file.write(out)
                os.remove("nodes.lock")
                break
