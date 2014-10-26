import os
import functools

from .warehouse import Vlermv

class CachedFunction(Vlermv):
    def __init__(self):
        raise NotImplementedError
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

def cache(*args, **kwargs):
    '''
    Cache a function with a pickle_warehouse.Warehouse.

    Decorate the function with @cache(*args, **kwargs).
    The args and kwargs get passed to the Warehouse.
    For example::

        @cache('~/.http')
        def get(url):
            return requests.get(url, auth = ('username', 'password'))

    pickle_warehouse.Warehouse would ordinarily fail if
    no arguments were passed to it. If you pass no arguments
    to cache, the Warehouse directory argument (the one
    required argument) will be set to the name of the function.
    '''

    def decorator(args, kwargs, func):
        if len(args) == 0:
            cachedir = func.__name__
        else:
            cachedir = os.path.expanduser(args[0])
            args = args[1:]
        warehouse = Vlermv(cachedir, *args, **kwargs)
        def wrapper(*_args, **_kwargs):
            if _args in warehouse:
                output = warehouse[_args]
            else:
                try:
                    result = func(*_args, **_kwargs)
                except Exception as error:
                    output = error, None
                else:
                    output = None, result
                warehouse[_args] = output
            error, result = output
            if error == None:
                return result
            else:
                raise error
        return wrapper
    return functools.partial(decorator, args, kwargs)
