import os

class delimit:
    def __init__(self, delimiter):
        self.delimiter = delimiter

    def to_path(self, key):
        return tuple(key.split(self.delimiter))

    def from_path(self, obj):
        return self.delimiter.join(obj)

slash = delimit('/')
backslash = delimit('\\')
