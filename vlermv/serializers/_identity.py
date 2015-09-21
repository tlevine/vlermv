import mmap
import os

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

class identity_mmap_bytes(_identity):
    'Dump and load raw bytes, loading with a memory-mapped file.'
    binary_mode = True

    @staticmethod
    def load(fp):
        if os.stat(fp.name).st_size > 0:
            return mmap.mmap(fp.fileno(), 0).read()
        else:
            return b''

class identity_mmap_str(_identity):
    'Dump and load raw strings, loading with a memory-mapped file.'
    binary_mode = True

    @staticmethod
    def dump(obj, fp):
        fp.write(obj.encode('utf-8'))

    @staticmethod
    def load(fp):
        return identity_mmap_bytes.load(fp).decode('utf-8')
