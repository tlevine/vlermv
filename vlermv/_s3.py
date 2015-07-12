import tempfile

from boto import connect_s3

from ._abstract import AbstractVlermv

def split(x):
    return tuple(x.split('/'))

class immutabledict:
    def __init__(self):
        self.log = []
        self.state = {}

    def _play_log(self):


    def __setitem__(self, k, v):
        if k in self:
            raise KeyError('%s[%s] already exists; you may not delete it.' % self, k)
        else:
            super(immutabledict, self)[k] = v

    def __getitem__(self, k):
        return self.state[k]

    def __contains__(self, k):
        return k in self.state

class S3Vlermv(AbstractVlermv):
    buckets = {}

    def __init__(self, bucketname, *args, buckets = None, **kwargs):
        super(S3Vlermv, self).__init__(**kwargs)
        if buckets:
            self.bucket = buckets[bucketname]
        else:
            # For parallel
            if bucketname not in self.buckets:
                self.buckets[bucketname] = connect_s3().create_bucket(bucketname)
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
        raise NotImplementedError

    def __len__(self):
        return sum(1 for _ in self.keys())
