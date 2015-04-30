import pickle, tempfile, os
from .base import Base
from ...vlermv import Vlermv

class TestDefaults(Base):
    def setup_method(self, method):
        self.directory = tempfile.mkdtemp()
        self.w = Vlermv(self.directory)

    def test_default_serializer(self):
        assert self.w.serializer == pickle

    def test_default_transformer(self):
        assert 'magic' in self.w.transformer.__name__

    def test_default_mutable(self):
        assert self.w.mutable

    def test_default_tempdir(self):
        assert self.w.tempdir == os.path.join(self.directory, '.tmp')
