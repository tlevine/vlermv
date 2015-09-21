from .base import Base
from .. import mmap

class TestMmap(Base):
    serializer = mmap
    obj = 'abc'.encode('ascii')
    dumped_obj = 'abc'.encode('ascii')
