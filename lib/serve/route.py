# -*- coding: utf-8 -*-


class Route(object):

    def __init__(self, host='.*', prefix=''):
        '''
        Args:
            host: 域名.
            prefix: uri前缀.
        '''
        self.handlers = []
        self.host = host
        self._prefix = prefix

    def __call__(self, url, **kwds):
        def _(cls):
            self.handlers.append((self._prefix + url, cls, kwds))
            return cls
        return _
