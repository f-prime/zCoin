import socket
import json
import config
import random
import sqlite3
import base64
import hashlib

def get_db(obj, data):
    db = sqlite3.connect("db.db").cursor()
    db.execute("CREATE TABLE IF NOT EXISTS difficulty (level INT default 7)")
    db.execute("CREATE TABLE IF NOT EXISTS coins (hash TEXT, address TEXT, starter TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS transactions (to_ TEXT, from_ TEXT, hash TEXT)")
    with open("db.db", 'rb') as file:
        while True:
            x = file.read(100)
            if not x:
                break
            md5sum = hashlib.md5(x).hexdigest()
            out = base64.b64encode(x)
            x = json.dumps({"md5sum":md5sum, "data":out})
            obj.send(x)

def get_db_send():
    node = sqlite3.connect("nodes.db")
    cmd = {"cmd":"get_db"}
    nodes = node.execute("SELECT ip, port FROM data WHERE relay=?", [True])
    if not nodes:
        return
    nodes = nodes.fetchall()
    random.shuffle(nodes)
    for x in nodes:
        
        s = socket.socket()
        try:
            s.settimeout(1)
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
                with open("db.db", 'wb') as file:
                    file.write(out)
