from .. import tuple

def test_to_tuple():
    assert tuple.to_tuple(('a',)) == ('a',)

def test_from_tuple():
    assert tuple.from_tuple(('a',)) == ('a',)
