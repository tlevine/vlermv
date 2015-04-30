import pickle, tempfile
from .base import Base

class TestDefaults(Base):
    def setup_method(self, method):
        self.directory = tempfile.mkdtemp()
        self.w = Vlermv(self.directory)

    def test_default_serializer(self):
        assert self.w.serializer == pickle

    def test_default_transformer(self):
        assert self.w.transformer.__name__ == 'magic'

    def test_default_mutable(self):
        assert self.w.mutable

    def test_default_tempdir(self):
        return self.w.tempdir

