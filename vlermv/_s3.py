import tempfile
from time import sleep

import boto

from ._abstract import AbstractVlermv

class S3Vlermv(AbstractVlermv):
    def __init__(self, bucketname, *args, connect_s3 = boto.connect_s3, **kwargs):
        super(S3Vlermv, self).__init__(bucketname, *args, **kwargs)
        self.bucket = connect_s3().create_bucket(bucketname)

    def __setitem__(self, index, obj):
        keyname = self.filename(index)
        key = self.bucket.new_key(keyname)
        with tempfile.NamedTemporaryFile('w+' + self._b()) as tmp:
            self.serializer.dump(obj, tmp.file)
            key.set_contents_from_file(tmp.name, replace = True)

    def __contains__(self, keyname):
        return self.bucket.get_key(keyname) != None

    def __getitem__(self, keyname):
        key = self.bucket.get_key(keyname)
        if key:
            with tempfile.NamedTemporaryFile('w+b') as tmp:
                key.get_contents_as_file(tmp.name)
                value = self.serializer.load(tmp.file)
            return value
        else:
            raise KeyError(keyname)
