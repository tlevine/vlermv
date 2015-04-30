from .. import base64

def test_to_tuple():
    assert base64.to_tuple('aoeu') == ('YW9ldQ==',)

def test_from_tuple():
    assert base64.from_tuple(('YW9ldQ==',)) == 'aoeu'
