import socket
import json
from rsa import *
import random
import get_nodes
import get_db
import register
import sqlite3
import config
import time
import thread
import string
import get_difficulty
import check_coin
import send_coin
import get_version
import sys

class zCoin:
    def __init__(self):
        self.cmds = {

                "register":register.register,
                "get_nodes":get_nodes.get_nodes,
                "get_db":get_db.get_db,
                "get_difficulty":get_difficulty.get_difficulty,
                "get_raw_difficulty":get_difficulty.get_raw_difficulty,
                "check_coin":check_coin.check_coin,
                "confirm_coin":check_coin.confirm_coin,
                "send_coin":send_coin.send_coin,
                "get_version":get_version.get_version,
        }   

    def first_run(self):
        print "Generating address..."
        pub, priv = newkeys(1024)
        address = "Z"+''.join([random.choice(string.uppercase+string.lowercase+string.digits) for x in range(50)])
        print "Your address is "+address
        wallet = sqlite3.connect("wallet.db")
        db = sqlite3.connect("db.db")
        nodes = sqlite3.connect("nodes.db")
        nodes.execute("CREATE TABLE IF NOT EXISTS data (address TEXT, relay INT, port INT,  public TEXT, ip TEXT, version TEXT)")
        db.execute("CREATE TABLE IF NOT EXISTS difficulty (level INT)")
        db.execute("CREATE TABLE IF NOT EXISTS  coins (starter TEXT, address TEXT, hash TEXT)")
        db.execute("CREATE TABLE IF NOT EXISTS transactions (to_ TEXT, from_ TEXT, hash TEXT)")
        db.execute("INSERT INTO difficulty (level) VALUES (7)")
        db.commit()
        wallet.execute("CREATE TABLE data (public TEXT, private TEXT, address TEXT)")
        wallet.execute("INSERT INTO data (public, private, address) VALUES (?, ?, ?)", [str(pub), str(priv), address])
        wallet.commit()
        print "Registering with broker node..."
        register.register_send(True) 
        print "Retrieving nodes db..."
        get_nodes.get_nodes_send(True)
        print "Retrieving coins db..."
        get_db.get_db_send()
        print "Syncing with network..."
        register.register_send()
        print "Done!"

    def handle(self, obj, ip):
        data = obj.recv(10240)
        if data:
            try:
                data = json.loads(data)
            except ValueError:
                return
            else:
                print data
                data['ip'] = ip
                if "cmd" in data:
                    if data['cmd']  in self.cmds:
                        self.cmds[data['cmd']](obj, data)
        obj.close()

    def relay(self):
        print "zCoin has started as a relay node"
        nodes = sqlite3.connect("nodes.db")
        cur = nodes.cursor()
        cur.execute("SELECT * FROM data")
        if not cur.fetchall(): #This must mean that it is the first node, thus it is a god node.
            wallet = sqlite3.connect("wallet.db").cursor()
            print "\nIt seems as though you are trying to run as the first God node in the network."
            ip = raw_input("\nJust to be safe, give me the IP address of this node: ")
            port = config.port
            relay = 1
            wallet.execute("SELECT address, public FROM data")
            out = wallet.fetchall()
            address = out[0][0]
            public = out[0][1]
            nodes.execute("INSERT INTO data (address, ip, port, public, relay, version) VALUES (?, ?, ?, ?, ?, ?)", [address, ip, port, public, relay, config.version])
            nodes.commit()
            print "All good"
        
        get_nodes.get_nodes_send()
        get_db.get_db_send()
        register.register_send()
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((config.host, config.port))
        sock.listen(5)
        while True:
            obj, conn = sock.accept()
            thread.start_new_thread(self.handle, (obj, conn[0]))

    def non_relay(self):
        while True:
            get_nodes.get_nodes_send()
            get_db.get_db_send()
            time.sleep(60)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-fixdb":
            get_nodes.get_nodes_send(god=True)
            get_db.get_db_send()
    update = False
    try:
        check = get_version.get_version_send()
        if check['version'] != config.version:
            print "Your version of zCoin is out of date. Please download the latest verion of zCoin from Github."
            update = True
    except:
        print "Couldn't get current zCoin version from any of the brokers, they all must be down. I suggest you restart your client in a bit to check again."
    if not update:
        wallet = sqlite3.connect("wallet.db").cursor()
        try:
            wallet.execute("SELECT * FROM data")
        except:
            zCoin().first_run()
        if config.relay:
            register.register_send()
            thread.start_new_thread(zCoin().non_relay, ())
            zCoin().relay()
        else:
            print "zCoin has started as a normal node."
            register.register_send()
            zCoin().non_relay()
