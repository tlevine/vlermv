Should I use Vlermv?
====================================
Before I tell you how to use Vlermv, let me help you decide whether
it's worth using at all.

When to use Vlermv
------------------------------------
Here are some situations in which Vlermv might be helpful.

You are manipulating lots of files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Vlermv maps ordinary files to Python objects. If you are manipulating
lots of files in Python, Vlermv might make your code a lot more legible!

You want a lightweight NoSQL database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Vlermv has few dependencies and does not run any services of its own;
Vlermv runs inside the thread in which you call it. Vlermv would be
a good place if you want to reduce the complexity of your system, which
might occur because have strong security requirements or because you
just want to keep things simple.

You might also consider `LevelDB <http://leveldb.org/>`_
(`Python bindings <https://pypi.python.org/pypi/leveldb>`_).

Reduced dependence on your database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Because Vlermv maps everything onto ordinary files, you usually never
need to "export" your data; they're already in a pretty legible format.
Moreover, since Vlermv's native format is an ordinary filesystem,
you can use :ref:`standard file manipulation tools <fs>`
to do anything that you find Vlermv to be lacking.

When not to use Vlermv
--------------------------
Here are some situations in which I recommend against using Vlermv.

You are not using Python.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Vlermv is written in Python. If you are using another language,
you might look for a similar library. If you don't find one,
study the older (simpler) versions of Vlermv's source code, and
write a simple equivalent of Vlermv in the language you are using.

You cannot mount your filesystem.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Vlermv is designed to make it easier to access ordinary filesystems.
If you are storing your data in HDFS, for example, there's no point
in using Vlermv.

You might still find that a dictionary interface to your data is
convenient. Tell Tom if you want one, and he might write it
(either inside vlermv or in a different package).

When you could use Vlermv if you extended it
---------------------------------------------------
Here are some things that would probably be easy to implement in Vlermv.
See the :ref:`recipes` section for more on this.

You require transactions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you require transactions, you can implement them with your own lock
files and temporary directories inside of the Vlermv directory.

You require database features that aren't available in Vlermv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Vlermv contains many standard database features, and your feature
requirements can sometimes be adjusted by changing your schema.
If you thing Vlermv would be appropriate if it had just one more feature,
you might try implementing it in Vlermv.

For example, you can combine several Vlermv instances to create a more powerful
query language, to create indexes, and to cache the output of complex queries,
to represent graph structures, and to join across datasets.
