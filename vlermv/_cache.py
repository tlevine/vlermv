from functools import partial

from .transformers import tuple as _tuple, magic, archive
from ._vlermv import Vlermv

def cache(*args, key_transformer = _tuple, **kwargs):
    '''
    Cache a function with a :py:class:`~vlermv.Vlermv`. ::

        @cache('~/.http')
        def get(url):
            return requests.get(url, auth = ('username', 'password'))

    The args and kwargs get passed to the Vlermv with some slight changes.
    Here are the changes.

    First, the default ``key_transformer`` is the tuple transformer
    rather than the simple transformer.

    Second, it is valid for cache to be called without arguments.
    Vlermv would ordinarily fail if no arguments were passed to it.
    If you pass no arguments to cache, the Vlermv directory argument
    (the one required argument) will be set to the name of the function.

    Third, you are more likely to use the ``cache_exceptions`` keyword
    argument; see :py:class:`~vlermv.Vlermv` for documentation on that.
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

def archive(*args, key_transformer = magic, **kwargs):
    '''
    A thin wrapper with reasonable defaults archival caches based on
    :py:func:`vlermv.cache` and :py:func:`vlermv.serializers.archive`
    '''
    return cache(*args, key_transformer = archive(magic), **kwargs)
