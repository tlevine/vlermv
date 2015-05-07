.. _recipes:

Recipes
=============================
Vlermv provides the building blocks for some more complex database
features.

Indices
---------------
All values in Vlermv have exactly one index: the key/filename. This is different
from most relational databases, for example, where you can make indices
on any column, on combinations of columns, and on the results of functions.
Said otherwise, Vlermv has primary keys and no other indexes.

But, you can build your own indices. Let's say I have categorized documents
into "a" documents and "b" documents and I want to be able to find the "a"
documents quickly. I could do this. ::

    db = Vlermv('~/.documents')
    index = {
        'a': [3, 9, 2],
        'b': [8, 1, 23],
    }
    for primary_key in index['a']:
        print(db[primary_key])

:py:obj:`index` could also be a :py:class:`~vlermv.Vlermv`, of course.

.. _fs:

Not reinventing the wheel
-----------------------------------------------

Vlermv is all about mapping Python objects to files in a normal filesystem.
Thus, you'll wind up using general file manipulation tools for more things
than you might expect.

For starters, you can use :command:`rsync` for replication;
shell (:command:`ls`, :command:`cat`, :command:`find`, &c.)
for ad-hoc queries and backups; and
:command:`chmod` and :command:`chown` for permissions management.

.. _sharding:

Sharding
------------

You can implement sharding by mounting different directories on different
hard driver or computers. For example, the "March 2014" and "April 2014"
directories could be on different hard drives, and then you could save your
data as "March 2014/2014-03-01", "March 2014/2014-03-02", ...,
"April 2014/2014-04-01", "March 2014/2014-04-02", ....

Vlermv in RAM
----------------------
In some cases, it is be beneficial to store Vlermv in RAM rather than on
a hard drive.

Before doing this, consider whether an ordinary :py:class:`dict` would work
better. Here are some instances where you might want to use Vlermv.

* Multiple different Python programs or processes are sharing data.
* Vlermv is used as a cache for a program that is run in a cron job;
  you could always rebuild the cache, but maintaining the cache saves time.
* You are debugging something involving lots of data and expect to run
  into lots of errors; you would like to keep the data in memory so you
  don't have to load it from disk.

To do this, create a `tmpfs <https://en.wikipedia.org/wiki/tmpfs>`_,
and initialize Vlermv in there. It is common in modern GNU/Linux distributions
that :file:`/tmp` is a tmpfs; you can run :command:`mount` to check whether this is the
case on your system. If it is, you can just do this. ::

    Vlermv('/tmp/this-is-a-tmpfs')

Replacing Mongo
-----------------
Like Mongo, Vlermv is designed for write-heavy workloads that need scalability
(easy sharding), flexible schemas, and highly configurable indexing.

Should I replace Mongo with Vlermv?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
I find that Mongo is often used where ordinary files would work just fine.
Mongo is beneficial if you are using any of its fancy features; if you aren't
using the fancy features, you might find that Vlermv is easier to manage.

Should you replace Mongo with Vlermv? Here are some things to consider.

* Do you have more than one index on any collection?
* Are you running complex queries?
* Are you using a language other than Python?
* Is Vlermv too slow?

If the answer to any of the above is "yes", stick with Mongo, at least for
now. If they are all "no", you can consider switching.

How to replace Mongo with Vlermv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Most likely, each Mongo collection should correspond to a Vlermv instance.
Instead of Object IDs, you have Vlermv keys (filenames), and instead of
documents you have Vlermv values (file contents).

See the above discussion on :ref:`sharding <sharding>` for ideas on implementing
sharding in Vlermv.

If you need to make isolated updates on properties of your documents,
separate the documents into a directory of several documents, one document
per field.

Considering that you have been using Mongo, it is likely that you can switch
the Vlermv's default pickle serializer for something faster and with more
constraints. Consider using :py:mod:`bson` or :py:mod:`json`.

If you are using GridFS simply to store and retrieve file contents, you
can put those contents directly into Vlermv. If you are accessing the file
metadata, consider writing a custom :py:mod:`serializer <vlermv.serializers>` or simply
storing those files outside of Vlermv.

Debugging
-------------------
If you want to look at the contents of a vlermv in the console, open Python
shell and import the vlermv. Consider the following (abridged) exception

.. code-block:: python
   :emphasize-lines: 3

   Traceback (most recent call last):
     File "/home/tlevine/git/scott2/usace/public_notices/__init__.py", line 11, in public_notices
       for link in parse.feed(download.feed(str(site))):
     File "/home/tlevine/git/scott2/usace/public_notices/parse.py", line 10, in feed
       rss = parse_xml_fp(StringIO(response.text))
     File "/usr/lib/python3.4/xml/etree/ElementTree.py", line 1187, in parse
       tree.parse(source, parser)
     File "/usr/lib/python3.4/xml/etree/ElementTree.py", line 598, in parse
       self._root = parser._parse_whole(source)
   xml.etree.ElementTree.ParseError: syntax error: line 1, column 0

I happen to know, because I wrote the program that generated the traceback,
that :samp:`feed`,
from :samp:`for link in parse.feed(download.{feed}(str(site)))`
is a function cached with vlermv and that it is defined in the module
:samp:`usace.public_notices.download` as :samp:`feed`.

To inspect the vlermv, open another console, and type this. ::

    from usace.public_notices.download import feed

:samp:`feed` is a vlermv, so now I can look at the data however I like. ::

    print(list(feed.keys()))

This query is wound up uncovering the problem. ::

    print(feed[('461',)])
