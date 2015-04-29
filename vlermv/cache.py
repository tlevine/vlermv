import os
from functools import partial

from .warehouse import Vlermv

class VlermvCache(Vlermv):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        kwargs = dict(kwargs)
        self.transformer = kwargs.pop('transformer', lambda x: x)
        # Add some tests for this based on immaterial-digital-labor

        if len(args) == 0:
            cachedir = func.__name__
        else:
            cachedir = os.path.expanduser(args[0])
            args = args[1:]

        Vlermv.__init__(self, cachedir, *args, **kwargs)

    def __repr__(self):
        return 'VlermvCache (%s)' % self.cachedir

    def __call__(self, *args, **kwargs):
        _args = self.transformer(args)
        if _args in self:
            output = self[_args]
        else:
            try:
                result = self.func(*args, **kwargs)
            except Exception as error:
                output = error, None
            else:
                output = None, result
            self[_args] = output
        error, result = output
        if error == None:
            return result
        else:
            raise error

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
