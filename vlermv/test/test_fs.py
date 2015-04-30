import os
from random import seed
from tempfile import mkdtemp

import pytest

from .. import fs

def test_mktemp():
    outer = mkdtemp()
    inner = os.path.join(outer, '1', '2', '3')
    filename = fs.mktemp(inner, filename = lambda: '4')

    assert os.path.isdir(inner), 'Temporary directory was not created properly.'
    assert filename == os.path.join(inner, '4'), 'Temporary file is named incorrectly.'
    assert not os.path.isfile(filename), 'Temporary file was created; it should not be created.'

def test_random_file_name():
    seed(1234534324)
    assert fs._random_file_name() == 'dZTruUBGba'

def test_reversed_directories():
    observed = list(fs._reversed_directories('/usr', '/usr/local/bin'))
    expected = ['/usr/local/bin', '/usr/local']
    assert observed == expected
