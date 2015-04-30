import os

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
        if mtime_before == mtime_after:
            return item
        else:
            raise EnvironmentError('File was edited during read: %s' % fn)
