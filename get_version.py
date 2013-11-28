import config

def get_version(obj, data):
    obj.send(config.version)
