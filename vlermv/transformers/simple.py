import os

def to_path(key):
    if '/' in key or '\\' in key:
        raise ValueError('The default transformer cannot handle slashes; try another transformer in vlermv.transformers.')
    return (key,)

def from_path(path):
    return os.path.join(*path)
