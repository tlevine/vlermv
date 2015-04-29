import os
from functools import partial

from .warehouse import Vlermv

def cache(*args, **kwargs):
    '''
    Cache a function with a vlermv.Vlermv.

    :param cache_exceptions: If the decorated function raises an exception,
        should the failure and exception be cached? The exception is raised
        either way.

    Decorate the function with @cache(*args, **kwargs).
    The args and kwargs get passed to the Vlermv.
    For example::

        @cache('~/.http')
        def get(url):
            return requests.get(url, auth = ('username', 'password'))

    vlermv.Vlermv would ordinarily fail if
    no arguments were passed to it. If you pass no arguments
    to cache, the Vlermv directory argument (the one
    required argument) will be set to the name of the function.
    '''
    return lambda func: VlermvCache(func, *args, **kwargs)
