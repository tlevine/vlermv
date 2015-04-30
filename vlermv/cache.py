from functools import partial

from .transformers import tuple as _tuple
from .vlermv import Vlermv

def cache(*args, key_transformer = _tuple, **kwargs):
    '''
    Cache a function with a vlermv.Vlermv.

    When you decorate a function with @cache(*args, **kwargs).
    The args and kwargs get passed to the Vlermv. For example::

        @cache('~/.http')
        def get(url):
            return requests.get(url, auth = ('username', 'password'))

    The arguments are slightly different from those of Vlermv.

    First, the default ``key_transformer`` is the tuple transformer
    rather than the simple transformer.

    Second, it is valid for cache to be called without arguments.
    vlermv.Vlermv would ordinarily fail if no arguments were passed to it.
    If you pass no arguments to cache, the Vlermv directory argument
    (the one required argument) will be set to the name of the function.

    Third, you are more likely to use the ``cache_exceptions`` keyword
    argument; see help(Vlermv) for documentation on that.
    '''
    def decorator(func):
        if len(args) == 0:
            _args = (func.__name__,)
        else:
            _args = args
        v = Vlermv(*_args, key_transformer = key_transformer, **kwargs)
        v.func = func
        return v
    return decorator
