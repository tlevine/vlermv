import os
from random import randint
from string import ascii_letters

def _random_file_name():
    n = len(ascii_letters) - 1
    return ''.join(ascii_letters[randint(0, n)] for _ in range(10))

def mktemp(tempdir, filename = _random_file_name):
    try:
        os.makedirs(tempdir, exist_ok = True)
    except TypeError:
        # Python 2
        if not os.path.isdir(tempdir):
            os.makedirs(tempdir)
    return os.path.join(tempdir, filename())

def _reversed_directories(outer, inner):
    while outer != inner:
        yield inner
        inner = os.path.dirname(inner)
