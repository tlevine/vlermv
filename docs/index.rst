Vlermv
==================================

Vlermv provides a dictionary-like object that is associated with a
particular directory on your computer. Install from PyPI. ::

    pip install vlermv

Then call it like this. ::

    from vlermv import Vlermv
    like_a_dictionary = Vlermv('/tmp/a-directory')

Now you can mostly pretend that ``like_a_dictionary`` is a :py:class:`dict`,
except that it will persist across Python sessions.

That was the three-line introduction to Vlermv; read on to see more of what
it can do.

.. toctree::
   :maxdepth: 2

   vlermv
   cache
   serializers
   transformers

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

