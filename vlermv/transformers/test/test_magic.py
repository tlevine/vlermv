import datetime

import pytest

from .. magic import parse, parse_partial, safe_type

def test_parse_int():
    assert parse_partial(3) == ['3']
    assert parse_partial(123) == ['123']
    assert parse(123) == ['123']

def test_parse_url():
    o = list(parse_partial('http://thomaslevine.com/!/about?a=b#lala'))
    e = ['http', 'thomaslevine.com', '!', 'about?a=b#lala']
    assert o == e

def test_parse_date():
    o = list(parse_partial(datetime.date(2014, 2, 5)))
    e = ['2014', '02', '05']
    assert o == e

def test_parse_datetime():
    o = list(parse_partial(datetime.datetime(2014, 2, 5, 11, 18, 30)))
    e = ['2014', '02', '05']
    assert o == e

def test_parse_none():
    assert parse_partial(None) == ['']
    assert parse(None) == []

testcases = [
    # iterables
    (('a','b','c'), ['a', 'b', 'c']),
    (['foo','bar','baz'], ['foo', 'bar', 'baz']),

    # strings
    ('def', ['def']),
    ('favorite color', ['favorite color']),

    # paths
    ('left/middle/right', ['left', 'middle', 'right']),
    ('backslashes\\also\\delimit', ['backslashes','also','delimit']),
    ('/home/tlevine/warehouse', ['home', 'tlevine', 'warehouse']),
    ('C:\\Users\\Documents', ['c', 'Users', 'Documents']),

    # URLs
    ('http://thomaslevine.com/!?foo=bar', ['http', 'thomaslevine.com', '!?foo=bar']),
    (['http://thomaslevine.com', 'foo/bar/baz', 'a b'], ['http', 'thomaslevine.com', 'foo', 'bar', 'baz', 'a b']),

    # . and .. are special
    ('a/b/c/..', ['a','b','c','\\..']),
    ('a/b/c/.', ['a','b','c','\\.']),
    ('a\\b\\c\\..', ['a','b','c','\\..']),
    ('a\\b\\c\\.', ['a','b','c','\\.']),

    # Nones
    ((None, 'abc'), ['abc']),

    # Starting with hash
    ('#9 BAC GIANG CONSTRUCTION JOINT STOCK COMPANY', ['#9 BAC GIANG CONSTRUCTION JOINT STOCK COMPANY']),
]

@pytest.mark.parametrize('index,path', testcases)
def test_parse(index, path):
    observed = parse(index)
    assert observed == path


def test_deterministic_order():
    'The iterable should have a deterministic order.'
    failures = [{3,5}, {'a':'apple','b':'banana'}]
    for thing in failures:
        assert not safe_type(thing)

    successes = [[3,6], (2,1), 'aoeua']
    for thing in successes:
        assert safe_type(thing)

def test_warn_unsafe_type():
    with pytest.raises(TypeError):
        parse({'one','two','three'})
