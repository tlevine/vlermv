import os
from random import randint
from string import ascii_letters

from ._exceptions import DeleteError, PermissionError
from ._abstract import AbstractVlermv
from ._util import split, _get_fn

def _random_file_name():
    n = len(ascii_letters) - 1
    return ''.join(ascii_letters[randint(0, n)] for _ in range(10))

def mktemp(tempdir, filename = _random_file_name):
    try:
        os.makedirs(tempdir, exist_ok = True)
    except TypeError:
        # Python 2
        if not os.path.isdir(tempdir):
            os.makedirs(tempdir)
    return os.path.join(tempdir, filename())

def _reversed_directories(outer, inner):
    while outer != inner:
        yield inner
        inner = os.path.dirname(inner)

class Vlermv(AbstractVlermv):
    '''
    A :py:class:`dict` API to a filesystem
    '''

    #: Should the cache directory be created when a Vlermv is initialized?
    #: This is is mostly relevant for testing.
    _mkdir = True

    def __repr__(self):
        return 'Vlermv(%s)' % repr(self.cachedir)

    def __setitem__(self, index, obj):
        fn = self.filename(index)
        os.makedirs(os.path.dirname(fn), exist_ok = True)
        exists = os.path.exists(fn)
        if (not self.mutable) and exists:
            raise PermissionError('This warehouse is immutable, and %s already exists.' % fn)
        elif (not self.appendable) and (not exists):
            raise PermissionError('This warehouse not appendable, and %s does not exist.' % fn)
        else:
            tmp = mktemp(self.tempdir)
            with open(tmp, 'w' + self._b()) as fp:
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
        return _get_fn(self.filename(index), 'r' + self._b(), self.serializer.load)

    def __delitem__(self, index):
        super(Vlermv, self).__delitem__(index)
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
                    path = split(os.path.relpath(os.path.join(dirpath, filename), self.cachedir))
                    yield self.transformer.from_path(path)

    def items(self):
        for key in self.keys():
            yield key, self[key]
