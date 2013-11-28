import send_command
import config
import random
import string
import json
from hashlib import sha512

def mine():
    starter = ''.join([random.choice(string.uppercase+string.lowercase+string.digits) for x in range(5)])    
    diff = send_command.send({"cmd":"get_difficulty"}, out=True)
    diff = json.loads(diff)['difficulty']
    on = 0
    while True:
        check = starter + str(on)
        print check
        if sha512(check).hexdigest().startswith("1"*diff):
            send_command.send({"cmd":"check_coin", "address":config.wallet.find("data", "all")[0]['address'], "starter":starter+str(on), "hash":sha512(check).hexdigest()})
            break
        else:
            on += 1
    mine()

mine()
