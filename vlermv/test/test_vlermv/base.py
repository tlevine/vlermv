import pickle
from shutil import rmtree

from ...vlermv import Vlermv

class Base:
    def teardown_method(self, method):
        rmtree(self.directory)

class transformer:
    @staticmethod
    def to_tuple(key):
        return key

    @staticmethod
    def from_tuple(path):
        return os.path.join(*path)

def simple_vlermv(cachedir):
    return Vlermv(cachedir, transformer = transformer, serializer = pickle)
