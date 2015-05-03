import datetime
from . import tuple

def archive(transformer = tuple,
            precision = 'day',
            position = 'left',
            now = datetime.date.now):
    '''
    Wrap a transformer to add a date component to a path.

    :param transformer: Transformer to be wrapped
    :type transformer: transformer
    :param str precision: How precise should the date component be?
        Options are 'millisecond', 'second', 'minute', 'hour', 'day',
        'week', and 'month'.
    :param str position: Should the date be added to the beginning
        of the path (:samp:`'left'`) or the end of the path
        (:samp:`'right'`). If (:samp:`'left'`), the new path will be
        :samp:`(date,) + old_path`; if right, the new path will be
        :samp:`old_path + (date,)`.
    :param function now: :py:func:`archive` will run this to determine
        the date that will be added to the path; you might change
        this for testing.
    '''

#@cache(transformer = vlermv.transformers.archive(vlermv.transformers.tuple)
