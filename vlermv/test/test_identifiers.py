import datetime

import nose.tools as n

from pickle_warehouse.identifiers import parse, parse_partial, safe_type

#def check_parse(index:str, path:list):
def check_parse(index, path):
    observed = parse(index)
    n.assert_list_equal(observed, path)

def test_parse():
    for index, path in testcases:
        yield check_parse, index, path

def test_parse_int():
    n.assert_equal(parse_partial(3), ['3'])
    n.assert_equal(parse_partial(123), ['123'])
    n.assert_equal(parse(123), ['123'])

def test_parse_url():
    o = list(parse_partial('http://thomaslevine.com/!/about?a=b#lala'))
    e = ['http', 'thomaslevine.com', '!', 'about?a=b#lala']
    n.assert_list_equal(o, e)

def test_parse_date():
    o = list(parse_partial(datetime.date(2014, 2, 5)))
    e = ['2014', '02', '05']
    n.assert_list_equal(o, e)

def test_parse_datetime():
    o = list(parse_partial(datetime.datetime(2014, 2, 5, 11, 18, 30)))
    e = ['2014', '02', '05']
    n.assert_list_equal(o, e)

def test_parse_none():
    n.assert_equal(parse_partial(None), [''])
    n.assert_equal(parse(None), [])

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

def test_deterministic_order():
    'The iterable should have a deterministic order.'
    failures = [{3,5}, {'a':'apple','b':'banana'}]
    for thing in failures:
        n.assert_false(safe_type(thing))

    successes = [[3,6], (2,1), 'aoeua']
    for thing in successes:
        n.assert_true(safe_type(thing))

try:
    n.assert_warns
except AttributeError:
    @n.nottest
    def test_warn_unsafe_type():
        pass
else:
    def test_warn_unsafe_type():
        with n.assert_warns(UserWarning):
            parse({'one','two','three'})
