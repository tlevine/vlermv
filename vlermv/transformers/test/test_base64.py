from .. import base64

def test_to_path():
    assert base64.to_path('aoeu') == ('YW9ldQ==',)

def test_from_path():
    assert base64.from_path(('YW9ldQ==',)) == 'aoeu'
