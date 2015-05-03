import datetime

import pytest

from .. import ( tuple, archive )


@pytest.mark.parametrize('position', [('left',), ('right',)])
def test_position(position):
    a = archive(transformer = tuple, date_format = 'DATE', position = position)
    key = (1, 2, 3)
    observed = a.from_path(key)
    if position == 'left':
        assert observed[0] == 'DATE'
        assert observed[1:] == key
    elif position == 'left':
        assert observed[-1] == 'DATE'
        assert observed[:-1] == key


#@pytest.mark.parameterize('position, transformer, key', testcases_position):
