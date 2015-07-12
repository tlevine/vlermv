import thready
from .._safe_buckets import SafeBuckets

class Count:
    def __init__(self):
        self._i = 0

    @property
    def i(self):
        self._i += 1
        return int(self._i)

def create_bucket(bucketname, counter = Count()):
    return (bucketname, counter.i)

def test_create_bucket():
    assert create_bucket('one') == ('one', 1)
    assert create_bucket('two') == ('two', 2)

def test_get_new():
    pass
   #sb = SafeBuckets(create_bucket = create_bucket)
   #assert sb['abc'] == ('abc', 1)
   #assert sb['abc'] == ('abc', 1)
