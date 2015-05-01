Key transformers
----------------------------
Vlermv uses the rather basic :py:data:`~vlermv.transformers.simple`
transformer by default; :py:class:`str` keys are mapped to file names
inside of the
vlermv directory, and writing to subdirectories is not allowed.

Other transformers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. py:module:: vlermv.transformers

The following transformers are included in Vlermv.

.. py:data:: magic

   Magically figure out a reasonable file name.

.. py:data:: base64

   File name is the base 64 encoding of the key.

.. py:data:: tuple

   Key must be a tuple; the right most element becomes a file name,
   and the preceding elements are directories.

.. py:data:: simple

   Key is used as the file name directory. It must be a string without slashes.

.. py:data:: slash

   Like simple, except that slashes may be used to separate directories

.. py:data:: backslash

   Like simple, except that backslashes may be used to separate directories

The magic transformer
~~~~~~~~~~~~~~~~~~~~~~~~~
One of the coolest parts of Vlermv is the
:py:data:`~vlermv.transformers.magic` transformer, as it interprets
keys in a very fancy way, combining the features of the
other transformers.

Aside from strings and string-like objects,
you can use iterables of strings; these indices both refer
to the file ``foo/bar/baz``::

    vlermv[('foo','bar','baz')]
    vlermv[['foo','bar','baz']]

(This is like the :py:module`vlermv.transformers.tuple`_ transformer.)

If you pass a relative path to a file, it will be broken up as you'd expect;
that is, strings get split on slashes and backslashes. ::

    vlermv['foo/bar/baz']
    vlermv['foo\\bar\\baz']

(This is like the :py:data:`~vlermv.transformers.tuple` transformer.)

If you pass a URL, it will also get broken up in a reasonable way. ::

    # /tmp/a-directory/http/thomaslevine.com/!/?foo=bar#baz
    vlermv['http://thomaslevine.com/!/?foo=bar#baz']

    # /tmp/a-directory/thomaslevine.com/!?foo=bar#baz
    vlermv['thomaslevine.com/!?foo=bar#baz']

Dates and datetimes get converted to :code:`YYYY-MM-DD` format. ::

    import datetime

    # /tmp/a-directory/2014-02-26
    vlermv[datetime.date(2014,2,26)]
    vlermv[datetime.datetime(2014,2,26,13,6,42)]

And you can mix these formats! ::

    # /tmp/a-directory/http/thomaslevine.com/open-data/2014-02-26
    vlermv[('http://thomaslevine.com/open-data', datetime.date(2014,2,26))]

Creating a transformer
~~~~~~~~~~~~~~~~~~~~~~~~~~
A transformer converts keys to paths and paths to keys, where keys
are things that we use to index a :py:class:`~vlermv.Vlermv` object
and paths Vlermv's internal representation of file paths.

In this section I define a "key" and a "path" and then explain how
to implement a transformer for translating between keys and paths.

Keys
^^^^^^^^^^
In the following query, ``234`` is the key. ::

    Vlermv('tmp')[234]

And in this one, ::

    Vlermv('tmp')[('a', (1, 2))]

``('a'), (1, 2))`` is the key.


Paths
^^^^^^^^^^
Internally in Vlermv, paths get represented as tuples of directory
and file names. Here are some examples of how the mapping works.

=======================  =====================
Vlermv tuple path        Ordinary string path 
=======================  =====================
``('./x', 'y', 'z')``    x/y/z              
``('x', 'y', 'z')``      x/y/z              
``('', 'x', 'y', 'z')``  x/y/z              
``('/', 'usr', 'bin')``  usr/bin             
=======================  =====================

All paths are relative the vlermv root; absolute directories are
converted to relative paths. Empty paths, paths resolving to ``./``,
and relative paths outside of the vlermv root are not allowed.
Here are more complex examples.

=============================   =========================
Vlermv tuple path               Ordinary string path     
=============================   =========================
``('a', '..', 'b', 'c')``       b/c
``('..', '..', 'bin', 'sh')``   (Not allowed)
``('/', '..')``                 (Not allowed)
``('./', 'd')``                 d
``('./',)``                     (Not allowed)
``('', '', '')``                (Not allowed)
``tuple()``                     (Not allowed)
=============================   =========================

When tuple paths are created from file names in
:py:func:`vlermv.Vlermv.keys` or  :py:func:`vlermv.Vlermv.items`,
they contain none of these elements: ``'/'``. ``'.'``, ``'..'``.
That is, they are normal and relative. For example,
a path ``./a/b/c`` becomes ``('a', 'b', 'c')``.

Transformer API
^^^^^^^^^^^^^^^^^^^
.. py:currentmodule:: vlermv.hypothetical_transformer

Now on to the transformer itself!
A transformer is a Python object with the following methods.

.. py:method:: to_path(key:str) -> path:tuple

    Convert a key to a path.

.. py:method:: from_path(path:tuple) -> key:str

    Convert a path to a key.

For example, this is what the default :py:data:`~vlermv.transformers.simple`
transformer looks like.

.. literalinclude:: ../vlermv/transformers/simple.py

Other notes
~~~~~~~~~~~~~~~~~~
Specifying an absolute path, regardless of the transformer, will not let you
save things outside the vlermv directory. Here's an example that uses the
magic transformer.

    vlermv['/foo/bar/baz'] # Saves to ./foo/bar/baz
    vlermv['C:\\foo\\bar\\baz'] # Saves to ./c/foo/bar/baz
                                # (lowercase "c")

As you see, absolute paths are converted into paths relative the root of
the vlermv directory.
