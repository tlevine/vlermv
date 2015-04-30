from tempfile import mkdtemp

import pytest

from .base import identity_transformer
from ...vlermv import Vlermv

class _mode_checker:
    def dump(self, obj, fp):
        assert ('b' in fp.mode) == self.vlermv_binary_mode

    def load(self, fp):
        assert ('b' in fp.mode) == self.vlermv_binary_mode

    def __init__(self, binary_mode):
        self.vlermv_binary_mode = binary_mode

@pytest.mark.parametrize('mode', [True, False])
def test_mode(mode):
    tmp = mkdtemp()
    w = Vlermv(tmp, serializer = _mode_checker(mode),
        key_transformer = identity_transformer)
    w[('a',)] = 8
    w[('a',)]
