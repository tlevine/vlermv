import os, pickle
from shutil import rmtree

from ...vlermv import Vlermv

def test_mkdir():
    d = '/tmp/not a directory'
    w = Vlermv(d)
    if os.path.exists(d):
        rmtree(d)
    w[('abc','def','ghi')] = 3
    with open(os.path.join('/tmp/not a directory/abc/def/ghi'), 'rb') as fp:
        observed = pickle.load(fp)
    assert observed == 3
