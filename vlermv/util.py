import os

def split(path):
    'Split a path into a tuple of all directories and then the final directory/file.'
    dn, fn = os.path.split(path)
    if dn == '':
        return path
    else:
        return split(dn) + (fn,)
