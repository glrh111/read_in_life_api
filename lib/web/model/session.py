#!/usr/bin/env python
# coding:utf-8

from lib.web.model.redis_db import redis, R
from os import urandom
import binascii
from base64 import urlsafe_b64encode, urlsafe_b64decode

SESSION_REDIS = R('session')

class Session(object):

    @classmethod
    def id_by_b64(cls, session):
        user_id, binary = _id_binary_decode(session)
        if user_id:
            key = SESSION_REDIS(user_id)
            user_id = int(user_id)
            if user_id and binary and binary == redis.get(key):
                return user_id

    @classmethod
    def new(cls, user_id, expire):
        user_id = int(user_id)
        if user_id:
            key = SESSION_REDIS(user_id)
            s = redis.get(key) or urandom(12)
            redis.setex(key, expire, s)
            return _id_binary_encode(user_id, s)

    @classmethod
    def rm(cls, user_id):
        redis.delete(SESSION_REDIS(user_id))


def _id_binary_decode(session):
    if not session:
        return None, None
    id, value = session.split('.', 1)
    try:
        value = urlsafe_b64decode(value)
    except (binascii.Error, TypeError):
        return None, None
    id = int(id)
    return id, value


def _id_binary_encode(id, session, encode=urlsafe_b64encode):
    ck_key = encode(session)
    return '%s.%s' % (id, ck_key)

if __name__ == '__main__':
    print 888
