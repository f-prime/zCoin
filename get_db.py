import socket
import json
import config
import random
import sqlite3

def get_db(obj, data):
    db = sqlite3.connect("db.db").cursor()
    db.execute("CREATE TABLE IF NOT EXISTS difficulty (level INT default 7)")
    db.execute("CREATE TABLE IF NOT EXISTS coins (hash TEXT, address TEXT, starter TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS transactions (to_ TEXT, from_ TEXT, hash TEXT)")
    with open("db.db", 'rb') as file:
        for x in file.readlines(1020):
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
            while True:
                data = s.recv(1024)
                if data:
                    out = out + data
                else:
                    break
            
            with open("db.db", 'wb') as file:
                file.write(out)
