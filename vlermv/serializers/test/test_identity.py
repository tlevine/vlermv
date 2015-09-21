from .base import Base
from .. import identity_str, identity_bytes, identity_mmap_str, identity_mmap_bytes

class TestIdentityStr(Base):
    serializer = identity_str
    obj = 'abc'
    dumped_obj = 'abc'

class TestIdentityBytes(Base):
    serializer = identity_bytes
    obj = 'abc'.encode('ascii')
    dumped_obj = 'abc'.encode('ascii')

class TestIdentityMmapStr(TestIdentityStr):
    serializer = identity_mmap_str

class TestIdentityMmapBytes(TestIdentityBytes):
    serializer = identity_mmap_bytes

class TestIdentityMmapEmpty(Base):
    serializer = identity_mmap_bytes
    obj = ''.encode('ascii')
    dumped_obj = ''.encode('ascii')
