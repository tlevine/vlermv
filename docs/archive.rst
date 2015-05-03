Using Vlermv as an archive rather than a cache
===============================================

.. I should change the name of the function "cache"
   Oooh maybe I just make vlermv.Vlermv() a decorator!

I find that I often want to download a webpage every day and save the result
every day. For example, I want to look for new [smoethings] every day on
[website]. Once I download the homepage of this website, I get the URLs for
each [something], and I can use :py:func:`~vlermv.cache`, but how do I save
the homepage?

That is what :py:func:`vlermv.transformers.archive` is for.

.. py:func:`vlermv.transformers.archive`


How to think about it
----------------------------
Consider the following function. ::

    def is_hackerspace_door_open():
        return reading_to_the_pin_on_my_microcontroller() == HIGH

This function takes no arguments, but its value might change if you run
it several times (especially if you open or close the door). This is
because the function really does have an argument, *implicitly*: the state
of the entire world at the moment that the function is run.

We don't put it in the function signature because we don't have a good
way of encoding the entire state of the world and thus can only run the
function on the present state of the world.

*the date at which a function is run* to functions
like this.
Moreover, the date is usually very meaningful for functions like this;
When functions give different results on different runs, it is because the
state of the world has changed between the different runs.




How it works
----------------------
:py:class:`~vlermv.Vlermv` only save things if its keys aren't empty.
:py:func:`~vlermv.cache` uses the decorated function's arguments as a
key, so it is possible that the key will be an empty tuple.
:py:func:`~vlermv.transformers.archive` changes the transformer to add
the date to the path; this way, the path won't be empty.




works when you can form a meaningful
filename from the arguments to the function you are decorating. Sometimes
you can't.


.. py:data:`archive_minutely`
.. py:data:`archive_hourly`
.. py:data:`archive_daily`
.. py:data:`archive_weekly`
.. py:data:`archive_yearly`

The archive decorator simply manipulates the path after the
::::`transformer` has been applied.

There are three components to the archive setting.

Interval
    millisecond, second, minute, hour, day, week, month, default is day
append_random
    Whether to append a random number after the date, just in case there
    are multiple calls within the same millisecond, default is False
position
    left (at the beginning of the path), right (end), replace, default is left

@cache(transformer = vlermv.transformers.archive(vlermv.transformers.tuple)
