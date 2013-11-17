import socket
import hashlib
import json
import random
import string
import sqlite3

def check_difficulty():
    db = sqlite3.connect("nodes.db")
    find = db.execute("SELECT ip, port FROM data WHERE relay=?", [True])
    find = find.fetchall()
    random.shuffle(find)
    for x in find:
        s = socket.socket()
        try:
            s.settimeout(1)
            s.connect((x[0], x[1]))
        except:
            s.close()
            continue
        else:
            s.send(json.dumps({"cmd":"get_difficulty"}))
            data = s.recv(1024)
            print data
            try:
                data = json.loads(data)
            except:
                continue
            s.close()
            return data
        s.close()

def check_coin(data):
    node = sqlite3.connect("nodes.db")
    node = node.execute("SELECT ip, port FROM data WHERE relay=?", [True]) 
    node = node.fetchall()
    random.shuffle(node)
    for x in node:
        s = socket.socket()
        try:
            s.settimeout(1)
            s.connect((x[0], x[1]))
        except:
            s.close()
            continue
        else:
            data['cmd'] = "check_coin"
            print data
            s.send(json.dumps(data))
        s.close()

def mine():
    while True:
        check = check_difficulty()
        starter = ''.join([random.choice(string.uppercase+string.lowercase+string.digits) for x in range(5)])
        on = 0
        while True:
            c = hashlib.sha512(starter+str(on)).hexdigest()
            startswith = "1"*check['difficulty']
            if c.startswith(startswith):
                print c
                wall = sqlite3.connect("wallet.db")
                address = wall.execute("SELECT address FROM data")
                address = address.fetchall()[0][0]
                check_coin({"starter":starter+str(on), "hash":c, "address":address})
                break
            else:
                on += 1
mine()
