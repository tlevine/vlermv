from base64 import b64encode

def base64(x):
    return b64encode(x.encode('utf-8'))

def slash(x):
    return str(x).split('/')

def backslash(x):
    return str(x).split('\\')

def iterable(x):
    return x
