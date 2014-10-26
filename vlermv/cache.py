import os
from functools import partial

from .warehouse import Vlermv

class VlermvCache(Vlermv):
    def __init__(self, func, *args, **kwargs):
        self.func = func

        if len(args) == 0:
            cachedir = func.__name__
        else:
            cachedir = os.path.expanduser(args[0])
            args = args[1:]

       #Vlermv = super(VlermvCache, self).
        Vlermv.__init__(self, cachedir, *args, **kwargs)

    def __repr__(self):
        return 'VlermvCache (%s)' % self.cachedir

    def __call__(self, *args, **kwargs):
        if args in self:
            output = self[args]
        else:
            try:
                result = self.func(*args, **kwargs)
            except Exception as error:
                output = error, None
            else:
                output = None, result
            self[args] = output
        error, result = output
        if error == None:
            return result
        else:
            raise error

def cache(*args, **kwargs):
    '''
    Cache a function with a vlermv.Vlermv.

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
    return partial(_decorator, args, kwargs)

def _decorator(args, kwargs, func):
    return VlermvCache(func, *args, **kwargs)
