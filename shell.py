import send_coin
import sqlite3

class Shell:
    def __init__(self):
        self.cmds = {

                "addr":self.addr,
                "send":self.send,
                "totalcoins":self.totalcoins,
                "coins":self.coins,


        }

    def run(self):
        while True:
            data = raw_input("> ")
            data = data.split()
            if len(data) < 1:
                continue
            if data[0] in self.cmds:
                print self.cmds[data[0]](data[1:])
    
    def addr(self, data):
        data = sqlite3.connect("wallet.db").cursor()
        data.execute("SELECT address FROM data")
        data = data.fetchall()
        return data[0][0]
    
    def send(self, data):
        send_coin.send_coin_send(data[0], data[1])

    def totalcoins(self, data):
        data = sqlite3.connect("db.db").cursor()
        data.execute("SELECT * FROM coins")
        data = data.fetchall()
        return len(data)

    def coins(self, data):
        data = sqlite3.connect("db.db").cursor()
        data.execute("SELECT * FROM coins WHERE address=?", [self.addr("a")])
        data = data.fetchall()
        return len(data)

Shell().run()
