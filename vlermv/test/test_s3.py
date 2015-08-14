import json, socket

import pytest

from .._s3 import S3Vlermv

class FakeBucket:
    def __init__(self, name, raise_timeout = False, **db):
        self.db = db
        self.name = name
        self.raise_timeout = raise_timeout
    def list(self, prefix = ''):
        for key in self.db:
            if key.startswith(prefix):
                yield self.new_key(key)
    def new_key(self, key):
        return FakeKey(self, key)
    def get_key(self, key):
        if key in self.db:
            return FakeKey(self, key)
    def delete_key(self, key):
        del(self.db[key])

class FakeKey:
    def __init__(self, bucket, name):
        self.bucket = bucket
        self.name = name
    def get_contents_as_string(self):
        if self.bucket.raise_timeout:
            raise socket.timeout('The read operation timed out')
        else:
            return self.bucket.db[self.name]
    def get_contents_to_filename(self, filename):
        if self.bucket.raise_timeout:
            raise socket.timeout('The read operation timed out')
        else:
            with open(filename, 'wb') as fp:
                fp.write(self.bucket.db[self.name])
    def set_contents_from_string(self, payload, **kwargs):
        self.bucket.db[self.name] = payload
    def set_contents_from_filename(self, filename, **kwargs):
        with open(filename, 'rb') as fp:
            self.bucket.db[self.name] = fp.read()

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
                 bucket = FakeBucket('aoeu', OP00032101 = PAYLOAD))
    assert d['OP00032101'] == CONTRACT

def test_write():
    fakebucket = FakeBucket('aoeu')
    d = S3Vlermv('contracts', bucket = fakebucket, serializer = json)
    assert fakebucket.db == {}
    d['OP00032101'] = CONTRACT
    assert fakebucket.db == {'OP00032101': PAYLOAD}

def test_delete():
    fakebucket = FakeBucket('aoeu')
    d = S3Vlermv('contracts', bucket = fakebucket, serializer = json)
    d['OP00032101'] = CONTRACT
    del(d['OP00032101'])
    assert len(fakebucket.db) == 0

def test_prefix():
    db = {'contracts/OP00032101': PAYLOAD}
    d = S3Vlermv('procurement-documents', 'contracts', serializer = json,
                 bucket = FakeBucket('procurement-documents', **db))

    with pytest.raises(KeyError):
        d.filename(tuple())
    assert d.filename(('OP00032101',)) == 'contracts/OP00032101'
    assert d.from_filename('contracts/OP00032101') == ('OP00032101',)
    assert list(d.keys()) == [('OP00032101',)]
    assert d['OP00032101'] == CONTRACT

def test_handle_socket_timeout():
    fakebucket = FakeBucket('aoeu', raise_timeout = True)
    d = S3Vlermv('contracts', bucket = fakebucket, serializer = json)
    d[9] = 'nine'
    with pytest.raises(S3Vlermv.Timeout):
        d[9]
    with pytest.raises(d.Timeout):
        d[9]

tc = [
    ('get_contents_to_filename', ('/not/a/file',)),
    ('get_contents_as_string', tuple()),
]
@pytest.mark.parametrize('method, args', tc) 
def test_fake_key_timeout(method, args):
    fakebucket = FakeBucket('aoeu', raise_timeout = True)
    k = fakebucket.new_key('abc')
    try:
        getattr(fakebucket.new_key('abc'), method)(*args)
    except socket.timeout as t:
        assert isinstance(t, socket.timeout)
        assert t.args == ('The read operation timed out',)
    else:
        raise AssertionError('FakeBucket did not raise timeout.')
