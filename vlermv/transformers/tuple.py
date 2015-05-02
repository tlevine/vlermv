def to_path(key):
    if not isinstance(key, tuple):
        raise TypeError('x must be of class tuple.')
    return key

def from_path(x):
    return x
