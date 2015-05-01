import pytest

from .. import simple

def test_to_path():
    assert simple.to_path('abc') == ('abc',)
    with pytest.raises(ValueError):
        simple.to_path('abc/def')

def test_from_path():
    with pytest.raises(ValueError):
        simple.from_path(('abc', 'def'))
