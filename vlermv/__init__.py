from ._fs import Vlermv
from ._s3 import S3Vlermv
from . import serializers, transformers

# For backwards compatibility
cache = Vlermv.memoize
