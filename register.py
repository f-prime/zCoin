import json
import socket
import config
import random
import sqlite3
import get_nodes, get_db
import os
import time

def register(obj, data):
    while os.path.exists("nodes.lock"):
        time.sleep(0.1)
    open("nodes.lock", 'w')
    check = sqlite3.connect("nodes.db") 
    c = check.execute("SELECT * FROM data WHERE address=?", [data['address']])
    if c.fetchall():
        check.execute("UPDATE data SET relay=?, ip=?, port=?, public=?, version=? WHERE address=?", [data['relay'], data['ip'], data['port'], data['address'], data['public'], data['version']])
    else:
        check.execute("INSERT INTO data (address, ip, port, relay, public, version) VALUES (?, ?, ?, ?, ?, ?)", [data['address'], data['ip'], data['port'], data['relay'], data['public'], data['version']])
    check.commit()
    os.remove("nodes.lock")

def register_send(god=False):
    node = sqlite3.connect("nodes.db")
    wallet = sqlite3.connect("wallet.db")
    data = wallet.execute("SELECT address, public FROM data")
    data = data.fetchall()[0]
    cmd = {"cmd":"register", "address":data[0], "public":data[1], "port":config.port, "relay":config.relay, "version":config.version}
    try:
        nodes = node.execute("SELECT ip, port FROM data WHERE relay=?", [True])
    except sqlite3.OperationalError:
        get_nodes.get_nodes_send(True)
        get_db.get_db_send()
        register_send()
        return
    nodes = nodes.fetchall()
    if god:
        nodes = config.brokers
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
        s.close()

