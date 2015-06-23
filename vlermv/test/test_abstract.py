import pytest
from testfixtures import LogCapture

from .. import _abstract as a

def test_logging():

    v = a.AbstractVlermv()
    v.func = lambda *args: 1/0
    assert not v.cache_exceptions

    with LogCapture() as l:
        with pytest.raises(ZeroDivisionError):
            v(8,9,3)

    msg = 'Exception in AbstractVlermv calling this memoized function:\n<lambda>(*(8, 9, 3), *{})'
    l.check(('vlermv._abstract', 'ERROR', msg),)

def test_logging_cache_exceptions():

    class DictVlermv(a.AbstractVlermv):
        d = {}
        def __setitem__(self, key, value):
            self.d[key] = value

    v = DictVlermv(cache_exceptions = True)
    assert v.cache_exceptions
    def f(*args):
        raise EnvironmentError('Pretend that something went wrong.')
    v.func = f

 #  with LogCapture() as l:
 #      v(8,9,3)

 #  msg = 'Exception in DictVlermv calling this memoized function:\n<lambda>(*(8, 9, 3), *{})'
 #  l.check(('vlermv._abstract', 'ERROR', msg),)

    # We should also check that the exc_info shows up.
