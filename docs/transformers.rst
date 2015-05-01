Key transformers
----------------------------
Vlermv uses the rather basic :py:data:`vlermv.transformers.simple`
transformer by default; ``str`` keys are mapped to file names inside of the
vlermv directory, and writing to subdirectories is not allowed.

Other transformers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. py:module:: vlermv.transformers

The following transformers are included in Vlermv.

.. py:data:: vlermv.transformers.magic

   Magically figure out a reasonable file name.

.. py:data:: vlermv.transformers.base64

   File name is the base 64 encoding of the key.

.. py:data:: vlermv.transformers.tuple

   Key must be a tuple; the right most element becomes a file name,
   and the preceding elements are directories.

.. py:data:: vlermv.transformers.simple

   Key is used as the file name directory. It must be a string without slashes.

.. py:data:: vlermv.transformers.slash

   Like simple, except that slashes may be used to separate directories

.. py:data:: vlermv.transformers.backslash

   Like simple, except that backslashes may be used to separate directories

The magic transformer
~~~~~~~~~~~~~~~~~~~~~~~~~
One of the coolest parts of Vlermv is the
:py:data:`vlermv.transformers.magic` transformer, as it interprets
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

(This is like the :py:data:`vlermv.transformers.tuple` transformer.)

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
