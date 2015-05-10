.. _archive:

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

The above implementation is not acceptable because it will always use the
same cache of the data. If we ran it for the first time three weeks ago,
it will always use that result. The RSS feed changes, so this doesn't work.

How to
----------
Here's how I implement this archive. ::

    import requests, vlermv

    @vlermv.cache()
    def feed(date):
        '''
        The date parameter is today's date. It is here only for affecting
        the cache file's name; we don't use it in the feed function.
        '''
        return requests.get('http://example.com/feed.rss')

Then I call it like this. ::

    import datetime
    response = feed(datetime.datetime.today())

If I want to access today's data, I can do this. ::

    feed[datetime.date.today()]

And if I want to access historical data, I do this. ::

    feed[datetime.date(2015,3,23)]

How to think about it
----------------------------
Consider the following function. ::

    def is_hackerspace_door_open():
        return reading_to_the_pin_on_my_microcontroller() == HIGH

This function takes no arguments, but its value might change if you run
it several times (especially if you open or close the door). This is
because the function really does implicitly have an argument: the state
of the entire world at the moment that the function is run.

We don't put it in the function signature because we don't have a good
way of encoding the entire state of the world and thus can only run the
function on the present state of the world.

But we know enough about the state of the world to give it a meaningful
name in our records. Each moment in time corresponds to a unique state
of the world (ignoring quantum effects and special relativity and other
things that I don't understand), so we can record simply the date and
time at which a function was run rather than recoring the entire state
of the world.

**Instead of passing the entire state of the world to the function, we pass
the present date.**

Also, we can round the present date. The world is always changing, but we
have some idea as to how it changes. In the present example, let's say that
we know that the RSS feeds tend to change once every few days and that we
are okay with our data being at most a day out-of-date. By rounding to day
(rather than hour or millisecond, for example), we allow our script to run
twice in the same day and use the cached RSS feed on the second run. This
can be very helpful for debugging.
