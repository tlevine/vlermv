Vlermv
==================================

Vlermv provides a dictionary-like object that is associated with a
particular directory on your computer. Here's a three-line introduction.

Install from PyPI. ::

    pip install vlermv

Then call it like this. ::

    from vlermv import Vlermv
    like_a_dictionary = Vlermv('a-directory')

Now you can mostly pretend that ``like_a_dictionary`` is a :py:class:`dict`,
except that it will persist across Python sessions.

Vlermv has many other features that you may read about below.

.. toctree::
   :maxdepth: 3

   vlermv
   cache
   serializers
   transformers
   acid
   recipes
   history

.. * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

