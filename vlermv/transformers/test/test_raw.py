import pytest

from .. import raw

testcases = [
    ('abc', ('abc',)),
    ('abc/def', ('abc', 'def')),
    ('abc/def/', ('abc', 'def')),
    ('/abc/def/', ('abc', 'def')),
]

@pytest.mark.parametrize('left, right', testcases)
def test_to_path(left, right):
    assert raw.to_path(left) == right

@pytest.mark.parametrize('left, right', testcases)
def test_from_path(left, right):
    assert left.strip('/') == raw.from_path(right)
