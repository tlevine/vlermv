class base:
    def __init__(self, binary_mode = True, cache_exceptions = False):
        if not getattr(self, 'vlermv_can_cache', False) and cache_exceptions:
            raise ValueError('Serializer %s cannot cache exceptions.' % self.__name__)
        self.vlermv_binary_mode = binary_mode
        self.vlermv_cache_exceptions = cache_exceptions
