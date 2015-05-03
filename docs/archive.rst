Using Vlermv as an archive rather than a cache
===============================================

.. I should change the name of the function "cache"
   Oooh maybe I just make vlermv.Vlermv() a decorator!

.. py:func:`vlermv.archive`

The :py:func:`~vlermv.cache` decorator works when you can form a meaningful
filename from the arguments to the function you are decorating. Sometimes
you can't.

I find that I often want to download a webpage every day and save the result
every day. For example, I want to look for new [smoethings] every day on
[website]. Once I download the homepage of this website, I get the URLs for
each [something], and I can use :py:func:`~vlermv.cache`, but how do I save
the homepage?

That is what the :py:func:`~vlermv.archive` [argument? decorator?] is for.

.. py:data:`archive_minutely`
.. py:data:`archive_hourly`
.. py:data:`archive_daily`
.. py:data:`archive_weekly`
.. py:data:`archive_yearly`

The archive decorator simply manipulates the path after the
::::`transformer` has been applied.

There are three components to the archive setting.

Interval
    millisecond, second, minute, hour, day, week, month
append_random
    Whether to append a random number after the date, just in case there
    are multiple calls within the same millisecond
position
    left (at the beginning of the path), right (end), replace
