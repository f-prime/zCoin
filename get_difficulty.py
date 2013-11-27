import socket
import json
import sqlite3
import config

def get_difficulty(obj, data):
    node = sqlite3.connect("nodes.db")
    nodes = node.execute("SELECT ip, port FROM data WHERE relay=1 AND version=?", [config.version])
    nodes = nodes.fetchall()
    difficulties = []
    for x in nodes:
        s = socket.socket()
        try:
            s.settimeout(120)
            s.connect((x[0], x[1]))
        except:
            s.close()
            continue
        else:
            s.send(json.dumps({"cmd":"get_raw_difficulty"}))
            data = s.recv(1024)
            if not data:
                s.close()
                continue
            try:
                data = int(data)
            except:
                continue
            else:
                difficulties.append(data)
    out = 0
    for x in difficulties:
        out += x
    try:
        out = out/len(difficulties)
        if out < 7:
            out = 7
    except ZeroDivisionError:
        out = 7
    try: # Without this it will raise an error when check_coin is called.
        obj.send(json.dumps({"difficulty":out}))
    except:
        pass
    return {"difficulty":out}

def get_raw_difficulty(obj, data):
    db = sqlite3.connect("db.db")
    check = db.execute("SELECT level FROM difficulty")
    check = check.fetchall()[0]
    obj.send(str(check[0]))
