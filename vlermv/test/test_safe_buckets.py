from functools import partial

import thready

from .._safe_buckets import SafeBuckets

class Count:
    def __init__(self):
        self._i = 0

    @property
    def i(self):
        self._i += 1
        return int(self._i)

def create_bucket(counter, bucketname):
    return (bucketname, counter.i)

def test_create_bucket():
    f = partial(create_bucket, Count())
    assert f('one') == ('one', 1)
    assert f('two') == ('two', 2)

def test_get_new():
    f = partial(create_bucket, Count())
    sb = SafeBuckets(create_bucket = f)
    assert sb['abc'] == ('abc', 1)
    assert sb['abc'] == ('abc', 1)

def test_get_old():
    f = partial(create_bucket, Count())
    sb = SafeBuckets(create_bucket = f)
    train = 'TRAAAAAAAAAAAIN'
    sb.state = {'abc': train}
    assert sb['abc'] == train
