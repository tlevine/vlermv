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

Second, ``vlermv_cache_exceptions`` tells us whether the caching of
exceptions is supported. (Default is ``False``.) This is relevant
when the serializer is used with ``vlermv.cache``. If it is ``False``
but ``Vlermv`` is initialized with ``cache_exceptions = True``,
an exception is raised.

What exactly is ``obj``?
---------------------

If ``Vlermv`` is initialized with ``cache_exceptions = False``,
``obj`` is simply the object that was passed to ``Vlermv.__setitem__``.
Most likely, this happened because the ``vlermv.cache`` decorator was
used, and ``obj`` is thus the result of the decorated function.
For example, in this case, ``obj`` is 103. ::

    @cache(cache_exceptions = False)
    def f(x):
        return x + 3
    f(100) # <- ``obj`` is 103

If ``cache_exceptions = True``, ``obj`` is a tuple of ``(exception, result)``,
where ``result`` is the result of the decorated function.
``exception`` is ``None`` if the function ran without error, and ``result``
is ``None`` if there was an error.

Example serializers
---------------------
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

__all__ = []

from .identity import identity_str, identity_bytes
__all__.extend(['identity_str', 'identity_bytes'])

try:
    from .lxml import html, xml
except ImportError:
    pass
else:
    __all__.extend(['html', 'lxml'])

