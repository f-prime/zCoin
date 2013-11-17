import cmd
import sqlite3
import send_coin

class zCoinShell(cmd.Cmd):
    prompt = "zShell$ "
    intro = "\nWelcome to the zCoin Shell for help type 'help'"    
    def do_coins(self, line):
        coins = sqlite3.connect("db.db").cursor()
        coins.execute("SELECT * FROM coins WHERE address=?", [self.addr()])
        print "You have "+str(len(coins.fetchall())) + " coins."
    def do_transactions(self, line):
        coins = sqlite3.connect("db.db").cursor()
        coins.execute("SELECT to_, from_, hash FROM transactions WHERE to_=?", [line])
        for x in coins.fetchall():
            print "\nTo: "+x[0]
            print "Coin: "+x[2]

    def do_totalcoins(self, line):
        coins = sqlite3.connect("db.db").cursor()
        coins.execute("SELECT * FROM coins")
        print "There are "+str(len(coins.fetchall()))+" coins in existance."
    def do_send(self, line):
        line = line.split() 
        to = line[0]
        amount = line[1]
        print send_coin.send_coin_send(line[0], line[1])
    def do_addr(self, line):    
        print "Your zCoin address is: "+self.addr()
    def addr(self):
        wallet = sqlite3.connect("wallet.db").cursor()
        wallet.execute("SELECT address FROM data")
        return wallet.fetchall()[0][0]
    def help_coins(self):
        print "Displayes the coins that you own."
        print "Syntax: coins"
    def help_send(self):
        print "Sends an amount of coins to a person."
        print "Syntax: send <address> <amount>"
    def help_totalcoins(self):
        print "Displayes the amount of coins that exist on the network."
        print "Syntax: totalcoins"
    def help_transactions(self):
        print "Displayes all transactions made over the network"
        print "Syntax: transactions <to>"
    def help_addr(self):
        print "Displayes your zCoin address."
        print "Syntax: addr"
    
if __name__ == "__main__":
    zCoinShell().cmdloop()

