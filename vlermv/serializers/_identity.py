class _identity:
    'Dump and load things that are already serialized.'
    @staticmethod
    def dump(obj, fp):
        fp.write(obj)

    @staticmethod
    def load(fp):
        return fp.read()

    cache_exceptions = False

class identity_str(_identity):
    'Dump and load raw strings.'
    binary_mode = False

class identity_bytes(_identity):
    'Dump and load raw bytes.'
    binary_mode = True
