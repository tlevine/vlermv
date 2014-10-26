import os

from .warehouse import Vlermv

class CachedFunction(Vlermv):
    def __init__(self, warehouse, func):
        self.warehouse = warehouse
        self.func = func

    def __call__(self, *args, **kwargs):
        if args in self.warehouse:
            output = self.warehouse[args]
        else:
            try:
                result = self.func(*args, **kwargs)
            except Exception as error:
                output = error, None
            else:
                output = None, result
            self.warehouse[args] = output
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
    def _decorator(func):
        if len(args) == 0:
            cachedir = func.__name__
        else:
            cachedir = os.path.expanduser(args[0])
            args = args[1:]
        warehouse = Vlermv(cachedir, *args, **kwargs)
        return CachedFunction(warehouse, func)
    return _decorator
