import datetime
from . import tuple

def archive(transformer = tuple,
            interval = 'day',
            position = 'left',
            append_random = False,
    '''
    Wrap a transformer to add a date component to a path.
    '''
Interval
    millisecond, second, minute, hour, day, week, month, default is day
append_random
    Whether to append a random number after the date, just in case there
    are multiple calls within the same millisecond, default is False
position
    left (at the beginning of the path), right (end), default is left
    (should there also be a "replace" option? i think

@cache(transformer = vlermv.transformers.archive(vlermv.transformers.tuple)
