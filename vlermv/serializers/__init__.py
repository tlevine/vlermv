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

