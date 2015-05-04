from itertools import product

import pytest

from .. import ( tuple, archive )


@pytest.mark.parametrize('position', ['left', 'right'])
def test_position(position):
    key = (1, 2, 3)
    class t:
        @staticmethod
        def from_path(_):
            return key
    a = archive(transformer = t, date_format = 'DATE', position = position)
    observed = a.from_path(key)
    if position == 'left':
        assert observed[0] == 'DATE'
        assert observed[1:] == key
    elif position == 'right':
        assert observed[-1] == 'DATE'
        assert observed[:-1] == key
    else:
        raise AssertionError('My test is broken.')

def test_to_path():
    'to_path should be the same as normal.'
    class t:
        @staticmethod
        def to_path(_):
            return 'abc'
    a = archive(transformer = t)
    assert a.to_path(('one', 'two', 'three', 'four')) == 'abc'

testcases_attrs = product(['binary_mode', 'cache_exceptions'],
                          [None, True, False])
@pytest.mark.parametrize('attr, attr_value', testcases_attrs)
def test_attrs(attr, attr_value):
    'binary_mode and cache_exceptions should be passed properly.'
    class t:
        pass
    if attr_value != None:
        setattr(t, attr, attr_value)
    a = archive(transformer = t)

    if attr_value == None:
        assert not hasattr(a, attr)
    else:
        assert getattr(a, attr) == attr_value

#@pytest.mark.parameterize('position, transformer, key', testcases_position):
