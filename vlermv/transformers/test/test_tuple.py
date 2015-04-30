from .. import tuple

def test_to_path():
    assert tuple.to_path(('a',)) == ('a',)

def test_from_path():
    assert tuple.from_path(('a',)) == ('a',)
