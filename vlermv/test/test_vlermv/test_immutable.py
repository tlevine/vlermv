import tempfile

from .base import Base

class TestImmutableVlermv(Base):
    def setup_method(self, method):
        self.directory = tempfile.mkdtemp()
        self.default = Vlermv(self.directory,
            transformer = identity_transformer, serializer = pickle)
        self.mutable = Vlermv(self.directory,
            mutable = True, transformer = identity_transformer, serializer = pickle)
        self.immutable = Vlermv(self.directory,
            mutable = False, transformer = identity_transformer, serializer = pickle)

    def test_setitem(self):
        self.mutable['a'] = 3
        self.default['a'] = 3
        with pytest.raises(PermissionError):
            self.immutable['a'] = 3

    def test_delitem(self):
        self.mutable['a'] = 3
        del(self.default['a'])

        self.mutable['a'] = 3
        del(self.mutable['a'])

        self.mutable['a'] = 3
        with pytest.raises(PermissionError):
            del(self.immutable['a'])

    def test_kwarg(self):
        assert (self.default.mutable)
        assert (self.mutable.mutable)
        assert not (self.immutable.mutable)
