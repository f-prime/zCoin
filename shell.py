import config
import cmd
import send_coin
import threading

class zc(cmd.Cmd):
    prompt = "zShell$ "
    intro = "Welcome to the zCoin shell, type `help` to get started."
    def do_send(self, line):
        line = line.split()
        try:
            to = line[0]
            amount = line[1]
        except:
            self.do_help()
        else:
            print "Coins are being sent"
            threading.Thread(target=send_coin.send, args=(to, amount)).start()

    def do_totalcoins(self, line):
        coin = config.db.find("coins", "all")
        if not coin:
            coin = 0
        else:
            coin = len(coin)
        print "Ther are "+str(coin)+" coins in existence."

    def do_coins(self, line):
        addr = config.wallet.find("data", "all")[0]
        addr = addr['address']
        coins = config.db.find("coins", {"address":addr})
        if not coins:
            coins = 0
        else:
            coins = len(coins)
        print "You have "+str(coins)+" coins."

    def do_addr(self, lines):
        addr = config.wallet.find("data", "all")[0]['addr']
        print "Your address is: "+addr

    def do_transactions(self, line):
        line = line.split()
        if not line:
            self.do_help()
        else:
            data = config.db.find("transactions", {"from":line})
            if not data:
                print "No transactions have been made from this address."
            else:
                for x in data:
                    a = """
                        ID: {0}
                        To: {1}
                        Amount: {2}

                    """.format(x['transid'], x['to'], x['amount'])
                    print a

    def do_help(self, line):
        print """
            
            Welcome to the zCoin shell

            send <to> <amount> - Send coins to an address
            coins - Shows the amount of coins you currently own
            totalcoins - Shows total coins on the network
            transactions <addr> - Shows transactions made from an address
            update - Updates the source code
            addr - Displays your address
            

        """

if __name__ == "__main__":
    zc().cmdloop()
