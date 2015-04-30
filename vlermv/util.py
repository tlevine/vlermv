import os

def split(path):
    'Split a path into a tuple of all directories and then the final directory/file.'
    if path == '':
        raise ValueError('Path may not be empty.')

    dn, fn = os.path.split(path)
    if fn == '':
        return (dn,)
    elif dn == '':
        return (fn,)
    else:
        return split(dn) + (fn,)
