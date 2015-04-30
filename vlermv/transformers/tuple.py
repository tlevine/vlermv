def to_tuple(key):
    if not isinstance(key, tuple):
        raise ValueError('x must be of class tuple.')
    return key

def from_tuple(x):
    return x
