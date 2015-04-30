from tempfile import TemporaryFile

class TestSerializer:

    def tmp(self):
        if getattr(self.serializer, 'vlermv_binary_mode', False):
            b = 'b'
        else:
            b = ''
        return TemporaryFile('w+' + b)

    def dump(self, obj, result):
        with self.tmp() as fp:
            self.serializer.dump(obj, fp)
            fp.seek(0)
            assert fp.read() == result

    def load(self, contents, obj):
        with self.tmp() as fp:
            fp.write(contents)
            fp.seek(0)
            assert self.serializer.load(fp) == obj

    def test_cache_exceptions(self):
        objs = [
            (ValueError('This is an exception.'), None),
            (None, 'This is not an exception.'),
        ]
        for obj in objs:
            if getattr(self.serializer, 'vlermv_cache_exceptions', False):
                with self.tmp() as fp:
                    self.serializer.dump(obj, fp)
                    fp.seek(0)
                    assert self.serializer.load(fp) == obj
