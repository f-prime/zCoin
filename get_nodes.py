import socket
import json
import config
import random
import sqlite3

"""

Added: 11/16/13 12:08 AM

This is the code for the "get_nodes" command, a command that will send or retrieve the global database of nodes.

{"cmd":"get_nodes"}

"""

def get_nodes(obj, data):
    with open("nodes.db", 'rb') as file:
        for x in file.readlines(1020):
            obj.send(x)

def get_nodes_send(god=False):
    node = sqlite3.connect("nodes.db")
    cmd = {"cmd":"get_nodes"}
    nodes = node.execute("SELECT ip, port FROM data WHERE relay=?", [True])
    nodes = nodes.fetchall()
    if god:
        nodes = config.brokers
    if not nodes:
        return
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

            
            with open("nodes.db", 'wb') as file:
                file.write(out)
