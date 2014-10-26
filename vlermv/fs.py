import os
from random import randint
from string import ascii_letters

def mktemp(tempdir):
    if not os.path.isdir(tempdir):
        os.mkdir(tempdir)
    return os.path.join(tempdir, _random_file_name())

def _random_file_name():
    n = len(ascii_letters) - 1
    return ''.join(ascii_letters[randint(0, n)] for _ in range(10))
