from Tkinter import *
import config
import send_coin
import thread
import time
import tkMessageBox
import zcoin

class zCoinUI:

    def __init__(self, root):
        self.root = root
        self.frame = Frame(self.root)
        self.frame.pack()
        self.c = StringVar()
        self.t = StringVar()
        self.addr_ = StringVar()
        thread.start_new_thread(self._update, ())
        self.addr()
        self.coins()
        self.totalcoins()
        self.send()

    def _update(self):
        while True:
            
            coins = config.db.find("coins", {"address":config.wallet.find("data", "all")[0]['address']})
            if not coins:
                coins = []
            coins = len(coins)
            totalcoins = config.db.find("coins", "all")
            if not totalcoins:
                totalcoins = []
            totalcoins = len(totalcoins)
            addr = config.wallet.find("data", "all")[0]['address']
            self.addr_.set(addr)
            self.c.set(coins)
            self.t.set(totalcoins)
            time.sleep(10)
    
    def addr(self):

        addr_f = LabelFrame(self.frame, text="Address", padx=5, pady=5)
        addr_f.grid(sticky=E+W)
        Entry(self.frame, state="readonly", textvariable=self.addr_, width=50).grid(in_=addr_f)
    
    def coins(self):
        coins_f = LabelFrame(self.frame, text="Your Coins", padx=5, pady=10)
        coins_f.grid(sticky=E+W)
        Label(self.frame, textvariable=self.c).grid(in_=coins_f)

    def totalcoins(self):
        total_f = LabelFrame(self.frame, text="Total Coins", padx=5, pady=10)
        total_f.grid(sticky=E+W)
        Label(self.frame, textvariable=self.t).grid(in_=total_f)

    def send(self):
        send_f = LabelFrame(self.frame, text="Send Coin", padx=5, pady=15)
        send_f.grid(sticky=E+W)
        to_l = Label(self.frame, text="To: ").grid(in_=send_f)
        self.to = Entry(self.frame)
        self.to.grid(in_=send_f, row=0, column=1, sticky=W)
        amount_l = Label(self.frame, text="Amount: ").grid(in_=send_f, row=0, column=3, sticky=W)
        self.amount = Entry(self.frame, width=4)
        self.amount.grid(in_=send_f, row=0, column=4, sticky=W)
        Label(self.frame, text="   ").grid(in_=send_f, row=0, column=5)
        Label(self.frame, text="   ").grid(in_=send_f, row=0, column=2)
        send_b = Button(self.frame, command=self._send, text="Send").grid(in_=send_f, row=0, column=8, sticky=W+E+N+S)
            
    def _send(self):
        amount = self.amount.get()
        to = self.to.get()
        addr = config.wallet.find("data", "all")[0]['address']
        check = config.db.find("coins", {"address":addr})
        if not check:
            check = []
        try:
            int(amount)
        except ValueError:
            tkMessageBox.showinfo("Woops!", "Amount must be a number.")
            return
        if len(check) < int(amount):
            tkMessageBox.showinfo("Woops!", "You don't have enough coins.")
            return
        check = config.nodes.find("nodes", {"address":to})
        if not check:
            tkMessageBox.showinfo("Woops!", "Address doesn't exist.")
            return
        thread.start_new_thread(send_coin.send, (to, amount))
        tkMessageBox.showinfo("Sending...", "Your coins are being sent, this could take a while.")

if __name__ == "__main__":
    if not config.wallet.find("data", "all"):
        zcoin.zCoin().firstrun()
    thread.start_new_thread(zcoin.run, ())
    root = Tk()
    root.geometry("450x250+350+100")
    zCoinUI(root=root)
    root.title("zCoin Client")
    root.mainloop()
