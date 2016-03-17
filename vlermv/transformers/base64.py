from base64 import b64encode, b64decode

def to_path(path):
    return (b64encode(path[0].encode('utf-8')).decode('ascii'),)

def from_path(key):
    if len(key) != 1:
        raise ValueError('Key must have exactly one element.')
    return b64decode(key[0]).decode('ascii')
