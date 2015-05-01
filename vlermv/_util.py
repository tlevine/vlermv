import os

from ._exceptions import OpenError

def split(path):
    'Split a path into a tuple of all directories and then the final directory/file.'
    if path == '':
        raise ValueError('Path may not be empty.')

    dn, fn = os.path.split(path)
    if fn == '':
        return (dn,)
    elif dn == '':
        return (fn,)
    else:
        return split(dn) + (fn,)

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
    except OpenError as e:
        raise KeyError(*e.args)
    else:
        mtime_after = os.path.getmtime(fn)
        if mtime_before in {None, mtime_after}:
            return item
        else:
            raise EnvironmentError('File was edited during read: %s' % fn)

def method_or_name(namespace, x):
    '''
    If x is a ``str``, get ``namespace.x``.

    Otherwise, simply return ``x``.
    '''
    if not isinstance(x, str):
        return x

    if hasattr(namespace, x):
        return getattr(namespace, x)

    attrs = [y for y in dir(namespace) if not y.startswith('_')]
    msg = '''"%s" is not available in %s.
These attributes are available: %s.''' % (x, namespace.__name__, attrs)
    raise AttributeError(msg)

def safe_path(dirpath, filename, root):
    if unsafe.startswith('/'):
        unsafe = unsafe[1:]
    unsafe = os.path.relpath(os.path.join(dirpath, filename), root)

    if not os.path.abspath(os.path.join(root, unsafe)).startswith(root):
        msg = 'Path %s references a directory above the starting directory.\nThis is not allowed.'
        raise ValueError(msg % unsafe)
