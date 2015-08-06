import posixpath

error_msg = '''The index must be a string.'''

def to_path(key):
    return tuple(key.strip('/').split('/'))

def from_path(path):
    return posixpath.join(*path)
