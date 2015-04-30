from .base import Base
from .. import base64

class TestBase64(Base):
    serializer = base64
    obj = 'abc'
    dumped_obj = ''
