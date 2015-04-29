import os, pickle

from .identifiers import parse as parse_identifier
from .fs import mktemp, _random_file_name, _reversed_directories
from .exceptions import (
    OpenError, PermissionError,
    DeleteError, FileExistsError,
    out_of_space,
)

class Vlermv:
    '''
    :param cachedir: Top-level directory of the vlermv
    :param serializer: A thing with dump and load attribute functions,
        like pickle, json, yaml, dill, bson, 
        or anything in vlermv.serializers
    :param mutable: Whether values can be updated and deleted
    :param tempdir: Directory to use for temporary files
    :param buffer: Size of the buffer in megabytes
    '''
    def __repr__(self):
        return 'Vlermv(%s)' % repr(self.cachedir)

    def __init__(self, cachedir, serializer = pickle, mutable = True, tempdir = '.tmp', buffer = 10):
        self.cachedir = cachedir
        self.serializer = serializer
        self.mutable = mutable
        self.tempdir = os.path.join(cachedir, tempdir)
        try:
            os.makedirs(self.tempdir)
        except FileExistsError:
            pass

        # Create buffer file
        mb = b'\x00' * int(1e6)
        self.buffer_file = os.path.join(self.tempdir, 'buffer')
        with open(self.buffer_file, 'wb') as fp:
            try:
                for i in range(buffer):
                    fp.write(mb)
            except Exception as e:
                if out_of_space(e):
                    fp.close()
                    os.remove(self.buffer_file)
                    msg = 'There isn\'t enough space to write the buffer file'
                    raise BufferError(msg)
                else:
                    raise

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
                        raise BufferError('Nearly out of space')
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
            for fn in _reversed_directories(self.cachedir, os.path.split(fn)[0]):
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
            if dirpath != os.path.join(self.cachedir, '.tmp'):
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
