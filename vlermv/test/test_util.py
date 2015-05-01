import tempfile, time

import pytest

from .._util import split, _get_fn, method_or_name, safe_path, _root

def test_split_empty():
    '''
    An error should be raised when you try to split an empty path.
    '''
    with pytest.raises(ValueError):
        split('')

testcases_split = [
    ('/', ('/',)),
    ('/abc', ('/', 'abc',)),
    ('123/abc', ('123', 'abc',)),
]

@pytest.mark.parametrize('path,expected', testcases_split)
def test_split(path, expected):
    assert split(path) == expected

def test_get_fn_success():
    with tempfile.NamedTemporaryFile('w') as tmp:
        tmp.file.write('abc')
        tmp.file.close()
        assert 'abc' == _get_fn(tmp.name, 'r', lambda fp: fp.read())

def test_get_fn_fail():
    def f(fp):
        time.sleep(0.1) # so mtime changes
        with open(fp.name, 'w') as fp2:
            fp2.write('other-process')
        return fp.read()

    with tempfile.NamedTemporaryFile('w') as tmp:
        tmp.file.write('this-process')
        tmp.file.close()
        with pytest.raises(EnvironmentError):
            _get_fn(tmp.name, 'r', f)

def test_method_or_name_not_str():
    class namespace:
        attribute = 8
    assert method_or_name(namespace, [2,9]) == [2,9]

def test_method_or_name_valid_str():
    class namespace:
        attribute = 8
    assert method_or_name(namespace, 'attribute') == 8

def test_method_or_name_invalid_str():
    class namespace:
        attribute = 8
    with pytest.raises(AttributeError):
        method_or_name(namespace, 'not_attribute')

import ntpath, posixpath, macpath
tuple_path_testcases = [
    ('/home/abc', 'home/abc'),
    ('/abc/../../..', '.'),
    ('/abc', 'abc'),
    ('/abc/def', 'abc/def'),
]

def check_safe_path(pathmodule, unsafe_path, expected):
    observed = safe_path(unsafe_path, pathmodule = pathmodule,
                         root = _root(pathmodule))
    assert observed == expected.replace('/', pathmodule.sep)

def test_safe_path_type():
    with pytest.raises(ValueError):
        safe_path('not/absolute/path', pathmodule = posixpath, root = '/')

@pytest.mark.parametrize('unsafe_path, expected', tuple_path_testcases)
def test_safe_path_posix(unsafe_path, expected):
    check_safe_path(posixpath, unsafe_path, expected)

@pytest.mark.parametrize('unsafe_path, expected', tuple_path_testcases)
def test_safe_path_nt(unsafe_path, expected):
    check_safe_path(ntpath, unsafe_path, expected)

#@pytest.mark.parametrize('unsafe_path, expected', tuple_path_testcases)
#def test_safe_path_mac(unsafe_path, expected):
#    check_safe_path(macpath, unsafe_path, expected)
