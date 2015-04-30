from shutil import rmtree

from ...vlermv import Vlermv

class Base:
    def teardown_method(self, method):
        rmtree(self.directory)

def list_identity_transformer(x):
    return [x]

def simple_vlermv(cachedir):
    return Vlermv(self.directory, transformer = list_identity_transformer, serializer = pickle)
