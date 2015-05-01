History
=====================
I wrote `pickle warehouse <https://pypi.python.org/pypi/pickle-warehouse>`_
so I could easily store pickles in files with meaningful names.
Then I extended it to support more than just pickles. Then I wrote
`picklecache <https://pypi.python.org/pypi/picklecache>`_, mainly for caching
responses to HTTP requests.

And then I finally changed the names because these two packages don't really
have much to do with pickles. ``pickle_warehouse.Warehouse`` became
``vlermv.Vlermv``, and ``picklecache.cache`` became ``vlermv.cache``.
I chose the name "vlermv" by banging on the keyboard; this is how I have
been naming things now that I have discovered Dada.

During the transition from pickle warehouse and pickle cache to vlermv,
I also added a particular feature that I wanted: the ability to refresh
the cache. (And I implemented this by subclassing ``vlermv.Vlermv``, as
discussed in the documentation above.)
