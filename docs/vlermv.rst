Using :py:class:`vlermv.Vlermv` as a dictionary
---------------------------------------------------
Vlermv provides a dictionary-like object
that is associated with a particular directory on
your computer. ::

    from vlermv import Vlermv
    vlermv = Vlermv('/tmp/a-directory')

Items are files
~~~~~~~~~~~~~~~~~
The keys correspond to file names, and the values get serialized to files.
The default serialization is :py:mod:`pickle`. ::

    vlermv['filename'] = range(100)

    import pickle
    range(100) == pickle.load(open('/tmp/a-directory/filename', 'rb'))

(Default serialization is technically :py:class:`vlermv.serializers.pickle`,
but it's pretty much the same thing as :py:mod:`pickle`.)

Get and delete
~~~~~~~~~~~~~~~~~
You can also get and delete things. ::

    # Read
    range(100) == vlermv['filename']

    # Delete
    del(vlermv['filename'])

Like a dictionary
~~~~~~~~~~~~~~~~~~~
And remember that vlermv is a :py:class:`dict`-like object, so things
like this work too. ::

    vlermv.items()
    vlermv.update({'a': 1, 'b': 2})

Further configuration
~~~~~~~~~~~~~~~~~~~~~~~~
There are several parameters that you can change when initializing Vlermv,

.. autoclass:: vlermv.Vlermv

and we'll discuss those in later sections.
