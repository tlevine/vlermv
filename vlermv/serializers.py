'''
A serializer is a Python object with the following methods.

``dump(obj, fp) -> None``
    Write the object to the file pointer ``fp``.
``dump(fp) -> obj``
    Represent the  the file pointer ``fp`` as an object.

It optionally includes another method.

``binary(obj) -> bool``
    Determine whether to use binary modes for opening file pointers.

For example, ``json`` is a valid serializer, ::

    import json

and so is ``simple_identity``.

    class simple_identity:
        @staticmethod
        def dump(obj, fp):
            fp.write(obj)

        @staticmethod
        def load(fp):
            return fp.read()

        def binary(obj):
            return True
'''

import io as _io
import base64 as _base64

class base64:
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

class identity:
    'Dump and load things that are already serialized.'
    dump = lambda obj, fp: fp.write(obj)
    load = lambda fp: fp.read()

class _meta_xml:
    def __init__(self, lxml_module):
        self.module = lxml_module
    @staticmethod
    def dump(obj, fp):
        fp.write(self.module.tostring(obj))
    @staticmethod
    def load(fp):
        return self.module.fromstring(fp.read())

try:
    import numpy.lib.npyio
except ImportError:
    pass
else:
    class npy:
        load = numpy.lib.npyio.load
        dump = numpy.lib.npyio.save

try:
    import lxml
except ImportError:
    pass
else:
    import lxml.html, lxml.etree
    html = _meta_xml(lxml.html)
    xml = _meta_xml(lxml.etree)
