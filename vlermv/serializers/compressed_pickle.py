import zlib, pickle

binary_mode = True
def load(fp):
    return pickle.loads(zlib.decompress(fp.read()))

def dump(obj, fp):
    fp.write(zlib.compress(pickle.dumps(obj)))
