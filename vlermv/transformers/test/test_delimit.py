from .._delimit import slash, backslash

def test_slash_to_path():
    assert slash.to_path('a') == ('a',)
    assert slash.to_path('a/b') == ('a','b')

def test_backslash_to_path():
    assert backslash.to_path('a') == ('a',)
    assert backslash.to_path('a\\b') == ('a','b')

def test_slash_from_path():
    assert slash.from_path(('a',)) == 'a'
    assert slash.from_path(('a','b')) == 'a/b'

def test_backslash_from_path():
    assert backslash.from_path(('a',)) == 'a'
    assert backslash.from_path(('a','b')) == 'a\\b'
