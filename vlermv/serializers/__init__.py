'''
A serializer is a Python object with the following methods.

``dump(obj, fp) -> None``
    Write the object to the file pointer ``fp``.
``load(fp) -> obj``
    Represent the  the file pointer ``fp`` as an object.

It optionally includes two boolean properties.

First, ``vlermv_binary_mode`` indicates whether binary modes be used
for opening file pointers. (Default is ``False``.) If this is ``True``,
pointers will be opened like this. ::

    open(filename, 'rb')
    open(filename, 'wb')

If it is ``False``, filenames will be opened like this.

    open(filename, 'r')
    open(filename, 'w')

Second, ``vlermv_cache_exceptions`` tells us whether to cache exceptions when
the serializer is used with ``vlermv.cache``. (Default is ``False``.)

* If this is ``True``, ``dump`` is passed a tuple of
  ``(exception, obj)``, and load is expected to return
  the same format. ``exception`` is ``None`` if the function
  ran without error, and ``obj`` is ``None`` if there was an error.
* If it is ``False``, ``dump`` is passed simply the ``obj``,
  and ``load`` is expected to return the ``obj``.

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

        vlermv_binary_mode = True
        vlermv_cache_exceptions = False

'''

import io as _io
import base64 as _base64



class base64:
    'Dump and load base64-encoded stuff.'
    def dump(self, obj, fp):
        input_fp = io.BytesIO(obj)
        _base64.encode(input_fp, fp)
    def load(self, fp):
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
