import tempfile

import pytest

from ..util import split, _get_fn

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
        with open(fp.name, 'w') as fp2:
            fp2.write('other-process')
        return fp.read()

    with tempfile.NamedTemporaryFile('w') as tmp:
        tmp.file.write('this-process')
        tmp.file.close()
        with pytest.raises(EnvironmentError):
            _get_fn(tmp.name, 'r', f)
