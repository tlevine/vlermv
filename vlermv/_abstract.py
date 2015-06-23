import os

from ._exceptions import PermissionError
from .serializers import pickle
from .transformers import magic
from ._util import safe_path

import logging

logger = logging.getLogger(__name__)

class AbstractVlermv:
    '''
    A :py:class:`dict` API to various things
    '''

    @classmethod
    def memoize(Class, *args, **kwargs):
        '''
        Memoize/record a function inside this vlermv. ::

            @Vlermv.cache('~/.http')
            def get(url):
                return requests.get(url, auth = ('username', 'password'))

        The args and kwargs get passed to the Vlermv with some slight changes.
        Here are the changes.

        First, the default ``key_transformer`` is the tuple key_transformer
        rather than the simple key_transformer.

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
            v = Class(*_args, **kwargs)
            v.func = func
            return v
        return decorator

    serializer = pickle
    key_transformer = magic
    appendable = True
    mutable = True
    tempdir = '.tmp'
    cache_exceptions = False
    base_directory = ''

    def __init__(self, **kwargs):
        '''
        :param str base_directory: Top-level directory of the vlermv
        :param serializer: A thing with dump and load functions for
            serializing and deserializing Python objects,
            like :py:mod:`json`, :py:mod:`yaml`, or
            anything in :py:mod:`vlermv.serializers`
        :type serializer: :py:mod:`serializer <vlermv.serializers>`
        :param key_transformer: A thing with to_path and from_path functions
            for transforming keys to file paths and back.
            Several are available in :py:mod:`vlermvtransformers`.
        :type key_transformer: :py:mod:`key_transformer <vlermvtransformers>`
        :param bool mutable: Whether values can be updated and deleted
        :param str tempdir: Subdirectory inside of base_directory to use for temporary files

        These are mostly relevant for initialization via :py:func:`vlermv.cache`.

        :param bool appendable: Whether new values can be added to the Vlermv
            (Set this to False to ensure that the decorated function is never
            run and that the all results are cached; this is useful for reviewing
            old data in a read-only mode.)
        :param bool cache_exceptions: If the decorated function raises
            an exception, should the failure and exception be cached?
            The exception is raised either way.
        :raises TypeError: If cache_exceptions is True but the serializer
            can't cache exceptions
        '''
        for key in ['serializer', 'appendable', 'mutable', 'base_directory',
                    'key_transformer', 'cache_exceptions']:
            setattr(self, key, kwargs.get(key, getattr(self.__class__, key)))

        if self.cache_exceptions and not getattr(self.serializer, 'cache_exceptions', True):
            msg = 'Serializer %s cannot cache exceptions.'
            raise TypeError(msg % repr(self.serializer))

        self.binary_mode = getattr(self.serializer, 'binary_mode', False)
        self.func = None

    def __call__(self, *args, **kwargs):
        if not self.func:
            msg = 'Set %s.func to something if you want to call %s.'
            raise NotImplementedError(msg % (self, self))
        if args in self:
            output = self[args]
        else:
            try:
                result = self.func(*args, **kwargs)
            except Exception as error:
                signature = self.__class__.__name__, self.func.__name__, args, kwargs
                msg = 'Exception in %s calling this memoized function:\n%s(*%s, *%s)' % signature
                logger.error(msg, exc_info = False)
                if self.cache_exceptions:
                    output = error, None
                else:
                    raise error
            else:
                if self.cache_exceptions:
                    output = None, result
                else:
                    output = result
            self[args] = output

        if self.cache_exceptions:
            if len(output) != 2:
                msg = '''Deserializer returned %d elements,
but it is supposed to return only two (exception, object).
Perhaps the serializer doesn't implement exception caching properly?'''
                raise TypeError(msg % len(output))

            error, result = output
            if error != None and result != None:
                raise TypeError('''The exception or the object (or both) must be None.
There's probably a problem with the serializer.''')

            if error:
                raise error
        else:
            result = output

        return result

    def filename(self, index):
        '''
        Get the filename corresponding to a key; that is, run the
        key_transformer on the key.

        :raises TypeError: if the key_transformer returns something other than
            a :py:class:`tuple` of :py:class:`strings <str>`
        :raises KeyError: if the key_transformer returns an empty path
        :returns: the filename
        :rtype: str
        '''
        subpath = self.key_transformer.to_path(index)
        if not isinstance(subpath, tuple):
            msg = 'subpath is a %s, but it should be a tuple.'
            raise TypeError(msg % type(subpath).__name__)
        elif len(subpath) == 0:
            raise KeyError('You specified an empty key.')
        elif not all(isinstance(x, str) for x in subpath):
            msg = 'Elements of subpath should all be str; here is subpath:\n%s' % repr(subpath)
            raise TypeError(msg)
        return os.path.join(self.base_directory, *safe_path(subpath))

    def __iter__(self):
        return (k for k in self.keys())

    def _b(self):
        return 'b' if self.binary_mode else ''

    def __delitem__(self, index):
        if not self.mutable:
            raise PermissionError('This warehouse is immutable, so you can\'t delete things.')

    def __contains__(self, index):
        fn = self.filename(index)
        return os.path.isfile(fn)

    def values(self):
        for key, value in self.items():
            yield value

    def update(self, d):
        generator = d.items() if hasattr(d, 'items') else d
        for k, v in generator:
            self[k] = v

    def get(self, index, default = None):
        if index in self:
            return self[index]
        else:
            return default

    def items(self):
        for key in self.keys():
            yield key, self[key]
