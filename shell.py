import cmd
import sqlite3
import send_coin
import get_nodes
import get_db
import urllib

class zCoinShell(cmd.Cmd):
    prompt = "zShell$ "
    intro = "\nWelcome to the zCoin Shell for help type 'help'"    
    def do_coins(self, line):
        coins = sqlite3.connect("db.db").cursor()
        coins.execute("SELECT * FROM coins WHERE address=?", [self.addr()])
        try:
            print "You have "+str(len(coins.fetchall())) + " coins."
        except sqlite3.DatabaseError:
            self.do_fixdb(None)
            self.do_coins(None)

    def do_transactions(self, line):
        coins = sqlite3.connect("db.db").cursor()
        coins.execute("SELECT to_, from_, hash FROM transactions WHERE to_=?", [line])
        for x in coins.fetchall():
            print "\nTo: "+x[0]
            print "Coin: "+x[2]

    def do_totalcoins(self, line):
        coins = sqlite3.connect("db.db").cursor()
        coins.execute("SELECT * FROM coins")
        try:
            print "There are "+str(len(coins.fetchall()))+" coins in existence."
        except sqlite3.DatabaseError:
            self.do_fixdb(None)
            self.do_totalcoins(None)
    def do_fixdb(self, line):
        print "Fixing your broken databases..."
        get_nodes.get_nodes_send(True)
        get_db.get_db_send()
        print "Fixed!"
    def do_update(self, line):
        data = {
            "check_coin.py":"https://raw.github.com/Max00355/zCoin/master/check_coin.py",
            "config.py":"https://raw.github.com/Max00355/zCoin/master/config.py",
            "get_db.py":"https://raw.github.com/Max00355/zCoin/master/get_db.py",
            "get_nodes.py":"https://raw.github.com/Max00355/zCoin/master/get_nodes.py",
            "get_difficulty.py":"https://raw.github.com/Max00355/zCoin/master/get_difficulty.py",
            "get_version.py":"https://raw.github.com/Max00355/zCoin/master/get_version.py",
            "register.py":"https://raw.github.com/Max00355/zCoin/master/register.py",
            "send_coin.py":"https://raw.github.com/Max00355/zCoin/master/send_coin.py",
            "zcoin.py":"https://raw.github.com/Max00355/zCoin/master/zcoin.py",
            "shell.py":"https://raw.github.com/Max00355/zCoin/master/shell.py",    
            "miner.py":"https://raw.github.com/Max00355/zCoin/master/miner.py",
            }
        for x in data:
            print "Updating "+x
            with open(x, 'wb') as file:
                file.write(urllib.urlopen(data[x]).read())
        print "Done!"

    def do_send(self, line):
        line = line.split() 
        to = line[0]
        amount = line[1]
        print send_coin.send_coin_send(line[0], line[1])
    def do_addr(self, line):    
        print "Your zCoin address is: "+self.addr()
    def do_exit(self, line):
        print "Bye!"

        exit()
    def addr(self):
        wallet = sqlite3.connect("wallet.db").cursor()
        wallet.execute("SELECT address FROM data")
        return wallet.fetchall()[0][0]
    
    
    def do_help(self, line):
        print """

        zCoin Commands

        addr - Displays your zCoin address.
        coins - Shows the amount of zCoins that you currently have.
        totalcoins - Shows the amount of total zCoins on the network.
        fixdb - If you are receiving any type of error about Sqlite3 run this command.
        update - Updates your zCoin files. It is suggested that you run these every startup.
        send <address> <amount> - Allows you to transfer coins to another wallet.
        exit - Closes the zCoin shell

        """

if __name__ == "__main__":
    zCoinShell().cmdloop()

