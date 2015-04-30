import os

class delimit:
    def __init__(self, delimiter):
        self.delimiter = delimiter

    @staticmethod
    def to_tuple(key):
        return tuple(key.split(self.delimiter))

    @staticmethod
    def from_tuple(obj):
        return self.delimiter.join(obj)

slash = delimit('/')
backslash = delimit('\\')
