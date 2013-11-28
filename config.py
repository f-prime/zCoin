import landerdb

relay = 0
brokers = [{"ip":"zcoin.zapto.org", "port":6564}]
version = "0.2.0"
host = "0.0.0.0"
port = 6565
nodes = landerdb.Connect("nodes.db")
wallet = landerdb.Connect("wallet.db")
db = landerdb.Connect("db.db")
