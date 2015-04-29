import os, pickle

from .serializers import identity
from .transformers import magic
from .fs import mktemp, _random_file_name, _reversed_directories
from .exceptions import (
    OpenError, PermissionError,
    DeleteError, FileExistsError,
    out_of_space,
)

class Vlermv:
    '''
    Fancy dictionary database

    :param cachedir: Top-level directory of the vlermv
    :param serializer: A thing with dump and load attribute functions,
        like pickle, json, yaml, dill, bson, 
        or anything in vlermv.serializers
    :param transformer: Function to transform keys to filenames.
        The identity function is used by default, other options include
        vlermv.transformers.magic and vlermv.transformers.base64.
    :param mutable: Whether values can be updated and deleted
    :param tempdir: Directory to use for temporary files

    This one is only relevant for initialization via ``vlermv.cache``.

    :param cache_exceptions: If the decorated function raises an exception,
        should the failure and exception be cached? The exception is raised
        either way.

    '''
    def __repr__(self):
        return 'Vlermv(%s)' % repr(self.cachedir)

    def __init__(self, cachedir,
            serializer = identity(binary = True), mutable = True,
            tempdir = '.tmp', transformer = lambda x: x,
            cache_exceptions = False):

        if cache_exceptions and not getattr(serializer, 'cache_exceptions', False):
            msg = 'Serializer %s cannot cache exceptions.'
            raise TypeError(msg % repr(serializer))

        # Default function, if called with ``Vlermv`` rather than ``cache``.
        self.func = self.__getitem__

        self.cachedir = os.path.expanduser(cachedir)
        self.serializer = serializer
        self.mutable = mutable
        self.transformer = transformer
        self.tempdir = os.path.join(self.cachedir, tempdir)
        self.cache_exceptions = cache_exceptions

        os.makedirs(self.tempdir, exist_ok = True)

    def __call__(self, *args, **kwargs):
        _args = self.transformer(args)
        if _args in self:
            output = self[_args]
        else:
            try:
                result = self.func(*args, **kwargs)
            except Exception as error:
                if self.cache_exceptions:
                    output = error, None
                else:
                    raise error
            else:
                output = None, result
            self[_args] = output

        if self.cache_exceptions:
            error, result = output
            if error:
                raise error
        else:
            result = output

        return result

    def filename(self, index):
        subpath = parse_identifier(index)
        if subpath == []:
            raise KeyError('You specified an empty key.')
        else:
            return os.path.join(self.cachedir, *subpath)

    def __iter__(self):
        return (k for k in self.keys())

    def __setitem__(self, index, obj):
        fn = self.filename(index)
        os.makedirs(os.path.dirname(fn), exist_ok = True)
        if (not self.mutable) and os.path.exists(fn):
            raise PermissionError('This warehouse is immutable, and %s already exists.' % fn)
        else:
            tmp = mktemp(self.tempdir)
            with open(tmp, 'wb') as fp:
                try:
                    self.serializer.dump(obj, fp)
                except Exception as e:
                    if out_of_space(e):
                        fp.close()
                        os.remove(tmp)
                        raise BufferError('Out of space')
                    else:
                        raise
            os.rename(tmp, fn)

    def __getitem__(self, index):
        fn = self.filename(index)

        return self._get_fn(fn)

    def _get_fn(self, fn):
        try:
            mtime_before = os.path.getmtime(fn)
        except OSError:
            mtime_before = None

        try:
            with open(fn, 'rb') as fp:
                item = self.serializer.load(fp)
        except OpenError as e:
            raise KeyError(*e.args)
        else:
            mtime_after = os.path.getmtime(fn)
            if mtime_before == mtime_after:
                return item
            else:
                raise EnvironmentError('File was edited during read: %s' % fn)

    def __delitem__(self, index):
        if not self.mutable:
            raise PermissionError('This warehouse is immutable, so you can\'t delete things.')

        fn = self.filename(index)
        try:
            os.remove(fn)
        except DeleteError as e:
            raise KeyError(*e.args)
        else:
            for fn in _reversed_directories(self.cachedir, os.path.dirname(fn)):
                if os.listdir(fn) == []:
                    os.rmdir(fn)
                else:
                    break

    def __contains__(self, index):
        fn = self.filename(index)
        return os.path.isfile(fn)

    def __len__(self):
        length = 0
        for dirpath, _, filenames in os.walk(self.cachedir):
            for filename in filenames:
                length += 1
        return length

    def keys(self):
        for dirpath, _, filenames in os.walk(self.cachedir):
            if dirpath != os.path.join(self.cachedir, self.tempdir):
                for filename in filenames:
                    yield os.path.relpath(os.path.join(dirpath, filename), self.cachedir)

    def values(self):
        for key, value in self.items():
            yield value

    def items(self):
        for key in self.keys():
            yield key, self[key]

    def update(self, d):
        generator = d.items() if hasattr(d, 'items') else d
        for k, v in generator:
            self[k] = v

    def get(self, index, default = None):
        if index in self:
            return self[index]
        else:
            return default
