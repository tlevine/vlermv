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

try:
    FileNotFoundError
except NameError:
    DeleteError = OSError
else:
    DeleteError = FileNotFoundError

try:
    FileExistsError
except NameError:
    FileExistsError = OSError

def out_of_space(exception):
    return isinstance(exception, IOError) and exception.args == (28, 'No space left on device')
