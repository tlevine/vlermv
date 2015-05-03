Vlermv
==================================
.. py:module:: vlermv

Vlermv provides a dictionary-like object that is associated with a particular
directory on your computer. Here's an introduction in six lines of Python.

Install from PyPI. ::

    pip install vlermv

Then call :py:class:`vlermv.Vlermv` like this. ::

    from vlermv import Vlermv
    like_a_dictionary = Vlermv('a-directory')

Now you can mostly pretend that :py:obj:`like_a_dictionary` is a :py:class:`dict`,
except that it will persist across Python session.

Alternatively, you can cache a function's results with :py:func:`vlermv.cache`. ::

    @cache()
    def f(x):
        return x + 8

Vlermv has many other features that you may read about below.

.. toctree::
   :maxdepth: 3

   vlermv
   cache
   serializers
   archive
   transformers
   acid
   recipes
   history

.. * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

