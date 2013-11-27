import socket
import sqlite3
import json
from rsa import *
import base64
import re
import hashlib
import config
import os
import time

def send_coin_send(address, amount):
    """
        
        send as
    
        {"cmd":"send_coin", "for":<address>, "hash":<hash>, "starter":<encrypted new one>}
    
    """
    amount = int(amount)
    db = sqlite3.connect("db.db").cursor()
    wallet = sqlite3.connect('wallet.db')
    nodes = sqlite3.connect('nodes.db').cursor()
    nodes.execute("SELECT public FROM data WHERE address=?", [address])
    check = nodes.fetchall()
    nodes.execute('SELECT ip, port FROM data WHERE relay=1')
    node = nodes.fetchall()
    if check[0][0]:
        my_key = wallet.execute('SELECT private, address FROM data')
        my_key = my_key.fetchall()[0]
        my_address = my_key[1]
        my_key = my_key[0]
        key = check[0][0]
    
        if key.startswith('PublicKey(') and key.endswith(')'):
            key = re.findall("([0-9]*)", key)
            key = filter(None, key)
            try:
                for x in key:
                    int(x)
            except:
                return "Address has an invalid PublicKey"

            key = PublicKey(int(key[0]), int(key[1]))
            
            my_key = re.findall("([0-9]*)", my_key)
            my_key = filter(None, my_key)
            my_key = PrivateKey(int(my_key[0]), int(my_key[1]), int(my_key[2]), int(my_key[3]), int(my_key[4]))
            check_coins = db.execute('SELECT starter, hash FROM coins WHERE address=?', [my_address])
            check_coins = check_coins.fetchall()
            if len(check_coins) < amount:
                return 'You have insufficient funds.'
            check_coins = check_coins[:amount]
            for x in check_coins:
                starter, hash_ = x[0], x[1]
                starter = base64.b64encode(encrypt(decrypt(base64.b64decode(starter), my_key), key))
                out = {'cmd': 'send_coin',
                 'for': address,
                 'starter': starter,
                 'hash': hash_}
                if not send_coin_do(out):
                    continue
                else:
                    return "You have invalid coins"
            return "Coins sent successfully!"
        else:
            return "Invalid Key"
    else:
        return "Address does not exist"


def send_coin_do(out):
    node = sqlite3.connect('nodes.db').cursor()
    to_send = json.dumps(out)
    node.execute('SELECT ip, port FROM data WHERE relay=1')
    nodes = node.fetchall()
    if not nodes:
        return
    for x in nodes:
        s = socket.socket()
        try:
            s.settimeout(120)
            s.connect((x[0], x[1]))
        except:
            s.close()
            continue
        else:
            s.send(to_send)

        s.close()


def send_coin(obj, data):
    
    while os.path.exists("db.lock"):
        time.sleep(0.1)
    open("db.lock", 'w')
    db = sqlite3.connect('db.db')
    db.execute('UPDATE coins SET address=?, starter=? WHERE hash=?', [data['for'], data['starter'], data['hash']])
    db.execute("INSERT INTO transactions (to_, from_, hash) VALUES (?, ?, ?)", [data['for'], data['starter'], data['hash']])
    db.commit()
    os.remove("db.lock")
