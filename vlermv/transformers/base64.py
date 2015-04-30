from base64 import b64encode, b64decode

def from_tuple(obj):
    return b64encode(obj[0].encode('utf-8')).encode('ascii')

def to_tuple(key):
    return (b64decode(key.encode('ascii')).decode('utf-8'),)
