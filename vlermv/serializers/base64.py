'Dump and load base64-encoded stuff.'
import io as _io
import base64 as _base64

def dump(obj, fp):
    input_fp = _io.BytesIO(obj)
    _base64.encode(input_fp, fp)

def load(fp):
    output_fp = _io.BytesIO()
    _base64.decode(fp, output_fp)
    return output_fp.read()

vlermv_cache_exceptions = False
vlermv_binary_mode = True
