import pytest

from .. import tuple

def test_to_path():
    assert tuple.to_path(('a',)) == ('a',)

def test_to_path_int():
    with pytest.raises(TypeError):
        tuple.to_path((8,))

def test_from_path():
    assert tuple.from_path(('a',)) == ('a',)
