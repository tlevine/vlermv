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
        def __contains__(self, key):
            return key in self.d
        def __getitem__(self, key):
            return self.d[key]
        def __setitem__(self, key, value):
            self.d[key] = value

    v = DictVlermv(cache_exceptions = True)
    v[(348203481034,)] = (EnvironmentError('Pretend that something went wrong.'), None)
    def f(*args):
        raise AssertionError('This should not run.')
    v.func = f

    with LogCapture() as l:
        with pytest.raises(EnvironmentError):
            v(348203481034)
        l.check()

def test_set_transformer():
    v = a.AbstractVlermv(key_transformer = 3)
    assert v.key_transformer == 3
