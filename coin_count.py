import config
import json
import send_command
import get_db

def coin_count(obj, data):
    coins = config.db.find("coins", "all")    
    if coins:
        obj.send(json.dumps({"coins":len(coins)}))
    else:
        obj.send(json.dumps({"coins":0}))
    
def send():
    coins = config.db.find("coins", "all")
    if coins:
        coins = len(coins)
    else:
        coins = 0
    out = send_command.send({"cmd":"coin_count"}, out=True)
    try:
        out = json.loads(out)
    except:
        print "Couldn't get number of coins, if this persists please reset."
        return
    else:
        print out
        if out['coins'] > coins:
            get_db.send()


