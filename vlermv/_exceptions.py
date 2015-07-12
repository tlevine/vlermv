try:
    FileNotFoundError
except NameError:
    OpenError = IOError
else:
    OpenError = FileNotFoundError

try:
    PermissionError
except NameError:
    class PermissionError(EnvironmentError):
        pass
else:
    PermissionError = PermissionError

try:
    FileNotFoundError
except NameError:
    DeleteError = OSError
else:
    DeleteError = FileNotFoundError

def out_of_space(exception):
    return isinstance(exception, IOError) and exception.args == (28, 'No space left on device')
