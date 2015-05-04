from . import ( magic, base64, tuple, simple, )
from ._delimit import ( slash, backslash, )

class archive:
    import datetime
    def __init__(self, transformer = tuple, date_format = '%Y-%m-%d',
                 position = 'right', now = datetime.datetime.now):
        '''
        Wrap a transformer to add a date component to a path.

        :param transformer: Transformer to be wrapped
        :type transformer: :ref:`transformer <transformers>`
        :param str date_format: This gets passed to
            :py:meth:`datetime.datetime.strftime`, and the result of this gets
            added to the file's path. Use :samp:`'%Y-%m-%d'`, for example,
            if you want to get new data once per day, or :samp:`'%Y-%m-%d %H:00'`
            if you want it every hour.
        :param str position: Should the date be added to the beginning
            of the path (:samp:`'left'`) or the end of the path
            (:samp:`'right'`). If (:samp:`'left'`), the new path will be
            :samp:`(date,) + old_path`; if right, the new path will be
            :samp:`old_path + (date,)`.
        :param function now: :py:func:`archive` will run this to determine
            the date that will be added to the path; you might change
            this for testing.
        '''
        self.base_transformer = transformer
        self.date_format = date_format
        self.position = position
        self.now = now

        for attr in ['binary_mode', 'cache_exceptions']:
            if hasattr(transformer, attr):
                setattr(self, attr, getattr(transformer, attr))

    def from_path(self, filename):
        '''
        Use the from_path from the base transformer;
        dates get included when you call Vlermv.keys().
        '''
        return self.base_transformer.from_path(filename)

    def to_path(self, key):
        path = self.base_transformer.to_path(key)
        date = self.now().strftime(self.date_format)
        if self.position == 'left':
            return (date,) + path
        elif self.position == 'right':
            return path + (date,)
        else:
            raise ValueError('"%s" is not a valid position.' % self.position)
