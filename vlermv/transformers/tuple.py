def dumps(x):
    if not isinstance(x, tuple):
        raise ValueError('x must be of class tuple.')
    return x

def loads(x):
    return x
