import tempfile
from time import sleep

import boto

from ._abstract import AbstractVlermv

def split(x):
    return x.split('/')

class S3Vlermv(AbstractVlermv):

    base_directory = ''
    def __init__(self, bucketname, *args, connect_s3 = boto.connect_s3, **kwargs):
        super(S3Vlermv, self).__init__(**kwargs)
        self.bucket = connect_s3().create_bucket(bucketname)

    def __repr__(self):
        return 'S3Vlermv(%s)' % repr(self.base_directory)

    def __setitem__(self, index, obj):
        keyname = self.filename(index)
        key = self.bucket.new_key(keyname)
        with tempfile.TemporaryFile('w+' + self._b()) as fp:
            self.serializer.dump(obj, fp)
            fp.seek(0)
            key.set_contents_from_file(fp, replace = True)

    def __contains__(self, keyname):
        return self.bucket.get_key(keyname) != None

    def __getitem__(self, keyname):
        key = self.bucket.get_key(keyname)
        if key:
            with tempfile.TemporaryFile('w+b') as fp:
                key.get_contents_as_file(fp)
                fp.seek(0)
                value = self.serializer.load(fp)
            return value
        else:
            raise KeyError(keyname)

    def keys(self):
        for k in self.bucket.list():
            yield self.transformer.from_path(split(k.name))

    def __delitem__(self, index):
        super(S3Vlermv, self).__delitem__(index)
        raise NotImplementedError

    def __len__(self):
        return sum(1 for _ in self.keys())
