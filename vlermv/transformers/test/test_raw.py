import pytest

from .. import raw

testcases_str = [
    ('abc', ('abc',)),
    ('abc/def', ('abc', 'def')),
    ('abc/def/', ('abc', 'def')),
    ('/abc/def/', ('abc', 'def')),
]

@pytest.mark.parametrize('left, right', testcases_str)
def test_to_path(left, right):
    assert raw.to_path(left) == right

@pytest.mark.parametrize('left, right', testcases_str)
def test_from_path(left, right):
    assert left.strip('/') == raw.from_path(right)

testcases_tuple = [
    (('abc/def',), ('abc', 'def')),
    (('abc', 'def'), None),
]

@pytest.mark.parametrize('left, right', testcases_tuple)
def test_tuple(left, right):
    if right == None:
        with pytest.raises(TypeError):
            raw.to_path(left)
    else:
        assert raw.to_path(left) == right
