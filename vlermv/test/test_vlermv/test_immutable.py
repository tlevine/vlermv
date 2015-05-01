import tempfile

import pytest

from .base import Base, identity_transformer
from ..._vlermv import Vlermv
from ...serializers import pickle

class TestImmutableVlermv(Base):
    def setup_method(self, method):
        self.directory = tempfile.mkdtemp()
        self.default = Vlermv(self.directory,
            key_transformer = identity_transformer, serializer = pickle)
        self.mutable = Vlermv(self.directory, mutable = True,
            key_transformer = identity_transformer, serializer = pickle)
        self.immutable = Vlermv(self.directory, mutable = False,
            key_transformer = identity_transformer, serializer = pickle)

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
