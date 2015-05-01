Key transformers
----------------------------
Vlermv uses the rather basic :py:mod:`vlermv.transformers.simple`
transformer by default; ``str`` keys are mapped to file names inside of the
vlermv directory, and writing to subdirectories is not allowed.

More about the simple transformer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Other notes
~~~~~~~~~~~~~~~~~~
Specifying an absolute path, regardless of the transformer, will not let you
save things outside the vlermv directory. ::
