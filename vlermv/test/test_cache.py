'''
These tests will be better off somewhere else in the code.
'''
import os, pickle, shutil, json
from tempfile import mkdtemp

import pytest

from ..transformers import tuple as _tuple
from .._fs import Vlermv

def test_new_success():
    tmp = mkdtemp()
    warehouse = Vlermv(tmp, key_transformer = _tuple)
    url = 'localhost'

    @Vlermv.cache(tmp, cache_exceptions = True)
    def get(_):
        return 88

    observed_response = get(url)
    assert observed_response == 88
    assert warehouse[(url,)] == (None, 88)

def test_old_success():
    tmp = mkdtemp()
    warehouse = Vlermv(tmp, key_transformer = _tuple)
    url = 'localhost'
    warehouse[(url,)] = (None, 88)

    @Vlermv.cache(tmp, cache_exceptions = True)
    def get(_):
        raise AssertionError('This should not run.')

    observed_response = get(url)
    assert observed_response == 88

def test_new_error():
    tmp = mkdtemp()
    warehouse = Vlermv(tmp, key_transformer = _tuple)
    url = 'localhost'
    error = ValueError('This is a test.')

    @Vlermv.cache(tmp, cache_exceptions = True)
    def get(_):
        raise error

    try:
        get(url)
    except ValueError as e:
        assert str(e) == str(error)
        assert str(warehouse[(url,)]) == str((error, None))
    else:
        raise AssertionError('An error should have been raised.')


def test_old_error():
    tmp = mkdtemp()
    warehouse = Vlermv(tmp, key_transformer = _tuple)
    url = 'localhost'
    error = ValueError('This is a test.')
    warehouse[(url,)] = (error, None)

    @Vlermv.cache(tmp, cache_exceptions = True)
    def get(_):
        raise AssertionError('This should not run.')

    try:
        get(url)
    except ValueError as e:
        assert str(e) == str(error)
    else:
        raise AssertionError('An error should have been raised.')


def test_expanduser():
    try:
        shutil.rmtree(os.path.expanduser('~/.picklecache-test'))
    except:
        pass

    @Vlermv.cache('~/.picklecache-test')
    def a(_):
        return 3
    a('b')
    assert os.path.isfile(os.path.expanduser('~/.picklecache-test/b'))

    try:
        shutil.rmtree(os.path.expanduser('~/.picklecache-test'))
    except:
        pass

def test_function_name():
    try:
        shutil.rmtree('a_function')
    except:
        pass

    @Vlermv.cache()
    def a_function(_):
        return 3
    assert os.path.isdir('a_function')

    try:
        shutil.rmtree('a_function')
    except:
        pass

def test_keys():
    tmp = mkdtemp()
    @Vlermv.cache(tmp)
    def f(x):
        return x

    f('4')
    f('5')
    assert set(f.keys()) == {('4',),('5',)}

def test_delete():
    tmp = mkdtemp()
    @Vlermv.cache(tmp)
    def f(x):
        return x

    f('4')
    f('5')
    f('6')
    del(f[('6',)])
    assert set(f.keys()) == {('4',),('5',)}

def test_type():
    tmp = mkdtemp()
    @Vlermv.cache(tmp)
    def f(x):
        pass

    assert isinstance(f, Vlermv)

def test_cache_exceptions_type_checker():
    import json
    json.cache_exceptions = False
    tmp = mkdtemp()

    with pytest.raises(TypeError):
        @Vlermv.cache(tmp, cache_exceptions = True, serializer = json)
        def f(x):
            return x
            
def test_cache_exceptions():
    tmp = mkdtemp()
    TestError = ZeroDivisionError

    @Vlermv.cache(tmp, cache_exceptions = False, serializer = json)
    def f(_):
        raise TestError('This error should not be cached.')

    with pytest.raises(TestError):
        f('x')
    assert ('x',) not in f
            
def test_cache_exceptions_save_type():
    tmp = mkdtemp()

    @Vlermv.cache(tmp, cache_exceptions = False, serializer = json)
    def f(_):
        return 3

    first = f('x')
    second = f('x')
    assert first == second == 3
