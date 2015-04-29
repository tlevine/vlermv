class _identity:
    'Dump and load things that are already serialized.'
    dump = lambda obj, fp: fp.write(obj)
    load = lambda fp: fp.read()
    vlermv_cache_exceptions = False
    def __init__(self, binary_mode = False):
        vlermv_binary_mode = binary_mode

identity_str = _identity(binary_mode = False)
identity_bytes = _identity(binary_mode = False)
