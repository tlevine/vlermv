import os

class delimit:
    def __init__(self, delimiter):
        self.delimiter = delimiter

    @staticmethod
    def to_tuple(key):
        return tuple(key.split(self.delimiter))

    @staticmethod
    def from_tuple(obj):
        return os.path.join(*obj)

slash = delimit('/')
backslash = delimit('\\')
