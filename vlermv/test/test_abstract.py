import pytest
from testfixtures import LogCapture

from .. import _abstract as a

def test_logging():

    v = a.AbstractVlermv()
    v.func = lambda *args: 1/0

    with LogCapture() as l:
        with pytest.raises(ZeroDivisionError):
            v(8,9,3)

    msg = 'Exception in AbstractVlermv calling this memoized function:\n<lambda>(*(8, 9, 3), *{})'
    l.check(('vlermv._abstract', 'ERROR', msg),)

    assert False, print(l)

def test_logging_cache_exceptions():

    v = a.AbstractVlermv(cache_exceptions = True)
    v.func = lambda *args: 1/0

    with LogCapture() as l:
        with pytest.raises(ZeroDivisionError):
            v(8,9,3)

    msg = 'Exception in AbstractVlermv calling this memoized function:\n<lambda>(*(8, 9, 3), *{})'
    l.check(('vlermv._abstract', 'ERROR', msg),)
