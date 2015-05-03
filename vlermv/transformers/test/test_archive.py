import datetime

import pytest

from .. import ( tuple, archive )


@pytest.mark.parametrize('position', ['left', 'right'])
def test_position(position):
    key = (1, 2, 3)
    class t:
        @staticmethod
        def to_path(_):
            return key
    a = archive(transformer = t, date_format = 'DATE', position = position)
    observed = a.to_path(key)
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

#@pytest.mark.parameterize('position, transformer, key', testcases_position):
