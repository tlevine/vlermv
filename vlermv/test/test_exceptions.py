import os, tempfile

import pytest

from .. import _exceptions as exceptions

def test_open_error():
    with pytest.raises(exceptions.OpenError):
        open('/not-a-file')

def test_permission_error():
    tmp = tempfile.NamedTemporaryFile()
    os.chmod(tmp.name, 000)
    with pytest.raises(exceptions.PermissionError):
        open(tmp.name, 'w').write('stuff')
    os.remove(tmp.name)

def test_delete_error():
    with pytest.raises(exceptions.DeleteError):
        os.remove('/not-a-file')

@pytest.mark.skipif(True, reason = 'Running out of space in a test is annoying.')
def test_out_of_space():
    raise NotImplementedError
