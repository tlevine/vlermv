import os
import pickle
import tempfile

import pytest

from .base import simple_vlermv, Base
from ...vlermv import Vlermv
from ... import exceptions

class TestVlermv(Base):
    def setup_method(self, method):
        self.directory = tempfile.mkdtemp()
        self.w = simple_vlermv(self.directory)

    def test_repr(self):
        assert repr(self.w) == "Vlermv('%s')" % self.directory
        assert str(self.w) == "Vlermv('%s')" % self.directory
        assert str(Vlermv('/tmp/a"b"c"')) == '''Vlermv('/tmp/a"b"c"')'''

    def test_setitem(self):
        self.w[("Tom's", 'favorite color')] = 'pink'
        with open(os.path.join(self.directory, "Tom's", 'favorite color'), 'rb') as fp:
            observed = pickle.load(fp)
        assert observed == 'pink'

    def test_cachedir(self):
        assert self.w.cachedir == self.directory

    def test_filename(self):
        assert os.path.join(self.directory, 'abc') == self.w.filename('abc')

    def test_getitem(self):
        with open(os.path.join(self.directory, 'profession'), 'wb') as fp:
            observed = pickle.dump('dada artist', fp)
        assert self.w[('profession',)] == 'dada artist'

        with pytest.raises(KeyError):
            self.w[('not a file',)]

    def test_get(self):
        with open(os.path.join(self.directory, 'profession'), 'wb') as fp:
            observed = pickle.dump('dada artist', fp)
        assert self.w[('profession',)] == 'dada artist'
        assert self.w.get(('hobby',),'business intelligence') == 'business intelligence'

    def test_delitem1(self):
        dirname = os.path.join(self.directory, 'foo')
        filename= os.path.join(dirname, 'bar')
        os.mkdir(dirname)
        with open(filename, 'wb') as fp:
            pass
        del(self.w[('foo','bar')])
        assert not (os.path.exists(filename))
        assert not (os.path.exists(dirname))

        with pytest.raises(KeyError):
            del(self.w[('not a file',)])

    def test_delitem2(self):
        dirname = os.path.join(self.directory, 'foo')
        filename= os.path.join(dirname, 'bar')
        os.mkdir(dirname)
        with open(filename, 'wb') as fp:
            pass
        with open(filename+'2', 'wb') as fp:
            pass
        del(self.w[('foo','bar')])
        assert not (os.path.exists(filename))
        assert (os.path.exists(dirname))

        with pytest.raises(KeyError):
            del(self.w[('not a file',)])

    def test_contains(self):
        assert not ('needle' in self.w)
        with open(os.path.join(self.directory, 'needle'), 'wb'):
            pass
        assert ('needle' in self.w)

    def test_len(self):
        for i in range(100):
            self.w[(str(i),)] = i
        assert len(self.w) == 100

    def test_update(self):
        self.w.update({('dictionary',): {'a':'z'}})
        with open(os.path.join(self.directory, 'dictionary'), 'rb') as fp:
            observed = pickle.load(fp)
        assert observed == {'a':'z'}

        self.w.update([(('tuple',), (2,4,8))])
        expected = {('tuple',): (2,4,8),  'dictionary': {'a':'z'}}
        assert len(self.w) == len(expected)
        for key in expected.keys():
            assert self.w[key] == expected[key]

    def test_iter(self):
        abc = os.path.join(self.directory, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb'):
            pass
        with open(os.path.join(self.directory, 'z'), 'wb'):
            pass

        observed = set(x for x in self.w)
        expected = {('a', 'b', 'c', 'd'), ('z',)}

        assert observed == expected

    def test_keys(self):
        abc = os.path.join(self.directory, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb'):
            pass
        with open(os.path.join(self.directory, 'z'), 'wb'):
            pass
        with open(os.path.join(self.directory, '.tmp', 'lalala'), 'wb'):
            pass

        observed = set(self.w.keys())
        expected = {('a', 'b', 'c', 'd'), ('z',)}

        assert observed == expected

    def test_values(self):
        abc = os.path.join(self.directory, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb') as fp:
            pickle.dump(123, fp)
        with open(os.path.join(self.directory, 'z'), 'wb') as fp:
            pickle.dump(str, fp)

        observed = set(self.w.values())
        expected = {123,str}

        assert observed == expected

    def test_items(self):
        abc = os.path.join(self.directory, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb') as fp:
            pickle.dump(9, fp)
        with open(os.path.join(self.directory, 'z'), 'wb') as fp:
            pickle.dump(str, fp)

        observed = set(self.w.items())
        expected = {(('a', 'b', 'c', 'd'), 9), (('z',),str)}

        assert observed == expected
