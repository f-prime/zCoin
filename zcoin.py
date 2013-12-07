import config
import socket
import get_db
import get_version
import get_nodes
import coin_count
import string
import register
import rsa
import random
import thread
import json
import time
import get_difficulty
import check_coin
import send_coin

class zCoin:
    def __init__(self):
        self.cmds = {

            "get_db":get_db.get_db,
            "get_nodes":get_nodes.get_nodes,
            "get_version":get_version.get_version,
            "coin_count":coin_count.coin_count,
            "register":register.register,
            "get_difficulty":get_difficulty.get_difficulty,
            "check_coin":check_coin.check_coin,
            "send_coin":send_coin.send_coin,
            "get_nodes_count":get_nodes.count,
            }

    def firstrun(self):
        print "Generating address..."
        pub, priv = rsa.newkeys(1024)
        address = "Z"+''.join([random.choice(string.uppercase+string.lowercase+string.digits) for x in range(50)])
        print "Your address is: "+address
        print "Getting nodes..."
        get_nodes.send(True)
        check = config.nodes.find("nodes", "all")
        if not check:
            print "It looks like you are the first node on this network."
            ip = raw_input("What is your IP address? ")
            config.nodes.insert("nodes", {"public":str(pub), "address":address, "ip":ip, "relay":config.relay, "port":config.port})
            config.nodes.save()
            config.db.insert("difficulty", {"difficulty":7})
            config.db.save()
        config.wallet.insert("data", {"public":str(pub), "address":address, "private":str(priv)})
        config.wallet.save()
        print "Registering..."
        register.send()
        print "Getting coins db..."
        get_db.send()
        print "Done!"

    def relay(self):
        get_nodes.send()
        register.send()
        get_db.send()
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((config.host, config.port))
        sock.listen(5)
        while True:
            obj, conn = sock.accept()
            thread.start_new_thread(self.handle, (obj, conn[0]))
    def handle(self, obj, ip):
        data = obj.recv(10240)
        if data:
            try:
                data = json.loads(data)
            except:
                obj.close()
                return
            else:
                if "cmd" in data:
                    if data['cmd'] in self.cmds:
                        data['ip'] = ip
                        print data
                        self.cmds[data['cmd']](obj, data)
                        obj.close()

    def normal(self):
        if not config.relay:
            get_db.send()
            register.send()
        while True:
            coin_count.send()
            get_nodes.count_send()
            time.sleep(60)

def run():
    zc = zCoin()
    check = config.nodes.find("nodes", "all")
    if not check:
        zc.firstrun()
    if config.relay:
        print "zCoin started as a relay node."
        thread.start_new_thread(zc.normal, ())
        zc.relay()
    else:
        print "zCoin started as a normal node."
        zc.normal()


if __name__ == "__main__":
    run()
