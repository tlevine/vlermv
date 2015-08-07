import posixpath

error_msg = '''The index must be a string.'''

def to_path(key):
    if isinstance(key, tuple) and len(key) == 1:
        key = key[0]

    if hasattr(key, 'strip') and hasattr(key, 'split'):
        return tuple(key.strip('/').split('/'))
    else:
        raise TypeError('Key must be string-like or a tuple of length one.')

def from_path(path):
    return posixpath.join(*path)
