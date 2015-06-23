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
        with pytest.raises(ZeroDivisionError):
            v(8,9,3)

    msg = 'Exception in AbstractVlermv calling this memoized function:\n<lambda>(*(8, 9, 3), *{})'
    l.check(*((('vlermv._abstract', 'ERROR', msg),) * 2))

def test_logging_cache_exceptions():
    '''
    The exception should be logged only on the initial call,
    not on the load from the cache.
    '''

    class DictVlermv(a.AbstractVlermv):
        d = {}
        def __setitem__(self, key, value):
            self.d[key] = value

    v = DictVlermv(cache_exceptions = True)
    def f(*args):
        raise EnvironmentError('Pretend that something went wrong.')
    v.func = f

    msg = 'Exception in DictVlermv calling this memoized function:\nf(*(8, 9, 3), *{})'

    with LogCapture() as l:
        with pytest.raises(EnvironmentError):
            v(8,9,3)
        l.check(('vlermv._abstract', 'ERROR', msg),)
    assert (8,9,3) in v.d
    assert v.d[(8,9,3)][1] == None

    with LogCapture() as l:
        with pytest.raises(EnvironmentError):
            v(8,9,3)
        l.check(tuple())
