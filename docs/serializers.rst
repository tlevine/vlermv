Serializers
=======================
Serializers specify how Python objects should be saved to disk and
how files from disk should be read as Python objects.

Components of a serializer
----------------------------
.. _transformer:

A serializer is a Python object with the following methods.

.. py:method:: dump(obj, fp) -> None

   Write the object ``obj`` to the file pointer ``fp``.
   
.. py:method:: load(fp) -> obj

   Represent the file pointer ``fp`` as an object ``obj``.

It optionally includes two boolean properties.

.. py:attribute:: vlermv_binary_mode

   Should binary modes be used for opening file pointers?
   Default is ``False``.
   If this is ``True``, pointers will be opened like this. ::

       open(filename, 'rb')
       open(filename, 'wb')

   If it is ``False``, pointers will be opened like this. ::

       open(filename, 'r')
       open(filename, 'w')

.. py:attribute:: vlermv_cache_exceptions

   Is caching of exceptions is supported? Default is ``True``.
   This is relevant when the serializer is used with
   :py:func:`vlermv.cache`.

   If :py:attr:`vermv_cache_exceptions` is ``False`` but
   :py:class:`vlermv.Vlermv` is initialized with
   ``cache_exceptions = True``, an exception is raised.

What exactly is ``obj``?
--------------------------
The ``obj`` that is referenced in the above function signatures is
manipulated if you enable the caching of exceptions. (Exception caching
is disabled by default.)

Default behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If :py:class:`vlermv.Vlermv` is initialized with ``cache_exceptions = False``,
``obj`` is simply the object that was passed to
:py:func:`vlermv.Vlermv.__setitem__`.
This is the default; in the following example ``obj`` is ``8``. ::

    Vlermv('/tmp/a')['b'] = 8 

And in the following case, ``obj`` is ``103``. ::

    @cache(cache_exceptions = False)
    def f(x):
        return x + 3
    f(100) # <- Returns 103

``cache_exceptions`` is ``False`` by default, so the following block is
the same as the previous one. ::

    @cache()
    def f(x):
        return x + 3
    f(100) # <- Returns 103

If exception caching is enabled
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You probably want to set ``cache_exceptions`` only if you are using the
:py:func:`vlermv.cache` decorator, as it doesn't do anything otherwise.

If ``cache_exceptions`` is ``True``, ``obj`` is a tuple of ``(exception, result)``,
where ``result`` is the result of the decorated function.
(If ``cache_exceptions`` is ``False``, ``obj`` is simply ``result``.)

``exception`` is ``None`` if the function ran without error, and ``result``
is ``None`` if there was an error.

Consider the function ``g`` below. ::

    @cache(cache_exceptions = True)
    def g(x):
        return x + 3

It is just like the ``f`` we saw before except with exception caching enabled.
If we call it like we called ``f`` before, ::

    g(100) # returns 103

``obj`` is ``(None, 103)``, because the value ``103`` is returned without error.
The following ``g`` call produces an error, ::

    >>> g('one hundred')
    TypeError: Can't convert 'int' object to str implicitly

In this case, ``obj`` looks like this. ::

    (TypeError("Can't convert 'int' object to str implicitly"), None)

If exception caching had been disabled, the serializer would never have gotten
called; the error would have been raised but not saved.

Example serializers
---------------------
The :py:mod:`json` module is a valid serializer, ::

    import json

and so is ``simple_identity``. ::

    class simple_identity:
        @staticmethod
        def dump(obj, fp):
            fp.write(obj)

        @staticmethod
        def load(fp):
            return fp.read()

        vlermv_binary_mode = True
        vlermv_cache_exceptions = False

On the other hand, :py:mod:`pickle` does not function properly as a
serializer. ::

    import pickle

This is because pickle requires that file pointers be opened in binary
mode rather than string mode; the Vlermv's default
:py:data:`~vlermv.serializers.pickle` serializer thus has to set
``vlermv_binary_mode`` to ``True``.

.. literalinclude:: ../vlermv/serializers/pickle.py

Serializers included with Vlermv
------------------------------------
.. py:module:: vlermv.serializers

The following serializers are included.

.. py:data:: vlermv.serializers.identity_str

   Write raw strings to files.

.. py:data:: vlermv.serializers.identity_bytes

   Write raw bytes to files.

.. py:data:: vlermv.serializers.pickle

   Serialize with :py:mod:`pickle`.

.. py:data:: vlermv.serializers.html

   Serialize HTML trees from `lxml <http://lxml.de/>`_.

.. py:data:: vlermv.serializers.xml

   Serialize XML etrees from `lxml <http://lxml.de/>`_.
