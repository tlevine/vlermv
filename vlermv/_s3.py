import pickle, zlib
from time import sleep

import boto

from .meta_memoize import meta_memoize

class s3dict:
    def __init__(self, bucketname, connect_s3 = boto.connect_s3):
        self.bucket = connect_s3().create_bucket(bucketname)

    def __setitem__(self, keyname, value):
        key = self.bucket.new_key(keyname)
        payload = zlib.compress(pickle.dumps(value)) # Compress
        key.set_contents_from_string(payload, replace = True)

    def __contains__(self, keyname):
        return self.bucket.get_key(keyname) != None

    def __getitem__(self, keyname):
        key = self.bucket.get_key(keyname)
        if key:
            payload = key.get_contents_as_string() # Read
            value = pickle.loads(zlib.decompress(payload)) # Decompress
            return value
        else:
            raise KeyError(keyname)
