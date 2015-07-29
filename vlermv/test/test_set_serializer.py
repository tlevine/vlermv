import codecs
from io import StringIO

from .._abstract import AbstractVlermv

class ChickenSerializer:
    extension = '.chicken'
    @classmethod
    def load(_, fp):
        return fp.read().lower()
    @classmethod
    def dump(_, obj, fp):
        return fp.write(obj.upper())

class Rot13Serializer:
    extension = '.rot13'
    @classmethod
    def load(_, fp):
        return codecs.encode(fp.read(), 'rot_13')
    @classmethod
    def dump(_, obj, fp):
        return codecs.encode(fp.write(obj), 'rot_13')

class DictVlermv(AbstractVlermv):
    def __init__(self, **kwargs):
        self.d = {}
        super(DictVlermv, self).__init__(**kwargs)

def test_one_serializer():
    v = DictVlermv(serializers = [ChickenSerializer])

    # Key
    assert v.filename('abc') == 'abc.chicken'

    # Set
    fp = StringIO()
    v.serializer.dump('aaaaaa', fp)
    assert fp.getvalue() == 'AAAAAA'

    # Get
    fp = StringIO('BBBBBBB')
    assert v.serializer.load(fp) == 'bbbbbbb'

def test_many_serializers():
    v = DictVlermv(serializers = [ChickenSerializer, Rot13Serializer])
    # Key
    assert v.filename('abc') == 'abc.chicken.rot13'

    # Set
    fp = StringIO()
    v.serializer.dump('aaaaaa', fp)
    assert fp.getvalue() == 'NNNNNN'

    # Get
    fp = StringIO('OOOOOOO')
    assert v.serializer.load(fp) == 'bbbbbbb'
