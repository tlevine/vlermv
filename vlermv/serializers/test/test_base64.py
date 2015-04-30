from .base import Base
from .. import base64

class TestBase64(Base):
    serializer = base64
    obj = 'abc'.encode('ascii')
    dumped_obj = 'YWJj\n'.encode('ascii')
