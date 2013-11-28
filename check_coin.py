import send_command
from rsa import PublicKey, encrypt
import time
import os
import json
import config
import hashlib
import re
import base64

def check_coin(obj, data):
    """

        {"address":<addr>, "hash":<hash>, "starter":starter}

    """
    check = config.db.find("coins", {"hash":data['hash']})
    if check:
        print "Coin already exists."
        return
    check_addr = config.nodes.find("nodes", {"address":data['address']})
    difficulty = config.db.find("coins", "all")
    if not difficulty:
        difficulty = []
    difficulty = len(difficulty)/50500 + 7
    if difficulty < 7:
        difficulty = 7

    if check_addr:
        c = check_addr[0]
        if len(data['hash']) == 128:
            if hashlib.sha512(str(data['starter'])).hexdigest() == data['hash'] and data['hash'].startswith("1"*int(difficulty)):
                key = re.findall("([0-9]*)", c['public'])
                key = filter(None, key)
                key = PublicKey(int(key[0]), int(key[1]))
                data['plain'] = data['starter']
                data['starter'] = base64.b64encode(encrypt(str(data['starter']), key))
                obj.send(json.dumps({"response":"Coin Confirmed!"}))
                while os.path.exists("db.lock"):
                    time.sleep(0.1)
                open("db.lock", 'w').close()
                config.db.insert("coins", {"starter":data['starter'], "hash":data['hash'], "address":data['address'], "difficulty":difficulty})
                config.db.save()
                os.remove("db.lock")
            else:
                print "Invalid Coin!"
        else:
            print "Hash not long enough"
    else:
        print "Addr invalid."
        
