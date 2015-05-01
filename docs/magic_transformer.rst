The magic transformer
-------------------------
One of the coolest parts of Vlermv is the
:py:module:`vlermv.transformers.magic`_ transformer, as it interprets
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

(This is like the :py:module`vlermv.transformers.tuple`_ transformer.)

Note well: Specifying an absolute path won't save things outside the vlermv directory. ::

    vlermv['/foo/bar/baz'] # -> foo, bar, baz
    vlermv['C:\\foo\\bar\\baz'] # -> c, foo, bar, baz
                                   # (lowercase "c")

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

It also has typical dictionary methods like :code:`keys`, :code:`values`, :code:`items`,
and :code:`update`.

