from tempfile import TemporaryFile

class Base:
    serializer = None
    obj = None
    dumped_obj = ''

    def tmp(self):
        if getattr(self.serializer, 'vlermv_binary_mode', False):
            b = 'b'
        else:
            b = ''
        return TemporaryFile('w+' + b)

    def test_dump(self):
        with self.tmp() as fp:
            self.serializer.dump(self.obj, fp)
            fp.seek(0)
            assert fp.read() == self.dumped_obj

    def test_load(self):
        with self.tmp() as fp:
            fp.write(self.dumped_obj)
            fp.seek(0)
            assert self.serializer.load(fp) == self.obj

    def test_cache_exceptions(self):
        objs = [
            (ValueError('This is an exception.'), self.obj),
            (self.obj, 'This is not an exception.'),
        ]
        for obj in objs:
            if getattr(self.serializer, 'vlermv_cache_exceptions', False):
                with self.tmp() as fp:
                    self.serializer.dump(obj, fp)
                    fp.seek(0)
                    assert self.serializer.load(fp) == obj
