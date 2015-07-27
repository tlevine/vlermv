import os
from random import randint
from string import ascii_letters

from ._exceptions import DeleteError, PermissionError, out_of_space
from ._abstract import AbstractVlermv
from ._exceptions import OpenError

def _get_fn(fn, mode, load):
    '''
    Load a contents, checking that the file was not modified during the read.
    '''
    try:
        mtime_before = os.path.getmtime(fn)
    except OSError:
        mtime_before = None

    try:
        with open(fn, mode) as fp:
            item = load(fp)
    except OpenError:
        raise
    else:
        mtime_after = os.path.getmtime(fn)
        if mtime_before in {None, mtime_after}:
            return item
        else:
            raise EnvironmentError('File was edited during read: %s' % fn)


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

    def __init__(self, *directory, tempdir = '.tmp', **kwargs):
        '''
        :param str directory: Top-level directory of the vlermv
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
        super(Vlermv, self).__init__(**kwargs)
        self.base_directory = os.path.expanduser(os.path.join(*directory))
        self.tempdir = os.path.join(self.base_directory, tempdir)
        if self._mkdir:
            os.makedirs(self.tempdir, exist_ok = True)

    def __repr__(self):
        return 'Vlermv(%s)' % repr(self.base_directory)

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
            for fn in _reversed_directories(self.base_directory, os.path.dirname(fn)):
                if os.listdir(fn) == []:
                    os.rmdir(fn)
                else:
                    break

    def __len__(self):
        length = 0
        for dirpath, _, filenames in os.walk(self.base_directory):
            for filename in filenames:
                length += 1
        return length

    def keys(self):
        for dirpath, _, filenames in os.walk(self.base_directory):
            if dirpath != os.path.join(self.base_directory, self.tempdir):
                for filename in filenames:
                    path = self.from_filename(os.path.relpath(os.path.join(dirpath, filename), self.base_directory))
                    if path != None:
                        yield path
