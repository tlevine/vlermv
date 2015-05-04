The dictionary API
---------------------------------------------------
:py:class:`~vlermv.Vlermv` create a dictionary-like object
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

(Default serialization is technically :py:data:`vlermv.serializers.pickle`,
but it's pretty much the same thing as pickle.)

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

More options
~~~~~~~~~~~~~~~~~~~~~~~~
There are several parameters that you can change when initializing Vlermv,
and we'll discuss those in later sections.

.. autoclass:: vlermv.Vlermv
    :members:
