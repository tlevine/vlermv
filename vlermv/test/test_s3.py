import json

import pytest

from .._s3 import S3Vlermv, split

class FakeS3:
    def __init__(self, **kwargs):
        self.db = kwargs
    def __call__(self):
        return self
    def create_bucket(self, bucketname):
        return FakeBucket(self)

class FakeBucket:
    def __init__(self, s3):
        self.s3 = s3
    def new_key(self, key):
        return FakeKey(self.s3, key)
    def get_key(self, key):
        if key in self.s3.db:
            return FakeKey(self.s3, key)

class FakeKey:
    def __init__(self, s3, key):
        self.s3 = s3
        self.key = key
    def get_contents_as_string(self):
        return self.s3.db[self.key]
    def get_contents_to_filename(self, filename):
        with open(filename, 'wb') as fp:
            fp.write(self.s3.db[self.key])
    def set_contents_from_string(self, payload, **kwargs):
        self.s3.db[self.key] = payload
    def set_contents_from_filename(self, filename, **kwargs):
        with open(filename, 'rb') as fp:
            self.s3.db[self.key] = fp.read()

CONTRACT = {
    'bids': [],
    'contract': 'http://search.worldbank.org/wcontractawards/procdetails/OP00032101',
    'method.selection': 'QCBS ? Quality andCost-Based Selection',
    'price': 'INR 1,96,53,750',
    'project': None
}
PAYLOAD = json.dumps(CONTRACT).encode('utf-8')

def test_read():
    d = S3Vlermv('contracts', serializer = json,
                 connect_s3 = FakeS3(OP00032101 = PAYLOAD))
    assert d['OP00032101'] == CONTRACT

def test_write():
    fakes3 = FakeS3()
    d = S3Vlermv('contracts', connect_s3 = fakes3, serializer = json)
    assert fakes3.db == {}
    d['OP00032101'] = CONTRACT
    assert fakes3.db == {'OP00032101': PAYLOAD}

def test_split():
    assert split('a/bb/cc') == ('a', 'bb', 'cc')
    assert split('one') == ('one',)
