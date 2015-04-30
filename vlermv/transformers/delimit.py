import os

class delimit:
    def __init__(self, delimiter):
        self.delimiter = delimiter

    def to_tuple(self, key):
        return tuple(key.split(self.delimiter))

    def from_tuple(self, obj):
        return self.delimiter.join(obj)

slash = delimit('/')
backslash = delimit('\\')
