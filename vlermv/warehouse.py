import os, pickle

from pickle_warehouse.identifiers import parse as parse_identifier
from pickle_warehouse.fs import mktemp

try:
    FileNotFoundError
except NameError:
    OpenError = IOError
else:
    OpenError = FileNotFoundError

try:
    PermissionError
except NameError:
    class PermissionError(EnvironmentError):
        pass

try:
    FileNotFoundError
except NameError:
    DeleteError = OSError
else:
    DeleteError = FileNotFoundError

try:
    FileExistsError
except NameError:
    FileExistsError = OSError

def mkdir(fn):
    'Make a directory that will contain the file.'
    try:
        os.makedirs(os.path.split(fn)[0])
    except FileExistsError:
        pass

class Warehouse:
    '''
    :param cachedir: cachedir
    :param serializer: A thing with dump and load attribute functions,
        like pickle, json, yaml, dill, bson, 
        or anything in pickle_warehouse.serializers
    '''
    def __repr__(self):
        return 'Warehouse(%s)' % repr(self.cachedir)

    def __init__(self, cachedir, serializer = pickle, mutable = True, tempdir = None, memcache = False):
        self.cachedir = cachedir
        self.serializer = serializer
        self.mutable = mutable
        if tempdir == None:
            self.tempdir = os.path.join(cachedir, '.tmp')
        try:
            os.makedirs(self.tempdir)
        except FileExistsError:
            pass
        if not memcache:
            self.memcache = None
        else:
            self.memcache = {}
            for key, value in zip(self.keys(), self.values()):
                self.memcache[key] = value

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
        mkdir(fn)
        if (not self.mutable) and ((self.memcache != None and fn in self.memcache) or os.path.exists(fn)):
            raise PermissionError('This warehouse is immutable, and %s already exists.' % fn)
        else:
            tmp = mktemp(self.tempdir)
            with open(tmp, 'wb') as fp:
                self.serializer.dump(obj, fp)
            os.rename(tmp, fn)
            if self.memcache != None:
                self.memcache[fn] = obj

    def __getitem__(self, index):
        fn = self.filename(index)

        if self.memcache == None:
            return self._get_fn(fn)
        else:
            if fn not in self.memcache and index in self._keys():
                self.memcache[fn] = self._get_fn(fn)
            return self.memcache[fn]

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
            if self.memcache != None and fn in self.memcache:
                del(self.memcache[fn])

    def __contains__(self, index):
        fn = self.filename(index)
        if self.memcache == None:
            return os.path.isfile(fn)
        else:
            if fn not in self.memcache and os.path.isfile(fn):
                self.memcache[fn] = self._get_fn(fn)
            return fn in self.memcache

    def __len__(self):
        if self.memcache != None:
            return len(self.memcache)

        length = 0
        for dirpath, _, filenames in os.walk(self.cachedir):
            for filename in filenames:
                length += 1
        return length

    def keys(self):
        return self._keys() if self.memcache == None else map(os.path.relpath, self.memcache.keys())

    def _keys(self):
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

def _reversed_directories(outer, inner):
    while outer != inner:
        yield inner
        try:
            inner = os.path.split(inner)[0]
        except OSError:
            pass
