#! /usr/bin/env python
# coding: utf-8


class Default:
    DEBUG = True
    PORT = 8000
    SIGNATURE_SECRET = 'iajfiseng,fuckyou'

    SESSION_EXPIRE = 100  # 100 day

    HOST = 'read-in-life.com'

    # redis config
    REDIS_CONFIG = {
        'host': '172.17.0.3',
        'port': 6379,
        'db': 0,
        'password': ''
    }

    # SQL server config
    SQL_SERVER_URL = 'postgresql://read_in_life:wocao@172.17.0.5/read_in_life'


class Development(Default):
    """for development"""
    pass


class Testing(Default):
    """for testing"""
    HOST = 'glrh11.com'


class Production(Default):
    """for production"""
    HOST = 'glrh11.com'
    SQL_SERVER_URL = 'postgresql://read_in_life:wocao@postgres/read_in_life'
    REDIS_CONFIG = {
        'host': 'redis',
        'port': 6379,
        'db': 0,
        'password': ''
    }

class UnitTesting(Default):
    """for unit_testing"""
    pass


config = {
    'default': Default,
    'development': Development,
    'testing': Testing,
    'production': Production,

    'unit_testing': UnitTesting
}