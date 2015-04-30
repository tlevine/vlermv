import os, tempfile

import pytest

from .. import exceptions

def test_open_error():
    with pytest.raises(exceptions.OpenError):
        open('/not-a-file')

def test_permission_error():
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write('')
    os.chmod(tmp.name, 000)
    with pytest.raises(exceptions.PermissionError):
        open(tmp.name, 'w').write('stuff')
    os.remomve(tmp.name)

def test_delete_error():
    with pytest.raises(exceptions.DeleteError):
        os.remove('/not-a-file')

def test_file_exists_error():
    with pytest.raises(exceptions.FileExistsError):
        os.mkdir('/')

def test_out_of_space(exception):
    import warnings
    warnings.warn('out_of_space is not tested.')
