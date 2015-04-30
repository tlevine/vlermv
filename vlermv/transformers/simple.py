from base64 import b64encode

def base64(x):
    return b64encode(x.encode('utf-8'))

def identity(x):
    '''
    Handle both tuple/list types and bytes/str types.
    '''
    if 
        str(x).split('/')
