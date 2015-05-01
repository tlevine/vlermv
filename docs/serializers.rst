Serializers
=======================
.. py:module:: vlermv.serializers

Serializers specify how Python objects should be saved to disk and
how files from disk should be read as Python objects.

Components of a serializer
----------------------------
A serializer is a Python object with the following methods.

.. py:module:: vlermv.serializers.hypothetical_serializer

.. py:function:: dump(obj, fp) -> None

   Write the object :py:obj:`obj` to the file pointer :py:obj:`fp`.
   
.. py:function:: load(fp) -> obj

   Represent the file pointer :py:obj:`fp` as an object :py:obj:`obj`.

It optionally includes two boolean properties.

.. py:attribute:: vlermv_binary_mode

   Should binary modes be used for opening file pointers?
   Default is :py:const:`False`.
   If this is :py:const:`True`, pointers will be opened like this. ::

       open(filename, 'rb')
       open(filename, 'wb')

   If it is :py:const:`False`, pointers will be opened like this. ::

       open(filename, 'r')
       open(filename, 'w')

.. py:attribute:: vlermv_cache_exceptions

   Is caching of exceptions is supported? Default is :py:const:`True`.
   This is relevant when the serializer is used with
   :py:func:`~vlermv.cache`.

   If :py:attr:`vermv_cache_exceptions` is :py:const:`False` but
   :py:class:`~vlermv.Vlermv` is initialized with
   ``cache_exceptions = True``, an exception is raised.

What exactly is :py:obj:`obj`?
--------------------------
The :py:obj:`obj` that is referenced in the above function signatures is
manipulated if you enable the caching of exceptions. (Exception caching
is disabled by default.)

Default behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If :py:class:`~vlermv.Vlermv` is initialized with ``cache_exceptions = False``,
:py:obj:`obj` is simply the object that was passed to
:py:func:`vlermv.Vlermv.__setitem__`.
This is the default; in the following example :py:obj:`obj` is :py:obj:`8`. ::

    Vlermv('/tmp/a')['b'] = 8 

And in the following case, :py:obj:`obj` is :py:obj:`103`. ::

    @cache(cache_exceptions = False)
    def f(x):
        return x + 3
    f(100) # <- Returns 103

:py:obj:`cache_exceptions` is :py:const:`False` by default,
so the following block is
the same as the previous one. ::

    @cache()
    def f(x):
        return x + 3
    f(100) # <- Returns 103

If exception caching is enabled
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You probably want to set :py:obj:`cache_exceptions` only if you are using the
:py:func:`~vlermv.cache` decorator, as it doesn't do anything otherwise.

If :py:obj:`cache_exceptions` is :py:const:`True`,
:py:obj:`obj` is a tuple of :py:obj:`(exception, result)`,
where :py:obj:`result` is the result of the decorated function.
(If :py:obj:`cache_exceptions` is :py:const:`False`,
:py:obj:`obj` is simply :py:obj:`result`.)

:py:obj:`exception` is :py:const:`None`
if the function ran without error, and :py:obj:`result`
is :py:const:`None` if there was an error.

Consider the function :py:func:`g` below. ::

    @cache(cache_exceptions = True)
    def g(x):
        return x + 3

It is just like the :py:func:`f` we saw before
except with exception caching enabled.
If we call it like we called :py:func:`f` before, ::

    g(100) # returns 103

then :py:obj:`obj` is :py:func:`(None, 103)`.
This is because the value :py:func:`103` is returned without error.

The following :py:func:`g` call, on the other hand, produces an error, ::

    >>> g('one hundred')
    TypeError: Can't convert 'int' object to str implicitly

In this case, :py:func:`obj` looks like this. ::

    (TypeError("Can't convert 'int' object to str implicitly"), None)

If exception caching had been disabled, the serializer would never have gotten
called; the error would have been raised but not saved.

Example serializers
---------------------
The :py:mod:`json` module is a valid serializer, ::

    import json

and so is :py:func:`simple_identity`. ::

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
:py:attr:`vlermv_binary_mode` to :py:const:`True`.

.. literalinclude:: ../vlermv/serializers/pickle.py

Serializers included with Vlermv
------------------------------------
.. py:currentmodule:: vlermv.serializers

The following serializers are included.

.. py:data:: identity_str

   Write raw :py:class:`strings <str>` to files.

.. py:data:: identity_bytes

   Write raw :py:class:`bytes` to files.

.. py:data:: pickle

   Serialize with :py:mod:`pickle`.

.. py:data:: html

   Serialize HTML trees from `lxml <http://lxml.de/>`_.

.. py:data:: xml

   Serialize XML etrees from `lxml <http://lxml.de/>`_.
