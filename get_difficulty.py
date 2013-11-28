import config
import json

def get_difficulty(obj, data):
    diff = config.db.find("coins", "all")
    if not diff:
        diff = []
    diff = len(diff)/50500 + 7
    if diff < 7:
        diff = 7
    obj.send(json.dumps({"difficulty":diff}))

