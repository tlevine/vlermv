from ._identity import identity_str, identity_bytes
try:
    from ._lxml import html, xml
except ImportError:
    pass
from . import pickle, compressed_pickle
from ._mmap import _mmap as mmap
