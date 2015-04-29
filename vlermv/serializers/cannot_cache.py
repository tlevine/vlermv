import io as _io
import base64 as _base64

from .base import base

class base64(base):
    'Dump and load base64-encoded stuff.'

    @staticmethod
    def dump(obj, fp):
        input_fp = io.BytesIO(obj)
        _base64.encode(input_fp, fp)

    @staticmethod
    def load(fp):
        output_fp = io.BytesIO()
        _base64.decode(fp, output_fp)
        return output_fp.read()

    vlermv_cache_exceptions = False
    vlermv_binary_mode = True

class identity:
    'Dump and load things that are already serialized.'
    dump = lambda obj, fp: fp.write(obj)
    load = lambda fp: fp.read()
    vlermv_cache_exceptions = False
    def __init__(self, binary_mode = False):
        vlermv_binary_mode = binary_mode
