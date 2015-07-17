import tempfile

from ._abstract import AbstractVlermv
from ._safe_buckets import SafeBuckets

def split(x):
    return tuple(x.split('/'))

class S3Vlermv(AbstractVlermv):
    buckets = SafeBuckets()

    def __init__(self, bucketname, *args, bucket = None, **kwargs):
        super(S3Vlermv, self).__init__(**kwargs)
        if bucket:
            self.bucket = bucket
        else:
            self.bucket = self.buckets[bucketname]

    def __repr__(self):
        return 'S3Vlermv(%s)' % repr(self.bucket.name)

    def __setitem__(self, index, obj):
        keyname = self.filename(index)
        key = self.bucket.new_key(keyname)
        with tempfile.NamedTemporaryFile('w+' + self._b()) as tmp:
            self.serializer.dump(obj, tmp.file)
            tmp.file.close()
            key.set_contents_from_filename(tmp.name, replace = True)

    def __contains__(self, index):
        keyname = self.filename(index)
        return self.bucket.get_key(keyname) != None

    def __getitem__(self, index):
        keyname = self.filename(index)
        key = self.bucket.get_key(keyname)
        if key:
            with tempfile.NamedTemporaryFile('w+' + self._b()) as tmp:
                key.get_contents_to_filename(tmp.name)
                tmp.file.seek(0)
                value = self.serializer.load(tmp.file)
            return value
        else:
            raise KeyError(keyname)

    def keys(self, **kwargs):
        for k in self.bucket.list(**kwargs):
            yield self.key_transformer.from_path(split(k.name.rstrip('/')))

    def __delitem__(self, index):
        super(S3Vlermv, self).__delitem__(index)
        keyname = self.filename(index)
        self.bucket.delete_key(keyname)

    def __len__(self):
        return sum(1 for _ in self.keys())
