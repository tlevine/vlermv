import datetime

import pytest

from .. import ( tuple, archive )


@pytest.mark.parametrize('position', [('left',), ('right',)])
def test_position(position):
    a = archive(transformer = tuple, date_format = 'DATE', position = position)
    @cache(transformer = a)
    def f(a, b, c):
        return a + b + c
    key = (1, 2, 3)
    value = 6
    f(*key)
    assert f[key] == value
    observed_value = next(f.keys())
    if position == 'left':
        assert observed_value[0] == 'DATE'
        assert observed_value[1:] == value
    elif position == 'left':
        assert observed_value[-1] == 'DATE'
        assert observed_value[:-1] == value


#@pytest.mark.parameterize('position, transformer, key', testcases_position):
