from ..simple import base64

def test_base64():
    assert base64('aoeu') == 'YW9ldQ=='.encode('ascii')

def test_identity():
    assert identity('bcoebu') == 'bcoebu'
