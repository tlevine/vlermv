from base64 import b64encode

def base64(x):
    return b64encode(x.encode('utf-8'))

def identity(x):
    return x
