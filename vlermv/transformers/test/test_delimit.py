from ..delimit import slash, backslash

def test_slash_to_tuple():
    assert slash.to_tuple('a') == ('a',)
    assert slash.to_tuple('a/b') == ('a','b')

def test_backslash_to_tuple():
    assert backslash.to_tuple('a') == ('a',)
    assert backslash.to_tuple('a\\b') == ('a','b')

def test_slash_from_tuple():
    assert slash.from_tuple(('a',)) == 'a'
    assert slash.from_tuple(('a','b')) == 'a/b'

def test_backslash_from_tuple():
    assert backslash.from_tuple(('a',)) == 'a'
    assert backslash.from_tuple(('a','b')) == 'a/b'
