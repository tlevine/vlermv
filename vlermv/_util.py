import os, posixpath

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

def safe_path(unsafe_path, not_allowed = {'', '.'}):
    unsafe_str = posixpath.join('', *unsafe_path)
    rough_tuple = posixpath.join('/', posixpath.normpath(unsafe_str)).split('/')[1:]
    safe_tuple = tuple(x for x in rough_tuple if x not in not_allowed)

    if len(safe_tuple) == 0:
        raise ValueError('Path must not be empty.')
    elif safe_tuple[0] == '..':
        raise ValueError('Relative paths above the starting directory (./..) are not allowed.')
    else:
        return safe_tuple
