import os

from ._exceptions import PermissionError
from .serializers import pickle
from .transformers import magic
from ._util import safe_path

class AbstractVlermv:
    '''
    A :py:class:`dict` API to various things
    '''

    def __init__(self,
            serializer = pickle,
            key_transformer = magic,
            appendable = True,
            mutable = True,
            tempdir = '.tmp',
            cache_exceptions = False):
        '''
        :param str base_directory: Top-level directory of the vlermv
        :param serializer: A thing with dump and load functions for
            serializing and deserializing Python objects,
            like :py:mod:`json`, :py:mod:`yaml`, or
            anything in :py:mod:`vlermv.serializers`
        :type serializer: :py:mod:`serializer <vlermv.serializers>`
        :param key_transformer: A thing with to_path and from_path functions
            for transforming keys to file paths and back.
            Several are available in :py:mod:`vlermv.transformers`.
        :type key_transformer: :py:mod:`transformer <vlermv.transformers>`
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

        if cache_exceptions and not getattr(serializer, 'cache_exceptions', True):
            msg = 'Serializer %s cannot cache exceptions.'
            raise TypeError(msg % repr(serializer))

        self.binary_mode = getattr(serializer, 'binary_mode', False)

        self.func = None

        self.serializer = serializer
        self.appendable = appendable
        self.mutable = mutable
        self.transformer = key_transformer
        self.cache_exceptions = cache_exceptions

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
        transformer on the key.

        :raises TypeError: if the transformer returns something other than
            a :py:class:`tuple` of :py:class:`strings <str>`
        :raises KeyError: if the transformer returns an empty path
        :returns: the filename
        :rtype: str
        '''
        subpath = self.transformer.to_path(index)
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
