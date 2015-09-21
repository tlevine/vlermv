import mmap

def dump(obj, fp):
    mmap.mmap(fp.fileno(), 0).write(obj)

def load(fp):
    return bytes(mmap.mmap(fp.fileno(), 0))

cache_exceptions = False
binary_mode = True
