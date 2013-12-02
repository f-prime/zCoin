import config
import json
from rsa import *
import base64
import re
import hashlib
import os
import time
import send_command
import hashlib
import uuid

def send(address, amount):

    """

        {"cmd":"send_coin", "for":<address>, "hash":<hash>, "starter":<encrypted new one>}

    """

    amount = int(amount)
    check = config.nodes.find("nodes", {"address":address})
    if not check:
        print "Address does not exist"    
    else:
        check = check[0]
        my_key = config.wallet.find("data", "all")[0]
        my_address = my_key['address']
        my_key = my_key['private']
        key = check['public']
        key = re.findall("([0-9]*)", key)
        key = filter(None, key)
        key = PublicKey(int(key[0]), int(key[1]))
        my_key = re.findall("([0-9]*)", my_key)
        my_key = filter(None, my_key)
        my_key = PrivateKey(int(my_key[0]), int(my_key[1]), int(my_key[2]), int(my_key[3]), int(my_key[4]))
        cc = config.db.find("coins", {"address":my_address})
        if len(cc) < amount:
            print "You have insufficient funds."
            return
        cc = cc[:amount]
        transactionid = uuid.uuid4().hex
        sent_ = 0
        for x in cc:
            starter, hash_ = x['starter'], x['hash']
            starter = base64.b64encode(encrypt(decrypt(base64.b64decode(starter), my_key), key))
            out_s = {'cmd': 'send_coin',
                    'for': address,
                    "transid":transactionid,
                    'starter': starter,
                    'hash': hash_,
                    "from":my_address,
                    "amount_sent":amount,
                    "plain":x['starter'],
                    "difficulty":x['difficulty'],
                    }

            send_command.send(out_s)
            sent_ += 1
            print str(sent_)+" coins sent to "+address
        print "Coins sent!"


def send_coin(obj, data):
    if not config.db.find("transactions", {"transid":data['transid']}):
        config.db.insert("transactions", {"to":data['for'], "from":data['from'], "amount":data['amount_sent'], "transid":data['transid']})
        while os.path.exists("db.lock"):
            time.sleep(0.1)
        open("db.lock", 'w').close()
        config.db.save()
        os.remove("db.lock")
    while os.path.exists("db.lock"):
        time.sleep(0.1)
    open("db.lock", 'w').close()
    check = config.db.find("coins", {"hash":data['hash']})
    for x in check:
        config.db.remove("coins", x)
        config.db.save()
    config.db.insert("coins",{"address":data['for'], "starter":data['starter'], "hash":data['hash'], "difficulty":data['difficulty']})
    config.db.save()
    os.remove("db.lock")

