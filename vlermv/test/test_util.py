import pytest

from ..util import split

testcases = [
    ('/', ('/',)),
    ('/abc', ('/', 'abc',)),
    ('123/abc', ('123', 'abc',)),
]

def test_empty():
    '''
    An error should be raised when you try to split an empty path.
    '''
    with pytest.raises(ValueError):
        split('')


@pytest.mark.parametrize('path,expected', testcases)
def test_split(path, expected):
    assert split(path) == expected
