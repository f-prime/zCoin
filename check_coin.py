import get_difficulty
import socket
import json
from rsa import *
import hashlib
import base64
import sqlite3
import config
import re
import os
import time

def check_coin(obj, data):
    """
    
        {"address":<addr>, "hash":<hash>, "starter":<starter>}

    """
    check = sqlite3.connect("db.db").cursor()
    check.execute("SELECT * FROM coins WHERE hash=?", [data['hash']])
    if check.fetchall():
        print "Coin already exists"
        return
    node = sqlite3.connect("nodes.db").cursor()
    c = node.execute("SELECT public FROM data WHERE address=?", [data['address']])
    c = c.fetchall()
    check.execute("SELECT level FROM difficulty")
    difficulty = check.fetchall()[0][0]
    if c:
        c = c[0]
        if len(data['hash']) == 128:
            if hashlib.sha512(str(data['starter'])).hexdigest() == data['hash'] and data['hash'].startswith("1"*int(difficulty)):
                if c[0].startswith("PublicKey(") and c[0].endswith(")"):
                    key = re.findall("([0-9]*)", c[0])
                    key = filter(None, key)
                    key = PublicKey(int(key[0]), int(key[1]))
                data['plain'] = data['starter']
                data['starter'] = base64.b64encode(encrypt(str(data['starter']), key))
                obj.send(json.dumps({"response":"Coin Confirmed!"}))
                try:
                    out = sqlite3.connect("db.db").cursor()
                    out.execute("SELECT * FROM coins")
                    data['difficulty'] = len(out.fetchall())/205000 + 7
                except TypeError:
                    data['difficulty'] = 7
                send_confirm(data)
            else:
                obj.send(json.dumps({"response":"Invalid Coin!"}))
        

def send_confirm(data):
    nodes = sqlite3.connect("nodes.db").cursor()
    nodes = nodes.execute("SELECT ip, port FROM data WHERE relay=1 AND version=?", [config.version])
    nodes = nodes.fetchall()
    for x in nodes:
        s = socket.socket()
        try:
            s.settimeout(120)
            s.connect((x[0], x[1]))
        except:
            continue
        else:
            data['cmd'] = "confirm_coin"
            s.send(json.dumps(data))
        s.close()

def confirm_coin(obj, data):
    db_ = sqlite3.connect("db.db")
    db = db_.cursor()
    check = sqlite3.connect("db.db").cursor()
    check.execute("SELECT level FROM difficulty")
    difficulty = check.fetchall()[0][0]
    db.execute("SELECT * FROM coins WHERE hash=?", [data['hash']])
    if data['hash'].startswith("1"*int(difficulty)) and len(data['hash']) == 128 and not db.fetchall() and hashlib.sha512(data['plain']).hexdigest() == data['hash']:
        while os.path.exists("db.lock"):
            time.sleep(0.1)
        open("db.lock", 'w')
        db_.execute("UPDATE difficulty SET level=? WHERE level=?", [data['difficulty'], difficulty])
        db_.execute("INSERT INTO coins (starter, hash, address) VALUES (?, ?, ?)", [data['starter'], data['hash'], data['address']])
        db_.commit()
        os.remove("db.lock")
    else:
        return

