Using Vlermv as an archive rather than a cache
===============================================

I find that I often want to download a webpage every day and save the result
every day. For example, I'm presently working on something that involves
downloading an RSS feed that changes daily, and I'm using a function that
goes like this. ::

    import requests
    def feed():
        return requests.get('http://example.com/feed.rss')

The RSS feed is always in the same place, but its contents change based on
what new articles have been added. I'm going to do lots of stuff based on
the RSS feed that I download, so I want to save it for future reference.

That is what :py:class:`vlermv.transformers.archive` is for.

.. py:class:`vlermv.transformers.archive`


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

But we know enough about the state of the world to give it a meaningful
name in our records. Each moment in time corresponds to a unique state
of the world (ignoring quantum effects and special relativity and other
things that I don't understand), so we can record simply the date and
time at which a function was run rather than recoring the entire state
of the world. :py:func:`~vlermv.transformers.archive` appends the
datetime at which a function was run to the path emitted by the
:py:mod:`transformer <vlermv.transformers>` that it wraps.

How it works
----------------------
:py:class:`~vlermv.Vlermv` cannot save an object whose path is empty;
if it received an empty path, it would not know what the filename should be.
:py:func:`~vlermv.cache` uses the decorated function's arguments as a
key, so the key will be an empty tuple if your function takes no arguments.
With the default tuple transformer, this empty tuple turns into an empty
path, and an error is raised.

:py:func:`~vlermv.transformers.archive` changes the transformer to add
the date to the path; this way, the path won't be empty.
